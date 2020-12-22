'''
*****************************************************************************************
*
*				===============================================
*					Nirikshak Bot (NB) Theme (eYRC 2020-21)
*				===============================================
*
*  This script is to implement Task 3 of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD (now MOE) project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
'''

# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_3.py
# Functions:		init_setup(rec_client_id), control_logic(center_x,center_y), change_setpoint(new_setpoint)
#					[ Comma separated list of functions in this file ]
# Global variables: client_id, setpoint=[]
#					[ List of global variables defined in this file ]


####################### IMPORT MODULES #########################
## You are not allowed to make any changes in this section.	  ##
## You have to implement this task with the six available	  ##
## modules for this task (numpy,opencv,os,sys,traceback,time) ##
################################################################
import numpy as np
import cv2
import os, sys
import traceback
import time
##############################################################

# Importing the sim module for Remote API connection with CoppeliaSim
try:
	import sim
	
except Exception:
	print('\n[ERROR] It seems the sim.py OR simConst.py files are not found!')
	print('\n[WARNING] Make sure to have following files in the directory:')
	print('sim.py, simConst.py and appropriate library - remoteApi.dll (if on Windows), remoteApi.so (if on Linux) or remoteApi.dylib (if on Mac).\n')
	sys.exit()


# Global variable "client_id" for storing ID of starting the CoppeliaSim Remote connection
# NOTE: DO NOT change the value of this "client_id" variable here
client_id = -1

# Global list "setpoint" for storing target position of ball on the platform/top plate
# The zeroth element stores the x pixel and 1st element stores the y pixel
# NOTE: DO NOT change the value of this "setpoint" list
setpoint = [640,640]

# Global variable "vision_sensor_handle" to store handle for Vision Sensor
# NOTE: DO NOT change the value of this "vision_sensor_handle" variable here
vision_sensor_handle = 0

# You can add your global variables here
##############################################################
global pitch_angle,add_angle,sub_angle,inital_error, center_x, center_y
global roll_angle, setflag,pos,neg
inerrx=0
innery=0
perror_x=2000
perror_y=2000
pos=0
neg=0
##############################################################


################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.		##
## Please add proper comments to ensure that your code is	##
## readable and easy to understand.							##
##############################################################
def correct_X(error_x,flag):
	Kp = 5
	PIDx = (error_x/100)*np.pi/180*Kp
	PIDx = constrain(PIDx)
	if flag==1:
		
		targets = [np.abs([10*np.pi/180]),-np.abs([10*np.pi/180]),-np.abs([PIDx]),np.abs([PIDx])]
		
		control_servo(targets)
		
	elif flag==2:
		targets = [-np.abs([PIDx]),np.abs([PIDx]),-np.abs([10*np.pi/180]),np.abs([10*np.pi/180])]
		control_servo(targets)
#targets=[np.abs([10*np.pi/180]),-np.abs([10*np.pi/180]),-np.abs([10*np.pi/180]),np.abs([10*np.pi/180])]

def correct_Y(error_y,flag):
	Kp = 5
	PIDy = (error_y/100)*np.pi/180*Kp
	PIDy = constrain(PIDy)
	if flag==3:
		targets = [0,np.abs([PIDy]),-np.abs([PIDy]),0]
		control_servo(targets)
	elif flag==4:
		targets = [-np.abs([PIDy]),-np.abs([PIDy]),np.abs([PIDy]),np.abs([PIDy])]
		control_servo(targets)

def constrain(angle):
	if angle>1.57:
		angle = 1.57
		
		
	elif angle<-1.57:
		angle = -1.57
	return angle
