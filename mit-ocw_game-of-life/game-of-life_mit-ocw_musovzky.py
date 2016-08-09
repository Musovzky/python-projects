# game-of-life_mit-ocw_musovzky.py
# Python version: 3.4.3
# Created by: Musovzky (viviyi4@gmail.com)
# Created on: July 24, 2016

# Conway's Game of Life is a zero-player game
# Run the program, and the pattern will "evolve" automatically
# This is the second project of MIT OpenCourseWare:
# A Gentle Introduction to Programming Using Python
# This program is created from the template provided in the course materials

# Note: Graphics.py and a python interpreter are needed to run the program

from graphics import *
import random

## Written by Sarina Canelake & Kelly Casteel, August 2010
## Revised January 2011

############################################################
# GLOBAL VARIABLES
############################################################
    
BLOCK_SIZE = 30
BLOCK_OUTLINE_WIDTH = 2
BOARD_WIDTH = 25
BOARD_HEIGHT = 25

neighbor_test_blocklist = [(0,0), (1,1)]
blink_blocklist = [(5,6),(6,6),(7,6)]
toad_blocklist = [(4,4), (3,5), (3,6), (5,7), (6,5), (6,6)]
beacon_blocklist = [(2,3), (2,4), (3,3), (3,4), (4,5), (4,6), (5,5), (5,6)]
glider_blocklist = [(1,2), (2,3), (3,1), (3,2), (3,3)]
pulsar_blocklist = [(2,4), (2,5), (2,6), (4,2), (4,7), (5,2), (5,7),
                    (6,2), (6,7), (7,4), (7,5), (7,6), ]
# for diehard, make board at least 25x25, might need to change block size
diehard_blocklist = [(5,7), (6,7), (6,8), (10,8), (11,8), (12,8), (11,6)]

############################################################
# TEST CODE (don't worry about understanding this section)
############################################################

def test_neighbors(board):
    '''
    Code to test the board.get_block_neighbor function
    '''
    for block in board.block_list.values():
        neighbors = board.get_block_neighbors(block)
        ncoords = [neighbor.get_coords() for neighbor in neighbors]
        if block.get_coords() == (0,0):
            zeroneighs = [(0,1), (1,1), (1,0)]
            for n in ncoords:
                if n not in zeroneighs:
                    print ("Testing block at (0,0)")
                    print ("Got", ncoords)
                    print ("Expected", zeroneighs)
                    return False

            for neighbor in neighbors:
                if neighbor.get_coords() == (1, 1):
                    if neighbor.is_live() == False:
                        print ("Testing block at (0, 0)...")
                        print ("My neighbor at (1, 1) should be live; it is not.")
                        print ("Did you return my actual neighbors, or create new copies of them?")
                        print ("FAIL: get_block_neighbors() should NOT return new Blocks!")
                        return False

        elif block.get_coords() == (1,1):
            oneneighs = [(0,0), (0,1), (0,2), (1,0), (1,2), (2,0), (2,1),(2,2)]
            for n in ncoords:
                if n not in oneneighs:
                    print ("Testing block at (1,1)")
                    print ("Got", ncoords)
                    print ("Expected", oneneighs)
                    return False
            for n in oneneighs:
                if n not in ncoords:
                    print ("Testing block at (1,1)")
                    print ("Got", ncoords)
                    print ("Expected", oneneighs)
                    return False
    print ("Passed neighbor test")
    return True


############################################################
# BLOCK CLASS (Read through and understand this part!)
############################################################

class Block(Rectangle):
    ''' Block class:
        Implement a block for a tetris piece
        Attributes: x - type: int
                    y - type: int
        specify the position on the board
        in terms of the square grid
    '''

    def __init__(self, pos, color):
        '''
        pos: a Point object specifing the (x, y) square of the Block (NOT in pixels!)
        color: a string specifing the color of the block (eg 'blue' or 'purple')
        '''
        self.x = pos.x
        self.y = pos.y
        
        p1 = Point(pos.x*BLOCK_SIZE,
                   pos.y*BLOCK_SIZE)
        p2 = Point(p1.x + BLOCK_SIZE, p1.y + BLOCK_SIZE)

        Rectangle.__init__(self, p1, p2)
        self.setWidth(BLOCK_OUTLINE_WIDTH)
        self.setFill(color)
        self.status = 'dead'
        self.new_status = 'None'
        
    def get_coords(self):
        return (self.x, self.y)

    def set_live(self,canvas):
        '''
        Sets the block status to 'live' and draws it on the grid.
        Be sure to do this on the canvas!
        '''
        if self.status=='dead':
          self.status = 'live'
          self.draw(canvas)

    def set_dead(self):
        '''
        Sets the block status to 'dead' and undraws it from the grid.
        '''
        if self.status=='live':
          self.status = 'dead'
          self.undraw()

    def is_live(self):
        '''
        Returns True if the block is currently 'live'. Returns False otherwise.
        '''
        if self.status == 'live':
            return True
        else:
            return False

    def reset_status(self,canvas):
        '''
        Sets the new_status to be the current status
        '''
        if self.new_status=='dead':
            self.set_dead()
        elif self.new_status=='live':
            self.set_live(canvas)
        

###########################################################
# BOARD CLASS (Read through and understand this part!)
# Print out and turn in this section.
# Name:
# Recitation:
###########################################################

