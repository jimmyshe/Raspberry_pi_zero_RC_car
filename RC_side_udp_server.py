import struct
import socket
import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()


UDP_IP = "192.168.2.33"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

pwm.set_pwm_freq(60)

while True:
    data, addr = sock.recvfrom(4*5) 
    v = struct.unpack_from('5i',data)
    pwm.set_pwm(0, 0, v[0])
    pwm.set_pwm(4, 0, v[1])
    pwm.set_pwm(5, 0, v[2])
    pwm.set_pwm(6, 0, v[3])
    pwm.set_pwm(7, 0, v[4])

    #print ("received message:" + str(v))


