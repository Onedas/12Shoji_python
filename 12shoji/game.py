
class Piece(object):

	def __init__(self,color,position,name):
		self.name = name
		self.position = position
		self.Color = color

	def isValid(self,startpos,endpos,Color,gameboard):
		if endpos in self.availableMoves(startpos[0],startpos[1],gameboard, Color=Color):
			return True
		return False

	def __repr__(self):
		return self.Color[0]+self.name

	def __str__(self):
		return self.Color[0]+self.name

	def availableMoves(self,gameboard,Color=None):
		print("Error : no movement for base class")

	def _availableMoves(self,gameboard,Color,dMoves):
		answer = []
		x = self.position[0]
		y = self.position[1]
		for dx,dy in dMoves:
			xtemp, ytemp = x+dx, y+dy
			if self.isInBounds(xtemp,ytemp):
				target = gameboard.get((xtemp,ytemp))
				if target == None:
					answer.append((xtemp,ytemp))
				elif target.Color != Color:
					answer.append((xtemp,ytemp))

		return answer


	def isInBounds(self,x,y):
		"Checks if a position is on the board"
		if x>=0 and x<4 and y>= 0 and y<3:
			return True
		return False

	def noConflict(self, gameboard, initialColor, x, y):
		"checks if a single position poses no conflict to the rules"
		if self.isInBounds(x,y) and (( (x,y) not in gameboard) or gameboard[(x,y)].Color != initialColor):
			return True
		return False

class King(Piece):
	def availableMoves(self,gameboard, Color=None):
		if Color is None:
			Color = self.Color
		dMoves = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
		return self._availableMoves(gameboard,Color,dMoves)

class Sang(Piece):
	def availableMoves(self,gameboard, Color = None):
		if Color is None:
			Color = self.Color
		dMoves = [(-1,-1),(-1,1),(1,-1),(1,1)]
		return self._availableMoves(gameboard,Color,dMoves)

class Jang(Piece):
	def availableMoves(self,gameboard, Color = None):
		if Color is None:
			Color = self.Color
		dMoves = [(-1,0),(0,-1),(0,1),(1,0)]
		return self._availableMoves(gameboard,Color,dMoves)

class Ja(Piece):
	def availableMoves(self,gameboard, Color = None):
		if Color is None:
			Color = self.Color
		
		if Color == "RED":
			dMoves = [(1,0)]
		elif Color == "GREEN":
			dMoves = [(-1,0)]
		return self._availableMoves(gameboard,Color,dMoves)

class Hoo(Piece):
	def availableMoves(self,gameboard, Color = None):
		if Color is None:
			Color = self.Color

		if Color == "RED":
			dMoves = [(-1,0),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
		elif Color == "GREEN":
			dMoves = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,-1),(1,0)]
		return self._availableMoves(gameboard,Color,dMoves)

class jangi(object):

	def __init__(self):
		self.turnName = ["RED","GREEN"]
		self.Turn = 0 # RED or GREEN
		self.message = ""
		self.gameboard = {}

		"""
			00 10 20 30
			01 11 21 31
			02 12 22 32
		"""

		self.REDCaptive = []
		self.GREENCaptive = []

		self.placePieces()

	def placePieces(self):
		self.gameboard[(0,0)] = Sang("RED",(0,0),"Sang")
		self.gameboard[(0,1)] = King("RED",(0,1),"King")
		self.gameboard[(0,2)] = Jang("RED",(0,2),"Jang")
		self.gameboard[(1,1)] = Ja("RED",(1,1),"Ja")

		self.gameboard[(3,0)] = Jang("GREEN",(3,0),"Jang")
		self.gameboard[(3,1)] = King("GREEN",(3,1),"King")
		self.gameboard[(3,2)] = Sang("GREEN",(3,2),"Sang")
		self.gameboard[(2,1)] = Ja("GREEN",(2,1),"Ja")

	def printBoard(self):
		print()
		print("====",self.turnName[self.Turn%2]+'Turn ====')
		print()
		print(" y  0       1      2      ")
		print("x "+"ㅡ"*11)
		for i in range(0,4):	
			print(i, end="| ")
			for j in range(0,3):
				item = self.gameboard.get((i,j),"     ")
				print("%-5s"%str(item)+"|", end=" ")
			print()
			print("  "+"ㅡ"*11)
		print("RED Captive :",self.REDCaptive)
		print("GRE Captive :",self.GREENCaptive)

	def iscanSelect(self,x,y):
		target = self.gameboard.get((x,y))
		if target:
			# print(target.Color,target.name,end= ' : ')
			if target.Color == self.turnName[self.Turn%2]:
				return True
		return False

	def iscanMove(self,x1,y1,x2,y2):
		if self.iscanSelect(x1,y1):
			target = self.gameboard.get((x1,y1))
			if (x2,y2) in target.availableMoves(self.gameboard):
				return True
		return False

	def Move(self,x1,y1,x2,y2):
		if self.iscanMove(x1,y1,x2,y2):
			target1 = self.gameboard.get((x1,y1))
			target2 = self.gameboard.get((x2,y2))
			if target2: #Color = self.playerTurn, #Name = target2.name
				eval("self.{Color}Captive.append({Name}('{Color}',None,'{Name}'))".format(Color=self.turnName[self.Turn%2],Name=target2.name))
			target1.position = (x2,y2)
			self.gameboard[(x2,y2)] = target1
			del self.gameboard[(x1,y1)]	
			self.Turn +=1
			return True

	def main(self):
		running = True
		while running:
			prisoner_state = False
			Turn_end = False
			#select piece
			self.printBoard()
			x1,y1 = map(int,input('select piece (x y) : ').split())

			if prisoner_state:
				pass
			else: # Piece select
				if self.iscanSelect(x1,y1):
					x2,y2 = map(int,input('select move position (x y) : ').split())
				else: continue

				if self.iscanMove(x1,y1,x2,y2):
					self.Move(x1,y1,x2,y2)
				else: continue

if __name__ == "__main__":
	game = jangi()
	game.main()
	