def calculate_target_angle(pos,neg,center_x,center_y):
	global set_x, set_y, error_x, error_y, flag, setflag, setflag2, setflag3,perror_x,perror_y,trigger
	set_x= setpoint[0]
	set_y = setpoint[1]
	#print(initial_error,"inerrarr")
	#print(setpoint, client_id, center_x, center_y, set_x, set_y)
	#errorCode = sim.simxSynchronousTrigger(client_id)
	#print(errorCode)
	
	#initial_ex = initial_error[2]
	#initial_ey = initial_error[3]
	
	#print("setpoints",set_x,set_y,setpoint)
	print("current location",center_x,center_y)
	#pitch and roll angles
	error_x = np.abs([center_x - set_x])
	error_y = np.abs([center_y - set_y])
	trigger=0
	signerrorx = set_x-center_x
	signerrory = set_y-center_y
	if error_x!=0:
		if signerrorx/error_x==1:
			pos=pos+1
		elif signerrorx/error_x==-1:
			neg=neg+1
	elif error_x==0:
		pos=pos+1
	if error_y!=0:
		if signerrory/error_y==1:
			pos=pos+1
		elif signerrory/error_y==-1:
			neg=neg+1
	elif error_y==0:
		pos=pos+1
	
	"""
	if set_x != center_x:
		error_x = center_x-set_x
	elif set_x==center_x:
		pitch_slope = 1
	if set_y!=center_y:
		roll_slope = ((set_x-center_x)/(set_y-center_y))
	elif set_y==center_y:
		roll_slope = 1
	pitch_angle, roll_angle = np.arctan([pitch_slope,roll_slope])
	add_angle,sub_angle = np.abs([pitch_angle+roll_angle,pitch_angle-roll_angle])
	"""
	#Flags
	#1 - Pure Right
	
		

	#	flag =9	
	box = 100
	box2=250
	box3 = 0
	box4=50
	#print(initial_ex,"inex")
	
	
	if np.abs([center_x-set_x])<box2 and np.abs([center_y-set_y])<box2:
		print("in box3")
		
		setflag = True
	if np.abs([center_x-set_x])<box and np.abs([center_y-set_y])<box:
		print("in box")
		
		setflag2 = True
	if np.abs([center_x-set_x])<box4 and np.abs([center_y-set_y])<box4:
		print("in box4")
		trigger=trigger+1
		
		setflag3 = True
	print(setflag2,"sf2")
	print(setflag,"sf1")
	print(setflag3,"sf3")
	"""
	if np.abs([center_x-set_x])<box2 and np.abs([center_y-set_y])<box2:
		print("in box2")
		if setreach==False:
			flag=13
		
		elif setreach==True:
		
			if center_x-set_x<box2:
				if np.abs([center_y-set_y])>20:
					if center_y-set_y<box2:
						print("error too much")
						flag = 12 #front right
					elif set_y-center_y<box2:
						flag=11 #back right
				elif np.abs([center_y-set_y])<20:
					flag=1
			elif set_x-center_x<box2:
				if np.abs([center_y-set_y])>20:
					if center_y-set_y<box2:
						flag = 10 #front left
					elif set_y-center_y<box2:
						flag=9 #back left
				elif np.abs([center_y-set_y])<20:
					flag=2
		"""		
	if perror_x!=2000:
		px = perror_x
		py = perror_y
	elif perror_x==2000:
		px = None
		py=None
	print(px,py,"pxpy")	   
	
	"""
	if setflag2==True:
		print(error_x,error_y)
		if error_x-error_y>20:
			
			if set_x-center_x>40:
				
				flag=1
			elif center_x-set_x>40:
				flag=2
		elif error_y-error_x>20:
			if set_y-center_y>40:
				flag=3
			elif center_y-set_y>40:
				flag=4
		elif np.abs([error_x-error_y]) in range(0,41):
			if px!=None and py!=None:
				if error_x-px>5:
					if flag==1:
						flag=2
					if flag==2:
						flag=1
					
				elif px-error_x>=0:
					flag=9
				if error_y-py>5:
					if flag==3:
						flag=4
					if flag==4:
						flag=3
				elif py-error_y>=0:
					flag=9
	"""		
	#elif setflag2==False:
	
	if (set_x-center_x>box3 and np.abs([set_y-center_y])<0):
		
		if setflag==False:
			flag = 1
		elif setflag==True:
			flag=1
		
		
	#2 - Pure Left
	elif (center_x-set_x>box3 and np.abs([set_y-center_y])<0):
		if setflag==False:
			flag = 2
		elif setflag==True:
			flag=2
		
	#3 - Pure forward
	elif (np.abs([set_x-center_x])<0 and set_y-center_y>box3):
		if setflag==False:
			flag = 3
		elif setflag==True:
			flag=3
		
	#4 - Pure backward
	elif (np.abs([set_x-center_x])<0 and center_y-set_y>box3):
		if setflag==False:
			flag = 4
		elif setflag==True:
			flag=4
		
	#5 - Forward+right
	elif (set_x-center_x>box3 and set_y-center_y>box3):
		if np.abs([error_x-error_y])<120:
			if setflag==False:
				flag = 5
			elif setflag==True:
				flag=5
		if error_x-error_y>120:
		
			if set_x-center_x>0:
				flag=1
			elif center_x-set_x>0:
				flag=2
		elif error_y-error_x>120:
			if set_y-center_y>0:
				flag=3
			elif center_y-set_y>0:
				flag=4
		
	#6 - Forward+left
	elif (center_x-set_x>box3 and set_y-center_y>box3):
		if np.abs([error_x-error_y])<=50:
			if setflag==False:
				
				flag = 6
			elif setflag==True:
				flag = 6
		if error_x-error_y>50:
		
			if set_x-center_x>0:
				flag=1
			elif center_x-set_x>0:
				flag=2
		elif error_y-error_x>50:
			if set_y-center_y>0:
				flag=3
			elif center_y-set_y>0:
				flag=4
	#7 - backward+right
	elif (set_x-center_x>box3 and center_y-set_y>box3):
		if np.abs([error_x-error_y])<=50:
			if setflag==False:
				flag = 7
			elif setflag==True:
				flag = 7
		if error_x-error_y>50:
		
			if set_x-center_x>0:
				flag=1
			elif center_x-set_x>0:
				flag=2
		elif error_y-error_x>50:
			if set_y-center_y>0:
				flag=3
			elif center_y-set_y>0:
				flag=4
		
	#8 - backward+left
	elif (center_x-set_x>box3 and center_y-set_y>box3):
		if np.abs([error_x-error_y])<50:
			if setflag==False:
				flag = 8
			elif setflag==True:
				flag=8
		if error_x-error_y>50:
		
			if set_x-center_x>0:
				flag=1
			elif center_x-set_x>0:
				flag=2
		elif error_y-error_x>50:
			if set_y-center_y>0:
				flag=3
			elif center_y-set_y>0:
				flag=4
	
	   
	print(flag)
	return pos,neg,trigger,error_x,error_y, flag
	


