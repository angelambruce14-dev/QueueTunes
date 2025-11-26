from DequeNode import DequeNode

"""

"""
class PlaybackQueue:
    def __init__(self):
        self.head = None
        self.tail = None

        #this is the "now playing" reference
        self.current = None


        self.size = 0

    #clears existing queue, traverses playlist linked list
    #calls push_back to insert into the queue
    #set current to the first node
    #GUI play button/clear queue
    def load_playlist(self, playlist):

        self.head = None
        self.tail = None
        self.size = 0

        pointer = playlist.head

        #assuming playlist is not empty
        while pointer is not None:
            self.push_back(pointer.song)
            pointer = pointer.next
        self.current = self.head

    #inserts a song into the end(back) of the queue
    def push_back(self, song):
        #create a new DequeNode
        new_node = DequeNode(song)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self.current = new_node

        else:
            self.tail.next = new_node
            new_node.previous = self.tail
            self.tail = new_node

        self.size += 1
        #when the queue is empty, a song should set the new node as both the head, tail and current
        #when the queue already has items, it should update the tail to the new node
        #and set the old tail's next pointer to the new node

    #moves the current pointer forward (does not modify queue)
    def next_song(self):
        #if the queue is empty: nothing to move forward
        if self.head is None:
            return
        #if next song exists, move forward
        elif self.current.next is not None:
            self.current = self.current.next
        else:
            #playback loop
            self.current = self.head

    #moves current pointer backwards
    def previous(self):
        #if queue is empty: do nothing
        #if no previous song: do nothing
        if self.head is None:
            return
        elif self.current.prev is not None:
            self.current = self.current.prev
        else:
            pass


    #add to up next using current song playing
    #move down (closer to tail)

    def insert_after(self, target_node, song):
        new_node = DequeNode(song)

        #case for empty queue
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self.current = new_node

        #target_node is at the end of the queue
        elif target_node == self.tail:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

        #to insert a node in the middle of the queue
        else:
            successor = target_node.next
            new_node.next = successor
            new_node.prev = target_node
            target_node.next = new_node
            successor.prev = new_node

        self.size +=1

    #move "up" the queue meaning closer to the head
    def insert_before(self, target_node, song):
        new_node = DequeNode(song)
        #case 1: queue is empty
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self.current = new_node

        #case 2: adding before head
        elif target_node == self.head:
            self.head.prev = new_node
            new_node.next = self.head
            self.head = new_node

        else:
            predecessor = target_node.prev
            new_node.next = target_node
            new_node.prev = predecessor
            predecessor.next = new_node
            target_node.prev = new_node

        self.size +=1




    def remove_node(self, node_to_remove):
        successor = node_to_remove.next
        predecessor = node_to_remove.prev

        if successor is not None:
            successor.prev = predecessor


        if predecessor is not None:
            predecessor.next = successor


        if node_to_remove == self.head:
            self.head = successor
        if node_to_remove == self.tail:
            self.tail = predecessor
        if self.current == node_to_remove:
            if successor is not None:
                self.current = successor
            else:
                self.current = predecessor
        self.size -=1


