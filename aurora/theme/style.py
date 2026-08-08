from __future__ import annotations

from typing import Any


def get_stylesheet(config: dict[str, Any]) -> str:
    """Generate the complete QSS (Qt Stylesheet) for the Aurora GUI shell components dynamically."""
    shell_config = config.get("shell", {})
    theme = shell_config.get("theme", "aurora-dark")

    # Establish modern color tokens based on theme
    if theme == "aurora-light":
        bg_color = "rgba(245, 246, 250, 0.85)"
        fg_color = "#2f3640"
        border_color = "rgba(47, 54, 64, 0.15)"
        accent_color = "#0984e3"
        accent_hover = "rgba(9, 132, 227, 0.15)"
        widget_bg = "rgba(0, 0, 0, 0.05)"
        status_color = "#2ecc71"
    else:
        # Default: aurora-dark (Tokyo Night inspired)
        bg_color = "rgba(26, 27, 38, 0.85)"
        fg_color = "#c0caf5"
        border_color = "rgba(255, 255, 255, 0.1)"
        accent_color = "#7aa2f7"
        accent_hover = "rgba(122, 162, 247, 0.2)"
        widget_bg = "rgba(255, 255, 255, 0.04)"
        status_color = "#9ece6a"

    # Allow custom config overrides
    bg_color = shell_config.get("background_color", bg_color)
    accent_color = shell_config.get("accent_color", accent_color)

    return f"""
    /* Top Panel Layout Container */
    #PanelWindow {{
        background: transparent;
    }}

    #PanelContainer {{
        background-color: {bg_color};
        border-bottom: 1px solid {border_color};
        color: {fg_color};
    }}

    /* Top-level Panel Widgets */
    QLabel {{
        color: {fg_color};
        font-family: "Outfit", "Inter", "Sans-Serif";
        font-size: 13px;
        background: transparent;
    }}

    /* Launcher Button */
    QPushButton#LauncherButton {{
        background-color: {widget_bg};
        border: 1px solid {border_color};
        border-radius: 6px;
        color: {accent_color};
        font-weight: bold;
        font-size: 13px;
        padding: 4px 12px;
    }}

    QPushButton#LauncherButton:hover {{
        background-color: {accent_hover};
        border-color: {accent_color};
    }}

    /* Workspace Indicator Buttons */
    QPushButton.WorkspaceButton {{
        background: transparent;
        border: none;
        border-radius: 6px;
        color: #565f89;
        font-weight: bold;
        font-size: 12px;
        min-width: 24px;
        min-height: 24px;
        max-width: 24px;
        max-height: 24px;
    }}

    QPushButton.WorkspaceButton:hover {{
        background-color: rgba(255, 255, 255, 0.05);
        color: {fg_color};
    }}

    QPushButton.ActiveWorkspaceButton {{
        background-color: {accent_hover};
        border: 1px solid {accent_color};
        color: {accent_color};
    }}

    /* Clock Widget */
    QLabel#ClockWidget {{
        font-weight: bold;
        color: #acb0d0;
    }}

    /* System Status Area */
    #StatusContainer {{
        background-color: {widget_bg};
        border: 1px solid {border_color};
        border-radius: 6px;
        padding: 4px 12px;
    }}

    QLabel#StatusLabel {{
        color: {status_color};
        font-family: monospace;
        font-size: 12px;
    }}

    /* Logo Widget */
    QLabel#LogoLabel {{
        color: #bb9af7;
        font-weight: bold;
        font-size: 14px;
        margin-right: 8px;
    }}

    /* Launcher Menu Overlay */
    #LauncherOverlay {{
        background-color: {bg_color};
        border: 1px solid {border_color};
        border-radius: 12px;
    }}

    #LauncherTitle {{
        color: #bb9af7;
        font-weight: bold;
        font-size: 18px;
    }}

    QLineEdit#LauncherSearch {{
        background-color: rgba(0, 0, 0, 0.2);
        border: 1px solid {border_color};
        border-radius: 6px;
        color: {fg_color};
        padding: 6px 10px;
        font-size: 13px;
    }}

    QLineEdit#LauncherSearch:focus {{
        border-color: {accent_color};
    }}

    QListWidget#LauncherList {{
        background: transparent;
        border: none;
        color: {fg_color};
        font-size: 13px;
    }}

    QListWidget#LauncherList::item {{
        padding: 6px;
        border-radius: 4px;
    }}

    QListWidget#LauncherList::item:hover {{
        background-color: {accent_hover};
        color: {accent_color};
    }}
    """