###
def current_rev_angle(handle_arr):
	ret = [-1,-1,-1,-1]
	j_angles = [0,0,0,0]
	#sim.simxPauseSimulation(client_id,sim.simx_opmode_oneshot)
	while ret != [sim.simx_return_ok,sim.simx_return_ok,sim.simx_return_ok,sim.simx_return_ok]:
		for i in range(4):
			ret[i],j_angles[i]=sim.simxGetJointPosition(client_id,handle_arr[i],sim.simx_opmode_buffer)
	#sim.simxStartSimulation(client_id,sim.simx_opmode_oneshot)
	#print(j_angles,"jangles")
	return j_angles
###
def control_servo(targets):
	global posarray
	
	#print(posarray,"posarray in servo")
	returnarray = [-1,-1,-1,-1]
	#while (np.abs([posarray[0]-targets[0]])>0.1*np.pi/180 and np.abs([posarray[1]-targets[1]])>0.1*np.pi/180) and (np.abs([posarray[2]-targets[2]])>0.1*np.pi/180 and np.abs([posarray[3]-targets[3]])>0.1*np.pi/180):
	#sim.simxSynchronousTrigger(client_id)
		
	#posarray = current_rev_angle(handle_arr)
	#if np.abs([posarray[0]-targets[0]]) >0.1*np.pi/180:
		#sim.simxSynchronousTrigger(client_id)
	_=sim.simxSetJointTargetPosition(client_id,handle_arr[0],targets[0],sim.simx_opmode_oneshot)		
		#sim.simxSetJointMaxForce(client_id,handle_arr[1],0.1,sim.simx_opmode_oneshot)
		#sim.simxSetJointTargetVelocity(client_id,handle_arr[0],360*np.pi/180,sim.simx_opmode_oneshot)
		#sim.simxSynchronousTrigger(client_id)
	#if np.abs([posarray[1]-targets[1]]) >0.1*np.pi/180:
		#sim.simxSynchronousTrigger(client_id)
		#sim.simxSetJointTargetVelocity(client_id,handle_arr[1],360*np.pi/180,sim.simx_opmode_oneshot)
		#sim.simxSetJointMaxForce(client_id,handle_arr[2],0.1,sim.simx_opmode_oneshot)
	_=sim.simxSetJointTargetPosition(client_id,handle_arr[1],targets[1],sim.simx_opmode_oneshot)	
	
	#sim.simxSetJointTargetVelocity(client_id,handle_arr[2],90*np.pi/180*signarray[2],sim.simx_opmode_oneshot)
		#sim.simxSynchronousTrigger(client_id)
	#if np.abs([posarray[2]-targets[2]]) >0.1*np.pi/180:
		#sim.simxSynchronousTrigger(client_id)
		#sim.simxSetJointTargetVelocity(client_id,handle_arr[2],360*np.pi/180,sim.simx_opmode_oneshot)
		#sim.simxSetJointMaxForce(client_id,handle_arr[2],0.1,sim.simx_opmode_oneshot)
	_=sim.simxSetJointTargetPosition(client_id,handle_arr[2],targets[2],sim.simx_opmode_oneshot)
		#sim.simxSynchronousTrigger(client_id)
	#sim.simxSetJointTargetVelocity(client_id,handle_arr[3],90*np.pi/180*signarray[3],sim.simx_opmode_oneshot)
	#sim.simxSetJointMaxForce(client_id,handle_arr[3],100,sim.simx_opmode_oneshot)
	#if np.abs([posarray[3]-targets[3]]) >0.1*np.pi/180:
		#sim.simxSynchronousTrigger(client_id)
		#sim.simxSetJointMaxForce(client_id,handle_arr[3],0.1,sim.simx_opmode_oneshot)
	_=sim.simxSetJointTargetPosition(client_id,handle_arr[3],targets[3],sim.simx_opmode_oneshot)				  
		#sim.simxSynchronousTrigger(client_id)
	
	#sim.simxSynchronousTrigger(client_id)
	
