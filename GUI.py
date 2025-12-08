import tkinter as tk
from PlaylistManager import PlaylistManager
from PlaybackQueue import PlaybackQueue




class MyApp:
    #GUI constructor
    def __init__(self):
        #instantiating PlaylistManager and PlaybackQueue
        self.manager = PlaylistManager()
        self.playback = PlaybackQueue()

        #window object
        self.root = tk.Tk()
        self.root.title("QueueTunes")


        center_window(self.root)

        #create playlist button
        self.button = tk.Button(self.root, width=20, text="Create New Playlist",
                                command=lambda: create_playlist(self.root))
        self.button.pack(pady=15)

        #view playlist
        self.button = tk.Button(self.root, width=20, text="View Playlists")
        self.button.pack(pady=15)

        #view songs
        self.button = tk.Button(self.root, width=20, text="My Songs")
        self.button.pack(pady=15)

    def run(self):
        self.root.mainloop()


def center_window(current_window, width = 300, height = 200):

    screen_width = current_window.winfo_screenwidth()
    screen_height = current_window.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    current_window.geometry('%dx%d+%d+%d' % (width, height, x, y))

def create_playlist(current_window):
    current_window.destroy()


    new_window = tk.Tk()
    center_window(new_window, 500, 200)
    new_window.title("New Playlist")

    label = tk.Label(new_window, text="Playlist Name")
    label.pack()
    entry = tk.Entry(new_window, width=40)
    entry.pack()

    button_frame = tk.Frame(new_window)
    button_frame.pack()


    button = tk.Button(button_frame, width=15, text="Create Playlist")
    button.grid(row=0, column=0, padx=10, pady=10)


    button = tk.Button(button_frame, width=15,  text="Add Song", command=lambda:add_song(new_window))
    button.grid(row=0, column=1,  padx=10, pady=10)

def add_song(current_window):
    current_window.destroy()

    new_window = tk.Tk()
    center_window(new_window, 500, 200)
    new_window.title("Add Song")

    label = tk.Label(new_window, text="Title")
    label.pack()
    entry=tk.Entry(new_window, width=40)
    entry.pack()

    