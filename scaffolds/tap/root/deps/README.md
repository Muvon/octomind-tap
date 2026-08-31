# Dependencies

Dependency installers live at `deps/<org>/<tool>.sh` with a required companion
document at `deps/<org>/<tool>.md`.

Copy `templates/dep.sh`, source `deps/lib/platform.sh`, implement every
supported platform branch, and verify the installed command before returning
success. Use the MCP or plain-tool documentation template as appropriate.

