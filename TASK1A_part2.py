'''
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This script is to implement Task 1A - Part 2 of Nirikshak Bot (NB) Theme (eYRC 2020-21).
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
# Filename:			task_1a_part1.py
# Functions:		process_video
# 					[ Comma separated list of functions in this file ]
# Global variables:	frame_details
# 					[ List of global variables defined in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv, os)                ##
##############################################################
import cv2
import numpy as np
import os
##############################################################


# Global variable for details of frames seleced in the video will be put in this dictionary, returned from process_video function
frame_details = {}


################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################






##############################################################


def process_video(vid_file_path, frame_list):

	"""
	Purpose:
	---
	this function takes file path of a video and list of frame numbers as arguments
	and returns dictionary containing details of red color circle co-ordinates in the frame

	Input Arguments:
	---
	`vid_file_path` :		[ str ]
		file path of video
	`frame_list` :			[ list ]
		list of frame numbers

	Returns:
	---
	`frame_details` :		[ dictionary ]
		co-ordinate details of red colored circle present in selected frame(s) of video
		{ frame_number : [cX, cY] }

	Example call:
	---
	frame_details = process_video(vid_file_path, frame_list)
	"""

	global frame_details

	##############	ADD YOUR CODE HERE	##############
    capture = cv2.VideoCapture(vid_file_path)
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    indexlist=[]
    imagelist = []
    for i in frame_list:
        i=i-1
        if i==0:
            _, frame = capture.read()
            imagelist.append(frame)
            indexlist.append(i)
            
        elif i>0 and i<frame_count:
            capture.set(cv2.CAP_PROP_POS_FRAMES,int(i))
            _, frame = capture.read()
            imagelist.append(frame)
            indexlist.append(i)
        
        for i in range(len(indexlist)):
            index = indexlist[i]
            if index>0 and index<frame_count:
                img = imagelist[i]
                
                lab = cv2.cvtColor(img,cv2.COLOR_BGR2LAB)
                b = lab[:,:,2]
                ret,thresh = cv2.threshold(b,240,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
                res = cv2.bitwise_xor(b,thresh)
                ret, thresh2 = cv2.threshold(res,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

                thresh3 = cv2.bitwise_xor(b,thresh2)

                minval,maxval,minloc,maxloc = cv2.minMaxLoc(thresh3)
                ret,thresh4 = cv2.threshold(thresh3,int(minval+29),255,cv2.THRESH_BINARY_INV)

                contours,_= cv2.findContours(thresh4.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                for cnt in contours:
                    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
                    M = cv2.moments(cnt)

                    area = cv2.contourArea(cnt)
                    if area>6000:

                        if M["m00"]!=0:
                            cx = int(M["m10"]/M["m00"])
                            cy = int(M["m01"]/M["m00"])
                        elif M["m00"]==0:
                            cx,cy=0,0


                frame_details[index+1]=[cx,cy]
            else:
                index=index-1
                img = imagelist[i]
                index = i
                lab = cv2.cvtColor(img,cv2.COLOR_BGR2LAB)
                b = lab[:,:,2]
                ret,thresh = cv2.threshold(b,240,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
                res = cv2.bitwise_xor(b,thresh)
                ret, thresh2 = cv2.threshold(res,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

                thresh3 = cv2.bitwise_xor(b,thresh2)

                minval,maxval,minloc,maxloc = cv2.minMaxLoc(thresh3)
                ret,thresh4 = cv2.threshold(thresh3,int(minval+29),255,cv2.THRESH_BINARY_INV)

                contours,_= cv2.findContours(thresh4.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                for cnt in contours:
                    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
                    M = cv2.moments(cnt)

                    area = cv2.contourArea(cnt)
                    if area>6000:

                        if M["m00"]!=0:
                            cx = int(M["m10"]/M["m00"])
                            cy = int(M["m01"]/M["m00"])
                        elif M["m00"]==0:
                            cx,cy=0,0


                frame_details[index+1]=[cx,cy]


	
	

	##################################################

	return frame_details


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:    main
#        Inputs:    None
#       Outputs:    None
#       Purpose:    the function first takes input for selecting one of two videos available in Videos folder
#                   and a input list of frame numbers for which the details are to be calculated. It runs process_video
#                   function on these two inputs as argument.

if __name__ == '__main__':

	curr_dir_path = os.getcwd()
	print('Currently working in '+ curr_dir_path)

	# path directory of videos in 'Videos' folder
	vid_dir_path = curr_dir_path + '/Videos/'
	
	try:
		file_count = len(os.listdir(vid_dir_path))
	
	except Exception:
		print('\n[ERROR] "Videos" folder is not found in current directory.')
		exit()
	
	print('\n============================================')
	print('\nSelect the video to process from the options given below:')
	print('\nFor processing ballmotion.m4v from Videos folder, enter \t=> 1')
	print('\nFor processing ballmotionwhite.m4v from Videos folder, enter \t=> 2')
	
	choice = input('\n==> "1" or "2": ')

	if choice == '1':
		vid_name = 'ballmotion.m4v'
		vid_file_path = vid_dir_path + vid_name
		print('\n\tSelected video is: ballmotion.m4v')
	
	elif choice=='2':
		vid_name = 'ballmotionwhite.m4v'
		vid_file_path = vid_dir_path + vid_name
		print('\n\tSelected video is: ballmotionwhite.m4v')
	
	else:
		print('\n[ERROR] You did not select from available options!')
		exit()
	
	print('\n============================================')

	if os.path.exists(vid_file_path):
		print('\nFound ' + vid_name)
	
	else:
		print('\n[ERROR] ' + vid_name + ' file is not found. Make sure "Videos" folders has the selected file.')
		exit()
	
	print('\n============================================')

	print('\nEnter list of frame(s) you want to process, (between 1 and 404) (without space & separated by comma) (for example: 33,44,95)')

	frame_list = input('\nEnter list ==> ')
	frame_list = list(frame_list.split(','))

	try:
		for i in range(len(frame_list)):
			frame_list[i] = int(frame_list[i])
		print('\n\tSelected frame(s) is/are: ', frame_list)
	
	except Exception:
		print('\n[ERROR] Enter list of frame(s) correctly')
		exit()
	
	print('\n============================================')

	try:
		print('\nRunning process_video function on', vid_name, 'for frame following frame(s):', frame_list)
		frame_details = process_video(vid_file_path, frame_list)

		if type(frame_details) is dict:
			print(frame_details)
			print('\nOutput generated. Please verify')
		
		else:
			print('\n[ERROR] process_video function returned a ' + str(type(frame_details)) + ' instead of a dictionary.\n')
			exit()
	
	except Exception:
		print('\n[ERROR] process_video function is throwing an error. Please debug process_video function')
		exit()

	print('\n============================================')
