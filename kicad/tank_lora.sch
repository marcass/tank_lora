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
LIBS:LoRa32u4
LIBS:JSN-SR40T
LIBS:Boost_mod
LIBS:MCP112-300
LIBS:FDC6331L
LIBS:tank_lora-cache
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
Text GLabel 1750 3100 0    60   Input ~ 0
Reset
Text GLabel 8850 2350 2    60   Input ~ 0
Reset
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
$Comp
L R R2
U 1 1 5948516D
P 8150 1800
F 0 "R2" V 8230 1800 50  0000 C CNN
F 1 "100k" V 8150 1800 50  0000 C CNN
F 2 "" V 8080 1800 50  0000 C CNN
F 3 "" H 8150 1800 50  0000 C CNN
	1    8150 1800
	1    0    0    -1  
$EndComp
Text Label 8300 2850 0    60   ~ 0
1hour
$Comp
L +3.3V #PWR?
U 1 1 59489424
P 7650 1250
F 0 "#PWR?" H 7650 1100 50  0001 C CNN
F 1 "+3.3V" H 7650 1390 50  0000 C CNN
F 2 "" H 7650 1250 50  0000 C CNN
F 3 "" H 7650 1250 50  0000 C CNN
	1    7650 1250
	1    0    0    -1  
$EndComp
$Comp
L +3.3V #PWR?
U 1 1 59489445
P 8150 1250
F 0 "#PWR?" H 8150 1100 50  0001 C CNN
F 1 "+3.3V" H 8150 1390 50  0000 C CNN
F 2 "" H 8150 1250 50  0000 C CNN
F 3 "" H 8150 1250 50  0000 C CNN
	1    8150 1250
	1    0    0    -1  
$EndComp
Text GLabel 4100 3700 2    60   Input ~ 0
Load
Text GLabel 5100 1150 2    60   Input ~ 0
Load
$Comp
L GND #PWR?
U 1 1 59489A99
P 5250 1550
F 0 "#PWR?" H 5250 1300 50  0001 C CNN
F 1 "GND" H 5250 1400 50  0000 C CNN
F 2 "" H 5250 1550 50  0000 C CNN
F 3 "" H 5250 1550 50  0000 C CNN
	1    5250 1550
	1    0    0    -1  
$EndComp
$Comp
L SolarCharger U?
U 1 1 59489C66
P 4450 1350
F 0 "U?" H 4300 1050 50  0000 C CNN
F 1 "SolarCharger" H 4450 1650 50  0000 C CNN
F 2 "TO_SOT_Packages_SMD:SOT-23-6" H 4450 950 50  0001 C CNN
F 3 "" H 4450 1400 50  0000 C CNN
	1    4450 1350
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X02 P?
U 1 1 59489CBB
P 3250 1200
F 0 "P?" H 3250 1350 50  0000 C CNN
F 1 "CONN_01X02" V 3350 1200 50  0000 C CNN
F 2 "" H 3250 1200 50  0000 C CNN
F 3 "" H 3250 1200 50  0000 C CNN
	1    3250 1200
	-1   0    0    1   
$EndComp
$Comp
L CONN_01X02 P?
U 1 1 59489D86
P 4500 1900
F 0 "P?" H 4500 2050 50  0000 C CNN
F 1 "CONN_01X02" V 4600 1900 50  0000 C CNN
F 2 "" H 4500 1900 50  0000 C CNN
F 3 "" H 4500 1900 50  0000 C CNN
	1    4500 1900
	-1   0    0    1   
$EndComp
$Comp
L LoRa32u4 U?
U 1 1 595AE2C2
P 2850 3850
F 0 "U?" H 2850 3750 50  0000 C CNN
F 1 "LoRa32u4" H 2850 3950 50  0000 C CNN
F 2 "MODULE" H 2850 3850 50  0001 C CNN
F 3 "DOCUMENTATION" H 2850 3850 50  0001 C CNN
	1    2850 3850
	1    0    0    -1  
