import math,sys,pygame

pygame.init()

# Setup
size = width, height = 720, 255
font = pygame.font.SysFont("Arial", 10)
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
pygame.mouse.set_visible(False)
db = True
w,a,s,d,right,left = False,False,False,False,False,False

# Colors
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
yellow = 255, 255, 0
black = 0, 0, 0
gray = 122, 122, 122
white = 255, 255, 255

# Other setup
#	Viewports
viewport1 = [[10, 10], [225, 225]]
viewport2 = [[245, 10], [225, 225]]
viewport3 = [[480, 10], [225, 225]]
vp1x = viewport1[0][0]
vp1y = viewport1[0][1]
vp2x = viewport2[0][0]
vp2y = viewport2[0][1]
vp3x = viewport3[0][0]
vp3y = viewport3[0][1]
#	Wall
vx1, vy1 = 200, 20
vx2, vy2 = 200, 200
#	Player
px, py = 110, 110
angle = 0

def FNcross(x1, y1,x2, y2): return x1 * y2 - y1 * x2

def Intersect(x1,y1, x2,y2, x3,y3, x4,y4):
	x = FNcross(x1,y1, x2,y2)
	y = FNcross(x3,y3, x4,y4)
	det = FNcross(x1-x2, y1-y2, x3-x4, y3-y4)
	x = FNcross(x, x1-x2, y, x3-x4) / det
	y = FNcross(x, y1-y2, y, y3-y4) / det
	return [x, y]
	

while True:
	screen.fill(black)
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
			elif event.key == pygame.K_RIGHT:
				right = True
			elif event.key == pygame.K_LEFT:
				left = True
			elif event.key == pygame.K_F3:
				db = not db
			elif event.key == pygame.K_ESCAPE: sys.exit()
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
		px = px + math.cos(angle)
		py = py + math.sin(angle)
	elif a:
		px += math.sin(angle)
		py -= math.cos(angle)
	elif s:
		px = px - math.cos(angle)
		py = py - math.sin(angle)
	elif d:
		px -= math.sin(angle)
		py += math.cos(angle)
	elif right:
		angle += .01
	elif left:
		angle -= .01
	
	# Draw the viewports
	pygame.draw.rect(screen, red, viewport1, 1)
	pygame.draw.rect(screen, green, viewport2, 1)
	pygame.draw.rect(screen, blue, viewport3, 1)
	# Draw titles
	vp1t = font.render("Bird's Eye Isometric", False, white)
	vp2t = font.render("Third Person", False, white)
	vp3t = font.render("First Person", False, white)
	helpt = font.render("LEFT/RIGHT to look, WASD to move", False, white)
	screen.blit(vp1t, [10, 0])
	screen.blit(vp2t, [245, 0])
	screen.blit(vp3t, [480, 0])
	screen.blit(helpt, [5, 240])
	
	# Draw into viewport 1
	#	Wall
	pygame.draw.line(screen, yellow, [vp1x + vx1, vp1y + vy1], [vp1x + vx2, vp1y + vy2], 1)
	#	Player
	pygame.draw.line(screen, gray, [vp1x + px, vp1y + py], [vp1x + math.cos(angle)*20 + px, vp1y + math.sin(angle)*20 + py], 1)
	pygame.draw.circle(screen, white, [vp1x + int(px), vp1y + int(py)], 1)
	
	# Draw into viewport 2
	#	Wall
	#		Transform vertexes relative to player
	tx1 = vx1 - px
	ty1 = vy1 - py
	tx2 = vx2 - px
	ty2 = vy2 - py
	#		Rotate them around the player's view
	tz1 = tx1 * math.cos(angle) + ty1 * math.sin(angle)
	tz2 = tx2 * math.cos(angle) + ty2 * math.sin(angle)
	tx1 = tx1 * math.sin(angle) - ty1 * math.cos(angle)
	tx2 = tx2 * math.sin(angle) - ty2 * math.cos(angle)
	#		Draw them relative to the player
	pygame.draw.line(screen, yellow, [vp2x + 110 - tx1, vp2y + 110 - tz1], [vp2x + 110 - tx2, vp2y + 110 - tz2], 1)
	wall1_2d = font.render("tx1, tz1", False, white)
	wall2_2d = font.render("tx2, tz2", False, white)

	#		Draw the actual player
	pygame.draw.line(screen, gray, [vp2x + 110, vp2y + 110], [vp2x + 110, vp2y + 100], 1)
	pygame.draw.circle(screen, white, [vp2x + 110, vp2y + 110], 1)
	player_2d = font.render("px, py", False, white)
	
	# Draw into viewport 3
	#	Wall
	#		Transform the 2d wall into a 3d object with a set height
	if tz1 > 0 or tz2 > 0:
		# If the line crosses the player's viewplane, clip it
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
		y1a = -110 / tz1
		y1b = 110 / tz1
		x2 = -tx2 * 16 / tz2
		y2a = -110 / tz2
		y2b = 110 / tz2
	#		Draw the rectangle onto the screen one edge at a time...
	pygame.draw.line(screen, yellow, [vp3x + 110 + x1, vp3y + 110 + y1a], [vp3x + 110 + x2, vp3y + 110 + y2a], 1) # Top
	pygame.draw.line(screen, yellow, [vp3x + 110 + x1, vp3y + 110 + y1b], [vp3x + 110 + x2, vp3y + 110 + y2b], 1) # Bottom
	pygame.draw.line(screen, yellow, [vp3x + 110 + x1, vp3y + 110 + y1a], [vp3x + 110 + x1, vp3y + 110 + y1b], 1) # Left
	pygame.draw.line(screen, yellow, [vp3x + 110 + x2, vp3y + 110 + y2a], [vp3x + 110 + x2, vp3y + 110 + y2b], 1) # Right
	
	topleft_3d = font.render("x1, y1a", False, white)
	topright_3d = font.render("x2, y2a", False, white)
	botleft_3d = font.render("x1, y1b", False, white)
	botright_3d = font.render("x2, y2b", False, white)
	
	# Debug screen and info
	if db:
		# 2d
		screen.blit(wall1_2d, [vp2x + 110 - tx1, vp2y + 110 - tz1])
		screen.blit(wall2_2d, [vp2x + 110 - tx2, vp2y + 110 - tz2])
		screen.blit(player_2d, [vp2x + 110, vp2y + 110])
		
		# 3d
		screen.blit(topleft_3d, [vp3x + 110 + x1, vp3y + 110 + y1a])
		screen.blit(topright_3d, [vp3x + 110 + x2, vp3y + 110 + y2a])
		screen.blit(botleft_3d, [vp3x + 110 + x1, vp3y + 110 + y1b])
		screen.blit(botright_3d, [vp3x + 110 + x2, vp3y + 110 + y2b])
	
	# Refresh the screen
	pygame.display.flip()
	clock.tick(60)