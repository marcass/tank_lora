EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L ATmega32U4 U?
U 1 1 59477692
P 3200 3850
F 0 "U?" H 2300 5550 50  0000 C CNN
F 1 "ATmega32U4" H 2550 2300 50  0000 C CNN
F 2 "" H 4400 4950 50  0000 C CNN
F 3 "" H 4400 4950 50  0000 C CNN
	1    3200 3850
	1    0    0    -1  
$EndComp
$Comp
L TPL5010 U?
U 1 1 59477875
P 7100 2450
F 0 "U?" H 6950 2150 50  0000 C CNN
F 1 "TPL5010" H 7100 2750 50  0000 C CNN
F 2 "TO_SOT_Packages_SMD:SOT-23-6" H 7100 2050 50  0001 C CNN
F 3 "" H 7100 2500 50  0000 C CNN
	1    7100 2450
	1    0    0    -1  
$EndComp
Wire Wire Line
	5850 2250 6800 2250
Wire Wire Line
	1700 1850 1700 2400
Wire Wire Line
	1700 2400 1950 2400
Wire Wire Line
	7700 3050 7700 2650
Wire Wire Line
	7700 2650 7400 2650
Wire Wire Line
	6800 2650 6800 2800
$Comp
L GND #PWR?
U 1 1 59477A51
P 6800 2800
F 0 "#PWR?" H 6800 2550 50  0001 C CNN
F 1 "GND" H 6800 2650 50  0000 C CNN
F 2 "" H 6800 2800 50  0000 C CNN
F 3 "" H 6800 2800 50  0000 C CNN
	1    6800 2800
	1    0    0    -1  
$EndComp
Text GLabel 1700 3700 0    60   Input ~ 0
Reset
Text GLabel 8000 2350 2    60   Input ~ 0
Reset
Wire Wire Line
	8000 2350 7400 2350
Wire Wire Line
	1950 3700 1700 3700
Wire Wire Line
	7400 2250 7650 2250
Wire Wire Line
	7650 2250 7650 1700
Text GLabel 7650 1500 1    60   Input ~ 0
PreboostV
$Comp
L R R1
U 1 1 59477B2B
P 8150 2850
F 0 "R1" V 8230 2850 50  0000 C CNN
F 1 "124.91" V 8150 2850 50  0000 C CNN
F 2 "" V 8080 2850 50  0000 C CNN
F 3 "" H 8150 2850 50  0000 C CNN
	1    8150 2850
	1    0    0    -1  
$EndComp
Wire Wire Line
	7400 2550 8150 2550
Wire Wire Line
	8150 2550 8150 2700
$Comp
L GND #PWR?
U 1 1 59477BBD
P 8150 3000
F 0 "#PWR?" H 8150 2750 50  0001 C CNN
F 1 "GND" H 8150 2850 50  0000 C CNN
F 2 "" H 8150 3000 50  0000 C CNN
F 3 "" H 8150 3000 50  0000 C CNN
	1    8150 3000
	1    0    0    -1  
$EndComp
Wire Wire Line
	5850 2250 5850 2600
Wire Wire Line
	5850 2600 4400 2600
Wire Wire Line
	7700 3050 5100 3050
Wire Wire Line
	5100 3050 5100 2700
Wire Wire Line
	5100 2700 4400 2700
$Comp
L Jumper_NO_Small JP?
U 1 1 594784A0
P 7650 1600
F 0 "JP?" H 7650 1680 50  0000 C CNN
F 1 "Jumper_NO_Small" H 7660 1540 50  0000 C CNN
F 2 "" H 7650 1600 50  0000 C CNN
F 3 "" H 7650 1600 50  0000 C CNN
	1    7650 1600
	0    1    1    0   
$EndComp
$EndSCHEMATC
