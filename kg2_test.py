"""
File to test the different functions and commands to control the Kinova Gen 2 robotic arm
"""

"""
Note that the API folder (/JACO-SDK/API/x64) must be added to the path environment in Windows
"""

from ctypes import *
import time
import numpy as np

# j2_cmd_layer_api_path = "C:/Program Files (x86)/JACO-SDK/API/x64/CommandLayerWindows.dll"
# j2_comm_layer_api_path = "C:/Program Files (x86)/JACO-SDK/API/x64/CommunicationLayerWindows.dll"

MAX_KINOVA_DEVICE = 20
# SERIAL_LENGTH = 20

# Define joint starting points
j1_init = 90.0  # degrees # THIS IS 90 DEGREES DIFFERENT FROM VORTEX as we placed box at a different angle in Vortex than how robot can be clamped on table
j2_init = 184.0  # degrees
j3_init = 0.0  # degrees
j4_init = 270.0  # degrees
j5_init = 0.0  # degrees
j6_init = 180.0  # degrees
j7_init = 0.0  # degrees
j_init = np.array([j1_init, j2_init, j3_init, j4_init, j5_init, j6_init, j7_init])


# Load dll
dll = CDLL(j2_cmd_layer_api_path)

# Define function's output type
dll.InitAPI.restype = c_int
dll.CloseAPI.restype = c_int

dll.GetDevices.restype = c_int
dll.GetAngularPosition.restype = c_int
dll.GetAngularVelocity.restype = c_int
dll.GetAngularCommand.restype = c_int
dll.GetAngularForce.restype = c_int
dll.GetAngularCurrent.restype = c_int
dll.GetCartesianForce.restype = c_int

dll.SendBasicTrajectory.restype = c_int

# You need to specify the argument types for the function
dll.GetDevices.argtypes = [POINTER(KinovaDevice), POINTER(c_int)]
dll.GetAngularPosition.argtypes = [POINTER(AngularPosition)]
dll.GetAngularVelocity.argtypes = [POINTER(AngularPosition)]
dll.GetAngularCommand.argtypes = [POINTER(AngularPosition)]
dll.GetAngularForce.argtypes = [POINTER(AngularPosition)]
dll.GetAngularCurrent.argtypes = [POINTER(AngularPosition)]
dll.GetCartesianForce.argtypes = [POINTER(CartesianPosition)]

dll.SendBasicTrajectory.argtypes = [POINTER(TrajectoryPoint)]

# Call API initialization function
# This function initializes the API. It is the first function you call if you want the rest of the library.
init_result = dll.InitAPI()
print("Initialization's result: " + str(init_result))

# Call API GetDevices
# This function returns a list of devices accessible by this API.
devices = (KinovaDevice * MAX_KINOVA_DEVICE)()
devicesCount = dll.GetDevices(devices, c_int(init_result))
print("Number of connected devices: " + str(devicesCount))

# Call API GetAngularPosition
# This function returns the angular position of the robotical arm's end effector. Units are in degrees.
dataAngularPos = (AngularPosition)()
resultAngPos = dll.GetAngularPosition(dataAngularPos)
print(
    "Angular Position of Joint 6: "
    + str(dataAngularPos.Actuators.Actuator6)
    + " degrees."
)

# Call API GetAngularVelocity
# This function gets the velocity of each actuator. Units are degrees / second.
dataAngularVel = (AngularPosition)()
resultAngVel = dll.GetAngularVelocity(dataAngularVel)
print(
    "Angular Velocity of Joint 7: "
    + str(dataAngularVel.Actuators.Actuator7)
    + " degrees/second."
)

# Call API GetAngularCommand
# This function gets the angular command of all actuators. Units are degrees.
dataAngularCom = (AngularPosition)()
resultAngCom = dll.GetAngularCommand(dataAngularCom)
print(
    "Angular Command of Joint 7: "
    + str(dataAngularCom.Actuators.Actuator7)
    + " degrees."
)

# Call API GetAngularForce
# This function returns the torque of each actuator. Unit is Newton meter [N * m].
dataAngularFor = (AngularPosition)()
resultAngFor = dll.GetAngularForce(dataAngularFor)
print("Angular Force of Joint 7: " + str(dataAngularFor.Actuators.Actuator7) + " N*m.")

# Call API GetCartesianForce
# This function returns the cartesian force at the robotical arm's end effector. The translation unit is in Newtons and the orientation unit is Newton meters [N * m].
dataCartesianFor = (CartesianPosition)()
resultCartFor = dll.GetCartesianForce(dataCartesianFor)
print("Cartesian Force in X-direction: " + str(dataCartesianFor.Coordinates.X) + " N.")
print(
    "Cartesian Torque along X-axis: "
    + str(dataCartesianFor.Coordinates.ThetaX)
    + " N*m."
)

# Call API GetAngularCurrent
# This function returns the current that each actuator consumes on the main power supply. Unit is Amperes.
dataAngularCur = (AngularPosition)()
resultAngCur = dll.GetAngularCurrent(dataAngularCur)
print("Current of Joint 7: " + str(dataAngularCur.Actuators.Actuator7) + " Amperes.")

# Call API SendBasicTrajectory (using our own defined functions for efficiency)
# This function sends a trajectory point (WITHOUT limitation) that will be added in the robotical arm's FIFO.
# x = 10.0 # angular velocity for a given joint
# n = 200 # number of steps to maintain a given velocity
# phase1 = defCommandAngVel([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, x]) # all joints are 0.0, except joint 7, which has velocity x degrees/second
# sendCommand(phase1, n, 0.009, 1) # sending phase1 command for n steps, every 5ms

# Test bringing joints to starting point. Make it a function where you can just say what joint position you want WITH a velocity?

startPoint(0.005)

# Bring End-effector downwards.

# Call API close function
# This function must called when your application stops using the API. It closes the USB link and the library properly.
close_result = dll.CloseAPI()
print("Closing's result: " + str(close_result))
