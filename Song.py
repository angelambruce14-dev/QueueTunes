class Song:
    #represents one Song
    def __init__(self, title, artist_name, genre, duration):
        self.title = title
        self.artist_name = artist_name
        self.genre = genre
        self.duration = duration

    #method to print song info
    def __str__(self):
        return f"{self.title} — {self.artist_name} ({self.genre}, {self.duration})"