###
def reposition(center_x,center_y):
	if center_x-center_y<5:
		xangle=12*np.pi/180
		yangle=0
	if center_y-center_x<5:
		yangle=12*np.pi/180
		xangle=0
###
def control_angle(handle_arr,center_x,center_y):
	global error_x, error_y, posarray, perror_x,perror_y, setflag, setflag2, setflag3,pos,neg
	
	pos,neg,trigger,error_x , error_y,flag = calculate_target_angle(pos,neg,center_x,center_y)
	print(pos,neg,"pn")
	Kp=1.26
	"""
	if pos>0 and neg>0:
		Kp=9.5
		print(Kp)
	elif pos>0 and neg==0:
		Kp=3
		print(Kp)
	else:
		Kp=3
		print(Kp)
	
	"""			
			
	
	#maxangle = 10*np.pi/180
	#if prev_errx!=0:
	PIDx =(error_x/100)*Kp*np.pi/180
	#-(Kd*(prev_errx-error_x)*(np.pi/180)/50*40)
	PIDx = constrain(PIDx)
	print(PIDx,"pidx")
	PIDy = (error_y/100)*Kp*np.pi/180
	#-(Kd*(prev_erry-error_y)*(np.pi/180)/100)
	PIDy = constrain(PIDy)
	"""
	elif prev_errx==0:
		PIDx =maxangle-((1000/error_x)*np.pi/180*Kp)
		PIDx = constrain(PIDx)
		PIDy = maxangle-((1000/error_y)*np.pi/180*Kp)
		PIDy = constrain(PIDy)
		prev_errx = error_x
		prev_erry = error_y
		"""
	"""
	maxangle2 = 5*np.pi/180
	if prev_errx2!=0:
	"""
	"""
	if setreach==False:
		Kp2 = 20*Kp
	elif setreach==True:
		Kp2 = 12*Kp
	print(Kp2/Kp)
	PIDx2 =(error_x/1000)*Kp2*np.pi/180
	PIDx2 = constrain(PIDx2)
	PIDy2 = (error_y/1000)*Kp2*np.pi/180
	PIDy2 = constrain(PIDy2)

		
	"""
	"""
	elif prev_errx2==0:
		PIDx =maxangle-((1000/error_x)*np.pi/180*Kp)
		PIDx = constrain(PIDx)
		PIDy = maxangle-((1000/error_y)*np.pi/180*Kp)
		PIDy = constrain(PIDy)
		prev_errx2 = error_x
		prev_erry2 = error_y
	"""
	"""
	"""
	#sim.simxPauseSimulation(client_id,sim.simx_opmode_oneshot)
	#if flag==9:
		#targets = [0,0,0,0]
		#print(targets)
		#control_servo(targets)
	if flag==1:
		#right
		if pos>0 and neg>0:
			targets = [np.abs([PIDx]),-np.abs([PIDx]),-np.abs([PIDx]),np.abs([PIDx])]
		else:
			targets = [0,0,-np.abs([PIDx]),np.abs([PIDx])]
		
		control_servo(targets)
	
	elif flag==2:
		#if setflag3==False:
		targets = [-np.abs([PIDx]),np.abs([PIDx]),0,0]
		control_servo(targets)
	
	elif flag==3:
		#if setflag3==False:
		if pos>0 and neg>0:
			targets = [np.abs([PIDy]),np.abs([PIDy]),-np.abs([PIDy]),-np.abs([PIDy])]
		else:
			targets = [0,np.abs([PIDy]),-np.abs([PIDy]),0]
		control_servo(targets)
	elif flag==4:
		#if setflag3==True:
		if pos>0 and neg>0:
			targets = [-np.abs([PIDy]),-np.abs([PIDy]),np.abs([PIDy]),np.abs([PIDy])]
		else:
			targets = [-np.abs([PIDy]),0,0,np.abs([PIDy])]
		control_servo(targets)
		
	elif flag==5:
		if pos>0 and neg>0:
			targets = [np.abs([PIDx]),0,-np.abs([PIDx]),0]
		else:
			targets = [0,0,-np.abs([PIDx]),0]
		control_servo(targets)
	
	elif flag==6:
		targets = [0,np.abs([PIDx]),0,0]
		control_servo(targets)
		
	elif flag==7:
		targets = [0,-np.abs([PIDx]),0,0]
		control_servo(targets)
		
		#sim.simxPauseCommunication(client_id,True)
		
		
	elif flag==8:
		targets = [-np.abs([PIDx]),0,np.abs([PIDx]),0]
		print(targets)
		control_servo(targets)
	elif flag==9:
		targets = [0,0,0,0]
		print(targets)
		control_servo(targets)
	"""
	elif flag==9:
		targets = [-np.abs([PIDx2]),-np.abs([10*np.pi/180]),np.abs([PIDx2]),np.abs([10*np.pi/180])]
		control_servo(targets)
	elif flag==10:
		targets = [np.abs([10*np.pi/180]),np.abs([PIDx2]),-np.abs([10*np.pi/180]),-np.abs([PIDx2])]
		control_servo(targets)
	elif flag==11:
		targets = [np.abs([PIDx2]),np.abs([10*np.pi/180]),-np.abs([PIDx2]),-np.abs([10*np.pi/180])]
		control_servo(targets)
	elif flag==12:
		targets = [0,0,-np.abs([PIDx2]),0]
		control_servo(targets)
	elif flag==13:
		
		targets = [0,0,0,0]
		control_servo(targets)
	"""
		
	

