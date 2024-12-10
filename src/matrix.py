class Matrix:

    UP = (0, -1)
    DOWN = (0, 1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)

    def __init__(self, matrix, x_pos=0, y_pos=0, direction=UP):
        self.matrix = matrix
        self.position = (x_pos, y_pos)
        self.direction = direction
        self.width = len(matrix[0])
        self.height = len(matrix)

    @classmethod
    def from_inputfile(cls, inputfile):
        matrix = []
        with open(inputfile) as f:
            for line in f.readlines():
                matrix.append([char for char in line.strip()])
        return cls(matrix)

    def __str__(self):
        return str(self.matrix)
        
    def set_direction(self, direction):
        self.direction = direction

    def is_out_of_bounds(self, position):
        return position[0] < 0 or position[0] >= self.width or position[1] < 0 or position[1] >= self.height
    
    def get(self, x, y):
        return self.matrix[y][x]
    
    def get_neighbors(self, x, y):
        neighbors = []
        for direction in [self.UP, self.DOWN, self.RIGHT, self.LEFT]:
            neighbor = (x + direction[0], y + direction[1])
            if not self.is_out_of_bounds(neighbor):
                neighbors.append(neighbor)
        return neighbors

    def move(self, direction, steps=1):
        '''
        move into one of the available directions UP, DOWN, RIGHT, LEFT.
        return the new position if in bounds, (-1, -1) if the chosen direction is out of bounds
        '''
        new_position = (self.position[0] + direction[0]*steps, self.position[1] + direction[1]*steps)
        if self.is_out_of_bounds(new_position):
            return (-1, -1)
        else:
            self.position = new_position
            return (new_position)
