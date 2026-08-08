from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:  # pragma: no cover
    from PyQt6 import QtCore, QtGui, QtWidgets

from aurora.theme.style import get_stylesheet
from aurora.ui.clock import ClockWidget
from aurora.ui.launcher import LauncherButton
from aurora.ui.status import StatusWidget
from aurora.ui.workspace import WorkspaceWidget


class AuroraShellWindow(QtWidgets.QMainWindow):
    """Main Aurora shell window containing the panel and wallpaper preview."""

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__()
        self.config = config
        shell_config = config.get("shell", {})

        self.setWindowTitle(shell_config.get("name", "Aurora"))
        self.setObjectName("AuroraShellWindow")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setMinimumSize(900, 560)

        self._base_stylesheet = get_stylesheet(config)
        self._build_ui()
        self.apply_theme()
        self.apply_background()

        if shell_config.get("animations", True):
            self.setWindowOpacity(0.0)
            QtCore.QTimer.singleShot(0, self._start_open_animation)

    def _build_ui(self) -> None:
        root = QtWidgets.QWidget()
        root.setObjectName("AuroraRoot")

        root_layout = QtWidgets.QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.panel = QtWidgets.QWidget()
        self.panel.setObjectName("PanelContainer")
        self.panel.setFixedHeight(self._panel_height())
        panel_layout = QtWidgets.QHBoxLayout(self.panel)
        panel_layout.setContentsMargins(16, 8, 16, 8)
        panel_layout.setSpacing(12)

        left_group = QtWidgets.QWidget()
        left_layout = QtWidgets.QHBoxLayout(left_group)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(10)

        logo_label = QtWidgets.QLabel(self.config.get("shell", {}).get("name", "Aurora"))
        logo_label.setObjectName("LogoLabel")
        left_layout.addWidget(logo_label)

        launcher_visible = self.config.get("shell", {}).get("launcher", {}).get("visible", True)
        if launcher_visible:
            left_layout.addWidget(LauncherButton(self.config))

        left_layout.addWidget(WorkspaceWidget(self.config))
        left_layout.addStretch(1)
        panel_layout.addWidget(left_group, 1)

        center_group = QtWidgets.QWidget()
        center_layout = QtWidgets.QHBoxLayout(center_group)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        center_group.setLayout(center_layout)
        self.clock_widget = ClockWidget(self.config)
        center_layout.addWidget(self.clock_widget)
        panel_layout.addWidget(center_group, 1)

        right_group = QtWidgets.QWidget()
        right_layout = QtWidgets.QHBoxLayout(right_group)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(8)
        right_layout.addStretch(1)
        right_layout.addWidget(StatusWidget(self.config))

        close_button = QtWidgets.QPushButton("⨉")
        close_button.setObjectName("CloseButton")
        close_button.setFixedSize(26, 26)
        close_button.clicked.connect(self.close)
        right_layout.addWidget(close_button)

        panel_layout.addWidget(right_group, 0)

        self.content_area = QtWidgets.QWidget()
        self.content_area.setObjectName("ContentArea")
        content_layout = QtWidgets.QVBoxLayout(self.content_area)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(16)

        placeholder = QtWidgets.QLabel(
            "Aurora graphical shell prototype running inside Hyprland.\n"
            "This panel is the first visible Aurora desktop shell interface."
        )
        placeholder.setWordWrap(True)
        placeholder.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("color: rgba(255, 255, 255, 0.92); font-size: 20px;")
        content_layout.addWidget(placeholder, 1)

        if self._panel_position() == "top":
            root_layout.addWidget(self.panel)
            root_layout.addWidget(self.content_area, 1)
        else:
            root_layout.addWidget(self.content_area, 1)
            root_layout.addWidget(self.panel)

        self.setCentralWidget(root)

    def _panel_position(self) -> str:
        return self.config.get("shell", {}).get("panel", {}).get("position", "top")

    def _panel_height(self) -> int:
        value = self.config.get("shell", {}).get("panel", {}).get("height", 48)
        try:
            return max(32, int(value))
        except (TypeError, ValueError):
            return 48

    def apply_theme(self) -> None:
        self.setStyleSheet(self._base_stylesheet)

    def apply_background(self) -> None:
        shell_config = self.config.get("shell", {})
        wallpaper = shell_config.get("wallpaper")
        background_color = shell_config.get("background_color", "#181a26")

        if wallpaper:
            wallpaper_path = Path(wallpaper).expanduser()
            if wallpaper_path.is_file():
                pixmap = QtGui.QPixmap(str(wallpaper_path))
                if not pixmap.isNull():
                    palette = self.palette()
                    brush = QtGui.QBrush(
                        pixmap.scaled(
                            self.size(),
                            QtCore.Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                            QtCore.Qt.TransformationMode.SmoothTransformation,
                        )
                    )
                    palette.setBrush(QtGui.QPalette.ColorRole.Window, brush)
                    self.setPalette(palette)
                    self.setAutoFillBackground(True)
                    return

        self.setStyleSheet(
            self._base_stylesheet
            + f"\n#AuroraRoot {{ background-color: {background_color}; }}"
        )

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)
        self.apply_background()

    def _start_open_animation(self) -> None:
        animation = QtCore.QPropertyAnimation(self, b"windowOpacity")
        animation.setDuration(360)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuad)
        animation.start(QtCore.QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        event.accept()


def run_aurora_gui(config: dict[str, Any]) -> int:
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    window = AuroraShellWindow(config)
    window.show()
    return app.exec()
