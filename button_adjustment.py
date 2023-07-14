# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 15:45:16 2023

@author: JISU
"""

import pygame

#button class
class Button():
	def __init__(self, x, y, image, width, height):
		self.image = pygame.transform.scale(image, (width, height))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()
		touch = False
		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			touch = True
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
        
		if touch:
			surface.blit(self.image, (self.rect.x, self.rect.y+2))
		else:
			surface.blit(self.image, (self.rect.x, self.rect.y))
                

		return action
