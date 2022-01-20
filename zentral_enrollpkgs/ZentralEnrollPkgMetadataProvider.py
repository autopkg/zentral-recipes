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
import re

from autopkglib import ProcessorError, URLGetter

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
        "configuration_name": {
            "description": "The name of the enrollment configuration",
        },
        "configuration_slug": {
            "description": "A slug based on the name of the enrollment configuration",
        },
    }
    description = __doc__

    def assemble_curl_cmd(self, token, url):
        """Assemble curl command and return it, as per example in core autopkg."""
        curl_cmd = self.prepare_curl_cmd()
        header = {"Authorization": f"Token {token}"}
        self.add_curl_headers(curl_cmd, header)
        curl_cmd.append(url)
        return curl_cmd

    def main(self):
        token = self.env["token"]
        self.env["lower_cased"] = self.env.get("enrollment", "osquery").lower()
        server_base_url = "https://{server_fqdn}/api/{lower_cased}".format(**self.env)

        # enrollment → url, version
        enrollment_id = self.env.get("enrollment_id", 1)
        enrollment_url = f"{server_base_url}/enrollments/{enrollment_id}/"
        enrollment_curl_cmd = self.assemble_curl_cmd(token, enrollment_url)
        enrollment_response = self.download_with_curl(enrollment_curl_cmd)
        try:
            enrollment_data = json.loads(enrollment_response)
        except (ValueError, KeyError, TypeError) as e:
            self.output(f"Enrollment JSON response was: {enrollment_response}")
            raise ProcessorError(f"Enrollment JSON format error: {e}")
        self.env["url"] = enrollment_data["package_download_url"]
        self.output(f"Found URL {self.env['url']}")
        self.env["version"] = str(enrollment_data["version"])
        self.output(f"Enrollment pkg version {self.env['version']}")

        # configuration → configuration_slug
        configuration_id = enrollment_data["configuration"]
        configuration_url = f"{server_base_url}/configurations/{configuration_id}/"
        configuration_curl_cmd = self.assemble_curl_cmd(token, configuration_url)
        configuration_response = self.download_with_curl(configuration_curl_cmd)
        try:
            configuration_data = json.loads(configuration_response)
        except (ValueError, KeyError, TypeError) as e:
            self.output(f"Configuration JSON response was: {configuration_response}")
            raise ProcessorError(f"Configuration JSON format error: {e}")
        self.env["configuration_name"] = configuration_data["name"]
        self.output(f"Configuration name: {self.env['configuration_name']}")
        self.env["configuration_slug"] = re.sub(r'\W', '', configuration_data["name"])
        self.output(f"Configuration slug: {self.env['configuration_slug']}")


if __name__ == "__main__":
    PROCESSOR = ZentralEnrollPkgMetadataProvider()
    PROCESSOR.execute_shell()
