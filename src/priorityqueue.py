import heapq

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0  # for handling items with equal priority
    
    def push(self, item, priority):
        # Note: heapq implements a min heap, so lower numbers = higher priority
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1
    
    def pop(self):
        return heapq.heappop(self._queue)[-1]
    
    def is_empty(self):
        return len(self._queue) == 0