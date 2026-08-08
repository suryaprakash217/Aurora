from __future__ import annotations

from aurora.theme.style import get_stylesheet


def test_get_stylesheet_contains_panel_selectors():
    config = {"shell": {"theme": "aurora-dark"}}
    stylesheet = get_stylesheet(config)

    assert "#PanelContainer" in stylesheet
    assert "QPushButton#LauncherButton" in stylesheet
    assert "WorkspaceButton" in stylesheet


def test_get_stylesheet_allows_overrides():
    config = {"shell": {"theme": "aurora-light", "background_color": "#123456"}}
    stylesheet = get_stylesheet(config)

    assert "#123456" in stylesheet
    assert "aurora-light" in config["shell"]["theme"]