$EndComp
Text GLabel 6500 2250 0    60   Input ~ 0
WAKE
Text GLabel 4200 4600 2    60   Input ~ 0
WAKE
Text GLabel 7550 2650 2    60   Input ~ 0
DONE
Text GLabel 4200 4100 2    60   Input ~ 0
DONE
$Comp
L +3.3V #PWR?
U 1 1 595B5B93
P 1100 3000
F 0 "#PWR?" H 1100 2850 50  0001 C CNN
F 1 "+3.3V" H 1100 3140 50  0000 C CNN
F 2 "" H 1100 3000 50  0000 C CNN
F 3 "" H 1100 3000 50  0000 C CNN
	1    1100 3000
	1    0    0    -1  
$EndComp
Text GLabel 3950 4000 2    60   Input ~ 0
TRIGGER
Text GLabel 4200 3900 2    60   Input ~ 0
ECHO
$Comp
L JSN-SR40T S?
U 1 1 595B5C99
P 2200 1350
F 0 "S?" H 2200 1250 50  0000 C CNN
F 1 "JSN-SR40T" H 2200 1450 50  0000 C CNN
F 2 "MODULE" H 2200 1350 50  0001 C CNN
F 3 "DOCUMENTATION" H 2200 1350 50  0001 C CNN
F 4 "Ultrasonic measuring device" H 2200 1350 50  0001 C CNN "Type"
	1    2200 1350
	1    0    0    -1  
$EndComp
Text GLabel 1250 1300 0    60   Input ~ 0
TRIGGER
Text GLabel 1200 1400 0    60   Input ~ 0
ECHO
$Comp
L GND #PWR?
U 1 1 595B5D48
P 1250 1850
F 0 "#PWR?" H 1250 1600 50  0001 C CNN
F 1 "GND" H 1250 1700 50  0000 C CNN
F 2 "" H 1250 1850 50  0000 C CNN
F 3 "" H 1250 1850 50  0000 C CNN
	1    1250 1850
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR?
U 1 1 595B5D67
P 1250 900
F 0 "#PWR?" H 1250 750 50  0001 C CNN
F 1 "+5V" H 1250 1040 50  0000 C CNN
F 2 "" H 1250 900 50  0000 C CNN
F 3 "" H 1250 900 50  0000 C CNN
	1    1250 900 
	1    0    0    -1  
$EndComp
$Comp
L Boost_mod U?
U 1 1 595B5EBC
P 6900 4000
F 0 "U?" H 6900 3900 50  0000 C CNN
F 1 "Boost_mod" H 6900 4100 50  0000 C CNN
F 2 "MODULE" H 6900 4000 50  0001 C CNN
F 3 "DOCUMENTATION" H 6900 4000 50  0001 C CNN
	1    6900 4000
	1    0    0    -1  
$EndComp
$Comp
L +3.3V #PWR?
U 1 1 595B60B2
P 5950 3050
F 0 "#PWR?" H 5950 2900 50  0001 C CNN
F 1 "+3.3V" H 5950 3190 50  0000 C CNN
F 2 "" H 5950 3050 50  0000 C CNN
F 3 "" H 5950 3050 50  0000 C CNN
	1    5950 3050
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 595B61A5
P 5600 5100
F 0 "#PWR?" H 5600 4850 50  0001 C CNN
F 1 "GND" H 5600 4950 50  0000 C CNN
F 2 "" H 5600 5100 50  0000 C CNN
F 3 "" H 5600 5100 50  0000 C CNN
	1    5600 5100
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 595B61D1
P 7800 4200
F 0 "#PWR?" H 7800 3950 50  0001 C CNN
F 1 "GND" H 7800 4050 50  0000 C CNN
F 2 "" H 7800 4200 50  0000 C CNN
F 3 "" H 7800 4200 50  0000 C CNN
	1    7800 4200
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 595B61FD
P 1000 4700
F 0 "#PWR?" H 1000 4450 50  0001 C CNN
F 1 "GND" H 1000 4550 50  0000 C CNN
F 2 "" H 1000 4700 50  0000 C CNN
F 3 "" H 1000 4700 50  0000 C CNN
	1    1000 4700
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR?
U 1 1 595B6297
P 7750 3650
F 0 "#PWR?" H 7750 3500 50  0001 C CNN
F 1 "+5V" H 7750 3790 50  0000 C CNN
F 2 "" H 7750 3650 50  0000 C CNN
F 3 "" H 7750 3650 50  0000 C CNN
	1    7750 3650
	1    0    0    -1  
