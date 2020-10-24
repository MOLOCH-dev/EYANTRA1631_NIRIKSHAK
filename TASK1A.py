'''
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This script is to implement Task 1A - Part 1 of Nirikshak Bot (NB) Theme (eYRC 2020-21).
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

# Team ID:			[1631]
# Author List:		[ Anushree Sabnis ]
# Filename:			task_1a_part1.py
# Functions:		scan_image
# 					[ Comma separated list of functions in this file ]
# Global variables:	shapes
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


# Global variable for details of shapes found in image and will be put in this dictionary, returned from scan_image function
shapes = {}
shapespure = []


################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################






##############################################################


def scan_image(img_file_path):


    """
    Purpose:
    ---
    this function takes file path of an image as an argument and returns dictionary
    containing details of colored (non-white) shapes in that image

    Input Arguments:
    ---
    `img_file_path` :		[ str ]
        file path of image

    Returns:
    ---
    `shapes` :              [ dictionary ]
        details of colored (non-white) shapes present in image at img_file_path
        { 'Shape' : ['color', Area, cX, cY] }
    
    Example call:
    ---
    shapes = scan_image(img_file_path)
    """

    global shapes

    ##############	ADD YOUR CODE HERE	##############
    
    shapes = {}
    img = cv2.imread(img_file_path)
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, thresh2 = cv2.threshold(img_gray,127,255,cv2.THRESH_BINARY_INV)
    contours,_= cv2.findContours(thresh2.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    font = cv2.FONT_HERSHEY_COMPLEX
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        cv2.drawContours(img,[approx],0,(0),5)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        M = cv2.moments(cnt)
        cx = int(M["m10"]/M["m00"])
        cy = int(M["m01"]/M["m00"])
        area = cv2.contourArea(cnt)
        (b,g,r) = img[cy,cx]
        if b>g and b>r:
            color = "blue"
        elif g>b and g>r:
            color = "green"
        elif r>b and r>g:
            color = "red"
        else:
            color = "none"
        if len(approx)==3:
            shapes["Triangle"] = [color,area,cx,cy]
            
            
        elif len(approx)==4:
            #cv2.putText(test_img_2_gray,"Rectangle",(x,y),font,1,(0))
            #print("quad")
            (a,b,c,d) = cv2.boundingRect(approx)
            #print(a,b,c,d)
            ar = c/float(d)
            print(ar)
            if ar>0.95 and ar<1.05:
                shapespure.append("Square")
                shapes["Square"]=[color,area,cx,cy]

                #cv2.putText(quad_img_gray,"Square",(x,y),font,0.5,(0))
            elif ar>1.5 and ar<2:
                shapespure.append("Rhombus")
                shapes["Rhombus"]=[color,area,cx,cy]
                #print("rhomb")
                #cv2.putText(quad_img_gray,"Rhombus",(x,y),font,0.5,(0))
            elif ar>1.05 and ar<1.5:
                shapespure.append("Rectangle")
                shapes["Rectangle"]=[color,area,cx,cy]
                #print("rect")
                #cv2.putText(test_img_2_gray,"Rectangle",(x,y),font,1,(0))
            elif ar>1.4 and ar<1.5:
                shapespure.append("Trapezium")
                shapes["Trapezium"]=[color,area,cx,cy]
                #print("trap")
                #cv2.putText(test_img_2_gray,"trap",(x,y),font,1,(0))
            elif ar>2 and ar<3:
                shapespure.append("Parallelogram")
                shapes["Parallelogram"]=[color,area,cx,cy]
                #print("Parallelogram")
                #cv2.putText(test_img_2_gray,"Parallelogram",(x,y),font,1,(0))
        elif len(approx)==5:
            shapespure.append("Pentagon")
            shapes["Pentagon"]=[color,area,cx,cy]
        elif len(approx)==6:
            shapespure.append("Hexagon")
            shapes["Hexagon"]=[color,area,cx,cy]
        elif len(approx)>6:
            shapespure.append("Circle")
            shapes["Circle"]=[color,area,cx,cy]

    
    
	

	##################################################
    
    return shapes


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:    main
#        Inputs:    None
#       Outputs:    None
#       Purpose:    the function first takes 'Sample1.png' as input and runs scan_image function to find details
#                   of colored (non-white) shapes present in 'Sample1.png', it then asks the user whether
#                   to repeat the same on all images present in 'Samples' folder or not

if __name__ == '__main__':

    curr_dir_path = os.getcwd()
    print('Currently working in '+ curr_dir_path)

    # path directory of images in 'Samples' folder
    img_dir_path = curr_dir_path + '/Samples/'
    
    # path to 'Sample1.png' image file
    file_num = 1
    img_file_path = img_dir_path + 'Sample' + str(file_num) + '.png'

    print('\n============================================')
    print('\nLooking for Sample' + str(file_num) + '.png')

    if os.path.exists('Samples/Sample' + str(file_num) + '.png'):
        print('\nFound Sample' + str(file_num) + '.png')
    
    else:
        print('\n[ERROR] Sample' + str(file_num) + '.png not found. Make sure "Samples" folder has the selected file.')
        exit()
    
    print('\n============================================')

    try:
        print('\nRunning scan_image function with ' + img_file_path + ' as an argument')
        shapes = scan_image(img_file_path)

        if type(shapes) is dict:
            print(shapes)
            print('\nOutput generated. Please verify.')
        
        else:
            print('\n[ERROR] scan_image function returned a ' + str(type(shapes)) + ' instead of a dictionary.\n')
            exit()

    except Exception:
        print('\n[ERROR] scan_image function is throwing an error. Please debug scan_image function')
        exit()

    print('\n============================================')

    choice = input('\nWant to run your script on all the images in Samples folder ? ==>> "y" or "n": ')

    if choice == 'y':

        file_count = 2
        
        for file_num in range(file_count):

            # path to image file
            img_file_path = img_dir_path + 'Sample' + str(file_num + 1) + '.png'

            print('\n============================================')
            print('\nLooking for Sample' + str(file_num + 1) + '.png')

            if os.path.exists('Samples/Sample' + str(file_num + 1) + '.png'):
                print('\nFound Sample' + str(file_num + 1) + '.png')
            
            else:
                print('\n[ERROR] Sample' + str(file_num + 1) + '.png not found. Make sure "Samples" folder has the selected file.')
                exit()
            
            print('\n============================================')

            try:
                print('\nRunning scan_image function with ' + img_file_path + ' as an argument')
                shapes = scan_image(img_file_path)

                if type(shapes) is dict:
                    print(shapes)
                    print('\nOutput generated. Please verify.')
                
                else:
                    print('\n[ERROR] scan_image function returned a ' + str(type(shapes)) + ' instead of a dictionary.\n')
                    exit()

            except Exception:
                print('\n[ERROR] scan_image function is throwing an error. Please debug scan_image function')
                exit()

            print('\n============================================')

    else:
        print('')
