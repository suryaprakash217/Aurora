from __future__ import annotations

import json
import subprocess
import time
from typing import Any

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("GtkLayerShell", "0.1")
from gi.repository import Gdk, GLib, Gtk, GtkLayerShell


class AuroraPanel(Gtk.Window):
    """Sleek top panel representing the foundation of the Aurora graphical shell."""

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(title="Aurora Top Panel")
        self.config = config

        # Initialize Layer Shell
        GtkLayerShell.init_for_window(self)
        GtkLayerShell.set_layer(self, GtkLayerShell.Layer.TOP)
        GtkLayerShell.auto_exclusive_zone_enable(self)

        # Set Anchors (Top, Left, Right)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.TOP, True)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.LEFT, True)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.RIGHT, True)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.BOTTOM, False)

        # Configurable Height
        shell_config = config.get("shell", {})
        height = shell_config.get("height", 36)
        self.set_default_size(100, height)

        # Layout container
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.main_box.get_style_context().add_class("panel-container")
        self.add(self.main_box)

        # Create Left, Center, Right segments
        self.left_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.left_box.get_style_context().add_class("panel-left")

        self.center_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.center_box.get_style_context().add_class("panel-center")

        self.right_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.right_box.get_style_context().add_class("panel-right")

        self.main_box.pack_start(self.left_box, False, False, 12)
        self.main_box.set_center_widget(self.center_box)
        self.main_box.pack_end(self.right_box, False, False, 12)

        # Setup subcomponents
        self._init_launcher()
        self._init_workspaces()
        self._init_clock()
        self._init_system_status()

        # Load styling
        self._load_styles()

        self.show_all()

    def _init_launcher(self) -> None:
        # App launcher placeholder
        self.launcher_btn = Gtk.Button(label="󰣇 Launcher")
        self.launcher_btn.get_style_context().add_class("launcher-button")
        self.launcher_btn.connect("clicked", self._on_launcher_clicked)
        self.left_box.pack_start(self.launcher_btn, False, False, 0)

    def _on_launcher_clicked(self, button: Gtk.Button) -> None:
        print("Launcher clicked! (Placeholder for future launcher menu)")

    def _init_workspaces(self) -> None:
        self.workspaces_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        self.workspaces_box.get_style_context().add_class("workspaces-container")
        self.left_box.pack_start(self.workspaces_box, False, False, 0)

        self._update_workspaces()
        GLib.timeout_add(250, self._update_workspaces)

    def _update_workspaces(self) -> bool:
        # Clear existing workspace buttons
        for child in self.workspaces_box.get_children():
            self.workspaces_box.remove(child)

        try:
            # Fetch workspaces and active workspace info from hyprland
            res_workspaces = subprocess.run(["hyprctl", "-j", "workspaces"], capture_output=True, text=True, check=True)
            res_active = subprocess.run(["hyprctl", "-j", "activeworkspace"], capture_output=True, text=True, check=True)

            workspaces = json.loads(res_workspaces.stdout)
            active_ws = json.loads(res_active.stdout)
            active_id = active_ws.get("id", 1)

            # Sort and build a list of unique workspaces (default to 1..5 if empty)
            active_ids = {w["id"] for w in workspaces}
            all_ids = sorted(list(active_ids.union({1, 2, 3, 4, 5})))

            for w_id in all_ids:
                btn = Gtk.Button(label=str(w_id))
                btn.get_style_context().add_class("workspace-button")
                if w_id == active_id:
                    btn.get_style_context().add_class("active-workspace")
                btn.connect("clicked", lambda b, i=w_id: self._switch_workspace(i))
                self.workspaces_box.pack_start(btn, False, False, 0)
        except Exception:
            # Fallback to static workspaces if hyprctl fails (e.g., outside Hyprland)
            for i in range(1, 6):
                btn = Gtk.Button(label=str(i))
                btn.get_style_context().add_class("workspace-button")
                if i == 1:
                    btn.get_style_context().add_class("active-workspace")
                self.workspaces_box.pack_start(btn, False, False, 0)

        self.workspaces_box.show_all()
        return True

    def _switch_workspace(self, workspace_id: int) -> None:
        try:
            subprocess.run(["hyprctl", "dispatch", "workspace", str(workspace_id)], check=False)
        except Exception as e:
            print(f"Failed to switch workspace: {e}")

    def _init_clock(self) -> None:
        self.clock_label = Gtk.Label()
        self.clock_label.get_style_context().add_class("clock-label")
        self.center_box.pack_start(self.clock_label, True, True, 0)

        self._update_clock()
        GLib.timeout_add(1000, self._update_clock)

    def _update_clock(self) -> bool:
        self.clock_label.set_text(time.strftime("%a %b %d  %I:%M:%S %p"))
        return True

    def _init_system_status(self) -> None:
        self.status_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.status_box.get_style_context().add_class("status-container")

        self.status_label = Gtk.Label()
        self.status_label.get_style_context().add_class("status-label")
        self.status_box.pack_start(self.status_label, False, False, 0)

        self.right_box.pack_start(self.status_box, False, False, 0)

        self._update_system_status()
        GLib.timeout_add(2000, self._update_system_status)

    def _update_system_status(self) -> bool:
        try:
            # Calculate simple CPU usage percentage
            cpu_cmd = "grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}'"
            cpu_res = subprocess.run(cpu_cmd, shell=True, capture_output=True, text=True, check=True)
            cpu = float(cpu_res.stdout.strip())

            # Calculate Memory usage percentage
            mem_cmd = "free | grep Mem | awk '{print $3/$2 * 100}'"
            mem_res = subprocess.run(mem_cmd, shell=True, capture_output=True, text=True, check=True)
            mem = float(mem_res.stdout.strip())

            self.status_label.set_text(f"CPU: {cpu:.1f}% | MEM: {mem:.1f}%")
        except Exception:
            self.status_label.set_text("CPU: --% | MEM: --%")
        return True

    def _load_styles(self) -> None:
        css_provider = Gtk.CssProvider()

        # Retrieve styling configuration from the config object
        shell_config = self.config.get("shell", {})
        theme_name = shell_config.get("theme", "aurora-dark")

        # Determine theme color palette dynamically based on the configuration
        if theme_name == "aurora-light":
            bg_color = "rgba(245, 246, 250, 0.9)"
            fg_color = "#2f3640"
            border_color = "rgba(0, 0, 0, 0.12)"
            accent_color = "#0984e3"
            accent_bg = "rgba(9, 132, 227, 0.15)"
            status_color = "#2ecc71"
        else:
            # Default to "aurora-dark"
            bg_color = "rgba(26, 27, 38, 0.85)"
            fg_color = "#c0caf5"
            border_color = "rgba(255, 255, 255, 0.1)"
            accent_color = "#7aa2f7"
            accent_bg = "rgba(122, 162, 247, 0.2)"
            status_color = "#9ece6a"

        # Apply override if custom background/accent color is specified in configuration
        bg_color = shell_config.get("background_color", bg_color)
        accent_color = shell_config.get("accent_color", accent_color)

        css_data = f"""
        .panel-container {{
            background-color: {bg_color};
            border-bottom: 1px solid {border_color};
            color: {fg_color};
            padding: 4px 12px;
            font-family: "Outfit", "Inter", "Sans-Serif";
            font-size: 13px;
        }}

        .launcher-button {{
            background: rgba(255, 255, 255, 0.07);
            border: 1px solid {border_color};
            border-radius: 6px;
            color: {accent_color};
            font-weight: bold;
            padding: 2px 10px;
        }}

        .launcher-button:hover {{
            background: {accent_bg};
            border-color: {accent_color};
        }}

        .workspace-button {{
            background: transparent;
            border: none;
            border-radius: 6px;
            color: #565f89;
            font-weight: bold;
            padding: 2px 8px;
            margin: 0 1px;
        }}

        .workspace-button:hover {{
            background: rgba(255, 255, 255, 0.05);
            color: {fg_color};
        }}

        .active-workspace {{
            background: {accent_bg};
            border: 1px solid {accent_color};
            color: {accent_color};
        }}

        .clock-label {{
            font-weight: bold;
            color: #acb0d0;
        }}

        .status-container {{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid {border_color};
            border-radius: 6px;
            padding: 2px 10px;
        }}

        .status-label {{
            color: {status_color};
            font-family: monospace;
        }}
        """

        css_provider.load_from_data(css_data.encode("utf-8"))
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )


def run_panel(config: dict[str, Any]) -> None:
    """Helper entry function to launch and spin the GTK panel app."""
    win = AuroraPanel(config)
    win.connect("destroy", Gtk.main_quit)
    Gtk.main()
