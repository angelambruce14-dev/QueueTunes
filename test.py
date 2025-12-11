import unittest
import os
from Song import Song
from Playlist import Playlist
from PlaybackQueue import PlaybackQueue
from PlaylistManager import PlaylistManager


# ======================
#   TEST SONG
# ======================

class TestSong(unittest.TestCase):
    def test_song_fields(self):
        s = Song("Test", "Artist", "Genre", "3:20")
        self.assertEqual(s.title, "Test")
        self.assertEqual(s.artist_name, "Artist")
        self.assertEqual(s.genre, "Genre")
        self.assertEqual(s.duration, "3:20")

    def test_song_str(self):
        s = Song("Test", "Artist", "Genre", "3:20")
        self.assertEqual(str(s), "Test — Artist (Genre, 3:20)")


# ======================
#   TEST PLAYLIST
# ======================

class TestPlaylist(unittest.TestCase):
    def setUp(self):
        self.p = Playlist("MyList")
        self.s1 = Song("A", "X", "Pop", "3:00")
        self.s2 = Song("B", "Y", "Rock", "2:10")

    def test_add_song(self):
        self.p.add_song(self.s1)
        self.p.add_song(self.s2)
        songs = self.p.get_all_songs()
        self.assertEqual(len(songs), 2)
        self.assertEqual(songs[0], self.s1)
        self.assertEqual(songs[1], self.s2)

    def test_remove_song(self):
        self.p.add_song(self.s1)
        self.p.add_song(self.s2)

        self.p.remove_song(self.s1)
        songs = self.p.get_all_songs()

        self.assertEqual(len(songs), 1)
        self.assertEqual(songs[0], self.s2)

    def test_sort_title(self):
        s3 = Song("C", "Z", "Indie", "3:40")
        self.p.add_song(self.s2)
        self.p.add_song(self.s1)
        self.p.add_song(s3)

        self.p.sort_by("title")
        titles = [s.title for s in self.p.get_all_songs()]
        self.assertEqual(titles, ["A", "B", "C"])


# ======================
#   TEST PLAYBACK QUEUE
# ======================

class TestPlaybackQueue(unittest.TestCase):
    def setUp(self):
        self.q = PlaybackQueue()
        self.s1 = Song("A", "Artist", "Pop", "3:00")
        self.s2 = Song("B", "Artist", "Pop", "2:30")
        self.s3 = Song("C", "Artist", "Pop", "4:00")

    def test_push_back(self):
        self.q.push_back(self.s1)
        self.assertEqual(self.q.head.song, self.s1)
        self.assertEqual(self.q.tail.song, self.s1)

        self.q.push_back(self.s2)
        self.assertEqual(self.q.tail.song, self.s2)
        self.assertEqual(self.q.head.next.song, self.s2)

    def test_next_song(self):
        self.q.push_back(self.s1)
        self.q.push_back(self.s2)
        self.q.push_back(self.s3)

        self.q.current = self.q.head
        self.q.next_song()
        self.assertEqual(self.q.current.song, self.s2)

        self.q.next_song()
        self.assertEqual(self.q.current.song, self.s3)

        # Loop back to start
        self.q.next_song()
        self.assertEqual(self.q.current.song, self.s1)

    def test_previous_song(self):
        self.q.push_back(self.s1)
        self.q.push_back(self.s2)
        self.q.push_back(self.s3)

        self.q.current = self.q.tail
        self.q.previous()
        self.assertEqual(self.q.current.song, self.s2)

        self.q.previous()
        self.assertEqual(self.q.current.song, self.s1)

        # Should stay at head (no looping backward)
        self.q.previous()
        self.assertEqual(self.q.current.song, self.s1)

    def test_clear(self):
        self.q.push_back(self.s1)
        self.q.push_back(self.s2)
        self.q.clear()

        self.assertIsNone(self.q.head)
        self.assertIsNone(self.q.current)
        self.assertEqual(self.q.size, 0)


# ======================
#   TEST PLAYLIST MANAGER
# ======================

TEST_FILE = "test_playlists.json"

class TestPlaylistManager(unittest.TestCase):
    def setUp(self):
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)
        self.pm = PlaylistManager()

    def tearDown(self):
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)

    def test_create_and_get(self):
        self.pm.create_playlist("MyList")
        self.assertIn("MyList", self.pm.playlists)
        pl = self.pm.get_playlist("MyList")
        self.assertIsNotNone(pl)

    def test_save_and_load(self):
        self.pm.create_playlist("TestList")
        pl = self.pm.get_playlist("TestList")

        song = Song("A", "Artist", "Pop", "3:00")
        pl.add_song(song)

        self.pm.save_to_file(TEST_FILE)

        pm2 = PlaylistManager()
        pm2.load_from_file(TEST_FILE)

        self.assertIn("TestList", pm2.playlists)
        songs = pm2.get_playlist("TestList").get_all_songs()

        self.assertEqual(len(songs), 1)
        self.assertEqual(songs[0].title, "A")


# ======================
# RUN ALL
# ======================

if __name__ == "__main__":
    unittest.main()
