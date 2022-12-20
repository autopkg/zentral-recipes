Recipe for swiftDialog by Bart Reardon - https://github.com/bartreardon/swiftDialog

- swiftDialog is an admin utility app for macOS 11+ written in SwiftUI that displays a popup dialog, displaying the content to your users that you want to display.\ .

## Notes:

This recipe will download from the latest release from GitHub https://github.com/bartreardon/swiftDialog.

It downloads the pkg to deploy to '/Library/Application Support/Dialog/Dialog.app' and symlink the CLI to '/usr/local/bin/dialog'.

- swiftDialog.download.recipe
- swiftDialog.install.recipe
- swiftDialog.jamf.recipe
- swiftDialog.munki.recipe


Dependency for jamf.recipe:  JamfUploader-AutoPkg-Processors see: https://github.com/grahampugh/jamf-upload/wiki/JamfUploader-AutoPkg-Processors