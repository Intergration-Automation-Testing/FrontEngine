import os
from pathlib import Path

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QIcon
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QMessageBox

from frontengine.utils.multi_language.language_wrapper import language_wrapper


class WebWidget(QWebEngineView):

    def __init__(self, url: str, opacity: float = 0.2,
                 is_file: bool = False, enable_input: bool = False
                 ):
        super().__init__()
        self.setWindowOpacity(opacity)
        if not enable_input:
            self.setWindowFlag(
                Qt.WindowType.WindowTransparentForInput
            )
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlag(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.CoverWindow
        )
        if not is_file:
            self.load(url)
        else:
            self.web_url = Path(url)
            if self.web_url.exists() and self.web_url.is_file():
                # QUrl non ascii path encode, Avoid read wrong path and file name
                source = QUrl.fromLocalFile(str(self.web_url).encode())
                source = source.fromEncoded(source.toEncoded())
                print(f"Origin file {str(self.web_url)}")
                self.load(source)
            else:
                message_box = QMessageBox(self)
                message_box.setText(
                    language_wrapper.language_word_dict.get("webview_message_box_text")
                )
                message_box.show()
        # Set Icon
        self.icon_path = Path(os.getcwd() + "/je_driver_icon.ico")
        if self.icon_path.exists() and self.icon_path.is_file():
            self.setWindowIcon(QIcon(str(self.icon_path)))
