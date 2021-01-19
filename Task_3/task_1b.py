'''
*****************************************************************************************
*
*				===============================================
*					Nirikshak Bot (NB) Theme (eYRC 2020-21)
*				===============================================
*
*  This script is to implement Task 1B of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
'''

# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_1b.py
# Functions:		applyPerspectiveTransform, detectMaze, writeToCsv
#					[ Comma separated list of functions in this file ]
# Global variables:	
#					[ List of global variables defined in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv, csv)				##
##############################################################
import numpy as np
import cv2
import csv
##############################################################


################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.		##
## Please add proper comments to ensure that your code is	##
## readable and easy to understand.							##
##############################################################

def preProcess(img):
	imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	imgBlur = cv2.GaussianBlur(imgGray, (5,5), 1)
	imgThreshold = cv2.threshold(imgBlur, 200,255,cv2.THRESH_BINARY)
	return imgThreshold

def pP(img):
	imgGray = img
	imgBlur = cv2.medianBlur(imgGray, 5)
	imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
	return imgThreshold

def pP1(img):
	imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	kernel = np.ones((5,5),np.float32)/25
	imgBlur = cv2.filter2D(imgGray,-1,kernel)
	imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
	return imgThreshold


def reorder(myPoints):
	myPoints = myPoints.reshape((4, 2))
	myPointsNew = np.zeros((4, 1, 2), dtype = np.float32)
	add = myPoints.sum(1)
	myPointsNew[0] = myPoints[np.argmin(add)]
	myPointsNew[3] = myPoints[np.argmax(add)]
	diff = np.diff(myPoints, axis = 1)
	myPointsNew[1] = myPoints[np.argmin(diff)]
	myPointsNew[2] = myPoints[np.argmax(diff)]
	
	return myPointsNew

