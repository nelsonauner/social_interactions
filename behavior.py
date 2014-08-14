from parameters import * 
import pygame
import random
import math
import os,sys


def distance(tuple1,tuple2):
	dx = tuple1[0]-tuple2[0]
	dy = tuple1[1]-tuple2[1]
	return(math.hypot(dx,dy))

def addVectors((angle1, length1), (angle2, length2)):
	x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
	y  = math.cos(angle1) * length1 + math.cos(angle2) * length2
	
	angle = 0.5 * math.pi - math.atan2(y, x)
	length  = math.hypot(x, y)

	return (angle, length)

def findParticle(particles, x, y):
	for p in particles:
		if math.hypot(p.x-x, p.y-y) <= p.size:
			return p
	return None


class Particle():
	def __init__(self, (x, y), size):
		self.x = x
		self.y = y
		self.size = size
		self.state = "roam"
		self.colour = LIME
		self.thickness =0
		self.bored = 0 #set to 1 if someone around, 0 otherwise...
		self.speed = 5
		self.angle = 0
		self.goal = (x,y)
		self.goal_time = 0
		(self.x_per, self.y_per) = (0,0)
		self.start_param = 1 #probability of new goal after stopping
		self.stop_param = .03 #probability of giving up current goal?
	
	def try_font(self):
		if pygame.font:
			font = pygame.font.Font(None, 17)
			text = font.render("hey", 1, (10, 10, 200))
			screen.blit(text, (self.x-9,self.y-5))

	def display(self):
		if self.state == "phone":
			screen.blit(phone_image,(self.x-5,self.y-5))
		else:
			pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)
			if self.state == "engaged":
				self.try_font()		
	
	def get_goal(self,conferences):
		""" sets self.goal """
		if distance(self.goal,(self.x,self.y)) < tolerance:
			#print("at goal")
			#self.colour = (255,0,0)
			if self.start_param > random.random():
				self.goal = (10+random.randrange(height-20),10+random.randrange(width-20))
				#print(self.goal)
	
	def move(self):
		self.angle = 0.5 * math.pi - math.atan2(self.goal[1]-self.y,self.goal[0]-self.x)
		#Move in direction of goal (along angle) at proper speed, with random permutation. 
		self.x_per = random.uniform(-1,1) + .8*self.x_per
		self.y_per = random.uniform(-1,1) + .8*self.y_per
		self.x += math.sin(self.angle) * self.speed + random.uniform(-1,1)
		self.y += math.cos(self.angle) * self.speed + random.uniform(-1,1)
		#finally, we'll see if we will check our phone--or stop looking at it: 
		if self.bored == 1:
			if self.state == "roam" and random.random() < prob_roam_to_phone:
				self.check_phone()
			elif self.state == "phone" and random.random() < prob_phone_to_roam:
				self.roam()
			elif self.state == "engaged":
				self.disengage()
		
	def bounce(self):
		if self.x > width - self.size:
			self.x = 2*(width - self.size) - self.x
			self.angle = - self.angle
			#self.speed *= elasticity

		elif self.x < self.size:
			self.x = 2*self.size - self.x
			self.angle = - self.angle
			#self.speed *= elasticity
	
		if self.y > height - self.size:
			self.y = 2*(height - self.size) - self.y
			self.angle = math.pi - self.angle
			#self.speed *= elasticity

		elif self.y < self.size:
			self.y = 2*self.size - self.y
			self.angle = math.pi - self.angle
			#self.speed *= elasticity
	
	def check_phone(self):
		self.speed = random.uniform(0,2) #either still or walking slowly
		self.state = "phone"
	
	def roam(self):
		self.speed = walking_speed
		self.state = "roam"
	
	def engage(self,target):
		self.speed = 0
		self.state = "engaged"
	
	def disengage(self):
		#here, either roam or phone :) 
		if random.random() > prob_phone:
			self.roam()
		else:
			self.check_phone()
	
	def interact(self, p2):
		"""Changes to implement: slow down when approaching? but better, switch to state "engaged" if popularity score is higher..."""
		dx = self.x - p2.x
		dy = self.y - p2.y
		dist = math.hypot(dx, dy)
		#This is engagement
		if dist < self.size+p2.size+engage_distance:
			self.bored = 0
		#draw engagement from the difference between status. -> if higher status, engage, if not, engage with probability proportional to status
			fame_diff = p2.fame - self.fame
			if self.state == "phone":
				fame_diff -= 1 #harder to engage someone when they're on the phone. 
			if fame_diff > 0:
				self.engage(p2)
			elif -fame_diff < random.randrange(10):
				self.engage(p2)
			else:
				self.disengage()
		if self.state == "engaged" and p2.state == "engaged": # mark as having 
			add_to_edges(self.id,p2.id,pygame.time.get_ticks())
		
		#This is collision
		if dist < self.size + p2.size:
			tangent = math.atan2(dy, dx)
			angle = 0.5 * math.pi + tangent

			angle1 = 2*tangent - self.angle
			angle2 = 2*tangent - p2.angle
			speed1 = self.speed
			speed2 = p2.speed

			(self.angle, self.speed) = (angle1, speed1)
			(p2.angle, p2.speed) = (angle2, speed2)

			self.x += math.sin(angle)
			self.y -= math.cos(angle)
			p2.x -= math.sin(angle)
			p2.y += math.cos(angle)
		else:
			self.bored = 1

