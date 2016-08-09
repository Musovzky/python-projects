# tetris_mit-ocw_musovzky.py
# Python version: 2.7.11
# Created by: Musovzky (viviyi4@gmail.com)
# Created on: August 8, 2016

# A simple Tetris game controlled with keyboard
# Features: Scoring, levels, pause/resume, restart

# This is the final project of MIT OpenCourseWare:
# A Gentle Introduction to Programming Using Python
# This program is created from the template provided in the course materials

# Note: Graphics.py and a python interpreter is needed to run the program

from graphics import *
import random

######################################
# GLOBAL VARIABLES
######################################

BLOCK_SIZE = 30
OUTLINE_WIDTH = 3
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
FONT = 'helvetica'
TEXT_COLOR = 'white'

######################################
# 0. Define UI text
######################################

class UItext(Text):
    
    def __init__(self,pos,content,size,style,canvas):
        Text.__init__(self,pos,content)
        self.setSize(size)
        self.setStyle(style)
        self.setFace(FONT)
        self.setTextColor(TEXT_COLOR)
        self.draw(canvas)

######################################
# 1. Draw a block
######################################

class Block(Rectangle):
    
    def __init__(self,pos,color):
        self.x = pos.x
        self.y = pos.y
        
        p1 = Point(pos.x*BLOCK_SIZE + OUTLINE_WIDTH,
                   pos.y*BLOCK_SIZE + OUTLINE_WIDTH)
        p2 = Point(p1.x + BLOCK_SIZE,
                   p1.y + BLOCK_SIZE)
        
        Rectangle.__init__(self,p1,p2)
        self.setOutline("grey")
        self.setWidth(OUTLINE_WIDTH)
        self.setFill(color)

    def can_move(self,board,dx,dy):
        return board.can_move(self.x+dx,self.y+dy)
    
    def move(self,dx,dy):
        self.x += dx
        self.y += dy # Update the position of the current shape
        Rectangle.move(self,dx*BLOCK_SIZE,dy*BLOCK_SIZE)
    
######################################
# 2. Define shapes
######################################

class Shape(object):
    
    def __init__(self,coords,color):
        self.blocks = []
        self.rotation_dir = 1
        # Defaults to false since only I, S and Z shift rotation directions
        self.shift_rotation_dir = False
        
        for pos in coords:
            self.blocks.append(Block(pos,color))

        self.center_block = self.blocks[1]
            
    def draw(self,win):
        for block in self.blocks:
            block.draw(win)

    def undraw(self):
        for block in self.blocks:
            block.undraw()

    def move(self,dx,dy):
        for block in self.blocks:
            block.move(dx,dy)

    def can_move(self,board,dx,dy):
        for block in self.blocks:
            if not block.can_move(board,dx,dy):
                return False
        return True
            
    def can_rotate(self,board):
        dir_ = self.rotation_dir
        center = self.center_block
        for block in self.blocks:
            nx = center.x + dir_*center.y - dir_*block.y
            ny = center.y - dir_*center.x + dir_*block.x
            if not board.can_move(nx,ny):
                return False
        return True

    def rotate(self,board):
        dir_ = self.rotation_dir
        center = self.center_block
        for block in self.blocks:
            px = block.x
            py = block.y
            nx = center.x + dir_*center.y - dir_*py
            ny = center.y - dir_*center.x + dir_*px
            block.move(nx-px,ny-py)

        if self.shift_rotation_dir:
            self.rotation_dir *= -1

# 2.1 Define I shapes

class I_shape(Shape):
    
    def __init__(self,ctr):
        coords = [Point(ctr.x-1,ctr.y),
                  Point(ctr.x  ,ctr.y),
                  Point(ctr.x+1,ctr.y),
                  Point(ctr.x+2,ctr.y)]
        Shape.__init__(self,coords,"royal blue")
        self.shift_rotation_dir = True

# 2.2 Define L shapes

class L_shape(Shape):
    
    def __init__(self,ctr):
        coords = [Point(ctr.x-1,ctr.y),
                  Point(ctr.x  ,ctr.y),
                  Point(ctr.x+1,ctr.y),
                  Point(ctr.x-1,ctr.y+1)]
        Shape.__init__(self,coords,"light sky blue")

# 2.3 Define J shapes

class J_shape(Shape):
    
    def __init__(self,ctr):
        coords = [Point(ctr.x-1,ctr.y),
                  Point(ctr.x ,ctr.y),
                  Point(ctr.x+1,ctr.y),
                  Point(ctr.x+1,ctr.y+1)]
        Shape.__init__(self,coords,"pink")

# 2.4 Define S shapes

class S_shape(Shape):
    
    def __init__(self,ctr):
        coords = [Point(ctr.x  ,ctr.y+1),
                  Point(ctr.x  ,ctr.y),
                  Point(ctr.x+1,ctr.y),
                  Point(ctr.x-1,ctr.y+1)]
        Shape.__init__(self,coords,"green yellow")
        self.shift_rotation_dir = True
        self.rotation_dir = -1

# 2.5 Define Z shapes

