#represents one link in Playlist
class PlaylistNode:
    def __init__(self, song):
        self.song = song
        self.next = None
