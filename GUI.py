import tkinter as tk
from tkinter import messagebox, ttk

from PlaylistManager import PlaylistManager
from PlaybackQueue import PlaybackQueue
from Song import Song


# ============================
# VAPORWAVE COLOR PALETTE
# ============================

BG_DARK = "#0D0221"       # Deep cosmic purple (background)
PANEL_DARK = "#1A0433"    # Slightly lighter purple (frames/panels)

NEON_PINK = "#FF77E9"     # Titles / highlights
ELECTRIC_BLUE = "#6BCBFF" # Buttons / accents
TEXT_LIGHT = "#F8F1FF"    # Lavender white text

SELECT_BG = "#FF77E9"     # Listbox selection
SELECT_FG = "#0D0221"     # Text on selected item


def center_window(window, width=420, height=420):
    sw = window.winfo_screenwidth()
    sh = window.winfo_screenheight()
    x = (sw // 2) - (width // 2)
    y = (sh // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


# =====================================================================
#                           THEMED APP CLASS
# =====================================================================

class MyApp:
    def __init__(self):
        self.manager = PlaylistManager()
        self.manager.load_from_file()
        self.playback = PlaybackQueue()

        self.current_playlist = None

        self.root = tk.Tk()
        self.root.title("QueueTunes")
        center_window(self.root)
        self.root.configure(bg=BG_DARK)

        self.style = ttk.Style()
        self.apply_global_style()

        self.current_frame = None

        self.show_main_menu()
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

    # -----------------------------------------------------------------
    # APPLY GLOBAL THEME
    # -----------------------------------------------------------------
    def on_exit(self):
        self.manager.save_to_file()
        self.root.destroy()

    def apply_global_style(self):
        self.style.configure("TLabel", foreground=TEXT_LIGHT, background=BG_DARK)
        self.style.configure("TFrame", background=BG_DARK)

        # Combobox styling
        self.style.map("TCombobox",
                       fieldbackground=[("readonly", PANEL_DARK)],
                       selectbackground=[("readonly", PANEL_DARK)],
                       selectforeground=[("readonly", TEXT_LIGHT)])
        self.style.configure("TCombobox",
                             foreground=TEXT_LIGHT,
                             background=PANEL_DARK,
                             borderwidth=0)

    # -------------------
    # Styled Button Maker
    # -------------------
    def vw_button(self, parent, text, cmd, width=20):
        return tk.Button(
            parent,
            text=text,
            command=cmd,
            width=width,
            bg=ELECTRIC_BLUE,
            fg=BG_DARK,
            activebackground=NEON_PINK,
            activeforeground=BG_DARK,
            font=("Courier New", 12, "bold"),
            relief="flat",
            bd=0,
            highlightthickness=0,
            pady=6
        )

    # -------------------
    # Styled Label Maker
    # -------------------
    def vw_label(self, parent, text, size=16, bold=False):
        style = "bold" if bold else "normal"
        return tk.Label(
            parent,
            text=text,
            fg=NEON_PINK if bold else TEXT_LIGHT,
            bg=BG_DARK,
            font=("Courier New", size, style)
        )

    # -------------------
    # Styled Listbox Maker
    # -------------------
    def vw_listbox(self, parent, width=50, height=12):
        lb = tk.Listbox(
            parent,
            width=width,
            height=height,
            bg=PANEL_DARK,
            fg=TEXT_LIGHT,
            selectbackground=SELECT_BG,
            selectforeground=SELECT_FG,
            bd=0,
            highlightthickness=0,
            font=("Courier New", 12)
        )
        return lb

    # ------------------
    # FRAME SWITCH
    # ------------------
    def switch_frame(self, frame):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = frame
        frame.configure(bg=BG_DARK)
        frame.pack(fill="both", expand=True)

    # -------------------------------------------------------------------
    # MAIN MENU (Vaporwave Styled)
    # -------------------------------------------------------------------
    def show_main_menu(self):
        frame = tk.Frame(self.root)

        self.vw_label(frame, "QueueTunes", size=24, bold=True).pack(pady=20)

        self.vw_button(frame, "Create Playlist", self.show_create_playlist).pack(pady=6)
        self.vw_button(frame, "View Playlists", self.view_playlists).pack(pady=6)
        self.vw_button(frame, "Now Playing", self.show_now_playing).pack(pady=6)

        self.vw_button(
            frame,
            "Load Playlists",
            lambda: [
                self.manager.load_from_file(),
                setattr(self, 'current_playlist', None),
                self.view_playlists()
            ],
        ).pack(pady=6)

        self.vw_button(frame, "Quit", self.on_exit).pack(pady=20)

        self.switch_frame(frame)

    # -------------------------------------------------------------------
    # CREATE PLAYLIST
    # -------------------------------------------------------------------
    def show_create_playlist(self):
        frame = tk.Frame(self.root)

        self.vw_label(frame, "Create Playlist", size=18, bold=True).pack(pady=10)

        self.vw_label(frame, "Name:", size=12).pack()
        name_entry = tk.Entry(frame, width=35, bg=PANEL_DARK, fg=TEXT_LIGHT,
                              insertbackground=TEXT_LIGHT, relief="flat")
        name_entry.pack(pady=5)

        def save():
            name = name_entry.get().strip()
            if not name:
                messagebox.showinfo("", "Enter a playlist name.")
                return
            if name in self.manager.playlists:
                messagebox.showinfo("", "Playlist already exists.")
                return

            self.manager.create_playlist(name)
            messagebox.showinfo("", f"Playlist '{name}' created.")
            self.view_playlists()

        self.vw_button(frame, "Create", save).pack(pady=10)
        self.vw_button(frame, "Back", self.show_main_menu).pack()

        self.switch_frame(frame)

    # -------------------------------------------------------------------
    # VIEW PLAYLISTS (Vaporwave Styled)
    # -------------------------------------------------------------------
    def view_playlists(self):
        frame = tk.Frame(self.root)

        self.vw_label(frame, "Playlists", size=18, bold=True).pack(pady=10)

        listbox = self.vw_listbox(frame)
        listbox.pack(pady=10)

        for name in self.manager.get_all_playlists():
            listbox.insert(tk.END, name)

        def open_selected(event=None):
            if not listbox.curselection():
                return
            name = listbox.get(listbox.curselection()[0])
            self.open_playlist_page(name)

        listbox.bind("<Double-Button-1>", open_selected)

        def play_playlist():
            if not listbox.curselection():
                return
            name = listbox.get(listbox.curselection()[0])
            playlist = self.manager.get_playlist(name)

            self.playback.load_playlist(playlist)
            self.playback.current = self.playback.head
            self.show_playback_queue()

        self.vw_button(frame, "Play Playlist", play_playlist).pack(pady=5)
        self.vw_button(frame, "Open Playlist", open_selected).pack(pady=5)
        self.vw_button(frame, "Back", self.show_main_menu).pack(pady=15)

        self.switch_frame(frame)

    # -------------------------------------------------------------------
    # PLAYLIST PAGE (Styled)
    # -------------------------------------------------------------------
    def open_playlist_page(self, playlist_name):
        self.current_playlist = playlist_name
        playlist = self.manager.get_playlist(playlist_name)

        frame = tk.Frame(self.root)

        self.vw_label(frame, f"Playlist: {playlist_name}", size=18, bold=True).pack(pady=10)

        listbox = self.vw_listbox(frame)
        listbox.pack(pady=10)

        def refresh():
            listbox.delete(0, tk.END)
            for s in playlist.get_all_songs():
                listbox.insert(tk.END, f"{s.title} — {s.artist_name} | {s.genre} | {s.duration}")

        refresh()

        btns = tk.Frame(frame, bg=BG_DARK)
        btns.pack(pady=10)

        # Add Song
        self.vw_button(btns, "Add Song", self.show_add_song, width=15).grid(row=0, column=0, padx=5)

        # Remove Song
        def remove_song():
            if not listbox.curselection():
                messagebox.showinfo("", "Select a song.")
                return
            idx = listbox.curselection()[0]
            song = playlist.get_all_songs()[idx]
            playlist.remove_song(song)
            self.manager.save_to_file()
            refresh()

        self.vw_button(btns, "Remove", remove_song, width=15).grid(row=0, column=1, padx=5)

        # Queue Song
        def queue_song():
            if not listbox.curselection():
                messagebox.showinfo("", "Select a song.")
                return
            song = playlist.get_all_songs()[listbox.curselection()[0]]
            self.playback.push_back(song)
            messagebox.showinfo("", f"Queued '{song.title}'.")

        self.vw_button(btns, "Queue Song", queue_song, width=15).grid(row=0, column=2, padx=5)

        # Play Now
        def play_now():
            if not listbox.curselection():
                messagebox.showinfo("", "Select a song.")
                return
            song = playlist.get_all_songs()[listbox.curselection()[0]]

            self.playback.clear()
            self.playback.push_back(song)
            self.playback.current = self.playback.head
            self.manager.save_to_file()
            self.show_playback_queue()

        self.vw_button(btns, "Play Now", play_now, width=15).grid(row=1, column=0, padx=5, pady=5)

        # Queue All
        def queue_all():
            songs = playlist.get_all_songs()
            if not songs:
                messagebox.showinfo("", "Playlist empty.")
                return
            self.playback.clear()
            for s in songs:
                self.playback.push_back(s)
            self.manager.save_to_file()
            messagebox.showinfo("", f"Queued all songs from '{playlist_name}'.")

        self.vw_button(btns, "Queue All", queue_all, width=15).grid(row=1, column=1, padx=5, pady=5)

        # Sorting
        def sort_title():
            playlist.sort_by("title")
            self.manager.save_to_file()
            refresh()

        def sort_artist():
            playlist.sort_by("artist_name")
            self.manager.save_to_file()
            refresh()

        def sort_genre():
            playlist.sort_by("genre")
            self.manager.save_to_file()
            refresh()

        def sort_duration():
            playlist.sort_by("duration")
            self.manager.save_to_file()
            refresh()

        self.vw_button(btns, "Sort Title", sort_title, width=15).grid(row=2, column=0, padx=5, pady=5)
        self.vw_button(btns, "Sort Artist", sort_artist, width=15).grid(row=2, column=1, padx=5, pady=5)
        self.vw_button(btns, "Sort Genre", sort_genre, width=15).grid(row=2, column=2, padx=5, pady=5)
        self.vw_button(btns, "Sort Duration", sort_duration, width=15).grid(row=3, column=1, padx=5, pady=5)

        self.vw_button(frame, "Back", self.view_playlists).pack(pady=15)

        self.switch_frame(frame)

    # -------------------------------------------------------------------
    # ADD SONG (Styled)
    # -------------------------------------------------------------------
    def show_add_song(self):
        playlist = self.manager.get_playlist(self.current_playlist)
        frame = tk.Frame(self.root)

        self.vw_label(frame, f"Add Song to '{self.current_playlist}'",
                      size=16, bold=True).pack(pady=10)

        # Title
        self.vw_label(frame, "Title:").pack()
        title_entry = tk.Entry(frame, width=40, bg=PANEL_DARK, fg=TEXT_LIGHT,
                               insertbackground=TEXT_LIGHT, relief="flat")
        title_entry.pack(pady=5)

        # Artist
        self.vw_label(frame, "Artist:").pack()
        artist_entry = tk.Entry(frame, width=40, bg=PANEL_DARK, fg=TEXT_LIGHT,
                                insertbackground=TEXT_LIGHT, relief="flat")
        artist_entry.pack(pady=5)

        # Genre Dropdown (with StringVar to avoid losing selection)
        genres = ["Pop", "R&B", "Hip-Hop", "Rock", "Indie", "Jazz", "Classical", "Electronic"]
        genre_var = tk.StringVar()
        self.vw_label(frame, "Genre:").pack()
        genre_box = ttk.Combobox(frame, values=genres, width=37, state="readonly", textvariable=genre_var)
        genre_box.pack(pady=5)

        # Duration
        self.vw_label(frame, "Duration (mm:ss):").pack()

        dur_frame = tk.Frame(frame, bg=BG_DARK)
        dur_frame.pack()

        min_entry = tk.Entry(dur_frame, width=5, bg=PANEL_DARK, fg=TEXT_LIGHT,
                             insertbackground=TEXT_LIGHT, relief="flat")
        min_entry.grid(row=0, column=0, padx=3)

        tk.Label(dur_frame, text=":", fg=TEXT_LIGHT, bg=BG_DARK).grid(row=0, column=1)

        sec_entry = tk.Entry(dur_frame, width=5, bg=PANEL_DARK, fg=TEXT_LIGHT,
                             insertbackground=TEXT_LIGHT, relief="flat")
        sec_entry.grid(row=0, column=2, padx=3)

        # -------------------------------
        # SAVE FUNCTION (Correct version)
        # -------------------------------
        def save_song():
            title = title_entry.get().strip()
            artist = artist_entry.get().strip()
            genre = genre_var.get().strip()
            mins = min_entry.get().strip()
            secs = sec_entry.get().strip()

            if not title or not artist:
                messagebox.showinfo("", "Title and Artist required.")
                return

            # Validate & format duration
            if mins.isdigit() and secs.isdigit():
                duration = f"{mins}:{secs.zfill(2)}"
            else:
                duration = ""

            song = Song(title, artist, genre, duration)
            playlist.add_song(song)
            self.manager.save_to_file()
            messagebox.showinfo("", f"Added '{title}'.")
            self.open_playlist_page(self.current_playlist)

        # Buttons
        self.vw_button(frame, "Save", save_song).pack(pady=10)
        self.vw_button(frame, "Back", lambda: self.open_playlist_page(self.current_playlist)).pack()

        self.switch_frame(frame)

    # -------------------------------------------------------------------
    # NOW PLAYING (Styled)
    # -------------------------------------------------------------------
    def show_now_playing(self):
        frame = tk.Frame(self.root)

        self.vw_label(frame, "Now Playing", size=20, bold=True).pack(pady=15)

        name_var = tk.StringVar()

        def refresh():
            if self.playback.current is None:
                name_var.set("No song is playing.")
            else:
                s = self.playback.current.song
                name_var.set(f"{s.title} — {s.artist_name}")

        lbl = tk.Label(frame, textvariable=name_var, fg=TEXT_LIGHT, bg=BG_DARK,
                       font=("Courier New", 16))
        lbl.pack(pady=10)

        refresh()

        ctrl = tk.Frame(frame, bg=BG_DARK)
        ctrl.pack(pady=10)

        self.vw_button(ctrl, "⟵ Previous", lambda: (self.playback.previous(), refresh()),
                       width=15).grid(row=0, column=0, padx=5)
        self.vw_button(ctrl, "Next ⟶", lambda: (self.playback.next_song(), refresh()),
                       width=15).grid(row=0, column=1, padx=5)

        self.vw_button(frame, "Back", self.show_main_menu).pack(pady=15)

        self.switch_frame(frame)

    # -------------------------------------------------------------------
    # PLAYBACK QUEUE (Styled)
    # -------------------------------------------------------------------
    def show_playback_queue(self):
        frame = tk.Frame(self.root)

        self.vw_label(frame, "Playback Queue", size=20, bold=True).pack(pady=10)

        now_playing_var = tk.StringVar()

        def update_now_playing():
            if self.playback.current is None:
                now_playing_var.set("Now Playing: (nothing)")
            else:
                s = self.playback.current.song
                now_playing_var.set(f"Now Playing: {s.title} — {s.artist_name}")

        tk.Label(frame, textvariable=now_playing_var, fg=TEXT_LIGHT, bg=BG_DARK,
                 font=("Courier New", 14)).pack(pady=5)

        listbox = self.vw_listbox(frame)
        listbox.pack(pady=10)

        def get_queue_as_list():
            out = []
            node = self.playback.head
            while node:
                out.append(node.song)
                node = node.next
            return out

        def refresh_listbox():
            listbox.delete(0, tk.END)
            for song in get_queue_as_list():
                listbox.insert(tk.END, f"{song.title} — {song.artist_name}")
            update_now_playing()

        refresh_listbox()

        def rebuild_queue(song_list):
            self.playback.clear()
            for s in song_list:
                self.playback.push_back(s)
            self.playback.current = self.playback.head

        ctrl = tk.Frame(frame, bg=BG_DARK)
        ctrl.pack(pady=10)

        def move_up():
            selection = listbox.curselection()
            if not selection or selection[0] == 0:
                return
            idx = selection[0]
            q = get_queue_as_list()
            q[idx - 1], q[idx] = q[idx], q[idx - 1]
            rebuild_queue(q)
            refresh_listbox()
            listbox.selection_set(idx - 1)

        self.vw_button(ctrl, "Move Up", move_up, width=12).grid(row=0, column=0, padx=5)

        def move_down():
            selection = listbox.curselection()
            q = get_queue_as_list()
            if not selection or selection[0] == len(q) - 1:
                return
            idx = selection[0]
            q[idx + 1], q[idx] = q[idx], q[idx + 1]
            rebuild_queue(q)
            refresh_listbox()
            listbox.selection_set(idx + 1)

        self.vw_button(ctrl, "Move Down", move_down, width=12).grid(row=0, column=1, padx=5)

        def remove_song():
            selection = listbox.curselection()
            if not selection:
                return
            idx = selection[0]
            q = get_queue_as_list()
            q.pop(idx)
            rebuild_queue(q)
            refresh_listbox()

        self.vw_button(ctrl, "Remove", remove_song, width=12).grid(row=0, column=2, padx=5)

        def play_from_here():
            selection = listbox.curselection()
            if not selection:
                return
            idx = selection[0]
            q = get_queue_as_list()

            self.playback.clear()
            for i, s in enumerate(q):
                self.playback.push_back(s)
                if i == idx:
                    self.playback.current = self.playback.tail

            refresh_listbox()

        self.vw_button(ctrl, "Play From Here", play_from_here, width=14)\
            .grid(row=1, column=0, columnspan=3, pady=5)

        def prev_song():
            self.playback.previous()
            refresh_listbox()

        self.vw_button(ctrl, "⟵ Previous", prev_song, width=12).grid(row=2, column=0, padx=5)

        def next_song():
            self.playback.next_song()
            refresh_listbox()

        self.vw_button(ctrl, "Next ⟶", next_song, width=12).grid(row=2, column=1, padx=5)

        self.vw_button(frame, "Back", self.show_main_menu).pack(pady=10)

        self.switch_frame(frame)

    # -------------------------------------------------------------------
    # RUN
    # -------------------------------------------------------------------
    def run(self):
        self.root.mainloop()
