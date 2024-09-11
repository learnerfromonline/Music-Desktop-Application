# Importings

import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtMultimedia import *


# App code
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUi()
        self.event_handler()



    #settings
    def settings(self):
        self.setWindowTitle("Ram's Application")
        self.setGeometry(800,500,400,400)


    #UI
    def initUi(self):
        self.titlle = QLabel("Audio Adjuster")
        self.titlle.setObjectName("title")
        self.titlle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_list = QListWidget()
        self.btn_opener = QPushButton("Choose a file")
        self.btn_play = QPushButton("Play")
        self.btn_resume = QPushButton("Resume")
        self.btn_pause  = QPushButton("Pause")
        self.btn_reset = QPushButton("Reset")



        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(50)
        self.slider.setMaximum(150)
        self.slider.setValue(100)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(10)

        self.slider_text = QLabel("Speed 100x")
        self.slider_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        slider_layout = QHBoxLayout()
        slider_layout.addWidget(self.slider_text)
        slider_layout.addWidget(self.slider)

        self.master = QVBoxLayout()
        row = QHBoxLayout()
        col1 = QVBoxLayout()
        col2 = QVBoxLayout()

        self.master.addWidget(self.titlle)
        self.master.addLayout(slider_layout)

        col1.addWidget(self.file_list)
        col2.addWidget(self.btn_play)
        col2.addWidget(self.btn_opener)
        col2.addWidget(self.btn_resume)
        col2.addWidget(self.btn_pause)
        col2.addWidget(self.btn_reset)

        row.addLayout(col1,2)
        row.addLayout(col2,4)
        self.master.addLayout(row)
        self.setLayout(self.master)

        self.audio_output = QAudioOutput()
        self.media_player = QMediaPlayer()
        self.media_player.setAudioOutput(self.audio_output)
        self.style()
    def event_handler(self):
        self.slider.valueChanged.connect(self.update_slider)
        self.btn_opener.clicked.connect(self.open_files)
        self.btn_play.clicked.connect(self.play_Audio)
        self.btn_pause.clicked.connect(self.pause_audio)
        self.btn_resume.clicked.connect(self.rsume_audio)
        self.btn_reset.clicked.connect(self.reset_audio)
    def update_slider(self):
        speed = self.slider.value()/100
        self.slider_text.setText(f"Speed {speed : .2f}x")
    def open_files(self):
        path = QFileDialog.getExistingDirectory(self,"Select Fooooolder")
        if path:
            self.file_list.clear()
            for file_name in os.listdir(path):
                if file_name.endswith(".mp3"):
                    self.file_list.addItem(file_name)
        else:
            file,_ = QFileDialog.getOpenFileName(self,"Select Files", filter="Audio Files (*.mp3)")
            if file:
                self.file_list.clear()
                self.file_list.addItem(os.path.basename(file))

    def play_Audio(self):
        if self.file_list.selectedItems():
            file_name = self.file_list.selectedItems()[0].text()
            folder_path = QFileDialog.getExistingDirectory(self,"Select Folder")
            file_path = os.path.join(folder_path,file_name)
            file_url = QUrl.fromLocalFile(file_path)

            self.media_player.setSource(file_url)
            self.media_player.setPlaybackRate(self.slider.value()/100.0)
            self.media_player.play()

            self.btn_pause.setEnabled(True)
            self.btn_resume.setDisabled(True)
            self.btn_reset.setEnabled(True)
            self.btn_play.setDisabled(True)
            pass
    def pause_audio(self):
        self.media_player.pause()
        self.btn_pause.setDisabled(True)
        self.btn_resume.setEnabled(True)
        # self.btn_reset.setEnabled(True)
        # self.btn_play.setDisabled(True)
    def rsume_audio(self):
        self.media_player.play()
        self.btn_pause.setEnabled(True)
        self.btn_resume.setDisabled(True)

    def reset_audio(self):
        if self.media_player.isPlaying():
            self.media_player.stop()
        self.media_player.setPosition(0)
        self.media_player.setPlaybackRate(self.slider.value()/100.0)
        self.media_player.play()

        self.btn_play.setEnabled(True)
        self.btn_pause.setEnabled(True)
        self.btn_resume.setEnabled(True)
        self.btn_reset.setDisabled(True)

        QTimer.singleShot(100,lambda :self.btn_reset.setEnabled(True))

    def style(self):
        self.setStyleSheet("""
            QWidget {
                text-align: center;
                font-size: 16px;
                font-weight: normal;
                background-image: url('https://st.depositphotos.com/1605581/3728/i/450/depositphotos_37286313-stock-photo-abstract-medical-background.jpg');
                background-size: cover;
                background-position: center center;
                background-attachment: fixed;
            }

            QPushButton {
                padding: 10px 20px;
                font-size: 26px;
                font-weight: bold;
                color: white;
                background-color: #007BFF;
                border: none;
                border-radius: 5px;
                margin:7px;
            }

            QPushButton:hover {
                background-color: #0056b3;
            }

            QPushButton:pressed {
                background-color: #004085;
            }

            QPushButton:focus {
                outline: none;
                border: 2px solid #007BFF;
            }

            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }

            QLabel {
                font-size: 18px;
                font-weight: normal;
                color: #333;
                background-color: #f0f0f0;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #ccc;
                font-family: 'Papyrus', fantasy;
            }

            #title {
                font-size: 24px;
                font-weight: bold;
                color:white;
                background-color: transparent;
                padding: 15px 20px;
                border-bottom: 2px solid #007BFF;
            }

            QSlider {
                min-height: 20px;
            }

            QSlider::groove:horizontal {
                border: 1px solid #bbb;
                background: #ddd;
                height: 8px;
                border-radius: 4px;
            }

            QSlider::handle:horizontal {
                background: #007BFF;
                border: 2px solid #007BFF;
                width: 20px;
                height: 20px;
                border-radius: 10px;
                margin: -6px 0;
            }

            QSlider::handle:horizontal:hover {
                background: #0056b3;
                border: 2px solid #0056b3;
            }

            QSlider::handle:horizontal:pressed {
                background: #004085;
                border: 2px solid #004085;
            }

            QSlider::sub-page:horizontal {
                background: #007BFF;
                border-radius: 4px;
            }

            QSlider::add-page:horizontal {
                background: #ddd;
                border-radius: 4px;
            }

            QListWidget {
                background-color: #f5f5f5;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 16px;
                color:black;
                font-family: 'Papyrus', fantasy;
            }

            QListWidget::item {
                background-color: #ffffff;
                padding: 10px;
                margin: 5px 0;
                border: 1px solid #ddd;
                border-radius: 3px;
            }

            QListWidget::item:hover {
                background-color: #007BFF;
                color: white;
            }

            QListWidget::item:selected {
                background-color: #0056b3;
                color: white;
            }

            QListWidget::item:selected:active {
                background-color: #004085;
            }

            QListWidget::item:selected:!active {
                background-color: #0056b3;
            }
        """)


if __name__ in "__main__":

    app = QApplication([])
    main = App()
    main.show()
    app.exec()