class Z_shape(Shape):
    
    def __init__(self,ctr):
        coords = [Point(ctr.x-1,ctr.y),
                  Point(ctr.x  ,ctr.y),
                  Point(ctr.x  ,ctr.y+1),
                  Point(ctr.x+1,ctr.y+1)]
        Shape.__init__(self,coords,"tomato")
        self.shift_rotation_dir = True
        self.rotation_dir = -1

# 2.6 Define T shapes

class T_shape(Shape):
    
    def __init__(self,ctr):
        coords = [Point(ctr.x-1,ctr.y),
                  Point(ctr.x  ,ctr.y),
                  Point(ctr.x+1,ctr.y),
                  Point(ctr.x  ,ctr.y+1)]
        Shape.__init__(self,coords,"gold")

# 2.7 Define O shapes

class O_shape(Shape):
    
    def __init__(self,ctr):
        coords = [Point(ctr.x-1,ctr.y),
                  Point(ctr.x  ,ctr.y),
                  Point(ctr.x-1,ctr.y+1),
                  Point(ctr.x  ,ctr.y+1)]
        Shape.__init__(self,coords,"firebrick")

    def rotate(self,board):
        return

######################################
# 3. Define board
######################################

class Board:

    def __init__(self,win):
        self.win = win
        self.canvas = CanvasFrame(win, BOARD_WIDTH * BLOCK_SIZE,
                                  BOARD_HEIGHT * BLOCK_SIZE)
        self.canvas.setBackground("black")
        self.grid = {}

    def draw_shape(self,shape):
        if shape.can_move(self,0,0):
            shape.draw(self.canvas)
            return True
        return False

    def can_move(self,x,y):
        if not (0 <= x < BOARD_WIDTH and 0 <= y < BOARD_HEIGHT):
            return False
        if (x,y) in self.grid.keys():
            return False
        return True

    def add_shape(self,shape):
        for block in shape.blocks:
            self.grid[(block.x,block.y)] = block

    def row_full(self,r):
        for x in range(0,BOARD_WIDTH):
            if (x,r) not in self.grid.keys():
                return False
        return True

    def del_row(self,r):
        for x in range(0,BOARD_WIDTH):
            self.grid[(x,r)].undraw()
            del self.grid[(x,r)]

    def move_down_rows(self,y_start):
        if y_start >= BOARD_HEIGHT:
            y_start = BOARD_HEIGHT-1
        for r in range(y_start,0,-1):
            for c in range(0,BOARD_WIDTH):
                if (c,r) in self.grid.keys():
                    target = self.grid[(c,r)]
                    del self.grid[(c,r)]
                    target.move(0,1)
                    self.grid[(target.x,target.y)] = target
                    
    def remove_full_rows(self):
        rows = 0
        for r in range(1,BOARD_HEIGHT):
            if self.row_full(r):
                self.del_row(r)
                self.move_down_rows(r-1)
                rows += 1
        return rows       

######################################
# 4. Define scoreboard
######################################
class ScoreBoard:

    def __init__(self,win):
        self.height = 0.2 * BOARD_HEIGHT * BLOCK_SIZE
        self.width = 0.5 * BOARD_WIDTH * BLOCK_SIZE
        self.canvas = CanvasFrame(win,self.width,self.height)
        self.canvas.setBackground('black')

        self.level = 1
        self.level_text = UItext(Point(0.5*self.width,0.3*self.height),
                          "Level\n%i" %self.level, 18, 'bold', self.canvas)
        self.score = 0
        self.score_text = UItext(Point(0.5*self.width,0.7*self.height),
                          "Score\n%i" %self.score, 18, 'bold', self.canvas)

        self.get_delay()

    def get_delay(self):
        return 100*(11-self.level)

    def add_score(self,rows):
        self.score += 10 * BOARD_WIDTH * rows ** 2 * (1 + 0.05 * self.level)
        self.score_text.setText("Score\n%i" %self.score)

    def add_level(self):
        if self.score >= 1000 * (2**self.level):
            self.level += 1
            self.level_text.setText("Level\n%i" %self.level)
            return True
        return False

######################################
# 5. Define preview
######################################
class Preview:

    def __init__(self,win):
        self.height = 0.3 * BOARD_HEIGHT * BLOCK_SIZE
        self.width = 0.5 * BOARD_WIDTH * BLOCK_SIZE
        self.canvas = CanvasFrame(win,self.width,self.height)
        self.canvas.setBackground('black')
        self.preview_text = UItext(Point(0.5*self.width,0.15*self.height),
                                 "Next Piece", 18, 'bold', self.canvas)
        
######################################
# 6. Define instructions
######################################
class Instructions:

    def __init__(self,win):
        self.height = 0.48 * BOARD_HEIGHT * BLOCK_SIZE
        self.width = 0.5 * BOARD_WIDTH * BLOCK_SIZE
        self.canvas = CanvasFrame(win,self.width,self.height)
        self.canvas.setBackground('black')
        self.title = UItext(Point(0.52*self.width,0.2*self.height),
                            "Instructions\n\n", 18, 'bold', self.canvas)
        self.instructions_text = UItext(Point(0.52*self.width,0.55*self.height),
                          "Move:\nLeft/Right/Down\n\n\
Rotate: Up\n\nDrop: Space\n\nPause/Resume:\nEsc\n\nRestart: Backspace",
                                        15, 'normal', self.canvas)
        
