import subprocess
import sys
from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette


class DisplayRotationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_mode = "normal"
        self._build_ui()
        self._refresh_status()

    def _build_window_icon(self):
        pixmap = QtGui.QPixmap(256, 256)
        pixmap.fill(Qt.transparent)

        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        painter.setBrush(QColor(71, 145, 255))
        painter.drawRoundedRect(48, 78, 160, 104, 24, 24)

        painter.setBrush(QColor(255, 255, 255))
        painter.drawRoundedRect(70, 94, 116, 72, 16, 16)
        painter.drawRect(104, 166, 48, 16)
        painter.drawRect(116, 182, 24, 12)

        painter.end()
        return QtGui.QIcon(pixmap)

    def _build_ui(self):
        self.setWindowTitle("Screen Flipper")
        self.resize(420, 240)
        self.setMinimumSize(360, 220)
        self.setWindowIcon(self._build_window_icon())

        container = QtWidgets.QWidget(self)
        layout = QtWidgets.QVBoxLayout(container)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QtWidgets.QLabel("Adjust the display orientation")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: 600;")
        layout.addWidget(title)

        self.toggle_button = QtWidgets.QPushButton("Flip display")
        self.toggle_button.setMinimumHeight(48)
        self.toggle_button.clicked.connect(self.toggle_display)
        layout.addWidget(self.toggle_button)

        self.status_label = QtWidgets.QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        self.setCentralWidget(container)

    def _refresh_status(self):
        if self.current_mode == "normal":
            self.status_label.setText("The display is currently in its default orientation.")
            self.toggle_button.setText("Flip display")
        else:
            self.status_label.setText("The display is currently inverted.")
            self.toggle_button.setText("Restore display")

    def _run_rotation_script(self, mode):
        script_path = Path(__file__).resolve().parent / "flip-screen-only.py"
        if not script_path.exists():
            raise FileNotFoundError("flip-screen-only.py was not found")

        subprocess.run([sys.executable, str(script_path), mode], check=True)

    def toggle_display(self):
        next_mode = "inverted" if self.current_mode == "normal" else "normal"
        try:
            self._run_rotation_script(next_mode)
            self.current_mode = next_mode
            self._refresh_status()
        except Exception as exc:
            self.status_label.setText(f"Rotation failed: {exc}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    window = DisplayRotationWindow()
    window.show()
    sys.exit(app.exec_())