$EndComp
$Comp
L Jumper_NC_Dual JP?
U 1 1 595B64BF
P 1550 4500
F 0 "JP?" H 1600 4400 50  0000 L CNN
F 1 "Jumper_NC_Dual" H 1550 4600 50  0000 C BNN
F 2 "" H 1550 4500 50  0000 C CNN
F 3 "" H 1550 4500 50  0000 C CNN
	1    1550 4500
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 595B660A
P 1550 4700
F 0 "#PWR?" H 1550 4450 50  0001 C CNN
F 1 "GND" H 1550 4550 50  0000 C CNN
F 2 "" H 1550 4700 50  0000 C CNN
F 3 "" H 1550 4700 50  0000 C CNN
	1    1550 4700
	1    0    0    -1  
$EndComp
$Comp
L Jumper_NC_Dual JP?
U 1 1 595B6858
P 7650 1750
F 0 "JP?" H 7700 1650 50  0000 L CNN
F 1 "Jumper_NC_Dual" H 7650 1850 50  0000 C BNN
F 2 "" H 7650 1750 50  0000 C CNN
F 3 "" H 7650 1750 50  0000 C CNN
	1    7650 1750
	0    1    1    0   
$EndComp
$Comp
L 2N7002 Q1
U 1 1 595DBAA6
P 5500 4250
F 0 "Q1" H 5700 4325 50  0000 L CNN
F 1 "2N7000" H 5700 4250 50  0000 L CNN
F 2 "TO_SOT_Packages_SMD:SOT-23" H 5700 4175 50  0001 L CIN
F 3 "" H 5500 4250 50  0000 L CNN
	1    5500 4250
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 595DBAFF
P 4700 5100
F 0 "#PWR?" H 4700 4850 50  0001 C CNN
F 1 "GND" H 4700 4950 50  0000 C CNN
F 2 "" H 4700 5100 50  0000 C CNN
F 3 "" H 4700 5100 50  0000 C CNN
	1    4700 5100
	1    0    0    -1  
$EndComp
$Comp
L R R4
U 1 1 595DBB24
P 4700 4750
F 0 "R4" V 4780 4750 50  0000 C CNN
F 1 "100k" V 4700 4750 50  0000 C CNN
F 2 "" V 4630 4750 50  0000 C CNN
F 3 "" H 4700 4750 50  0000 C CNN
	1    4700 4750
	1    0    0    -1  
$EndComp
$Comp
L R R5
U 1 1 595DBBF2
P 5150 4300
F 0 "R5" V 5230 4300 50  0000 C CNN
F 1 "10" V 5150 4300 50  0000 C CNN
F 2 "" V 5080 4300 50  0000 C CNN
F 3 "" H 5150 4300 50  0000 C CNN
	1    5150 4300
	0    1    1    0   
$EndComp
$Comp
L MCP112-300 U?
U 1 1 595FFD4F
P 1800 6450
F 0 "U?" H 1800 6350 50  0000 C CNN
F 1 "MCP112-300" H 1800 6550 50  0000 C CNN
F 2 "MODULE" H 1800 6450 50  0001 C CNN
F 3 "DOCUMENTATION" H 1800 6450 50  0001 C CNN
	1    1800 6450
	-1   0    0    1   
