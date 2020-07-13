import pygame as pg
import game

_surface = None
_world = None
_game = None

class _Piece(object):
	def __init__(self,color,name):
		self.image = pg.image.load('../images/{color}_{name}.png'.format(color = color, name=name))
		self.click_image = pg.image.load('../images/{color}_{name} (2).png'.format(color=color, name=name))
		self.click = False
		self.img_size = self.image.get_size()
		self.position = (0,0)

	def __call__(self):
		if self.click:
			return self.click_image.copy()
		else:
			return self.image.copy()

	def get_size(self):
		return self.img_size

	def click(self):
		self.click = True


class _Board(object):
	def __init__(self):
		self.image = pg.image.load('../images/board.png')
		self.size = self.get_size()
		self.position = (0,0)
		self.square_size = (self.size[0]/3, self.size[1]/4)
		self.square_positions = {}

		for i in range(3):
			for j in range(4):
				self.square_positions[(i,j)] = [self.position[0]+ i*self.square_size[0], self.position[1]+ j*self.square_size[1]]

	def __call__(self):
		return self.image

	def get_size(self):
		return self.image.get_size()

	def update_grid(self):r 


class _World(object):

	def __init__(self):

		# Image load
		self.Board = _Board()
		
		self.RED_King = _Piece("RED","KING")
		self.RED_Sang = _Piece("RED","SANG")
		self.RED_Jang = _Piece("RED","JANG")
		self.RED_Ja = _Piece("RED","JA")
		self.RED_Hoo = _Piece("RED","HOO")
		
		self.GREEN_King = _Piece("GREEN","KING")
		self.GREEN_Sang = _Piece("GREEN","SANG")
		self.GREEN_Jang = _Piece("GREEN","JANG")
		self.GREEN_Ja = _Piece("GREEN","JA")
		self.GREEN_Hoo = _Piece("GREEN","HOO")

		self.RED_Captive = None
		self.GREEN_Captive = None

		# Position values
		self.Board_position = (0,0)
		self.Board_size = self.Board.get_size()
		self.grid_positions = [[[25+i*self.Board_size[0]/3,25+j*self.Board_size[1]/4] for i in range(3)] for j in range(4)]
		self.Piece_size = self.RED_King.get_size()

	def calBoard_position(self):
		w1, h1 = _surface.get_size()
		w2, h2 = self.Board.get_size()
		x,y = (w1-w2)/2 , (h1-h2)/2
		self.Board_position = (x,y)
		
	def create_board(self):
		return self.Board().copy()

	def update_board(self):
		new_Board = self.create_board()
		for x,y in _game.gameboard:
			piece = _game.gameboard[(x,y)]
			target = eval("self.{Color}_{Name}".format(Color = piece.Color, Name = piece.name))
			position = self.grid_positions[x][y]
			new_Board.blit(target(),position)
		_surface.blit(new_Board,self.Board_position)

	def pos2cord(self,position):
		px,py = position
		s1 = False
		s2 = False
		for i in range(3):
			xstart = 25+i*self.Board_size[0]/3+self.Board_position[0]
			xend = xstart + self.Piece_size[0]
			if px>=xstart and px<=xend:
				s1 = True
				break

		for j in range(4):
			ystart = 25+j*self.Board_size[1]/4+self.Board_position[1]
			yend = ystart + self.Piece_size[1]
			if py>=ystart and py<=yend:
				s2 = True
				break

		if s1 and s2:
			print(j,i)
			return (j,i)
		else:
			return (None,None)
			
	def main(self):
		global _game, _surface, _world
		pg.init() # pg : pygame
		_surface = pg.display.set_mode((1000,1000))
		_game = game.jangi()
		self.calBoard_position()
		self.update_board()
		pg.display.update()

		running = True
		select1 = False
		select2 = False
		while running:
			for event in pg.event.get():
				if event.type == pg.MOUSEBUTTONUP:
					print(event.pos)
					if not select1:
						x1,y1 = self.pos2cord(event.pos)
						if _game.iscanSelect(x1,y1):
							select1 =True

					elif select1:
						x2,y2 = self.pos2cord(event.pos)
						if _game.iscanMove(x1,y1,x2,y2):
							select2 = True

						if x1==x2!=None and y1==y2!=None:
							select1 = False
							select2 = False

					if select2:
						_game.Move(x1,y1,x2,y2)
						select1 = False
						select2 = False

					print('select1 : ',select1)
					print('select2 : ',select2)
					
				# QUIT event
				if event.type == pg.QUIT:
					running = False
			#
			_world.update_board()
			pg.display.update()



if __name__ == "__main__":
	_world = _World()
	_world.main()