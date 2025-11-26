from PlaylistNode import PlaylistNode

#represents an ordered singly-linked list of Songs
class Playlist:
    def __init__(self, playlist_name):
        self.playlist_name = playlist_name
        self.head = None
        self.tail = None

    #core linked list functionality
    def add_song(self, song):
        #creates an instance of a new_song with head and tail set as itself
        self.append_node(PlaylistNode(song))


    def append_node(self, new_node):
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def remove_song(self, song_to_remove):
        previous = None
        current = self.head
        while current is not None:
            if current.data == song_to_remove:
                self.remove_node_after(previous)
                return True
            previous = current
            current = current.next
        #not found
        return False
    def remove_node_after(self, current_node):
        if current_node is None:
            self.head = self.head.next
        if self.head is None:
            self.tail = None
        elif current_node.next is not None:
            succeeding_node = current_node.next.next
            current_node.next = succeeding_node
            if succeeding_node is None:
                self.tail = current_node



    def get_all_songs(self):
        song_list = []
        current_node = self.head
        while current_node is not None:
            #extract the song stored in node
            song_list.append(current_node.song)
            current_node = current_node.next
        return song_list

    def sort_by(self, attribute):
        #fetch list of songs using get_all_songs
        song_list = self.get_all_songs()

        #store sorted_list using merge_sort
        sorted_list = self.merge_sort(song_list, attribute)

        #rebuild linked list using the sorted_list
        self.head = None
        self.tail = None
        for i in sorted_list:
            self.append_node(PlaylistNode(i))



    def merge_sort(self, song_list, attribute):
        #base case: song_list has 1 or 0 items
        if len(song_list) == 1 or len(song_list) == 0:
            return song_list
        else:
            #find the mid of the song_list
            mid = len(song_list) // 2

            #slice the list into two partitions
            left = song_list[:mid]
            right = song_list[mid:]

            #recursively calls merge_sort() on both partitions
            sorted_left = self.merge_sort(left, attribute)
            sorted_right = self.merge_sort(right, attribute)
        #merge sorted_left and sorted_right using merge()
        return self.merge(sorted_left, sorted_right, attribute)

    def merge(self, left_half, right_half, attribute):
        #create empty result list
        merged_songs = []

        #i pointing into left list
        #j pointing into right list
        i = 0
        j = 0

        while i < len(left_half) and j < len(right_half):
            #getattr() to fetch attribute name passed in from sort_by()
            # could be 'title', 'artist_name', etc.
            #
            if getattr(left_half[i], attribute) < getattr(right_half[j], attribute):
                merged_songs.append(left_half[i])
                i += 1
            else:
                merged_songs.append(right_half[j])
                j += 1
        #check to see if left partitions has remaining elements
        while i < len(left_half):
            merged_songs.append(left_half[i])
            i += 1
        #check to see if right partition has remaining elements
        while j < len(right_half):
            merged_songs.append(right_half[j])
            j += 1

        return merged_songs
