from random import randrange
from pygame import Rect, draw
from clock import Clock


class Squares:
    """method for malipulating squares in the game"""
    def __init__(self, st, screen):
        self.st = st
        self.screen = screen
        self.empty_line = [False for i in range(st.square_num_x)]
        self.squares = [self.empty_line.copy() for i in range(st.square_num_y)]
        self.renew_sq()
        self.clock = Clock(st)

    # generate a new current square
    def renew_sq(self):
        self.curr_sq = self.st.new
        self.curr_shape = self.get_shape(self)
        # if new squares are crashed, game over.
        if self.should_stop(self):
            self.st.game_active = False

    # draw all squares
    def draw_squares(self):
        self.draw_exist_sq(self)
        self.draw_curr_sq(self)

    # update squares' information according to settings
    def update(self):
        updated = False # for update screen
        # crash detection
        if self.should_stop(self):
            self.stop(self)
            self.clean_full_lines(self)
            updated = True
        # vertical drop
        if self.st.down or self.clock.is_time_to_drop():
            self.drop(self)
            self.clock.update_drop()
            updated = True
        # rotation
        if self.st.rotate and self.clock.is_time_to_rotate():
            self.rotate(self)
            self.clock.update_rotate()
            updated = True
        # horizontal move
        if self.st.right:
            if self.clock.is_time_to_move() or self.clock.is_time_to_quick_right():
                self.right(self)
            self.clock.update_move()
            updated = True
        if self.st.left:
            if self.clock.is_time_to_move() or self.clock.is_time_to_quick_left():
                self.left(self)
            self.clock.update_move()
            updated = True
        return updated

    @staticmethod
    def drop(self):
        new_sq = self.curr_sq.copy()
        new_sq[0] += 1
        if self.valid(self, new_sq, self.curr_shape):
            self.curr_sq = new_sq

    @staticmethod
    def rotate(self):
        new_shape = self.get_rotated_shape(self)
        if self.valid(self, self.curr_sq, new_shape):
            self.curr_shape = new_shape

    @staticmethod
    def right(self):
        new_sq = self.curr_sq.copy()
        new_sq[1] += 1
        if self.valid(self, new_sq, self.curr_shape):
            self.curr_sq = new_sq

    @staticmethod
    def left(self):
        new_sq = self.curr_sq.copy()
        new_sq[1] -= 1
        if self.valid(self, new_sq, self.curr_shape):
            self.curr_sq = new_sq

    @staticmethod
    def stop(self):
        # copy squares to map
        for sq in self.curr_shape:
            x = sq[1] + self.curr_sq[1]
            y = sq[0] + self.curr_sq[0]
            if y >= 0:
                self.squares[y][x] = True
        x = self.curr_sq[1]
        y = self.curr_sq[0]
        if y >= 0:
            self.squares[y][x] = True
        self.renew_sq()

    @staticmethod
    def clean_full_lines(self):
        for index, line in enumerate(self.squares):
            if sum(line) == self.st.square_num_x:
                self.squares.pop(index)
                self.squares.insert(0, self.empty_line)

    @staticmethod
    def should_stop(self):
        # check shape squares
        for sq in self.curr_shape:
            x = sq[1] + self.curr_sq[1]
            y = sq[0] + self.curr_sq[0] + 1
            if y - 1 >= 0 and not (self.valid_sq(self, [y, x])):
                return True
        # check center square
        x = self.curr_sq[1]
        y = self.curr_sq[0] + 1
        return not (self.valid_sq(self, [y, x]))

    @staticmethod
    def valid(self, square, shape):
        # check shape squares
        for sq in shape:
            x = sq[1] + square[1]
            y = sq[0] + square[0]
            if y >= 0 and not (self.valid_sq(self, [y, x])):
                return False
        # check center square
        return self.valid_sq(self, square)

    @staticmethod
    def valid_sq(self, sq):
        # check border
        if sq[0] >= self.st.square_num_y or \
                        sq[1] >= self.st.square_num_x or \
                        sq[1] < 0:
            return False
        # check crash
        return not (self.squares[sq[0]][sq[1]])

    @staticmethod
    def get_rotated_shape(self):
        new_shape = []
        for sq in self.curr_shape:
            new_shape.append([-sq[1], sq[0]])
        return new_shape

    @staticmethod
    def get_shape(self):
        shape_index = randrange(0, self.st.shape_num)
        return list(self.st.shapes[shape_index])

    @staticmethod
    def draw_exist_sq(self):
        color = self.st.square_color
        for y, row in enumerate(self.squares):
            for x, square in enumerate(row):
                self.draw_square(self, y, x, color, square)

    @staticmethod
    def draw_curr_sq(self):
        color = self.st.square_active_color
        self.draw_square(self, self.curr_sq[0], self.curr_sq[1], color)
        curr_y, curr_x = self.curr_sq[0], self.curr_sq[1]
        for y, x in self.curr_shape:
            self.draw_square(self, y + curr_y, x + curr_x, color)

    @staticmethod
    def draw_square(self, y, x, color=None, square=True):
        x_pos = x * (self.st.square_space + self.st.square_length)
        y_pos = y * (self.st.square_space + self.st.square_length)
        rect = Rect(x_pos, y_pos, self.st.square_length, self.st.square_length)
        if square:
            draw.rect(self.screen, color, rect)
        else:
            draw.rect(self.screen, self.st.square_null_color, rect)