##############################################################


def init_setup(rec_client_id):
	"""
	Purpose:
	---
	This function should:
	
	1. Get all the required handles from the CoppeliaSim scene and store them in global variables.
	2. Initialize the vision sensor in 'simx_opmode_streaming' operation mode (if required). 
	   Teams are allowed to choose the appropriate the oeration mode depending on their code and logic.

	Input Arguments:
	---
	`rec_client_id`		:  [ integer ]
		the client_id generated from start connection remote API in Task 2A, should be stored in a global variable
	
	Returns:
	---
	None
	
	Example call:
	---
	init_setup()
	
	"""
	global client_id, vision_sensor_handle,handle_arr,pitch_angle,roll_angle,add_angle,sub_angle,initial_error,prev_errx,prev_erry

	# since client_id is defined in task_2a.py file, it needs to be assigned here as well.
	client_id = rec_client_id

	##############	ADD YOUR CODE HERE	##############
	
	errorcode, vision_sensor_handle = sim.simxGetObjectHandle(client_id,"vision_sensor_1",sim.simx_opmode_oneshot_wait)
	return_code, image_resolution, vision_sensor_image = sim.simxGetVisionSensorImage(client_id,vision_sensor_handle,0,sim.simx_opmode_streaming) #getting vision sensor image in non-blocking function call
	errorcode, rev1 = sim.simxGetObjectHandle(client_id,"revolute_joint_ss_1",sim.simx_opmode_blocking)
	#sim.simxSynchronousTrigger(client_id)
	errorcode, rev2 = sim.simxGetObjectHandle(client_id,"revolute_joint_ss_2",sim.simx_opmode_blocking)
	#sim.simxSynchronousTrigger(client_id)
	errorcode, rev3 = sim.simxGetObjectHandle(client_id,"revolute_joint_ss_3",sim.simx_opmode_blocking)
	#sim.simxSynchronousTrigger(client_id)
	errorcode, rev4 = sim.simxGetObjectHandle(client_id,"revolute_joint_ss_4",sim.simx_opmode_blocking)
	#sim.simxSynchronousTrigger(client_id)
	handle_arr = [rev1,rev2,rev3,rev4]
	print(rev1,rev2,rev3,rev4)
	
	print("in init setup")
	print("client_id",client_id)
	pitch_angle=0
	roll_angle=0
	add_angle=0
	sub_angle=0
	initial_error=[0,0]
	prev_errx=0
	prev_erry=0
	
	
	##################################################


