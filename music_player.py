import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLabel,
    QVBoxLayout, QFileDialog, QSlider, QListWidget, QHBoxLayout
)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QPixmap, QIcon, QFont, QImage
from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.flac import FLAC
import pygame
from PyQt6.QtGui import QFontDatabase
from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtWidgets import QGridLayout

class MusicPlayer(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loopi.io")
        self.setFixedSize(1000, 600)

        pygame.init()
        font_path = "assets/fonts/SanFrancisco/SF-Pro-Display-Regular.otf"
        QFontDatabase.addApplicationFont(font_path)
        self.player = pygame.mixer.music
        self.song_paths = []
        self.current_duration = 0
        self.is_playing = False
        self.updating_slider = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.init_ui()
        self.set_background()

    def set_background(self):
        path = "assets/background.jpg"
        if os.path.exists(path):
            self.bg_label = QLabel(self)
            pixmap = QPixmap(path).scaled(self.size(), Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.bg_label.setPixmap(pixmap)
            self.bg_label.setGeometry(0, 0, self.width(), self.height())
            self.bg_label.lower()
            self.bg_label.setScaledContents(True)
            self.bg_label.show()

    def resizeEvent(self, event):
        if hasattr(self, 'bg_label'):
            self.bg_label.setPixmap(QPixmap("assets/background.jpg").scaled(self.size()))
            self.bg_label.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

    def init_ui(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.list_widget = QListWidget()
        self.list_widget.hide()

        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background-color: rgba(255, 255, 255, 0.08); border-radius: 20px;")
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)
        self.content_widget.setLayout(content_layout)

        progress_wrapper = QWidget()
        progress_wrapper.setFixedHeight(70)
        progress_wrapper.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.04);
            border-radius: 16px;
            border: none;
        """)

        # shadow = QGraphicsDropShadowEffect()
        # shadow.setOffset(0, 4)
        # shadow.setBlurRadius(25)
        # shadow.setColor(Qt.GlobalColor.black)
        # progress_wrapper.setGraphicsEffect(shadow)

        wrapper_layout = QVBoxLayout()
        wrapper_layout.setContentsMargins(12, 8, 12, 4)
        wrapper_layout.setSpacing(0)
        progress_wrapper.setLayout(wrapper_layout)

            # NOVO: Grid com ícones e tempos
        # SLIDER SETUP

        slider_layout = QGridLayout()
        slider_layout.setContentsMargins(0, 0, 0, 0)
        slider_layout.setHorizontalSpacing(8)
        slider_layout.setVerticalSpacing(4)
        slider_layout.setColumnStretch(1, 1)

        # ícones e labels
        repeat_icon = QLabel()
        repeat_icon.setPixmap(QPixmap("assets/icons/repeat.png").scaled(18, 18, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        repeat_icon.setStyleSheet("background: transparent; border: none;")

        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.progress_slider.setRange(0, 100)
        self.progress_slider.sliderReleased.connect(self.seek_music)

        download_icon = QLabel()
        download_icon.setPixmap(QPixmap("assets/icons/download.png").scaled(18, 18, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        download_icon.setStyleSheet("background: transparent; border: none;")

        self.time_label = QLabel("00:00")
        self.time_label.setStyleSheet("color: white; font-size: 11px; background: transparent; border: none;")

        self.duration_label = QLabel("-00:00")
        self.duration_label.setStyleSheet("color: white; font-size: 11px; background: transparent; border: none;")

        # GRID
        slider_layout.addWidget(repeat_icon, 0, 0)
        slider_layout.addWidget(self.progress_slider, 0, 1)
        slider_layout.addWidget(download_icon, 0, 2)

        slider_layout.addWidget(self.time_label, 1, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        slider_layout.addWidget(QWidget(), 1, 1)  # espaço entre os tempos
        slider_layout.addWidget(self.duration_label, 1, 2, alignment=Qt.AlignmentFlag.AlignRight)

        wrapper_layout.addLayout(slider_layout)

        # ✅ aqui é o certo de adicionar o progress_wrapper
        content_layout.addWidget(progress_wrapper)


        info_control_layout = QHBoxLayout()
        info_control_layout.setContentsMargins(20, 0, 20, 0)
        info_control_layout.setSpacing(30)

        self.album_art_label = QLabel()
        self.album_art_label.setFixedSize(180, 180)
        self.album_art_label.setPixmap(QPixmap("assets/no_cover.png"))
        self.album_art_label.setScaledContents(True)
        self.album_art_label.setStyleSheet("border-radius: 20px; border: 5px solid #3B3A3C;")

        text_and_controls = QVBoxLayout()
        self.label = QLabel("Love Sunshine & Hysteria")
        self.label.setFont(QFont("San Francisco", 14, QFont.Weight.Bold))
        self.label.setStyleSheet("color: white; background: transparent; border: none;")

        self.artist_label = QLabel("Artista desconhecido")
        self.artist_label.setStyleSheet("color: #cccccc; font-size: 12px; background: transparent; border: none;")

        control_layout = QHBoxLayout()
        control_layout.setSpacing(10)
        control_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.prev_button = QPushButton()
        self.prev_button.setIcon(QIcon("assets/icons/previous.png"))
        self.prev_button.setIconSize(QSize(32, 32))
        self.prev_button.setStyleSheet("background: transparent; border: none;")

        self.play_button = QPushButton()
        self.play_button.setIcon(QIcon("assets/icons/play-button.png"))
        self.play_button.setIconSize(QSize(32, 32))
        self.play_button.setStyleSheet("background: transparent; border: none;")
        self.play_button.clicked.connect(self.toggle_play_pause)

        self.next_button = QPushButton()
        self.next_button.setIcon(QIcon("assets/icons/next-button.png"))
        self.next_button.setIconSize(QSize(32, 32))
        self.next_button.setStyleSheet("background: transparent; border: none;")

        for btn in [self.prev_button, self.play_button, self.next_button]:
            shadow = QGraphicsDropShadowEffect()
            shadow.setOffset(2, 2)
            shadow.setBlurRadius(8)
            btn.setGraphicsEffect(shadow)
            control_layout.addWidget(btn)

        text_and_controls.addWidget(self.label)
        text_and_controls.addWidget(self.artist_label)
        text_and_controls.addLayout(control_layout)

        info_control_layout.addWidget(self.album_art_label)
        info_control_layout.addLayout(text_and_controls)

        dance_layout = QHBoxLayout()
        dance_layout.setSpacing(20)
        for style in ["Dance", "Rock", "Eletronic", "Chill"]:
            btn = QPushButton(style)
            btn.setFixedSize(100, 36)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3B3A3C;
                    color: white;
                    border: none;
                    border-radius: 18px;
                    font-weight: bold;
                }
            """)
            shadow = QGraphicsDropShadowEffect()
            shadow.setOffset(2, 2)
            shadow.setBlurRadius(12)
            shadow.setColor(Qt.GlobalColor.black)
            btn.setGraphicsEffect(shadow)

            dance_layout.addWidget(btn)


        source_layout = QHBoxLayout()
        source_layout.setSpacing(40)
        source_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        stream_btn = QPushButton("Stream")
        stream_btn.setIcon(QIcon("assets/icons/streaming.png"))
        stream_btn.setIconSize(QSize(32, 32))
        stream_btn.setStyleSheet("background: transparent; border: none; color: white; font-weight: bold;")

        local_btn = QPushButton("Local")
        local_btn.setIcon(QIcon("assets/icons/music.png"))
        local_btn.setIconSize(QSize(32, 32))
        local_btn.setStyleSheet("background: transparent; border: none; color: white; font-weight: bold;")
        local_btn.clicked.connect(self.load_music)

        source_layout.addWidget(stream_btn)
        source_layout.addWidget(local_btn)

        content_layout.addLayout(info_control_layout)
        content_layout.addLayout(dance_layout)
        content_layout.addLayout(source_layout)

        main_layout.addStretch()
        main_layout.addWidget(self.content_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch()

        if os.path.exists("style.qss"):
            with open("style.qss", "r") as f:
                qss = f.read()
                self.setStyleSheet(qss) 



    def toggle_play_pause(self):
        if self.is_playing:
            self.pause_music()
        else:
            self.play_music()
        self.update_play_icon()

    def update_play_icon(self):
        icon_path = "assets/icons/pause.png" if self.is_playing else "assets/icons/play-button.png"
        self.play_button.setIcon(QIcon(icon_path))

    def load_music(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Music Folder")
        if folder:
            self.song_paths.clear()
            self.list_widget.clear()
            for file in os.listdir(folder):
                if file.endswith(('.mp3', '.wav', '.ogg')):
                    full_path = os.path.join(folder, file)
                    self.song_paths.append(full_path)
                    self.list_widget.addItem(file)

    def play_music(self):
        current_item = self.list_widget.currentRow()
        if 0 <= current_item < len(self.song_paths):
            file_path = self.song_paths[current_item]
            self.player.load(file_path)
            self.player.play()
            self.display_album_art(file_path)
            try:
                audio = MP3(file_path, ID3=ID3)
                self.current_duration = int(audio.info.length)
                self.progress_slider.setRange(0, self.current_duration)
                self.duration_label.setText(f"-{self.format_time(self.current_duration)}")
                self.timer.start(500)
                self.is_playing = True
                self.update_play_icon()
                title = audio.get("TIT2")
                artist = audio.get("TPE1")
                self.label.setText(str(title) if title else os.path.basename(file_path))
                self.artist_label.setText(str(artist) if artist else "Artista desconhecido")
            except Exception as e:
                print(f"[ERRO] Metadados: {e}")
                self.label.setText(os.path.basename(file_path))
                self.artist_label.setText("Artista desconhecido")

    def pause_music(self):
        self.player.pause()
        self.is_playing = False
        self.timer.stop()
        self.update_play_icon()

    def seek_music(self):
        value = self.progress_slider.value()
        pygame.mixer.music.play(start=value)
        self.is_playing = True
        self.update_play_icon()

    def update_progress(self):
        if self.is_playing:
            position_ms = pygame.mixer.music.get_pos()
            if position_ms >= 0:
                seconds = position_ms // 1000
                self.updating_slider = True
                self.progress_slider.setValue(seconds)
                self.updating_slider = False
                self.time_label.setText(self.format_time(seconds))
                self.duration_label.setText(f"-{self.format_time(self.current_duration - seconds)}")

    def format_time(self, seconds):
        m, s = divmod(seconds, 60)
        return f"{int(m):02}:{int(s):02}"

    def display_album_art(self, file_path):
        try:
            image_data = None
            if file_path.lower().endswith('.mp3'):
                audio = MP3(file_path, ID3=ID3)
                for tag in audio.tags.values():
                    if tag.FrameID == "APIC":
                        image_data = tag.data
                        break
            elif file_path.lower().endswith('.flac'):
                audio = FLAC(file_path)
                if audio.pictures:
                    image_data = audio.pictures[0].data
            if image_data:
                image = QImage()
                image.loadFromData(image_data)
                self.album_art_label.setPixmap(QPixmap.fromImage(image))
            else:
                self.album_art_label.setPixmap(QPixmap("assets/no_cover.png"))
        except Exception as e:
            print(f"[ERRO] ao extrair imagem: {e}")
            self.album_art_label.setPixmap(QPixmap("assets/no_cover.png"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MusicPlayer()
    window.show()
    sys.exit(app.exec())