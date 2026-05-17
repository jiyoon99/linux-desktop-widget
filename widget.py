#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import platform
import shutil
import socket
import subprocess
import time
import urllib.error
import urllib.request
from dataclasses import dataclass

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gdk, GLib, Gtk, Pango


REFRESH_MS = 3000
OLLAMA_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
LOCAL_PORTS = (3000, 5000, 5173, 8000, 8001, 8080, 11434)


@dataclass(frozen=True)
class Check:
    key: str
    title: str
    state: str
    detail: str
    ok: bool


def docker_check() -> Check:
    if shutil.which("docker") is None:
        return Check("docker", "Docker", "OFF", "docker CLI not found", False)

    try:
        result = subprocess.run(
            ["docker", "info", "--format", "{{.ServerVersion}}|{{.ContainersRunning}}"],
            capture_output=True,
            check=True,
            text=True,
            timeout=2,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError) as exc:
        message = getattr(exc, "stderr", "") or str(exc)
        return Check("docker", "Docker", "OFF", message.strip()[:90] or "daemon unavailable", False)

    version, _, running = result.stdout.strip().partition("|")
    detail = f"v{version or '?'} · running {running or '0'}"
    return Check("docker", "Docker", "ON", detail, True)


def local_check() -> Check:
    open_ports = [port for port in LOCAL_PORTS if _port_open(port)]
    host = platform.node() or socket.gethostname() or "localhost"
    if open_ports:
        detail = f"{host} · ports {', '.join(str(port) for port in open_ports[:5])}"
    else:
        detail = f"{host} · no watched local ports"
    return Check("local", "Local", "ON", detail, True)


def ai_check() -> Check:
    url = f"{OLLAMA_URL}/api/tags"
    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (OSError, urllib.error.URLError, TimeoutError, UnicodeDecodeError, ValueError) as exc:
        return Check("ai", "AI", "OFF", f"Ollama unreachable · {exc}"[:90], False)

    models = payload.get("models") if isinstance(payload, dict) else []
    names = [item.get("name") for item in models if isinstance(item, dict) and item.get("name")]
    detail = names[0] if names else "Ollama running · no models"
    if len(names) > 1:
        detail = f"{detail} +{len(names) - 1}"
    return Check("ai", "AI", "ON", detail, True)


def _port_open(port: int) -> bool:
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=0.25):
            return True
    except OSError:
        return False


class StatusWidget(Gtk.Window):
    def __init__(self) -> None:
        super().__init__(title="Linux Status Widget")
        self.set_decorated(False)
        self.set_resizable(False)
        self.set_keep_above(True)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.stick()
        self.set_type_hint(Gdk.WindowTypeHint.UTILITY)
        self.set_app_paintable(True)
        self.set_default_size(330, 190)
        self.set_position(Gtk.WindowPosition.NONE)
        self.move(24, 72)

        screen = Gdk.Screen.get_default()
        if screen is not None:
            provider = Gtk.CssProvider()
            provider.load_from_data(CSS.encode("utf-8"))
            Gtk.StyleContext.add_provider_for_screen(
                screen,
                provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
            )

        self.root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.root.get_style_context().add_class("widget")
        self.add(self.root)

        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        header.get_style_context().add_class("header")
        self.root.pack_start(header, False, False, 0)

        self.title_label = Gtk.Label(label="SYSTEM WIDGET")
        self.title_label.set_xalign(0)
        self.title_label.get_style_context().add_class("title")
        header.pack_start(self.title_label, True, True, 0)

        self.time_label = Gtk.Label(label="--:--:--")
        self.time_label.get_style_context().add_class("time")
        header.pack_start(self.time_label, False, False, 0)

        self.rows: dict[str, tuple[Gtk.Label, Gtk.Label, Gtk.Label]] = {}
        for key, title in (("docker", "Docker"), ("local", "Local"), ("ai", "AI")):
            self._add_row(key, title)

        hint = Gtk.Label(label="drag to move · right click to quit")
        hint.set_xalign(0)
        hint.get_style_context().add_class("hint")
        self.root.pack_start(hint, False, False, 0)

        self.connect("button-press-event", self._on_button_press)
        self.connect("destroy", Gtk.main_quit)
        GLib.timeout_add(REFRESH_MS, self.refresh)
        self.refresh()

    def _add_row(self, key: str, title: str) -> None:
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        row.get_style_context().add_class("row")
        self.root.pack_start(row, False, False, 0)

        title_label = Gtk.Label(label=title)
        title_label.set_xalign(0)
        title_label.set_size_request(64, -1)
        title_label.get_style_context().add_class("row-title")
        row.pack_start(title_label, False, False, 0)

        state_label = Gtk.Label(label="...")
        state_label.set_size_request(42, -1)
        state_label.get_style_context().add_class("state")
        row.pack_start(state_label, False, False, 0)

        detail_label = Gtk.Label(label="checking")
        detail_label.set_xalign(0)
        detail_label.set_ellipsize(Pango.EllipsizeMode.END)
        detail_label.get_style_context().add_class("detail")
        row.pack_start(detail_label, True, True, 0)

        self.rows[key] = (title_label, state_label, detail_label)

    def refresh(self) -> bool:
        checks = [docker_check(), local_check(), ai_check()]
        for check in checks:
            _, state_label, detail_label = self.rows[check.key]
            state_label.set_text(check.state)
            detail_label.set_text(check.detail)
            context = state_label.get_style_context()
            context.remove_class("ok")
            context.remove_class("bad")
            context.add_class("ok" if check.ok else "bad")

        self.time_label.set_text(time.strftime("%H:%M:%S"))
        return True

    def _on_button_press(self, _widget, event) -> bool:
        if event.button == 1:
            self.begin_move_drag(event.button, int(event.x_root), int(event.y_root), event.time)
            return True
        if event.button == 3:
            self.destroy()
            return True
        return False


CSS = """
window {
  background-color: transparent;
}

.widget {
  padding: 14px;
  border: 1px solid rgba(105, 224, 184, 0.38);
  border-radius: 14px;
  background: rgba(8, 12, 15, 0.82);
  box-shadow: 0 18px 50px rgba(0, 0, 0, 0.42);
}

.header {
  padding-bottom: 4px;
}

.title {
  color: #e8f4ef;
  font: 700 14px "JetBrains Mono", "Noto Sans Mono", monospace;
  letter-spacing: 0;
}

.time,
.hint,
.detail {
  color: #93a29d;
  font: 12px "JetBrains Mono", "Noto Sans Mono", monospace;
}

.row {
  min-height: 34px;
  padding: 8px 10px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.045);
}

.row-title {
  color: #e8f4ef;
  font: 700 13px "JetBrains Mono", "Noto Sans Mono", monospace;
}

.state {
  padding: 2px 7px;
  border-radius: 999px;
  font: 700 12px "JetBrains Mono", "Noto Sans Mono", monospace;
}

.state.ok {
  color: #34f5a6;
  background: rgba(52, 245, 166, 0.12);
}

.state.bad {
  color: #ff6673;
  background: rgba(255, 102, 115, 0.13);
}

.hint {
  padding-top: 2px;
}
"""


def main() -> None:
    widget = StatusWidget()
    widget.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
