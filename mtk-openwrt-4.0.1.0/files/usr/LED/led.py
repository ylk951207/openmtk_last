import os, sys
from time import sleep

GPIO_FILE="/sys/devices/platform/10005000.pinctrl/mt_gpio"

WIFI24='16'
WIFI50='17'
RRESET='19'
SYSTEM='81'

LED_LIST=[WIFI24, WIFI50, RRESET, SYSTEM]


def gpioModeSet(gpio, mode):
	commandStrings='echo mode ' + gpio + ' ' + mode + ' > ' + GPIO_FILE
	os.system(commandStrings)

def gpioDirectionSet(gpio, direct):
	commandStrings='echo dir ' + gpio + ' ' + direct + ' > ' + GPIO_FILE
	os.system(commandStrings)

def gpioOutSet(gpio, out):
	commandStrings='echo out ' + gpio + ' ' + out + ' > ' + GPIO_FILE
	os.system(commandStrings)

if __name__ == '__main__':
	
	for gpio in LED_LIST:
		gpioModeSet(gpio, '1')
		gpioDirectionSet(gpio, '1')

	for loop in range(10):
		gpioOutSet(WIFI24, '1')
		gpioOutSet(WIFI50, '1')
		gpioOutSet(SYSTEM, '1')
		sleep(1)
		gpioOutSet(WIFI24, '0')
		gpioOutSet(WIFI50, '0')
		gpioOutSet(SYSTEM, '0')
		sleep(1)