$EndComp
$Comp
L FDC6331L U?
U 1 1 595FFE22
P 4650 6400
F 0 "U?" H 4650 6300 50  0000 C CNN
F 1 "FDC6331L" H 4650 6500 50  0000 C CNN
F 2 "MODULE" H 4650 6400 50  0001 C CNN
F 3 "DOCUMENTATION" H 4650 6400 50  0001 C CNN
	1    4650 6400
	1    0    0    -1  
$EndComp
Text GLabel 5550 6500 2    60   Input ~ 0
VBAT_IN
Text GLabel 2950 5750 1    60   Input ~ 0
Load
Text GLabel 3900 6500 0    60   Input ~ 0
VBAT_OUT
$Comp
L GND #PWR?
U 1 1 5960060B
P 2850 6700
F 0 "#PWR?" H 2850 6450 50  0001 C CNN
F 1 "GND" H 2850 6550 50  0000 C CNN
F 2 "" H 2850 6700 50  0000 C CNN
F 3 "" H 2850 6700 50  0000 C CNN
	1    2850 6700
	1    0    0    -1  
$EndComp
$Comp
L R R6
U 1 1 59605E4D
P 5400 5900
F 0 "R6" V 5480 5900 50  0000 C CNN
F 1 "100k" V 5400 5900 50  0000 C CNN
F 2 "" V 5330 5900 50  0000 C CNN
F 3 "" H 5400 5900 50  0000 C CNN
	1    5400 5900
	1    0    0    -1  
$EndComp
Wire Wire Line
	6800 2650 6800 2800
Wire Wire Line
	2000 3100 1750 3100
Wire Wire Line
	7400 2250 7650 2250
Wire Wire Line
	7400 2550 8150 2550
Wire Wire Line
	8150 2550 8150 2700
Wire Wire Line
	7400 2350 8850 2350
Wire Wire Line
	8150 1950 8150 2350
Connection ~ 8150 2350
Wire Wire Line
	8150 1250 8150 1650
Wire Wire Line
	5250 1550 5250 1250
Wire Wire Line
	5250 1250 4750 1250
Wire Wire Line
	3450 1150 4150 1150
Wire Wire Line
	4150 1550 4150 1250
Wire Wire Line
	4150 1250 3450 1250
Wire Wire Line
	4750 1500 4750 1850
Wire Wire Line
	4750 1850 4700 1850
Wire Wire Line
	4950 1950 4700 1950
Wire Wire Line
	4200 4100 3700 4100
Wire Wire Line
	4200 4600 3700 4600
Wire Wire Line
	7400 2650 7550 2650
Wire Wire Line
	6800 2250 6500 2250
Wire Wire Line
	4750 1150 5100 1150
Wire Wire Line
	4100 3700 3700 3700
Wire Wire Line
	2000 3200 1100 3200
Wire Wire Line
	1100 3200 1100 3000
Wire Wire Line
	4200 3900 3700 3900
Wire Wire Line
	3950 4000 3700 4000
Wire Wire Line
	6150 3950 5950 3950
Wire Wire Line
	5950 3950 5950 3050
Wire Wire Line
	7800 4200 7800 4050
Wire Wire Line
	7800 4050 7650 4050
Wire Wire Line
	7750 3650 7750 3950
Wire Wire Line
	7750 3950 7650 3950
Wire Wire Line
	1000 3400 1000 4700
Wire Wire Line
	1000 3400 2000 3400
Wire Wire Line
	1450 1500 1250 1500
Wire Wire Line
	1250 1500 1250 1850
Wire Wire Line
	1450 1200 1250 1200
Wire Wire Line
	1250 1200 1250 900 
Wire Wire Line
	1250 1300 1450 1300
Wire Wire Line
	1200 1400 1450 1400
Wire Wire Line
	1800 4500 2000 4500
Wire Wire Line
	1550 4600 1550 4700
Wire Wire Line
	7650 2250 7650 2000
Wire Wire Line
	7650 1500 7650 1250
Wire Wire Line
	3700 4300 5000 4300
Wire Wire Line
	4700 4600 4700 4300
Connection ~ 4700 4300
Wire Wire Line
	4700 4900 4700 5100
