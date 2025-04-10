
import time
import serial
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

ser = serial.Serial('/dev/ttyUSB0', 115200)

def Pick_up(turn):
    gcode = ["G0 Z8r\n", "G0 Z11.7\r\n", "G0 Z15.4\r\n", "G0 Z19.1\r\n", "G0 Z22.8\r\n"]
    ser.write(gcode[turn].encode())
    GPIO.output(12, GPIO.HIGH)
    time.sleep(5)
    ser.write(up.encode())
    #time.sleep(5)
    
def Drop():
    time.sleep(3)
    ser.write(down.encode())
    time.sleep(7)
    GPIO.output(12, GPIO.LOW)
    time.sleep(1)
    ser.write(up.encode())
    #time.sleep(5)

init_gcode ='''
G21
G90
G28\r\n
'''

up = '''
G0 Z40\r\n
'''

down = '''
G0 Z5\r\n
'''

Goto_triangle = '''
G0 Z40
G0 X175 Y141\r\n
'''

Goto_circle = '''
G0 Z40
G0 X175 Y75\r\n
'''

O1_gcode ='''
G0 X12 Y209\r\n
'''

O2_gcode ='''
G1 X67 Y209\r\n
'''

O3_gcode ='''
G1 X122 Y209\r\n
'''

O4_gcode ='''
G1 X12 Y143\r\n
'''

O5_gcode ='''
G1 X67 Y143\r\n
'''

O6_gcode ='''
G1 X122 Y143\r\n
'''

O7_gcode ='''
G1 X12 Y77\r\n
'''

O8_gcode ='''
G1 X67 Y77\r\n
'''

O9_gcode ='''
G1 X122 Y77\r\n
'''

h_turn ='''
G0 X220 Y220 Z40\r\n
'''
camera ='''
G0 Y157\r\n
'''

position = {1:O1_gcode, 2:O2_gcode, 3:O3_gcode, 4:O4_gcode, 5:O5_gcode, 6:O6_gcode, 7:O7_gcode, 8:O8_gcode, 9:O9_gcode}

def Pick_up1(move_o):
    ser.write(position[move_o].encode())
    time.sleep(5)
    ser.write(down.encode())
    time.sleep(5)
    GPIO.output(12, GPIO.HIGH)
    time.sleep(5)
    ser.write(up.encode())
    #time.sleep(5)
