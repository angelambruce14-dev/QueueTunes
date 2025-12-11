from Playlist import Playlist
class PlaylistManager:
    def __init__(self):
        self.playlists = {} # key = name, value = Playlist object


    def create_playlist(self, name):
        if name is None or name in self.playlists:
            pass

        else:
            new_playlist = Playlist(name)
            self.playlists[name] = new_playlist

    def delete_playlist(self, name):
        if name in self.playlists:
            del self.playlists[name]
        else:
            pass


    def get_playlist(self, name):
        if name in self.playlists:
            return self.playlists[name]
        else:
            return None

   #def get_all_playlists(self):