def vertical_wall(pimg, r , sci, eci):
	prepart1 = pP(pimg)

	cnt, hierarchy = cv2.findContours(prepart1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	good_c = []
	for c in cnt:
		area = cv2.contourArea(c)
		if area > 50:
			peri = cv2.arcLength(c, True)
			approx = cv2.approxPolyDP(c, 0.02 * peri, True)
			if (len(approx) == 4 or len(approx) == 5 or len(approx) == 6 ):
				good_c.append(c)
	
	if(len(good_c) == 0):
		prepart1 = preProcess(pimg)

		cnt, hierarchy = cv2.findContours(prepart1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		
		for c in cnt:
			area = cv2.contourArea(c)
			if area > 50:
				peri = cv2.arcLength(c, True)
				approx = cv2.approxPolyDP(c, 0.02 * peri, True)
				if (len(approx) == 4 or len(approx) == 5 or len(approx) == 6 or len(approx) == 7):
					good_c.append(c)
				
	
	good_c.sort(reverse = True, key = lambda x : cv2.contourArea(x))
	if len(good_c) != 0:
		area_good = cv2.contourArea(good_c[0])
		if area_good > 2300:
			return False
		else:
			return True
	else:
		return False  


def horizontal_wall(pimg, c , sci, eci):
	prepart1 = pP(pimg)

	cnt, hierarchy = cv2.findContours(prepart1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	good_c = []
	for c in cnt:
		area = cv2.contourArea(c)
		if area > 50:
			peri = cv2.arcLength(c, True)
			approx = cv2.approxPolyDP(c, 0.02 * peri, True)
			
			
			if (len(approx) == 4 or len(approx) == 5 or len(approx) == 6):
				good_c.append(c)
	
	if(len(good_c) == 0):
		prepart1 = preProcess(pimg)
		
		cnt, hierarchy = cv2.findContours(prepart1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		
		for c in cnt:
			area = cv2.contourArea(c)
			if area > 50:
				peri = cv2.arcLength(c, True)
				approx = cv2.approxPolyDP(c, 0.02 * peri, True)
				if (len(approx) == 4 or len(approx) == 5 or len(approx) == 6 or len(approx) == 7 or len(approx) == 8):
					good_c.append(c)
		
	good_c.sort(reverse = True, key = lambda x : cv2.contourArea(x))
	if len(good_c) != 0:
		area_good = cv2.contourArea(good_c[0])
		if area_good > 2300:
			return False
		else:
			return True
	else:
		return False	


##############################################################


def applyPerspectiveTransform(input_img):

	"""
	Purpose:
	---
	takes a maze test case image as input and applies a Perspective Transfrom on it to isolate the maze

	Input Arguments:
	---
	`input_img` :	[ numpy array ]
		maze image in the form of a numpy array
	
	Returns:
	---
	`warped_img` :	[ numpy array ]
		resultant warped maze image after applying Perspective Transform
	
	Example call:
	---
	warped_img = applyPerspectiveTransform(input_img)
	"""

	warped_img = None

	##############	ADD YOUR CODE HERE	##############
	#cv2.imwrite("initial.png",input_img)
	imgThreshold = pP(input_img)
	
	contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)


	max_area = 0
	biggest = np.array([])
	for i in contours:
		
		area = cv2.contourArea(i)
		if area > 50:
			peri = cv2.arcLength(i, True)
			approx = cv2.approxPolyDP(i, 0.02 * peri, True)
			if area > max_area and len(approx) == 4:
				biggest = approx
				max_area = area

				
	biggest = reorder(biggest)
	biggest = np.int0(biggest)

	pts1 = np.float32(biggest)
	pts2 = np.float32([[0,0], [1024, 0], [0,1024], [1024,1024]])
	matrix = cv2.getPerspectiveTransform(pts1, pts2)
	warp = cv2.warpPerspective(input_img, matrix, (1024, 1024))
	#cv2.imwrite("befwarp.png",warp)
	warped_img = cv2.resize(warp, (1280,1280),interpolation = cv2.INTER_NEAREST)
	#plt.imshow(warped_img,cmap="gray")
	#plt.show()
	#cv2.imwrite("wimh.png",warped_img)



	

	##################################################

	return warped_img


def detectMaze(warped_img):

	"""
	Purpose:
	---
	takes the warped maze image as input and returns the maze encoded in form of a 2D array

	Input Arguments:
	---
	`warped_img` :	  [ numpy array ]
		resultant warped maze image after applying Perspective Transform
	
	Returns:
	---
	`maze_array` :	  [ nested list of lists ]
		encoded maze in the form of a 2D array

	Example call:
	---
	maze_array = detectMaze(warped_img)
	"""

	maze_array = []

	##############	ADD YOUR CODE HERE	##############
	arr_boxes = np.zeros(shape=(10,10), dtype = int)
	for i in range(10):
		arr_boxes[i,0] += 1
		arr_boxes[0,i] += 2
		arr_boxes[i,9] += 4
		arr_boxes[9,i] += 8

	for r in range(10):
		c = 0
		sci = 0
		eci = 100
		while(c != 9):	
			part = warped_img[r * 50: r * 50 + 50 , sci:eci]
			vw = vertical_wall(part, r , sci, eci)
			if(vw):
				arr_boxes[r,c] += 4
				arr_boxes[r,c+1] += 1
			sci += 50
			eci += 50
			c += 1

	for c in range(10):
		r = 0
		sri = 0
		eri = 100
		while(r != 9):	
			part = warped_img[sri:eri ,c * 50: c * 50 + 50]
			hw = horizontal_wall(part, c , sri, eri)
			if(hw):
				arr_boxes[r,c] += 8
				arr_boxes[r+1,c] += 2
			sri += 50
			eri += 50
			r += 1

	maze_array = arr_boxes.tolist()
	
	
	##################################################

	return maze_array


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
def writeToCsv(csv_file_path, maze_array):

	"""
	Purpose:
	---
	takes the encoded maze array and csv file name as input and writes the encoded maze array to the csv file

	Input Arguments:
	---
	`csv_file_path` :	[ str ]
		file path with name for csv file to write
	
	`maze_array` :		[ nested list of lists ]
		encoded maze in the form of a 2D array
	
	Example call:
	---
	warped_img = writeToCsv('test_cases/maze00.csv', maze_array)
	"""

	with open(csv_file_path, 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerows(maze_array)


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:	main
#		 Inputs:	None
#		Outputs:	None
#		Purpose:	This part of the code is only for testing your solution. The function first takes 'maze00.jpg'
#					as input, applies Perspective Transform by calling applyPerspectiveTransform function,
#					encodes the maze input in form of 2D array by calling detectMaze function and writes this data to csv file
#					by calling writeToCsv function, it then asks the user whether to repeat the same on all maze images
#					present in 'test_cases' folder or not. Write your solution ONLY in the space provided in the above
#					applyPerspectiveTransform and detectMaze functions.

if __name__ == "__main__":

	# path directory of images in 'test_cases' folder
	img_dir_path = 'test_cases/'

	# path to 'maze00.jpg' image file
	file_num = 0
	img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

	print('\n============================================')
	print('\nFor maze0' + str(file_num) + '.jpg')

	# path for 'maze00.csv' output file
	csv_file_path = img_dir_path + 'maze0' + str(file_num) + '.csv'
	
	# read the 'maze00.jpg' image file
	input_img = cv2.imread(img_file_path)

	# get the resultant warped maze image after applying Perspective Transform
	warped_img = applyPerspectiveTransform(input_img)

	if type(warped_img) is np.ndarray:

		# get the encoded maze in the form of a 2D array
		maze_array = detectMaze(warped_img)

		if (type(maze_array) is list) and (len(maze_array) == 10):

			print('\nEncoded Maze Array = %s' % (maze_array))
			print('\n============================================')
			
			# writes the encoded maze array to the csv file
			writeToCsv(csv_file_path, maze_array)

			cv2.imshow('warped_img_0' + str(file_num), warped_img)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
		
		else:

			print('\n[ERROR] maze_array returned by detectMaze function is not complete. Check the function in code.\n')
			exit()
	
	else:

		print('\n[ERROR] applyPerspectiveTransform function is not returning the warped maze image in expected format! Check the function in code.\n')
		exit()
	
	choice = input('\nDo you want to run your script on all maze images ? => "y" or "n": ')

	if choice == 'y':

		for file_num in range(1, 10):
			
			# path to image file
			img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

			print('\n============================================')
			print('\nFor maze0' + str(file_num) + '.jpg')

			# path for csv output file
			csv_file_path = img_dir_path + 'maze0' + str(file_num) + '.csv'
			
			# read the image file
			input_img = cv2.imread(img_file_path)

			# get the resultant warped maze image after applying Perspective Transform
			warped_img = applyPerspectiveTransform(input_img)

			if type(warped_img) is np.ndarray:

				# get the encoded maze in the form of a 2D array
				maze_array = detectMaze(warped_img)

				if (type(maze_array) is list) and (len(maze_array) == 10):

					print('\nEncoded Maze Array = %s' % (maze_array))
					print('\n============================================')
					
					# writes the encoded maze array to the csv file
					writeToCsv(csv_file_path, maze_array)

					cv2.imshow('warped_img_0' + str(file_num), warped_img)
					cv2.waitKey(0)
					cv2.destroyAllWindows()
				
				else:

					print('\n[ERROR] maze_array returned by detectMaze function is not complete. Check the function in code.\n')
					exit()
			
			else:

				print('\n[ERROR] applyPerspectiveTransform function is not returning the warped maze image in expected format! Check the function in code.\n')
				exit()

	else:

		print('')

