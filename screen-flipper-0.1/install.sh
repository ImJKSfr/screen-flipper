#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_ROOT="${HOME}/.local/share/screen-flipper"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/scalable/apps"

mkdir -p "$INSTALL_ROOT" "$DESKTOP_DIR" "$ICON_DIR"

rm -rf "$INSTALL_ROOT"/* "$INSTALL_ROOT"/.[!.]* "$INSTALL_ROOT"/..?* 2>/dev/null || true
cp -R "$SCRIPT_DIR"/. "$INSTALL_ROOT"/

chmod +x "$INSTALL_ROOT/run-screen-flipper.sh"
cp "$INSTALL_ROOT/screen-icon.svg" "$ICON_DIR/screen-flipper.svg"

cat > "$DESKTOP_DIR/screen-flipper.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Screen Flipper
Comment=Flip the screen orientation on Linux
Exec=$INSTALL_ROOT/run-screen-flipper.sh
Path=$INSTALL_ROOT
Icon=$ICON_DIR/screen-flipper.svg
Terminal=false
Categories=Utility;GTK;Qt;
StartupNotify=true
EOF

update-desktop-database "$DESKTOP_DIR" >/dev/null 2>&1 || true

echo "Installed to $INSTALL_ROOT"
echo "Launcher entry created at $DESKTOP_DIR/screen-flipper.desktop"
