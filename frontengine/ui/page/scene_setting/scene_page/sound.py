from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QSlider, QMessageBox

from frontengine.ui.dialog.choose_file_dialog import choose_player_sound
from frontengine.ui.page.scene_setting.scene_manager import SceneManagerUI
from frontengine.user_setting.scene_setting import scene_json
from frontengine.utils.multi_language.language_wrapper import language_wrapper


class SoundSceneSettingUI(QWidget):

    def __init__(self, script_ui: SceneManagerUI):
        super().__init__()
        self.script_ui = script_ui
        self.ready_to_play = False
        # Volume setting
        self.volume_label = QLabel(
            language_wrapper.language_word_dict.get("Volume")
        )
        self.volume_slider = QSlider()
        self.volume_slider.setMinimum(1)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setTickInterval(1)
        self.volume_slider.setValue(100)
        self.volume_slider_value_label = QLabel(str(self.volume_slider.value()))
        self.volume_slider.setOrientation(Qt.Orientation.Horizontal)
        # Choose file button
        self.player_sound_path: [str, None] = None
        # Choose file button
        self.choose_player_file_button = QPushButton(
            language_wrapper.language_word_dict.get("sound_player_setting_choose_sound_file")
        )
        self.choose_player_file_button.clicked.connect(self.choose_and_copy_sound_file_to_cwd_sound_dir_then_play)
        # Ready label and variable
        self.player_ready_label = QLabel(
            language_wrapper.language_word_dict.get("Not Ready")
        )
        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(self.volume_label, 0, 0)
        self.grid_layout.addWidget(self.volume_slider_value_label, 0, 1)
        self.grid_layout.addWidget(self.volume_slider, 0, 2)
        self.grid_layout.addWidget(self.choose_player_file_button, 1, 0)
        self.grid_layout.addWidget(self.player_ready_label, 1, 1)
        self.setLayout(self.grid_layout)

    def choose_and_copy_sound_file_to_cwd_sound_dir_then_play(self) -> None:
        self.player_ready_label.setText(
            language_wrapper.language_word_dict.get("Not Ready")
        )
        self.ready_to_play = False
        self.player_sound_path = choose_player_sound(self)
        if self.player_sound_path is not None:
            self.player_ready_label.setText(
                language_wrapper.language_word_dict.get("Ready")
            )
            self.ready_to_play = True

    def update_scene_json(self):
        if self.player_sound_path is None:
            message_box = QMessageBox(self)
            message_box.setText(
                language_wrapper.language_word_dict.get('not_prepare')
            )
            message_box.show()
        else:
            scene_json.update(
                {
                    "SCENE": {
                        "type": "SOUND",
                        "sound_path": self.player_sound_path,
                        "volume": float(self.volume_slider.value() / 100)
                    }
                }
            )
            self.script_ui.renew_json_plain_text()
