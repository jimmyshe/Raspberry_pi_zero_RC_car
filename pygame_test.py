import pygame
from pygame.locals import QUIT ,JOYAXISMOTION ,JOYBUTTONDOWN ,JOYBUTTONUP
from sys import exit
import socket
import struct
UDP_IP = "192.168.2.33"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP



pygame.init()
SCREEN_SIZE = (50, 50)
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)

font = pygame.font.SysFont("arial", 16)
font_height = font.get_linesize()
event_text = []

pygame.joystick.init()

print(pygame.joystick.get_count())

_joystick = pygame.joystick.Joystick(0)
_joystick.init()

def map(x, in_min, in_max, out_min, out_max):
    if x>= in_max:
        return out_max
    if x<=in_min:
        return out_min
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

direction = 375
gas = 0
in1 = 0
in2 = 0
standby = 0
while True:

    # 获得事件的名称
    event = pygame.event.wait()
    print(event)
    if event.type == QUIT:
        exit()

    if event.type == JOYAXISMOTION:
        if event.dict['axis'] == 0:
            w = event.dict['value']
            direction = int(map(w,-0.2,0.2,450,320))

        if event.dict['axis'] == 2:
            g =event.dict['value']
            gas =int(map(g,-1,1,1024,0))

    if event.type == JOYBUTTONDOWN:
        if event.dict['button'] == 14:
            in2 = 0
            in1 = 4095
            standby = 4095
        if event.dict['button'] == 8:
            in2 = 4095
            in1 = 0
            standby = 4095

    if event.type == JOYBUTTONUP:
        if event.dict['button'] == 14 or event.dict['button'] == 8:
            in1 = 0
            in2 = 0
            standby = 0


    data_frame = struct.pack("5i",direction,gas,in1,in2,standby)
    print([direction,gas,in2,in1,standby])
    sock.sendto(data_frame, (UDP_IP, UDP_PORT))

