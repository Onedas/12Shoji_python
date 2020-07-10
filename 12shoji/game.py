
class Piece(object):

	def __init__(self,color,position,name,captive=False):
		self.name = "%-4s"%name
		self.position = position
		self.Color = color
		self.Captive = captive

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
		if not self.Captive:
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
		elif self.Captive:
			if self.Color =="RED":
				xtemp = 0
			elif self.Color =="GREEN":
				xtemp = 3

			for ytemp in range(0,3):
				if not gameboard.get((xtemp,ytemp)):
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

"""
	
"""

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

	def _printGame(self):
		self.__printBoard()
		self.__printCaptive()

	def __printBoard(self):
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

	def __printCaptive(self):
		print(" y|  4   |  5   |  6   |  7   |  8   |")
		print("x ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
		print("4",self.REDCaptive, "REDCaptive")
		print("5",self.GREENCaptive,"GREENCaptive")

	def iscanSelect(self,x,y):
		if x in (0,1,2,3) and y in (0,1,2):
			target = self.gameboard.get((x,y))
			if target:
				# print(target.Color,target.name,end= ' : ')
				if target.Color == self.turnName[self.Turn%2]:
					return True
			return False

		elif x == 4 and y in (4,5,6,7,8):

			if self.Turn%2 == 0: # right turn
				if y-4 < len(self.REDCaptive): # have captive
					return True
			return False

		elif x == 5 and y in (4,5,6,7,8):
			if self.Turn%2 == 1:
				if y-4 < len(self.GREENCaptive):
					return True
			return False

		else:
			return False

	def iscanMove(self,x1,y1,x2,y2):
		if self.iscanSelect(x1,y1):
			if x1 in (0,1,2,3) and y1 in (0,1,2):
				target = self.gameboard.get((x1,y1))
			elif x1 == 4 and y1 in (4,5,6,7,8):
				target = self.REDCaptive[y1-4]
			elif x1 == 5 and y1 in (4,5,6,7,8):
				target = self.GREENCaptive[y1-4]
			print(target.availableMoves(self.gameboard))
			if (x2,y2) in target.availableMoves(self.gameboard):
				return True
		return False

	def Move(self,x1,y1,x2,y2):
		if self.iscanMove(x1,y1,x2,y2):
			if x1 in (0,1,2,3) and y1 in (0,1,2):
				target1 = self.gameboard.get((x1,y1))	
				del self.gameboard[(x1,y1)]

			elif x1 == 4 and y1 in (4,5,6,7,8):
				target1 = self.REDCaptive.pop(y1-4)
				target1.Captive = False

			elif x1 == 5 and y1 in (4,5,6,7,8):
				target1 = self.GREENCaptive.pop(y1-4)
				target1.Captive = False

			target2 = self.gameboard.get((x2,y2))
			if target2: #Color = self.playerTurn, #Name = target2.name
				Color = self.turnName[self.Turn%2]
				Name = "Ja" if target2.name == "Hoo " else target2.name #Hoo가 죽으면 Ja로 바꿔줌
				eval("self.{Color}Captive.append({Name}('{Color}',None,'{Name}',True))".format(Color=Color,Name=Name))

			target1.position = (x2,y2)
			# Ja가 상대편 진영에 가면 Hoo로 변환
			print(target1.name, target1.name =="Ja  ")
			if target1.name == "Ja  ":
				if target1.Color == "RED" and target1.position[0] == 3:
					target1 = Hoo("RED",(x2,y2),"Hoo")
				elif target1.Color == "GREEN" and target1.position[0] ==0:
					target1 = Hoo("GREEN",(x2,y2),"Hoo")

			self.gameboard[(x2,y2)] = target1
			self.Turn +=1

			return True

	def main(self):
		"""
			CLI 로 실행
		"""

		running = True
		while running:

			#select piece
			self._printGame()
			
			try:x1,y1 = map(int,input('select piece (x y) : ').split())
			except:continue

			if self.iscanSelect(x1,y1):
				try:x2,y2 = map(int,input('select move position (x y) : ').split())
				except:continue
			else: continue

			if self.iscanMove(x1,y1,x2,y2):
				self.Move(x1,y1,x2,y2)
			else: continue

if __name__ == "__main__":
	game = jangi()
	game.main()
	