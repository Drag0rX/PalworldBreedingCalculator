# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 00:02:46 2024

@author: Joshua Hicks
"""

#%% DATA

import pandas as pd

enumVals = pd.read_excel('Data.xlsx',sheet_name='Enums')
data = pd.read_excel('Data.xlsx',sheet_name='EnumedData')

#data = pd.read_excel('Data.xlsx',sheet_name='CombinationsUnpivot')


#%% ENUM FUNCTIONS

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



#%% MOST DIRECT PATH

#check values for most direct path
#if one parent and one child, find shortest path
	# if available list provided, priorotise using them for shortest path

def mostDirectPath(parent, child, available, exclude, 
				   initPathLen = 3, maxPathLen = 4, 
				   fixedPathLen = 0, noUseChild = 0):
	
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
	
	shortestPath = [-1]*initPathLen
	shortestPathLength = fixedPathLen+1
	path = []
	
	def checkChild(a, b):
		nonlocal shortestPath
		nonlocal path
		nonlocal pals
		nonlocal exclude
		
		c = data[a][b]
		if c == child:
			shortestPath = path.copy()
			required = []
			for pal in path:
				required.append(pal[1])
			
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
		nonlocal child
		nonlocal noUseChild
		nonlocal exclude
		
		# check for child using new pal against current pals
		for b in pals:
			if checkChild(a, b):
				return
		
		
		if fixedPathLen == 0:
			shortestPathLength = len(shortestPath)
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
	
	pathStep(parent)
	
	
	# return shortest path
	if shortestPath[0] != -1:
		return 1
	else:
		# try with next path size up
		if initPathLen < maxPathLen:
			return mostDirectPath(parent, child, available, exclude, 
				  initPathLen+1, maxPathLen, fixedPathLen, noUseChild)
		return 0

#%% RUN

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

# NOTE, for initPathLen and maxPathLen, it will RETRY every inbetween path, 
# I would recommend keeping these as 3 & 4 respectively, or using fixedPathLen
# to find all paths with EXACTLY n number

# this will intially start checking paths of n value
# if it finds a shorter path, it will only check from 
# then on for that size or less
# initPathLen = 3 (default 3)

# this will stop checking if it reaches n value in path length
# maxPathLen = 4 (default 4)

# this will forgo the above path lengths, and always look for n path length
# AND ONLY n path length, nothing shorter nor longer
# fixedPathLen = 0 (default 0, 0 skip, n forced value)

# skips using the inital child as a parent in calculations
# noUseChild = 0 (default 0, 1 keep, 0 skip)


# mostDirectPath(parent enum, child enum, 
# 				 available enum list, exclude enum list, 
# 				 initPathLen, maxPathLen, fixedPathLen, noUseChild)
if mostDirectPath(palToEnum("Lamball"), palToEnum("Mammorest Cryst"), 
			   palToEnumArr(available), palToEnumArr(exclude)):
	print("Success!")
else:
	print("No path available.")


#%% LEAST PALS FOR ALL PALS

