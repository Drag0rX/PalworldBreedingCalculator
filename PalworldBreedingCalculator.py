# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 00:02:46 2024

@author: Joshua Hicks
"""

#%% SETUP DATA

import pandas as pd

enumVals = pd.read_excel('Data.xlsx',sheet_name='Enums')
data = pd.read_excel('Data.xlsx',sheet_name='EnumedData')

#data = pd.read_excel('Data.xlsx',sheet_name='CombinationsUnpivot')


#%% SETUP FUNCTIONS

# pal to enum
def palToEnum(pal):
	for i, row in enumVals.iterrows():
		if row['Pal'] == pal:
			return row['Enum']
	return -1

# pal array to enum array
def palToEnumArr(pals):
	i = 0
	output = []
	while i < len(pals):
		output.append(palToEnum(pals[i]))
		i+=1
	return output

# enum to pal
def enumToPal(enum):
	for i, row in enumVals.iterrows():
		if row['Enum'] == enum:
			return row['Pal']
	return -1

# enum array to pal array
def enumToPalArr(enums):
	i = 0
	output = []
	while i < len(enums):
		output.append(enumToPal(enums[i]))
		i+=1
	return output


#%% SETUP TARGETS

	# 0 Lamball, 2 Chikipi, 25 Mau, 17 Teafant
	# 111 Mammorest Cryst
	# Jolthog, Ragnahawk
	# Depresso
	parent = "Jolthog"
	child = "Ragnahawk"
	# provide a list of already captured pal usable for breeding
	available = []
	# exclude as a capture option
	exclude = ["Gumoss (Special)", 
			   "Jormuntide Ignis", 
			   "Paladius", 
			   "Necromus",
			   "Frostallion", 
			   "Frostallion Noct", 
			   "Jetragon", 
			   "Blazamut"]
	
	maxPathLen = 5
	fixedPathLen = 0
	
	noUseChild = 0

	#convert to enum
	parent = palToEnum(parent)
	child = palToEnum(child)
	available = palToEnumArr(available)
	exclude = palToEnumArr(exclude)


#%% MOST DIRECT PATH

#check values for most direct path
#if one parent and one child, find shortest path
	# if available list provided, priorotise using them for shortest path

def mostDirectPath():
	global parent
	global child
	global maxPathLen
	global fixedPathLen
	global noUseChild
	global available
	
	pals = available.copy()
	pals.append(parent)
	
	enumLen = len(enumVals)
	
	# confirm parent and child exist
	if parent == -1 or child == -1:
		print("Need both a parent and child.")
		return 0
	
	# confirm parent and child aren't the same
	if parent == child:
		print("Parent and child must be different.")
		return 0
	
	shortestPath = [-1]*maxPathLen
	shortestPathLength = fixedPathLen+1
	path = []
	
	def checkChild(a, b):
		nonlocal shortestPath
		nonlocal path
		nonlocal pals
		global exclude
		
		c = data[a][b]
		if c == child:
			shortestPath = path.copy()
			required = []
			for pal in path:
				required.append(pal[1])
			required.pop(0)
			
			pals.append(c)
			shortestPath.append([a,b,c])
			
			print("New shortest: " + str(shortestPath))
			print("All pals:" + str(pals))
			print("Need to catch: " + str(required))
			
			pals.pop()
			
			return 1
		return 0

	
	def pathStep(a):
		nonlocal shortestPath
		nonlocal path
		nonlocal shortestPathLength
		global child
		global noUseChild
		global exclude
		
		# check for child using new pal against current pals
		for b in pals:
			if checkChild(a, b):
				return
		
		
		if fixedPathLen == 0:
			shortestPathLength = len(shortestPath)-1
		# check if next will become too long
		if len(path)+1 >= shortestPathLength:
			return
		
		# check for more paths using unlisted pals
		b = 1
		while b < enumLen:
			
			# excluded from catching
			if b in exclude:
				b += 1
				continue
			
			# check if found in pals already
			if not b in pals:
				
				# skip if you can't use the child as an option
				if noUseChild:
					if b == child:
						b += 1
						continue
				
				# iteratively check against the new pal
				pals.append(b)
				c = data[a][b]
				if not c in pals:
					pals.append(c)
					path.append([a,b,c])
					pathStep(c)
					pals.pop()
					path.pop()
				pals.pop()
			b += 1

		return
	
	path.append([parent,parent,parent])
	pathStep(parent)
	
	
	# return shortest path
	if shortestPath[0] != -1:
		return
	else:
		print("No path available.")
		return

#%% RUN

mostDirectPath()


#%% LEAST PALS FOR ALL PALS

