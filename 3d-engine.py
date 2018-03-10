# TODO: Solid walls/ceilings/floors

import math,sys,pygame

pygame.init()

# Setup
size = width, height = 1920, 1080
font = pygame.font.SysFont("Arial", 10)
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
db = False
w,a,s,d,right,left = False,False,False,False,False,False
walls = []
kb = False
fs = True

# Colors
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
yellow = 255, 255, 0
orange = 255, 150, 0
pink = 255, 150, 148
black = 0, 0, 0
gray = 122, 122, 122
white = 255, 255, 255

# Minimap
minimap = [[width-110, height-110], [100, 100]]
minimap_x = minimap[0][0]
minimap_y = minimap[0][1]

# Wall
class Wall:
	def __init__(self, color, vx1, vy1, vx2, vy2):
		self.vx1, self.vy1 = vx1, vy1
		self.vx2, self.vy2 = vx2, vy2
		self.color = color

yellow_wall = Wall(yellow, 645, 315, 645, 340)
blue_wall = Wall(blue, 645, 315, 620, 315)
red_wall = Wall(red, 620, 315, 620, 340)
orange_wall = Wall(orange, 645, 340, 620, 340)
walls.append(orange_wall)
walls.append(yellow_wall)
walls.append(blue_wall)
walls.append(red_wall)

# Player
px, py = 635, 325
angle = 0
fov = 50
f1 = float(1)


def FNcross(x1, y1,x2, y2): return x1 * y2 - y1 * x2

def Intersect(x1,y1, x2,y2, x3,y3, x4,y4):
	x = FNcross(x1,y1, x2,y2)
	y = FNcross(x3,y3, x4,y4)
	det = FNcross(x1-x2, y1-y2, x3-x4, y3-y4)
	x = FNcross(x, x1-x2, y, x3-x4) / det
	y = FNcross(x, y1-y2, y, y3-y4) / det
	return [x, y]
	

