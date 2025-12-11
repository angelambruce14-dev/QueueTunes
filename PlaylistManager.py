import json
import os
from Playlist import Playlist
from Song import Song


class PlaylistManager:
    def __init__(self):
        self.playlists = {}

    # -----------------------------------------------------
    # Create playlist (autosaves immediately)
    # -----------------------------------------------------
    def create_playlist(self, name):
        if name and name not in self.playlists:
            self.playlists[name] = Playlist(name)
            self.save_to_file()

    # -----------------------------------------------------
    # Return list of all playlist names
    # -----------------------------------------------------
    def get_all_playlists(self):
        return list(self.playlists.keys())

    # -----------------------------------------------------
    # Get a specific playlist by clean name
    # -----------------------------------------------------
    def get_playlist(self, name):
        clean = name.strip().replace("\ufeff", "")
        return self.playlists.get(clean)

    # -----------------------------------------------------
    # Save playlists to playlists.json
    # -----------------------------------------------------
    def save_to_file(self, filename="playlists.json"):
        data = {}

        for name, playlist in self.playlists.items():
            songs = []
            node = playlist.head

            while node:
                s = node.song
                songs.append({
                    "title": s.title,
                    "artist_name": s.artist_name,
                    "genre": s.genre,
                    "duration": s.duration
                })
                node = node.next

            data[name] = songs

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    # -----------------------------------------------------
    # Load playlists from JSON (with BOM cleaning)
    # -----------------------------------------------------
    def load_from_file(self, filename="playlists.json"):
        use_starter = False
        data = None

        # ---------- Determine which file to load ----------
        if not os.path.exists(filename):
            use_starter = True

        else:
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # If playlists.json contains no playlists (empty dict)
                # or keys map to empty lists → treat as invalid
                if not data or all(len(v) == 0 for v in data.values()):
                    use_starter = True

            except:
                use_starter = True

        # ---------- Load starter file if needed ----------
        if use_starter:
            if os.path.exists("starter_playlists.json"):
                with open("starter_playlists.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                return  # nothing to load

        # ---------- Rebuild playlists ----------
        self.playlists = {}

        for raw_name, song_list in data.items():
            # CLEAN THE PLAYLIST NAME
            name = raw_name.strip().replace("\ufeff", "")

            playlist_obj = Playlist(name)

            for s in song_list:
                title = s.get("title", "")
                artist = s.get("artist_name", "")
                genre = s.get("genre") or ""
                duration = s.get("duration") or ""

                song_obj = Song(title, artist, genre, duration)
                playlist_obj.add_song(song_obj)

            self.playlists[name] = playlist_obj
