from PlaylistNode import PlaylistNode

# Represents an ordered singly-linked list of Songs
class Playlist:
    def __init__(self, playlist_name):
        self.playlist_name = playlist_name
        self.head = None
        self.tail = None

    # -----------------------------------------------------
    # Add a song to the end of the playlist
    # -----------------------------------------------------
    def add_song(self, song):
        new_node = PlaylistNode(song)

        if self.head is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    # -----------------------------------------------------
    # Remove a specific song from the playlist
    # -----------------------------------------------------
    def remove_song(self, song_to_remove):
        previous = None
        current = self.head

        while current is not None:
            if current.song == song_to_remove:
                # Removing head
                if previous is None:
                    self.head = current.next
                    if self.head is None:
                        self.tail = None
                else:
                    previous.next = current.next
                    if current == self.tail:
                        self.tail = previous
                return True

            previous = current
            current = current.next

        return False

    # -----------------------------------------------------
    # Remove the node AFTER the given node
    # -----------------------------------------------------
    def remove_node_after(self, current_node):
        if current_node is None:
            # Removing the head
            self.head = self.head.next if self.head else None
            if self.head is None:
                self.tail = None
            return

        # Removing after current_node
        if current_node.next is not None:
            succeeding_node = current_node.next.next
            current_node.next = succeeding_node

            if succeeding_node is None:
                self.tail = current_node

    # -----------------------------------------------------
    # Return all songs as a Python list
    # -----------------------------------------------------
    def get_all_songs(self):
        song_list = []
        current_node = self.head

        while current_node is not None:
            song_list.append(current_node.song)
            current_node = current_node.next

        return song_list

    # -----------------------------------------------------
    # Sort playlist by an attribute using merge sort
    # -----------------------------------------------------
    def sort_by(self, attribute):
        song_list = self.get_all_songs()
        sorted_list = self.merge_sort(song_list, attribute)

        # Rebuild linked list
        self.head = None
        self.tail = None

        for song in sorted_list:
            self.add_song(song)

    # -----------------------------------------------------
    # Merge sort implementation for songs
    # -----------------------------------------------------
    def merge_sort(self, song_list, attribute):
        if len(song_list) <= 1:
            return song_list

        mid = len(song_list) // 2
        left = song_list[:mid]
        right = song_list[mid:]

        sorted_left = self.merge_sort(left, attribute)
        sorted_right = self.merge_sort(right, attribute)

        return self.merge(sorted_left, sorted_right, attribute)

    # -----------------------------------------------------
    # Merge two sorted lists
    # -----------------------------------------------------
    def merge(self, left_half, right_half, attribute):
        merged_songs = []
        i = j = 0

        while i < len(left_half) and j < len(right_half):
            if getattr(left_half[i], attribute) < getattr(right_half[j], attribute):
                merged_songs.append(left_half[i])
                i += 1
            else:
                merged_songs.append(right_half[j])
                j += 1

        # Append leftovers
        merged_songs.extend(left_half[i:])
        merged_songs.extend(right_half[j:])

        return merged_songs