######################################
# 7. Define tetris
######################################
class Tetris:
    DIRECTION = {'Left':(-1,0), 'Right':(1,0), 'Down':(0,1)}
    SHAPES = [I_shape,J_shape,L_shape,S_shape,Z_shape,T_shape,O_shape]

    def __init__(self,win):
        self.board = Board(win)
        self.board.canvas.canvas.pack(side='left')
        
        self.preview = Preview(win)
        self.preview.canvas.canvas.pack()

        self.scoreboard = ScoreBoard(win)
        self.scoreboard.canvas.canvas.pack()
        
        self.instructions = Instructions(win)
        self.instructions.canvas.canvas.pack()
        
        self.win = win
        self.win.bind_all('<Key>',self.key_pressed)
        
        self.start()

    def create_shape(self):
        return random.choice(self.SHAPES)(
            Point(0.2*BOARD_WIDTH,0.15*BOARD_HEIGHT))

    def animate_shape(self):
        self.do_move("Down")
        if self.state == 'Play': # Note the IF statement here!
            self.timer = self.win.after(self.scoreboard.get_delay(),
                                        self.animate_shape)

    def start(self):
        self.current_shape = random.choice(self.SHAPES)(
            Point(int(0.5*BOARD_WIDTH),0))
        self.board.draw_shape(self.current_shape)
        self.next_shape = self.create_shape()
        self.next_shape.draw(self.preview.canvas)
        self.timer = self.win.after(self.scoreboard.get_delay(),
                                    self.animate_shape)
        self.state = 'Play'

    def pause(self):
        self.win.after_cancel(self.timer)
        self.pause_text = UItext(Point(0.5 * BOARD_WIDTH * BLOCK_SIZE,
                              0.5 * BOARD_HEIGHT * BLOCK_SIZE),
                        "PAUSED\n\nCurrent Level\n%i\nCurrent Score\n%i\n"
                        "\nPress ESC to resume"
                             %(self.scoreboard.level,self.scoreboard.score),
                                 20, 'bold', self.board.canvas)
        self.state = 'Pause'

    def resume(self):
        self.pause_text.undraw()
        self.timer = self.win.after(self.scoreboard.get_delay(),
                                    self.animate_shape)
        self.state = 'Play'
        
    def game_over(self):
        self.win.after_cancel(self.timer)
        self.msg = UItext(Point(0.5 * BOARD_WIDTH * BLOCK_SIZE,
                              0.5 * BOARD_HEIGHT * BLOCK_SIZE),
                        "GAME OVER\n\nTotal Score\n %i\n"
                        "\n Press BACKSPACE\nto restart" %self.scoreboard.score,
                          20, 'bold', self.board.canvas)
        self.state = 'Gameover'
    
    def restart(self):
        self.clear_board()
        self.start()

    def clear_board(self):
        self.msg.undraw()
        self.next_shape.undraw()
        self.scoreboard.score = 0
        self.scoreboard.level = 1
        self.scoreboard.score_text.setText("Score\n%i" %self.scoreboard.score)
        self.scoreboard.level_text.setText("Level\n%i" %self.scoreboard.level)
        
        for block in self.board.grid.values():
            block.undraw()
        self.board.grid = {}

    def do_move(self,direction):
        dx = self.DIRECTION[direction][0]
        dy = self.DIRECTION[direction][1]

        if not self.current_shape.can_move(self.board,dx,dy):
            
            if direction == "Down":
                self.board.add_shape(self.current_shape)
                # No need to call the remove_full_rows method twice to remove
                # completed rows and count scores.
                self.scoreboard.add_score(self.board.remove_full_rows())
                self.scoreboard.add_level()
                self.current_shape = type(self.next_shape)(
                    Point(int(0.5*BOARD_WIDTH),0))
                
                if not self.board.draw_shape(self.current_shape):
                    self.game_over() 
                else:
                    self.next_shape.undraw()
                    self.next_shape = self.create_shape()
                    self.next_shape.draw(self.preview.canvas)
                    
            return False

        else:
            self.current_shape.move(dx,dy)
            return True

    def do_rotate(self):
        if self.current_shape.can_rotate(self.board):
            self.current_shape.rotate(self.board)
                
    def key_pressed(self,event):
        key = event.keysym

        if self.state == 'Gameover':
            if key == 'BackSpace':
                self.restart()

        elif self.state == 'Pause':
            if key =='Escape':
                self.resume()

        elif self.state == 'Play':            
            if key in self.DIRECTION.keys():
                self.do_move(key)
            elif key == "space":
                while self.do_move("Down"):
                    pass               
            elif key == "Up":
                self.do_rotate()
            elif key == "Escape":
                self.pause()

######################################
# TEST
######################################

win = Window('This is Tetris')
Tetris(win)
win.mainloop()
