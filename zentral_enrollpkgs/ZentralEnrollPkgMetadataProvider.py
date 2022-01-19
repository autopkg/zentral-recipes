#!/usr/bin/env python
#
# Copyright 2022 Allister Banks, with parts/format borrowed from Hannes and Zack Thompson
# (hjuutilainen and mlbz521)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import json

from autopkglib import Processor, ProcessorError, URLGetter

__all__ = ["ZentralEnrollPkgMetadataProvider"]


class ZentralEnrollPkgMetadataProvider(URLGetter):
    """Provides metadata for enrollment pkgs when pointed at a Zentral server.
    Optional input variables may not work if you're hoping to fetch a munki
    enrollment pkg or if you have more than one configuration, see the
    guidance below"""

    input_variables = {
        "token": {
            "required": True,
            "description": "Service account token with read access "
            "to 'munki/osquery | enrollment | Can view enrollment'",
        },
        "server_fqdn": {
            "required": True,
            "description": "The top-level domain of your zentral "
            "server without https:// or a trailing /",
        },
        "enrollment": {
            "required": False,
            "description": "The name of the enrollment pkg to fetch. Possible "
            "values are Munki (capitalized pls) or Osquery (default)",
        },
        "enrollment_id": {
            "required": False,
            "description": "Enrollment id which you'd see at the end of "
            "the osquery/configurations/ or munki/.. url. Defaults to 1",
        },
    }
    output_variables = {
        "lower_cased": {
            "description": "Used in installcheck script and URL",
        },
        "url": {
            "description": "URL to the pkg",
        },
        "version": {
            "description": "Version as iterated on for the enrollment",
        },
    }
    description = __doc__

    def assemble_curl_cmd(self, token, server_url):
        """Assemble curl command and return it, as per example in core autopkg."""
        curl_cmd = self.prepare_curl_cmd()
        header = {"Authorization": f"Token {token}"}
        self.add_curl_headers(curl_cmd, header)
        curl_cmd.append(server_url)
        return curl_cmd

    def main(self):
        token = self.env.get("token")
        enrollment = self.env.get("enrollment", "osquery")
        lower_cased = enrollment.lower()
        self.env["lower_cased"] = lower_cased
        enrollment_id = self.env.get("enrollment_id", "1")
        server_url = "/".join(
            [
                "https:/",
                self.env.get("server_fqdn"),
                "api",
                lower_cased,
                "enrollments",
                enrollment_id,
            ]
        )
        curl_cmd = self.assemble_curl_cmd(token, server_url)
        response = self.download_with_curl(curl_cmd)
        try:
            json_data = json.loads(response)
        except (ValueError, KeyError, TypeError) as e:
            self.output(f"JSON response was: {response}")
            raise ProcessorError(f"JSON format error: {e}")

        self.env["url"] = json_data["package_download_url"]
        self.output("Found URL {self.env['url']}")
        self.env["version"] = str(json_data["version"])
        self.output("Enrollment pkg version {self.env['version']}")


if __name__ == "__main__":
    PROCESSOR = ZentralEnrollPkgMetadataProvider()
    PROCESSOR.execute_shell()
