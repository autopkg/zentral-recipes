Recipe for tailwindcss-cli - https://tailwindcss.com

- tailwindcss-cli is tool to work with TailwindCSS, a utility-first CSS framework for rapidly building custom user interfaces. Installs to /usr/local/bin//tailwindcss-cli

## Notes:

This recipe will download from the latest release from GitHub https://github.com/timberio/vector.

It copies the tailwindcss-macos-arm64 (Apple Silicon) binary and creates a pkg to deploy to `/usr/local/bin/tailwindcss-cli`.
TODO: add logic to download intel version