def control_logic(center_x,center_y):
	"""
	Purpose:
	---
	This function should implement the control logic to balance the ball at a particular setpoint on the table.

	The orientation of the top table should "ONLY" be controlled by the servo motor as we would expect in a 
	practical scenario.

	Hence "ONLY" the shaft of the servo motor or in other words the revolute joint between servo and servo fin 
	should have 'motor enabled' and 'control loop enabled option' checked. Refer documentation for further understanding of 
	these options.

	This function should use the necessary Legacy Python Remote APIs to control the revolute joints.

	NOTE: In real life, a 180 degree servo motor can rotate between -90 to +90 degrees or -1.57 to 1.57 radians only. 
		  Hence the command to be sent to servo motor should be between this range only. When the top plate is parallel to
		  base plate, the revolute joint between servo and servo fin should be at 0 degrees orientation. Refer documentation
		  for further understanding.

	NOTE: Since the simulation is dynamic in nature there should not by any bottlenecks in this code due to which the 
		  processing may take a lot of time. As a result 'control_logic' function should be called in every iteration of 
		  the while loop. Use global variables instead of reinitialising the varibles used in this function.
	
	Input Arguments:
	---
	`center_x`	:  [ int ]
		the x centroid of the ball
	
	`center_y`	:  [ int ]
		the y centroid of the ball
	
	Returns:
	---
	None
	
	Example call:
	---
	control_logic(center_x,center_y)
	
	"""
	global setpoint, client_id, initial_error,setflag,setflag2,setflag3
	##############	ADD YOUR CODE HERE	##############
	
	
	#posarray = [0,0,0,0]
	returnarray2 = [-1,-1,-1,-1]
	##---##
	##Initilialising streaming operations and getting joint properties
	#for i in range(4):
		#while returnarray2!=[0,0,0,0]:
	
	#_,posarray[0]=sim.simxGetJointPosition(client_id, handle_arr[0], sim.simx_opmode_streaming)
	#sim.simxSynchronousTrigger(client_id)
	#sim.simxSetJointTargetVelocity(client_id,handle_arr[0],360*np.pi/180,sim.simx_opmode_oneshot)
	#sim.simxSetJointMaxForce(client_id,handle_arr[0],10000,sim.simx_opmode_oneshot)
	
	#returnarray2[0]=sim.simxSetJointTargetPosition(client_id,handle_arr[0],0,sim.simx_opmode_oneshot)
	#_,posarray[1]=sim.simxGetJointPosition(client_id, handle_arr[1], sim.simx_opmode_streaming)
	#sim.simxSynchronousTrigger(client_id)
	#sim.simxSetJointTargetVelocity(client_id,handle_arr[0],360*np.pi/180,sim.simx_opmode_oneshot)
	#sim.simxSetJointMaxForce(client_id,handle_arr[0],10000,sim.simx_opmode_oneshot)
	
	#returnarray2[1]=sim.simxSetJointTargetPosition(client_id,handle_arr[1],0,sim.simx_opmode_oneshot)
	#_,posarray[2]=sim.simxGetJointPosition(client_id, handle_arr[2], sim.simx_opmode_streaming)
	##sim.simxSynchronousTrigger(client_id)
	#sim.simxSetJointTargetVelocity(client_id,handle_arr[0],360*np.pi/180,sim.simx_opmode_oneshot)
	#sim.simxSetJointMaxForce(client_id,handle_arr[0],10000,sim.simx_opmode_oneshot)
	
	#returnarray2[2]=sim.simxSetJointTargetPosition(client_id,handle_arr[2],0,sim.simx_opmode_oneshot)
	#_,posarray[3]=sim.simxGetJointPosition(client_id, handle_arr[3], sim.simx_opmode_streaming)
	#sim.simxSynchronousTrigger(client_id)
	#sim.simxSetJointTargetVelocity(client_id,handle_arr[0],360*np.pi/180,sim.simx_opmode_oneshot)
	#sim.simxSetJointMaxForce(client_id,handle_arr[0],10000,sim.simx_opmode_oneshot)
	
	#returnarray2[3]=sim.simxSetJointTargetPosition(client_id,handle_arr[3],0,sim.simx_opmode_oneshot)		
		#print(_,"pos code")
	
	print("out")
	#sim.simxGetPingTime(client_id)
	initial_error.append(center_x)
	initial_error.append(center_y)
	setflag=False
	setflag2=False
	setflag3=False
	perror_x=0
	perror_y=0
	control_angle(handle_arr,center_x,center_y)
	
	#print(sim.simxGetPingTime(client_id))
	#sim.simxSynchronousTrigger(client_id)
	#center_x, center_y = 
	

	##################################################


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:	change_setpoint
#		 Inputs:	list of new setpoint-
#						new_setpoint=[x_pixel,y_pixel]
#		Outputs:	None
#		Purpose:	The function updates the value of global "setpoint" list after every 15 seconds of simulation time.
#					This will be ONLY called by executable file. 
def change_setpoint(new_setpoint):

	global setpoint
	setpoint=new_setpoint[:]


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:	main
#		 Inputs:	None
#		Outputs:	None
#		Purpose:	This part of the code is only for testing your solution. The function does the following:
#						- imports 'task_1b' file as module
#						- imports 'task_1a_part1' file as module
#						- imports 'task_2a' file as module
#						- calls init_remote_api_server() function in 'task_2a' to connect with CoppeliaSim Remote API server
#						- then calls start_simulation() function in 'task_2a' to start the simulation
#						- then calls init_setup() function to store the required handles in respective global variables and complete initializations if required
#						- then calls get_vision_sensor_image() function in 'task_2a' to capture an image from the Vision Sensor in CoppeliaSim scene
#						- If the return code is 'simx_return_ok':
#									- then calls transform_vision_sensor_image() function in 'task_2a' to transform the captured image
#									  to a format compatible with OpenCV. 
#									- then the transformed image is given as input and Perspective Transform is applied
#									  by calling applyPerspectiveTransform function	from 'task_1b'
#									- then the output of warped_img is given to 'scan_image' function from 'task_1a_part1'
#						- then calls control_logic() function to command the servo motors

