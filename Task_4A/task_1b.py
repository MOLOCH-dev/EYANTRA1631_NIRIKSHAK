'''
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
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

# Team ID:			[ 1631 ]
# Author List:		[ Names of team members worked on this file separated by Comma: Kushal Shah, Dushant Panchbhai ]
# Filename:			task_1b.py
# Functions:		applyPerspectiveTransform, detectMaze, writeToCsv, preProcess, pP1,
#					reorder, detect_wall
# 					[ Comma separated list of functions in this file ]
# Global variables:	
# 					[ List of global variables defined in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv, csv)               ##
##############################################################
import numpy as np
import cv2
import csv
##############################################################


################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################

# Function to preprocess the image
def preProcess(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5,5), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, 1, 1, 11, -2)
    return imgThreshold

# Another preprocessing function using different thresholding and kernel
def pP1(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((5,5),np.float32)/25
    imgBlur = cv2.filter2D(imgGray,-1,kernel)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return imgThreshold

# Function to reorder the points to avoid rotation of image
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

# Function to detect the wall
def detect_wall(pimg):
    prepart1 = preProcess(pimg) # preprocessed the image

    cnt, _ = cv2.findContours(prepart1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    good_c = [] # list to include filtered out the contours
    for c in cnt:
        area = cv2.contourArea(c)
        if area > 700:
            good_c.append(c)

    # Now sorting the list in descending order according to their areas
    good_c.sort(reverse = True, key = lambda x : cv2.contourArea(x))

    area_good = cv2.contourArea(good_c[0])

	# Bigger contour had area greater than 2250 so checking the areas accordingly
	# if the area is less than this it means that the contours detected are smaller due 
	# to a wall present between the 2 boxes
    if area_good > 2250:
        return False
    else:
        return True 


##############################################################


def applyPerspectiveTransform(input_img):

	"""
	Purpose:
	---
	takes a maze test case image as input and applies a Perspective Transfrom on it to isolate the maze

	Input Arguments:
	---
	`input_img` :   [ numpy array ]
		maze image in the form of a numpy array
	
	Returns:
	---
	`warped_img` :  [ numpy array ]
		resultant warped maze image after applying Perspective Transform
	
	Example call:
	---
	warped_img = applyPerspectiveTransform(input_img)
	"""

	warped_img = None

	##############	ADD YOUR CODE HERE	##############
	imgThreshold = pP1(input_img) # preprocessing the image
	contours, _ = cv2.findContours(imgThreshold, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

	# We need to find the second largest contour as the largest contour had edges of the image
	# itself. So using for loops twice to find second largest areawise contour

	max_area = 0
	second_last_area = 0
	second_big = np.array([])
	for i in contours:
		
		area = cv2.contourArea(i)
		if area > 50:
			peri = cv2.arcLength(i, True)
			approx = cv2.approxPolyDP(i, 0.02 * peri, True)
			if area > max_area and len(approx) == 4:
				max_area = area

				
	for i in contours:
		
		area = cv2.contourArea(i)
		if area > 50:
			peri = cv2.arcLength(i, True)
			approx = cv2.approxPolyDP(i, 0.02 * peri, True)
			if area > second_last_area and len(approx) == 4:
				if area != max_area:
					second_big = approx
					second_last_area = area
				

	second_big = reorder(second_big) # reordering the points to avoid rotation
	second_big = np.int0(second_big)

	pts1 = np.float32(second_big)
	pts2 = np.float32([[0,0], [500, 0], [0,500], [500,500]])

    # Now doing perspective transform
	matrix = cv2.getPerspectiveTransform(pts1, pts2) 
	warped_img = cv2.warpPerspective(input_img, matrix, (500, 500))

	

	##################################################

	return warped_img


def detectMaze(warped_img):

	"""
	Purpose:
	---
	takes the warped maze image as input and returns the maze encoded in form of a 2D array

	Input Arguments:
	---
	`warped_img` :    [ numpy array ]
		resultant warped maze image after applying Perspective Transform
	
	Returns:
	---
	`maze_array` :    [ nested list of lists ]
		encoded maze in the form of a 2D array

	Example call:
	---
	maze_array = detectMaze(warped_img)
	"""

	maze_array = []

	##############	ADD YOUR CODE HERE	##############
    # arr_boxes is a numpy array filled with zeros
	arr_boxes = np.zeros(shape=(10,10), dtype = int)

	# Initializing the array as outer borders were present in all images
	for i in range(10):
		arr_boxes[i,0] += 1
		arr_boxes[0,i] += 2
		arr_boxes[i,9] += 4
		arr_boxes[9,i] += 8

    # Slicing the images to have a 50x100 part of image to detect if vertical wall is there
	# between them 
	# r is the row index
	for r in range(10):
		c = 0   # column index
		sci = 0  # starting column pixel value
		eci = 100  # ending column pixel value
		while(c != 9):  
			part = warped_img[r * 50: r * 50 + 50 , sci:eci]
			vw = detect_wall(part)
			if(vw):
				arr_boxes[r,c] += 4
				arr_boxes[r,c+1] += 1
			sci += 50
			eci += 50
			c += 1

    # Slicing the images to have a 100x50 part of image to detect if vertical wall is there
	# between them 
	# c is the column index
	for c in range(10):
		r = 0    # row index
		sri = 0  # starting row pixel value
		eri = 100  # ending row pixel value
		while(r != 9):  
			part = warped_img[sri:eri ,c * 50: c * 50 + 50]
			hw = detect_wall(part)
			if(hw):
				arr_boxes[r,c] += 8
				arr_boxes[r+1,c] += 2
			sri += 50
			eri += 50
			r += 1

    # Finally converting numpy array to list
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
# Function Name:    main
#        Inputs:    None
#       Outputs:    None
#       Purpose:    This part of the code is only for testing your solution. The function first takes 'maze00.jpg'
# 					as input, applies Perspective Transform by calling applyPerspectiveTransform function,
# 					encodes the maze input in form of 2D array by calling detectMaze function and writes this data to csv file
# 					by calling writeToCsv function, it then asks the user whether to repeat the same on all maze images
# 					present in 'test_cases' folder or not. Write your solution ONLY in the space provided in the above
# 					applyPerspectiveTransform and detectMaze functions.

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

