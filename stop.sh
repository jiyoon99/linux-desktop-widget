#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "$0")" && pwd)"

pkill -f "$APP_DIR/widget.py" 2>/dev/null || true
pkill -f "python3 .*linux-desktop-widget/widget.py" 2>/dev/null || true