Wire Wire Line
	5600 4450 5600 5100
Wire Wire Line
	5600 4050 6150 4050
Wire Wire Line
	2550 6350 2950 6350
Wire Wire Line
	2950 6350 2950 5750
Wire Wire Line
	2550 6550 2550 7150
Wire Wire Line
	3900 6400 3900 6500
Wire Wire Line
	2550 6450 2850 6450
Wire Wire Line
	2850 6450 2850 6700
Wire Wire Line
	5400 6050 5400 6300
Text GLabel 5400 5750 1    60   Input ~ 0
VBAT
Wire Wire Line
	2550 7150 6100 7150
Wire Wire Line
	6100 7150 6100 6400
Wire Wire Line
	6100 6400 5400 6400
Wire Wire Line
	5550 6500 5400 6500
$Comp
L GND #PWR?
U 1 1 59606172
P 3350 6650
F 0 "#PWR?" H 3350 6400 50  0001 C CNN
F 1 "GND" H 3350 6500 50  0000 C CNN
F 2 "" H 3350 6650 50  0000 C CNN
F 3 "" H 3350 6650 50  0000 C CNN
	1    3350 6650
	1    0    0    -1  
$EndComp
Wire Wire Line
	3350 6300 3350 6650
Text GLabel 4750 1400 2    60   Input ~ 0
VBAT_IN
Wire Wire Line
	3900 6300 3350 6300
Text GLabel 4950 1950 2    60   Input ~ 0
VBAT_OUT
$Comp
L CONN_01X08 P?
U 1 1 59606AFB
P 10300 3700
F 0 "P?" H 10300 4150 50  0000 C CNN
F 1 "CONN_01X08" V 10400 3700 50  0000 C CNN
F 2 "" H 10300 3700 50  0000 C CNN
F 3 "" H 10300 3700 50  0000 C CNN
	1    10300 3700
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 59606B5C
P 10000 4250
F 0 "#PWR?" H 10000 4000 50  0001 C CNN
F 1 "GND" H 10000 4100 50  0000 C CNN
F 2 "" H 10000 4250 50  0000 C CNN
F 3 "" H 10000 4250 50  0000 C CNN
	1    10000 4250
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR?
U 1 1 59606B9D
P 9300 3950
F 0 "#PWR?" H 9300 3800 50  0001 C CNN
F 1 "+5V" H 9300 4090 50  0000 C CNN
F 2 "" H 9300 3950 50  0000 C CNN
F 3 "" H 9300 3950 50  0000 C CNN
	1    9300 3950
	1    0    0    -1  
$EndComp
$Comp
L +3.3V #PWR?
U 1 1 59606BF0
P 9600 3850
F 0 "#PWR?" H 9600 3700 50  0001 C CNN
F 1 "+3.3V" H 9600 3990 50  0000 C CNN
F 2 "" H 9600 3850 50  0000 C CNN
F 3 "" H 9600 3850 50  0000 C CNN
	1    9600 3850
	1    0    0    -1  
$EndComp
Text GLabel 2000 3600 0    60   Input ~ 0
A1
Text GLabel 10100 3750 0    60   Input ~ 0
A1
Text GLabel 10100 3650 0    60   Input ~ 0
A2
Text GLabel 2000 3700 0    60   Input ~ 0
A2
Text GLabel 10100 3450 0    60   Input ~ 0
D3
Text GLabel 10100 3350 0    60   Input ~ 0
D5
Text GLabel 3700 4400 2    60   Input ~ 0
D5
Text GLabel 3700 4500 2    60   Input ~ 0
D3
Text GLabel 3700 4200 2    60   Input ~ 0
D9
Text GLabel 10100 3550 0    60   Input ~ 0
D9
Wire Wire Line
	10100 4050 10000 4050
Wire Wire Line
	10000 4050 10000 4250
Wire Wire Line
	10100 3950 9300 3950
Wire Wire Line
	10100 3850 9600 3850
$EndSCHEMATC
