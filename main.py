import customtkinter as ctk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox, Toplevel
import os
import pygame

#Using Custom Tkinter

class MusicPlayer(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        ctk.CTkFrame.__init__(self, master, **kwargs)
        self.song_paths = []
        self.master = master
        self.master.title("SpotiPlay")
        self.master.geometry("1000x600")

        self.dark_mode = False
        self.font = ("Segoe UI", 12)
        self.now_playing_window = None

        pygame.init()
        self.music_player = pygame.mixer.music

        style = ttk.Style()
        style.configure("Custom.Treeview", 
                        background="#393E46", 
                        foreground="#EEEEEE", 
                        fieldbackground="#393E46", 
                        bordercolor="#00ADB5", 
                        borderwidth=0,
                        rowheight=25)

        style.configure("Custom.Treeview.Heading",
                        background="#222831", 
                        foreground="#EEEEEE", 
                        bordercolor="#222831", 
                        borderwidth=1)

        style.map('Custom.Treeview', 
                  background=[('selected', '#00ADB5')], 
                  foreground=[('selected', '#EEEEEE')])

        self.header_frame = ctk.CTkFrame(self, height=60, corner_radius=10, fg_color="#222831")
        self.header_frame.pack(side="top", fill="x", pady=(10, 0))

        self.content_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#393E46")
        self.content_frame.pack(side="top", fill="both", expand=True, padx=20, pady=(10, 10))

        self.footer_frame = ctk.CTkFrame(self, height=60, corner_radius=10, fg_color="#222831")
        self.footer_frame.pack(side="bottom", fill="x", pady=(0, 10))

        self.logo_label = ctk.CTkLabel(self.header_frame, text="🎵 SpotiPlay", font=("Segoe UI", 16, "bold"), text_color="#EEEEEE")
        self.logo_label.pack(side="left", padx=20)

        self.search_entry = ctk.CTkEntry(self.header_frame, width=300, height=30, font=self.font, placeholder_text="Search...", text_color="#EEEEEE", fg_color="#393E46", border_color="#00ADB5")
        self.search_entry.pack(side="left", padx=10)

        self.search_button = ctk.CTkButton(self.header_frame, text="🔍 Search", command=self.search_music, width=100, height=30, font=self.font, text_color="#EEEEEE", fg_color="#00ADB5", hover_color="#00BFFF")
        self.search_button.pack(side="left", padx=10)

        self.load_button = ctk.CTkButton(self.header_frame, text="📁 Carregar Músicas", command=self.load_songs_from_directory, width=150, height=30, font=self.font, text_color="#EEEEEE", fg_color="#00ADB5", hover_color="#00BFFF")
        self.load_button.pack(side="left", padx=10)

        self.playlist_listbox = ttk.Treeview(self.content_frame, columns=("Column1",), show="headings", height=15, style="Custom.Treeview")
        self.playlist_listbox.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        self.playlist_listbox.heading("Column1", text="Playlist")
        self.playlist_listbox.column("Column1", width=400)

        self.song_info_label = ctk.CTkLabel(self.content_frame, text="", wraplength=400, font=("Segoe UI", 12, "italic"), text_color="#EEEEEE")
        self.song_info_label.pack(side="right", padx=20)

        self.dark_mode_button = ctk.CTkButton(self.content_frame, text="🌙 Dark Mode", command=self.toggle_dark_mode, width=120, height=30, font=self.font, text_color="#EEEEEE", fg_color="#00ADB5", hover_color="#00BFFF")
        self.dark_mode_button.pack(pady=20)

        self.play_button = ctk.CTkButton(self.footer_frame, text="▶️ Play", command=self.play_music, width=100, height=40, font=self.font, text_color="#EEEEEE", fg_color="#00ADB5", hover_color="#00BFFF")
        self.play_button.pack(side="left", padx=20)

        self.pause_button = ctk.CTkButton(self.footer_frame, text="⏸️ Pause", command=self.pause_music, width=100, height=40, font=self.font, text_color="#EEEEEE", fg_color="#00ADB5", hover_color="#00BFFF")
        self.pause_button.pack(side="left", padx=10)

        self.stop_button = ctk.CTkButton(self.footer_frame, text="⏹️ Stop", command=self.stop_music, width=100, height=40, font=self.font, text_color="#EEEEEE", fg_color="#00ADB5", hover_color="#00BFFF")
        self.stop_button.pack(side="left", padx=10)

        self.volume_slider = ctk.CTkSlider(self.footer_frame, from_=0, to=1, number_of_steps=100, command=self.change_volume, width=150, fg_color="#00ADB5", button_color="#EEEEEE")
        self.volume_slider.set(0.5)
        self.volume_slider.pack(side="right", padx=20)

    def toggle_dark_mode(self):
        if self.dark_mode:
            self.master.configure(bg="#FFFFFF")
            self.content_frame.configure(fg_color="#EEEEEE")
            self.song_info_label.configure(text_color="#222831")
            self.dark_mode_button.configure(text="🌙 Dark Mode")
            self.dark_mode = False
        else:
            self.master.configure(bg="#222831")
            self.content_frame.configure(fg_color="#393E46")
            self.song_info_label.configure(text_color="#EEEEEE")
            self.dark_mode_button.configure(text="☀️ Light Mode")
            self.dark_mode = True

    def search_music(self):
        pass

    def load_songs_from_directory(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            supported_formats = ('.mp3', '.wav', '.ogg')
            for root, _, files in os.walk(folder_path):
                for file in files:
                    if file.endswith(supported_formats):
                        file_path = os.path.join(root, file)
                        self.song_paths.append(file_path)
                        self.playlist_listbox.insert("", "end", values=(os.path.basename(file_path),))

    def show_now_playing_window(self, song_name):
        if self.now_playing_window is None or not self.now_playing_window.winfo_exists():
            self.now_playing_window = Toplevel(self)
            self.now_playing_window.title("Now Playing")
            self.now_playing_window.geometry("400x200")
            self.now_playing_label = ctk.CTkLabel(self.now_playing_window, text="", font=("Segoe UI", 16, "bold"))
            self.now_playing_label.pack(expand=True, pady=50)
        self.now_playing_label.config(text=f"Now Playing: {song_name}")

    def play_music(self):
        selected_item = self.playlist_listbox.selection()[0]
        song_index = self.playlist_listbox.index(selected_item)
        song_path = self.song_paths[song_index]
        self.music_player.load(song_path)
        self.music_player.play()
        self.song_info_label.config(text=f"Playing: {os.path.basename(song_path)}")
        self.show_now_playing_window(os.path.basename(song_path))

    def pause_music(self):
        self.music_player.pause()
        self.song_info_label.config(text="Paused")

    def stop_music(self):
        self.music_player.stop()
        self.song_info_label.config(text="Stopped")

    def change_volume(self, value):
        self.music_player.set_volume(float(value))

if __name__ == "__main__":
    root = ctk.CTk()
    app = MusicPlayer(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
