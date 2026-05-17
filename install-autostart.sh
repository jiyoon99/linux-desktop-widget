#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
AUTOSTART_DIR="$HOME/.config/autostart"
DESKTOP_FILE="$AUTOSTART_DIR/linux-desktop-widget.desktop"

mkdir -p "$AUTOSTART_DIR"
cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Name=Linux Desktop Widget
Comment=Desktop widget for Docker, local services, and Ollama AI status
Exec=$APP_DIR/run.sh
Terminal=false
X-GNOME-Autostart-enabled=true
EOF

echo "Installed: $DESKTOP_FILE"