# NOTE: Write your solution ONLY in the space provided in the above functions. Main function should not be edited.

if __name__ == "__main__":

	# Import 'task_1b.py' file as module
	try:
		import task_1b

	except ImportError:
		print('\n[ERROR] task_1b.py file is not present in the current directory.')
		print('Your current directory is: ', os.getcwd())
		print('Make sure task_1b.py is present in this current directory.\n')
		sys.exit()
		
	except Exception as e:
		print('Your task_1b.py throwed an Exception. Kindly debug your code!\n')
		traceback.print_exc(file=sys.stdout)
		sys.exit()
	
	# Import 'task_1a_part1.py' file as module
	try:
		import task_1a_part1

	except ImportError:
		print('\n[ERROR] task_1a_part1.py file is not present in the current directory.')
		print('Your current directory is: ', os.getcwd())
		print('Make sure task_1a_part1.py is present in this current directory.\n')
		sys.exit()
		
	except Exception as e:
		print('Your task_1a_part1.py throwed an Exception. Kindly debug your code!\n')
		traceback.print_exc(file=sys.stdout)
		sys.exit()
	
	# Import 'task_2a.py' file as module
	try:
		import task_2a

	except ImportError:
		print('\n[ERROR] task_2a.py file is not present in the current directory.')
		print('Your current directory is: ', os.getcwd())
		print('Make sure task_2a.py is present in this current directory.\n')
		sys.exit()
		
	except Exception as e:
		print('Your task_2a.py throwed an Exception. Kindly debug your code!\n')
		traceback.print_exc(file=sys.stdout)
		sys.exit()

	# Initiate the Remote API connection with CoppeliaSim server
	print('\nConnection to CoppeliaSim Remote API Server initiated.')
	print('Trying to connect to Remote API Server...')

	try:
		client_id = task_2a.init_remote_api_server()

		if (client_id != -1):
			print('\nConnected successfully to Remote API Server in CoppeliaSim!')

			# Starting the Simulation
			try:
				return_code = task_2a.start_simulation()
				

				if (return_code == sim.simx_return_novalue_flag):
					print('\nSimulation started correctly in CoppeliaSim.')
					
					# Storing the required handles in respective global variables.
					try:
						init_setup(client_id)
					except Exception:
						print('\n[ERROR] Your init_setup() function throwed an Exception. Kindly debug your code!')
						print('Stop the CoppeliaSim simulation manually if started.\n')
						traceback.print_exc(file=sys.stdout)
						print()
						sys.exit()

				else:
					print('\n[ERROR] Failed starting the simulation in CoppeliaSim!')
					print('start_simulation function in task_2a.py is not configured correctly, check the code!')
					print()
					sys.exit()

			except Exception:
				print('\n[ERROR] Your start_simulation function in task_2a.py throwed an Exception. Kindly debug your code!')
				print('Stop the CoppeliaSim simulation manually.\n')
				traceback.print_exc(file=sys.stdout)
				print()
				sys.exit()
		
		else:
			print('\n[ERROR] Failed connecting to Remote API server!')
			print('[WARNING] Make sure the CoppeliaSim software is running and')
			print('[WARNING] Make sure the Port number for Remote API Server is set to 19997.')
			print('[ERROR] OR init_remote_api_server function in task_2a.py is not configured correctly, check the code!')
			print()
			sys.exit()

	except Exception:
		print('\n[ERROR] Your init_remote_api_server function in task_2a.py throwed an Exception. Kindly debug your code!')
		print('Stop the CoppeliaSim simulation manually if started.\n')
		traceback.print_exc(file=sys.stdout)
		print()
		sys.exit()
	
	# Initialising the center_x and center_y variable to the current position of the ball
	center_x = 1063
	center_y = 1063
	
	init_simulation_time = 0
	curr_simulation_time = 0

	# Storing time when the simulation started in variable init_simulation_time
	return_code_signal,init_simulation_time_string=sim.simxGetStringSignal(client_id,'time',sim.simx_opmode_streaming)

	if(return_code_signal==0):
		init_simulation_time=float(init_simulation_time_string)

	# Running the coppeliasim simulation for 15 seconds
	while(curr_simulation_time - init_simulation_time <=15):
		
		return_code_signal,curr_simulation_time_string=sim.simxGetStringSignal(client_id,'time',sim.simx_opmode_buffer)
		
		if(return_code_signal == 0):
			curr_simulation_time=float(curr_simulation_time_string)
		
		try:
			vision_sensor_image, image_resolution, return_code = task_2a.get_vision_sensor_image(vision_sensor_handle)
			#print(sim.simxGetPingTime(client_id),"time for 2agv")

			if ((return_code == sim.simx_return_ok) and (len(image_resolution) == 2) and (len(vision_sensor_image) > 0)):
				# print('\nImage captured from Vision Sensor in CoppeliaSim successfully!')

				# Get the transformed vision sensor image captured in correct format
				try:
					transformed_image = task_2a.transform_vision_sensor_image(vision_sensor_image, image_resolution)
					#print(sim.simxGetPingTime(client_id),"time for 2ati")

					if (type(transformed_image) is np.ndarray):

						#plt.imshow(transformed_image,cmap="gray")
						
						#plt.show()

						# Get the resultant warped transformed vision sensor image after applying Perspective Transform
						try:
							warped_img = task_1b.applyPerspectiveTransform(transformed_image)
							#print(sim.simxGetPingTime(client_id),"time for 1b")
							if (type(warped_img) is np.ndarray):
								
								# Get the 'shapes' dictionary by passing the 'warped_img' to scan_image function
								try:
									shapes = task_1a_part1.scan_image(warped_img)
									#print(sim.simxGetPingTime(client_id),"time for 1a")

									if (type(shapes) is dict and shapes!={}):
										print('\nShapes detected by Vision Sensor are: ')
										print(shapes)
										
										# Storing the detected x and y centroid in center_x and center_y variable repectively
										center_x = shapes['Circle'][1]
										center_y = shapes['Circle'][2]

									elif(type(shapes) is not dict):
										print('\n[ERROR] scan_image function returned a ' + str(type(shapes)) + ' instead of a dictionary.')
										print('Stop the CoppeliaSim simulation manually.')
										print()
										sys.exit()
								
								except Exception:
									print('\n[ERROR] Your scan_image function in task_1a_part1.py throwed an Exception. Kindly debug your code!')
									print('Stop the CoppeliaSim simulation manually.\n')
									traceback.print_exc(file=sys.stdout)
									print()
									sys.exit()
							
							else:
								print('\n[ERROR] applyPerspectiveTransform function is not configured correctly, check the code.')
								print('Stop the CoppeliaSim simulation manually.')
								print()
								sys.exit()
						
						except Exception:
							print('\n[ERROR] Your applyPerspectiveTransform function in task_1b.py throwed an Exception. Kindly debug your code!')
							print('Stop the CoppeliaSim simulation manually.\n')
							traceback.print_exc(file=sys.stdout)
							print()
							sys.exit()

					else:
						print('\n[ERROR] transform_vision_sensor_image function in task_2a.py is not configured correctly, check the code.')
						print('Stop the CoppeliaSim simulation manually.')
						print()
						sys.exit()

				except Exception:
					print('\n[ERROR] Your transform_vision_sensor_image function in task_2a.py throwed an Exception. Kindly debug your code!')
					print('Stop the CoppeliaSim simulation manually.\n')
					traceback.print_exc(file=sys.stdout)
					print()
					sys.exit()
			
			try:
				control_logic(center_x,center_y)
			
			except:
				print('\n[ERROR] Your control_logic function throwed an Exception. Kindly debug your code!')
				print('Stop the CoppeliaSim simulation manually.\n')
				traceback.print_exc(file=sys.stdout)
				print()
				sys.exit()

		except Exception:
			print('\n[ERROR] Your get_vision_sensor_image function in task_2a.py throwed an Exception. Kindly debug your code!')
			print('Stop the CoppeliaSim simulation manually.\n')
			traceback.print_exc(file=sys.stdout)
			print()
			sys.exit()

	# Ending the Simulation
	try:
		return_code = task_2a.stop_simulation()
		
		if (return_code == sim.simx_return_novalue_flag):
			print('\nSimulation stopped correctly.')

			# Stop the Remote API connection with CoppeliaSim server
			try:
				task_2a.exit_remote_api_server()

				if (task_2a.start_simulation() == sim.simx_return_initialize_error_flag):
					print('\nDisconnected successfully from Remote API Server in CoppeliaSim!')

				else:
					print('\n[ERROR] Failed disconnecting from Remote API server!')
					print('[ERROR] exit_remote_api_server function in task_2a.py is not configured correctly, check the code!')

			except Exception:
				print('\n[ERROR] Your exit_remote_api_server function in task_2a.py throwed an Exception. Kindly debug your code!')
				print('Stop the CoppeliaSim simulation manually.\n')
				traceback.print_exc(file=sys.stdout)
				print()
				sys.exit()
		
		else:
			print('\n[ERROR] Failed stopping the simulation in CoppeliaSim server!')
			print('[ERROR] stop_simulation function in task_2a.py is not configured correctly, check the code!')
			print('Stop the CoppeliaSim simulation manually.')
		
		print()
		sys.exit()

	except Exception:
		print('\n[ERROR] Your stop_simulation function in task_2a.py throwed an Exception. Kindly debug your code!')
		print('Stop the CoppeliaSim simulation manually.\n')
		traceback.print_exc(file=sys.stdout)
		print()
		sys.exit()