class Board():
    ''' Board class: it represents the Game of Life board

        Attributes: width - type:int - width of the board in squares
                    height - type:int - height of the board in squares
                    canvas - type:CanvasFrame - where the blocks will be drawn
                    block_list - type:Dictionary - stores the blocks for a given position
    '''
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # self.delay is the number of ms between each simulation. Change to be
        # shorter or longer if you wish!
        self.delay = 1000

        # create a canvas to draw the blocks on
        self.canvas = GraphWin('Conway\'s Game of Life', self.width * BLOCK_SIZE,
                               self.height * BLOCK_SIZE)
        self.canvas.setBackground('white')

        # initialize grid lines
        for x in range(1,self.width):
            self.draw_gridline(Point(x, 0), Point(x, self.height))

        for y in range(1,self.height):
            self.draw_gridline(Point(0, y), Point(self.width, y))

        # For each square on the board, we need to initialize
        # a block and store that block in a data structure. A
        # dictionary (self.block_list) that has key:value pairs of
        # (x,y):Block will be useful here.
        self.block_list = {}
        for i in range(0,self.width):
            for j in range(0,self.height):
                block = Block(Point(i,j),'sky blue') 
                self.block_list[(i,j)] = block

        self.counter = 1

    def draw_gridline(self, startp, endp):
        ''' Parameters: startp - a Point of where to start the gridline
                        endp - a Point of where to end the gridline
            Draws **two** straight 1 pixel lines next to each other, to create
            a nice looking grid on the canvas.
        '''
        line = Line(Point(startp.x*BLOCK_SIZE, startp.y*BLOCK_SIZE), \
                    Point(endp.x*BLOCK_SIZE, endp.y*BLOCK_SIZE))
        line.draw(self.canvas)
        
        line = Line(Point(startp.x*BLOCK_SIZE-1, startp.y*BLOCK_SIZE-1), \
                    Point(endp.x*BLOCK_SIZE-1, endp.y*BLOCK_SIZE-1))
        line.draw(self.canvas)


    def random_seed(self, percentage):
        ''' Parameters: percentage - a number between 0 and 1 representing the
                                     percentage of the board to be filled with
                                     blocks
            This method activates the specified percentage of blocks randomly.
        '''
        for block in self.block_list.values():
            if random.random() < percentage:
                block.set_live(self.canvas)

    def seed(self, block_coords):
        '''
        Seeds the board with a certain configuration.
        Takes in a list of (x, y) tuples representing block coordinates,
        and activates the blocks corresponding to those coordinates.
        '''
        for k in self.block_list.keys():
            if k in block_coords:
                block = self.block_list[k]
                block.set_live(self.canvas)
        self.display_count()
    

    def get_block_neighbors(self, block):
        '''
        Given a Block object, returns a list of neighboring blocks.
        Should not return itself in the list.
        '''
        neighbors = []
        (x,y) = block.get_coords()
        ncoords = [(x-1,y-1),(x,y-1),(x+1,y-1),(x+1,y),(x+1,y+1),(x,y+1),
                   (x-1,y+1),(x-1,y)]
        
        ncoords = [(p,q) for (p,q) in ncoords if p >= 0 and
                   p < self.width and q >=0 and q < self.height]
        # Something tricky happens here...
        # I tested a few simplified scenarios in testground.py.

        for ncoord in ncoords:
            neighbors.append(self.block_list[ncoord])
            # Don't create new blocks (e.g. using Block(ncoord,color))!
            # They will override existing ones and switch the latter's status!

        return neighbors


    def simulate(self):
        '''
        Executes one turn of Conways Game of Life using the rules
        listed in the handout. Best approached in a two-step strategy:
        
        1. Calculate the new_status of each block by looking at the
           status of its neighbors.

        2. Set blocks to 'live' if their new_status is 'live' and their
           status is 'dead'. Similarly, set blocks to 'dead' if their
           new_status is 'dead' and their status is 'live'. Then, remember
           to call reset_status(self.canvas) on each block.
        '''
        for block in self.block_list.values():
            
            neighbors = self.get_block_neighbors(block)
            live_neighbors = 0
            for n in neighbors:
                if n.is_live() == True:
                    live_neighbors += 1
                
            if block.is_live() == True:
                if live_neighbors < 2 or live_neighbors >3:
                    block.new_status = 'dead'
            elif block.is_live() == False:
                if live_neighbors == 3:
                    block.new_status = 'live'
                    
        for block in self.block_list.values():
            block.reset_status(self.canvas)
        # IMPORTANT: Don't reset status immediately after defining new status!
        # If you reset the status immediately, the new status will be applied
        # and affect the result of next status check.

    def animate(self):
        '''
        Animates the Game of Life, calling "simulate" once every second
        '''
        self.simulate()
        self.counter += 1
        self.display_count()
        self.canvas.after(self.delay, self.animate)

    def display_count(self):
        gen_count = Text(Point(0.5*BLOCK_SIZE,0.5*BLOCK_SIZE),self.counter)
        gen_count.draw(self.canvas)
        self.canvas.after(self.delay,gen_count.undraw)
        

################################################################
# RUNNING THE SIMULATION
################################################################

if __name__ == '__main__':    
    # Initalize board
    board = Board(BOARD_WIDTH, BOARD_HEIGHT)

    ## PART 1: Make sure that the board __init__ method works    
    # board.random_seed(.15)

    ## PART 2: Make sure board.seed works. Comment random_seed above and uncomment
    ##  one of the seed methods below
    # board.seed(toad_blocklist)

    ## PART 3: Test that neighbors work by commenting the above and uncommenting
    ## the following two lines:
    # board.seed(neighbor_test_blocklist)
    # test_neighbors(board)


    ## PART 4: Test that simulate() works by uncommenting the next two lines:
    board.seed(diehard_blocklist)
    # board.canvas.after(2000,board.simulate)

    ## PART 5: Try animating! Comment out win.after(2000, board.simulate) above, and
    ## uncomment win.after below.
    board.canvas.after(1000,board.animate)

    ## Yay, you're done! Try seeding with different blocklists (a few are provided at the top of this file!)
    
    board.canvas.mainloop()
                
