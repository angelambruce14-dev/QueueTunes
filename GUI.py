import tkinter as tk
from PlaylistManager import PlaylistManager
from PlaybackQueue import PlaybackQueue
from tkinter import messagebox
from Song import Song


def center_window(current_window, width=300, height=200):
    screen_width = current_window.winfo_screenwidth()
    screen_height = current_window.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    current_window.geometry('%dx%d+%d+%d' % (width, height, x, y))

class MyApp:
    #GUI constructor
    def __init__(self):
        #instantiating PlaylistManager and PlaybackQueue
        self.manager = PlaylistManager()
        self.playback = PlaybackQueue()

        #window object
        self.root = tk.Tk()
        self.root.title("QueueTunes")


        center_window(self.root, 300, 250)

        #create playlist button
        self.create_btn = tk.Button(self.root, width=20, text="Create New Playlist",
                                    command=lambda: self.open_create_playlist(self.root))
        self.create_btn.pack(pady=15)

        #view playlist
        self.view_btn = tk.Button(self.root, width=20, text="View Playlists", command=lambda: self.view_playlists(self.root))
        self.view_btn.pack(pady=15)

        #view songs
        self.songs_btn = tk.Button(self.root, width=20, text="My Songs")
        self.songs_btn.pack(pady=15)

        self.songs_btn = tk.Button(self.root, width=20, text="Quit", command=lambda: self.root.destroy())
        self.songs_btn.pack(pady=15)

    def run(self):
        self.root.mainloop()

    #def view_playlists(self):


    def open_create_playlist(self, current_window):
        current_window.destroy()

        this_window = tk.Tk()
        center_window(this_window, 500, 100)
        this_window.title("New Playlist")

        label = tk.Label(this_window, text="Playlist Name")
        label.pack()

        entry = tk.Entry(this_window, width=40)
        entry.pack()

        button_frame = tk.Frame(this_window)
        button_frame.pack()

        create_btn = tk.Button(button_frame, width=15, text="Create", command=lambda: self.create_save(this_window, entry))
        create_btn.grid(row=0, column=0, padx=10, pady=10)

        song_btn = tk.Button(button_frame, width=15, text="Add Song", command=lambda: self.add_song(this_window))
        song_btn.grid(row=0, column=1, padx=10, pady=10)

        menu_btn = tk.Button(button_frame, width=15, text="Main Menu", command=lambda: self.back_to_main(this_window))
        menu_btn.grid(row=0, column=2, padx=10, pady=10)


    def create_save(self, window, entry):

        name = entry.get().strip()
        if name:
            message = f"Playlist '{str(name)} created.'"
            messagebox.showinfo(f" ", message)
            playlist_name = self.manager.create_playlist(name)
            window.destroy()

            self.__init__() #back to main menu



        else:

            message = f"Please enter a name."
            messagebox.showinfo(f"!", message)


    def add_song(self, current_window):
        current_window.destroy()

        this_window = tk.Tk()
        this_window.title("Add Song")
        center_window(this_window, 500, 200)

        form = tk.Frame(this_window)
        form.pack(pady=10)

        title_label = tk.Label(form, text="Title")
        title_label.grid(row=0, column=0, padx=10, pady=5)

        title_entry=tk.Entry(form, width=40)
        title_entry.grid()

        artist_label = tk.Label(this_window, text="Artist")
        artist_label.pack()

        artist_entry = tk.Entry(this_window, width=40)
        artist_entry.pack()


        title = title_entry.get()
        artist = artist_entry.get()
        #genre = genre_entry.get()
        #duration = duration_entry.get()



        add_btn = tk.Button(this_window, width=200, text="Add", command=lambda: self.handle_save_songs(this_window, title_entry, artist_entry))

    def handle_save_songs(self, window, title, artist):

        new_song = Song(title, artist, None, None,)
        playlist = self.manager

    def view_playlists(self, current_window):
        current_window.destroy()

        this_window = tk.Tk()
        this_window.title("Your Playlists")
        center_window(this_window, 400, 300)

        tk.Label(this_window, text="Playlists", font=("Arial", 14)).pack(pady=10)

        #listbox
        playlist_listbox = tk.Listbox(this_window, width=40, height=10)
        playlist_listbox.pack(pady=10)

        for name in self.manager.get_playlist():
            playlist_listbox.insert(tk.END, name)
        back_btn = tk.Button(
            this_window,
            text="Main Menu",
            width=20,
            command=lambda: self.back_to_main(this_window)
        )
        back_btn.pack(pady=10)


    def back_to_main(self, current_window):
        current_window.destroy()
        self.__init__()
        self.run()