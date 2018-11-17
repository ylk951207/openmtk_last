#coding: utf-8

import os, sys
from time import sleep
from multiprocessing import Process, Queue
from led import gpioOutSet

ON ='0'
OFF='1'


WIFI24='16'
WIFI50='17'
RRESET='19'
SYSTEM='81'

LED_LIST=[WIFI24, WIFI50, RRESET, SYSTEM]


def blink(led, frequency):
	gpioOutSet(led, OFF)
	sleep(1.00/(2.0*frequency))
	gpioOutSet(led, ON)
	sleep(1.00/(2.0*frequency))

def infinite_blink(led_list, frequency):
	while True:
		for led in led_list:
			blink(led, frequency)

if __name__ == '__main__':
	Process.daemon=True
    led_blink = Process(target=infinite_blink, args=(LED_LIST, 1))
    led_blink.start()
    led_blink.join()
    