while True:
	# if int(f1) is not 0: fov = 10 / f1
	screen.fill(black)
	foc = pygame.mouse.get_focused()
	mospos = pygame.mouse.get_pos()
	mosrel = pygame.mouse.get_rel()[0]
	if foc and not kb: 
		pygame.mouse.set_pos([width/2, height/2])
		pygame.mouse.get_rel()
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w:
				w = True
			elif event.key == pygame.K_a:
				a = True
			elif event.key == pygame.K_s:
				s = True
			elif event.key == pygame.K_d:
				d = True
			elif event.key == pygame.K_UP:
				f1 += 0.1
			elif event.key == pygame.K_DOWN:
				f1 -= 0.1
			elif event.key == pygame.K_RIGHT:
				right = True
			elif event.key == pygame.K_LEFT:
				left = True
			elif event.key == pygame.K_F3:
				db = not db
			elif event.key == pygame.K_SPACE:
				kb = not kb
			elif event.key == pygame.K_ESCAPE:
				sys.exit()
			elif event.key == pygame.K_F11:
				if not fs:
					fs = True
					width = 1920
					height = 1080
					size = width, height
					screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
				else:
					fs = False
					width = 1280
					height = 720
					size = width, height
					screen = pygame.display.set_mode(size)
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_w:
				w = False
			elif event.key == pygame.K_a:
				a = False
			elif event.key == pygame.K_s:
				s = False
			elif event.key == pygame.K_d:
				d = False
			elif event.key == pygame.K_RIGHT:
				right = False
			elif event.key == pygame.K_LEFT:
				left = False
	
	if w:
		px += math.cos(angle) / 5
		py += math.sin(angle) / 5
	elif a:
		px += math.sin(angle) / 5
		py -= math.cos(angle) / 5
	elif s:
		px -= math.cos(angle) / 5
		py -= math.sin(angle) / 5
	elif d:
		px -= math.sin(angle) / 5
		py += math.cos(angle) / 5
	elif right and kb:
		angle += .01
	elif left and kb:
		angle -= .01
	elif not kb and foc:
		angle += float(mosrel) / width
	
	for wall in walls:
		# Transform vertexes relative to player
		tx1 = wall.vx1 - px
		ty1 = wall.vy1 - py
		tx2 = wall.vx2 - px
		ty2 = wall.vy2 - py
		#		Rotate them around the player's view
		tz1 = tx1 * math.cos(angle) + ty1 * math.sin(angle)
		tz2 = tx2 * math.cos(angle) + ty2 * math.sin(angle)
		tx1 = tx1 * math.sin(angle) - ty1 * math.cos(angle)
		tx2 = tx2 * math.sin(angle) - ty2 * math.cos(angle)
		
		# Draw into the screen
		#	Wall
		#	Transform the 2d wall into a 3d object with a set height
		if tz1 > 0 or tz2 > 0:
			# If the line crosses the player's viewplane, clip it.
			ix1 = Intersect(tx1,tz1, tx2,tz2, -0.0001,0.0001, -20,5)[0]
			iz1 = Intersect(tx1,tz1, tx2,tz2, -0.0001,0.0001, -20,5)[1]
			ix2 = Intersect(tx1,tz1, tx2,tz2,  0.0001,0.0001,  20,5)[0]
			iz2 = Intersect(tx1,tz1, tx2,tz2,  0.0001,0.0001,  20,5)[1]
			if tz1 <= 0: 
				if iz1 > 0: 
					tx1=ix1
					tz1=iz1
				else:
					tx1=ix2
					tz1=iz2
			if tz2 <= 0: 
				if iz1 > 0: 
					tx2=ix1
					tz2=iz1 
				else:
					tx2=ix2
					tz2=iz2
			
			x1 = -tx1 * 16 / tz1
			y1a = -height/2 / tz1
			y1b = height/2 / tz1
			x2 = -tx2 * 16 / tz2
			y2a = -height/2 / tz2
			y2b = height/2 / tz2
		
			#		Draw the rectangle onto the screen one edge at a time...
			pygame.draw.line(screen, wall.color, [width/2 + x1 * fov, height/2 + y1a], [width/2 + x2 * fov, height/2 + y2a], 1) # Top
			pygame.draw.line(screen, wall.color, [width/2 + x1 * fov, height/2 + y1b], [width/2 + x2 * fov, height/2 + y2b], 1) # Bottom
			pygame.draw.line(screen, wall.color, [width/2 + x1 * fov, height/2 + y1a], [width/2 + x1 * fov, height/2 + y1b], 1) # Left
			pygame.draw.line(screen, wall.color, [width/2 + x2 * fov, height/2 + y2a], [width/2 + x2 * fov, height/2 + y2b], 1) # Right
			
			"""
			for xf in range(int(x1), int(x2)):
				ya = y1a + (xf-x1) * int(y2a-y1a) / (x2-x1)
				yb = y1b + (xf-x1) * int(y2b-y1b) / (x2-x1)
				
				pygame.draw.line(screen, pink, [width/2 + xf * fov, 0], [width/2 + xf * fov, height/2 - ya], 1) # Draw a line starting from the top of the screen
				pygame.draw.line(screen, gray, [width/2 + xf * fov, height/2 + yb], [width/2 + xf * fov, height], 1) # Draw a line down to the bottom of the screen
				
				pygame.draw.line(screen, wall.color, [width/2 + xf * fov, height/2 + ya], [width/2 + xf * fov, height/2 + yb], 1)
			"""
			# This FOR loop is supposed to loop through and make the walls solid/add ceilings but it's not for some reason...
	
		# Draw the minimap
		# pygame.draw.rect(screen, green, minimap, 1)
		if tx1>109: tx1 = 109
		if tx1<-89: tx1 = -89
		if tx2>109: tx2 = 109
		if tx2<-89: tx2 = -89
		if tz2>109: tz2 = 109
		if tz2<-89: tz2 = -89
		if tz1>109: tz1 = 109
		if tz1<-89: tz1 = -89
		# pygame.draw.line(screen, wall.color, [minimap_x + (110 - tx1)//2, minimap_y + (110 - tz1)//2], [minimap_x + (110 - tx2)//2, minimap_y + (110 - tz2)//2], 1)
		
		
	# pygame.draw.line(screen, gray, [minimap_x + 110//2, minimap_y + 110//2], [minimap_x + 110//2, minimap_y + 100//2], 1)
	# pygame.draw.circle(screen, white, [minimap_x + 110//2, minimap_y + 110//2], 1)	
	topleft_3d = font.render("tx1: " + str(tx1), False, white)
	topright_3d = font.render("tz1: " + str(tz1), False, white)
	botleft_3d = font.render("tx2: " + str(tx2), False, white)
	botright_3d = font.render("tz2: " + str(tz2), False, white)
	debug = font.render("tx1", False, white)
	playerpos = font.render("Player: " + str([px, py]), False, white)
	fovtxt = font.render("FOV: " + str(fov), False, white)
	kbtxt = font.render("KB: " + str(kb), False, white)
	controls_txt = font.render("CONTROLS: WASD to move; MOUSE to look; SPACE to change to arrow key look (DOOM-style); F3 for debug; F11 to toggle fullscreen; ESCAPE to exit", False, white)
	
	# Debug screen and info
	if db:
		# 3d
		screen.blit(topleft_3d, [minimap_x, minimap_y-40])
		screen.blit(topright_3d, [minimap_x, minimap_y-30])
		screen.blit(botleft_3d, [minimap_x, minimap_y-20])
		screen.blit(botright_3d, [minimap_x, minimap_y-10])
		# screen.blit(debug, [minimap_x + (110 - tx1)//2, minimap_y + (110 - tz1)//2])
		screen.blit(playerpos, [0, 0])
		screen.blit(fovtxt, [400, 0])
		screen.blit(kbtxt, [450, 0])
	screen.blit(controls_txt, [675, 0])
	
	# Refresh the screen
	pygame.display.flip()
	clock.tick(60)