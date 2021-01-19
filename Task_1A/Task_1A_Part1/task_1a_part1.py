'''
*****************************************************************************************
*
*           ===============================================
*               Nirikshak Bot (NB) Theme (eYRC 2020-21)
*           ===============================================
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

# Team ID:      [1631]
# Author List:    [ Anushree Sabnis, Saurabh Powar ]
# Filename:     task_1a_part1.py
# Functions:    scan_image
#           [ detect_sides, detect_quad ]
# Global variables: shapes
#           [ List of global variables defined in this file ]


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



def detect_sides(box1,box2,box3,box4):
    #this functions calculates the length of 4 sides of a quadrilateral, given 4 vertices
    
    ylist = []
    box = [box1,box2,box3,box4]
    
    
    for i in box:
        
        ylist.append(i[1]) #taking y co-ords of 4 vertices
    
    ylist = np.array([ylist])
    
    
    sort_indy = np.argsort(ylist) #sorted y co-ords in ascending order
    sort_indy = sort_indy.ravel()
    
    
    if box[sort_indy[0]][0]>box[sort_indy[1]][0]:
        #comparing x-co-ords or the 2 minimum values of y
        br = box[sort_indy[0]] #the vertex with greater x value becomes the bottom right vertex
        bl = box[sort_indy[1]] #the vertex with smaller x value becomes the bottom left vertex
    elif box[sort_indy[0]][0]<box[sort_indy[1]][0]:
        br = box[sort_indy[1]]
        bl = box[sort_indy[0]]
    if box[sort_indy[2]][0]>box[sort_indy[3]][0]:
        #comparing x-co-ords or the 2 maximum values of y
        tr = box[sort_indy[2]] #the vertex with greater x value becomes the top right vertex
        tl = box[sort_indy[3]] #the vertex with smaller x value becomes the top left vertex
    elif box[sort_indy[2]][0]<box[sort_indy[3]][0]:
        tr = box[sort_indy[3]]
        tl = box[sort_indy[2]]
    return bl,br,tr,tl


def detect_quad(imfinal):
    #this function detects quadrialteral contained within roi of contour specified by minAreaRect
    corners = cv2.goodFeaturesToTrack(imfinal,4,0.01,10)
    #detecting 4 strongest corners of the quadrilateral with param2=4
    corners = np.int0(corners)
    #int0 is an alias for int64 or int32, useful for indexing
    bl,br,tr,tl = detect_sides(corners[0][0],corners[1][0],corners[2][0],corners[3][0])
    #bl,br,tr,tl respectively represent bottom-left, bottom-right, top-right, and top-left vertices of quadrilateral


    hs1 = tr[0] - tl[0] #the topmost horizontal side
    vs1 = tr[1] - br[1] #the topmost vertical side
    hs2 = br[0] - bl[0] #the bottom-most horizontal side
    vs2 = tl[1] - bl[1] #the bottom-most vertical side

    if tr[0]==tl[0] or tr[1]==tl[1]: #if both x and y coords of top vertices are equal
        sltop = 0 #slope is zero (infinite slope prevented)
    elif tr[1]!=tl[1] and tr[0]!=tl[0]:
        sltop = ((tr[1])-(tl[1]))/((tr[0])-(tl[0])) #top side
    if br[1]==bl[1] or br[0]==bl[0]:
        slbot = 0
    elif br[1]!=bl[1] and br[0]!=bl[0]:
        slbot = ((br[1])-(bl[1]))/((br[0])-(bl[0])) #bottom side
    if tr[0]==br[0] or tr[1]==br[1]:
        slright = 0
    elif tr[0]!=br[0] and tr[1]!=br[1]:
        slright = ((tr[1])-(br[1]))/((tr[0])-(bl[0]))
    if tl[0]==bl[0] or tl[1]==bl[1]:
        slleft = 0
    elif tl[0]!=bl[0] and tl[1]!=bl[1]:
        slleft = ((tl[1])-(bl[1]))/((tl[0])-(bl[0]))


    d1 = ((((tl[0])-(br[0]))**2)+(((tl[1])-(br[1]))**2))**0.5 #left diagonal
    d2 = ((((tr[0])-(bl[0]))**2)+(((tr[1])-(bl[1]))**2))**0.5 #right diagonal
    if hs1>hs2-2 and hs1<hs2+2: #range of +/-1 given to allow for inaccuracies of cv2.goodFeaturesToTrack function
        if vs1>vs2-2 and vs1<vs2+2:
            if d1==d2:
                if hs1<vs1+2 and hs1>vs1-2:
                    
                    shape= "Square" #all sides and diagonals equal
                elif hs1!=vs1:
                    #print("parallelogram")
                    shape = "Parallelogram" #opposite sides and diagonals equal (every rectangle is a parallelogram)
            elif d1!=d2:
                if hs1<vs1+2 and hs1>vs1-2:
                    #print("rhombus")
                    shape = "Rhombus" #all sides equal, diagonals inequal
                elif hs1!=vs1:
                    #print("parallelogram")
                    shape = "Parallelogram" #opposite sides equal, diagonals inequal
        elif vs1!=vs2:
            if sltop==slbot or slleft==slright:
                #print("trapezium")
                shape = "Trapezium" #horizontal sides equal, atleast two opposite sides have equal slopes(isoceles trap.)
            elif sltop!=slbot and slleft!=slright:
                #print("quadrilateral")
                shape = "Quadrilateral" #horizontal sides equal, varying slopes
    elif hs1!=hs2:
        if vs1!=vs2:
            if sltop==slbot or slleft==slright:
                #print("trapezium")
                shape = "trapezium" #no sides equal, atleast two opposite sides have equal slopes
            elif sltop!=slbot and slleft!=slright:
                #print("quadrilateral")
                shape = "Quadrilateral" #no sides equal,varying slopes
        if vs1<vs2+2 and vs1>vs2-2:
            if sltop==slbot or slleft==slright:
                #print("isoceles trapezium")
                shape = "trapezium" #vertical sides equal, atleast two opposite sides have equal slopes(isoceles trap.)
            elif sltop!=slbot and slleft!=slright:
                #print("quadrilateral")
                shape = "Quadrilateral" #vertical sides equal, varying slopes


    

    return shape







##############################################################


def scan_image(img_file_path):


    """
    Purpose:
    ---
    this function takes file path of an image as an argument and returns dictionary
    containing details of colored (non-white) shapes in that image
    Input Arguments:
    ---
    `img_file_path` :   [ str ]
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

    ##############  ADD YOUR CODE HERE  ##############
    
    shapes = {}
    img = cv2.imread(img_file_path)
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    
    
    
    ret, thresh2 = cv2.threshold(img_gray,120,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU) #histogram based otsu thresholding
    thresh2 = cv2.dilate(thresh2,kernel,iterations=1) #image dilation for recovering pixels excluded in thresholding
    
    
    
    
    
    
    contours,_= cv2.findContours(thresh2.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #finding largest contour
    contours = sorted(contours, key=cv2.contourArea, reverse=True) #sorting contours based on area
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        #approximates a polygon around the contour with minimum number of vertices
        
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        M = cv2.moments(cnt)
        if M["m00"]!=0:
            cx = int(M["m10"]/M["m00"])
            cy = int(M["m01"]/M["m00"])
        elif M["m00"]==0:
            cx,cy=0,0
        #area = cv2.contourArea(approx)
        rx,ry,rw,rh = cv2.boundingRect(cnt)
        roi = thresh2[ry:ry+rh-2,rx:rx+rw-2] #bounding rectangle of contour as roi
        area = cv2.countNonZero(roi) #counting nonzero pixels in roi for accurate contour area
        (b,g,r) = img[cy,cx] #opencv reads images as bgr
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
            rect = cv2.minAreaRect(cnt) #minAreaRect works when the shape is rotated, as well
            box = cv2.boxPoints(rect)
            box = np.int0(box) #int0 is alias for np.int32 and np.int64, useful for indexing

            bl,br,tr,tl = detect_sides(box[0],box[1],box[2],box[3]) #detecting four sides of min area rect
            hs1 = tr[0] - tl[0]
            vs1 = tr[1] - br[1]
            hs2 = br[0] - bl[0]
            vs2 = tl[1] - bl[1]
            imfinal = img_gray[bl[1]-20:bl[1]+max(vs2,vs1)+40,bl[0]-20:bl[0]+max(hs1,hs2)+40].copy() #roi of min area rect
            shape = detect_quad(imfinal) 
            shapes[str(shape)]=[color,area,cx,cy]
            
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


# NOTE: YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
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
