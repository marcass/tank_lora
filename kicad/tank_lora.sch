EESchema Schematic File Version 2
LIBS:tank_lora-rescue
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
L TPL5010 U3
U 1 1 59477875
P 7100 2450
F 0 "U3" H 6950 2150 50  0000 C CNN
F 1 "TPL5010" H 7100 2750 50  0000 C CNN
F 2 "TO_SOT_Packages_SMD:SOT-23-6_Handsoldering" H 7100 2050 50  0001 C CNN
F 3 "" H 7100 2500 50  0000 C CNN
	1    7100 2450
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR01
U 1 1 59477A51
P 6800 2800
F 0 "#PWR01" H 6800 2550 50  0001 C CNN
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
F 2 "Resistor_mw:Resistor_SMD+THTuniversal_0805to1206_RM10_HandSoldering" V 8080 2850 50  0001 C CNN
F 3 "" H 8150 2850 50  0000 C CNN
	1    8150 2850
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR02
U 1 1 59477BBD
P 8150 3000
F 0 "#PWR02" H 8150 2750 50  0001 C CNN
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
F 2 "Resistor_mw:Resistor_SMD+THTuniversal_0805to1206_RM10_HandSoldering" V 8080 1800 50  0001 C CNN
F 3 "" H 8150 1800 50  0000 C CNN
	1    8150 1800
	1    0    0    -1  
$EndComp
Text Label 8300 2850 0    60   ~ 0
1hour
$Comp
L +3.3V #PWR03
U 1 1 59489424
P 7650 1250
F 0 "#PWR03" H 7650 1100 50  0001 C CNN
F 1 "+3.3V" H 7650 1390 50  0000 C CNN
F 2 "" H 7650 1250 50  0000 C CNN
F 3 "" H 7650 1250 50  0000 C CNN
	1    7650 1250
	1    0    0    -1  
$EndComp
$Comp
L +3.3V #PWR04
U 1 1 59489445
P 8150 1250
F 0 "#PWR04" H 8150 1100 50  0001 C CNN
F 1 "+3.3V" H 8150 1390 50  0000 C CNN
F 2 "" H 8150 1250 50  0000 C CNN
F 3 "" H 8150 1250 50  0000 C CNN
	1    8150 1250
	1    0    0    -1  
$EndComp
Text GLabel 4100 3700 2    60   Input ~ 0
Load
Text GLabel 6800 900  2    60   Input ~ 0
Load
$Comp
L GND #PWR05
U 1 1 59489A99
P 6950 1300
F 0 "#PWR05" H 6950 1050 50  0001 C CNN
F 1 "GND" H 6950 1150 50  0000 C CNN
F 2 "" H 6950 1300 50  0000 C CNN
F 3 "" H 6950 1300 50  0000 C CNN
	1    6950 1300
	1    0    0    -1  
$EndComp
$Comp
L SolarCharger U1
U 1 1 59489C66
P 6150 1100
F 0 "U1" H 6000 800 50  0000 C CNN
F 1 "SolarCharger" H 6150 1400 50  0000 C CNN
F 2 "solar_charger:Solar_charger" H 6150 700 50  0001 C CNN
F 3 "" H 6150 1150 50  0000 C CNN
	1    6150 1100
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X02 P1
U 1 1 59489D86
P 6200 1650
F 0 "P1" H 6200 1800 50  0000 C CNN
F 1 "CONN_01X02" V 6300 1650 50  0000 C CNN
F 2 "Connectors_JST:JST_PH_B2B-PH-K_02x2.00mm_Straight" H 6200 1650 50  0001 C CNN
F 3 "" H 6200 1650 50  0000 C CNN
	1    6200 1650
	-1   0    0    1   
$EndComp
$Comp
L LoRa32u4 U2
U 1 1 595AE2C2
P 2850 3850
F 0 "U2" H 2850 3750 50  0000 C CNN
F 1 "LoRa32u4" H 2850 3950 50  0000 C CNN
F 2 "LoRa32u4:LoRa32u4" H 2850 3850 50  0001 C CNN
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
Text GLabel 4200 4200 2    60   Input ~ 0
DONE
$Comp
L +3.3V #PWR06
U 1 1 595B5B93
P 1100 3000
F 0 "#PWR06" H 1100 2850 50  0001 C CNN
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
L JSN-SR40T S1
U 1 1 595B5C99
P 2200 1350
F 0 "S1" H 2200 1250 50  0000 C CNN
F 1 "JSN-SR40T" H 2200 1450 50  0000 C CNN
F 2 "jsn--sr04t:JSN-SR04T" H 2200 1350 50  0001 C CNN
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
L GND #PWR07
U 1 1 595B5D48
P 1250 1850
F 0 "#PWR07" H 1250 1600 50  0001 C CNN
F 1 "GND" H 1250 1700 50  0000 C CNN
F 2 "" H 1250 1850 50  0000 C CNN
F 3 "" H 1250 1850 50  0000 C CNN
	1    1250 1850
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR08
U 1 1 595B5D67
P 1250 900
F 0 "#PWR08" H 1250 750 50  0001 C CNN
F 1 "+5V" H 1250 1040 50  0000 C CNN
F 2 "" H 1250 900 50  0000 C CNN
F 3 "" H 1250 900 50  0000 C CNN
	1    1250 900 
	1    0    0    -1  
$EndComp
$Comp
L Boost_mod U4
U 1 1 595B5EBC
P 6900 4000
F 0 "U4" H 6900 3900 50  0000 C CNN
F 1 "Boost_mod" H 6900 4100 50  0000 C CNN
F 2 "Boost_module:Boost_module" H 6900 4000 50  0001 C CNN
F 3 "DOCUMENTATION" H 6900 4000 50  0001 C CNN
	1    6900 4000
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR09
U 1 1 595B61A5
P 5600 5100
F 0 "#PWR09" H 5600 4850 50  0001 C CNN
F 1 "GND" H 5600 4950 50  0000 C CNN
F 2 "" H 5600 5100 50  0000 C CNN
F 3 "" H 5600 5100 50  0000 C CNN
	1    5600 5100
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR011
U 1 1 595B61FD
P 1000 4700
F 0 "#PWR011" H 1000 4450 50  0001 C CNN
F 1 "GND" H 1000 4550 50  0000 C CNN
F 2 "" H 1000 4700 50  0000 C CNN
F 3 "" H 1000 4700 50  0000 C CNN
	1    1000 4700
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR012
U 1 1 595B6297
P 7750 3650
F 0 "#PWR012" H 7750 3500 50  0001 C CNN
F 1 "+5V" H 7750 3790 50  0000 C CNN
F 2 "" H 7750 3650 50  0000 C CNN
F 3 "" H 7750 3650 50  0000 C CNN
	1    7750 3650
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR013
U 1 1 595DBAFF
P 4700 5300
F 0 "#PWR013" H 4700 5050 50  0001 C CNN
F 1 "GND" H 4700 5150 50  0000 C CNN
F 2 "" H 4700 5300 50  0000 C CNN
F 3 "" H 4700 5300 50  0000 C CNN
	1    4700 5300
	1    0    0    -1  
$EndComp
$Comp
L R R4
U 1 1 595DBB24
P 4700 4950
F 0 "R4" V 4780 4950 50  0000 C CNN
F 1 "100k" V 4700 4950 50  0000 C CNN
F 2 "Resistor_mw:Resistor_SMD+THTuniversal_0805to1206_RM10_HandSoldering" V 4630 4950 50  0001 C CNN
F 3 "" H 4700 4950 50  0000 C CNN
	1    4700 4950
	1    0    0    -1  
$EndComp
$Comp
L FDC6331L U5
U 1 1 595FFE22
P 4650 6400
F 0 "U5" H 4650 6300 50  0000 C CNN
F 1 "FDC6331L" H 4650 6500 50  0000 C CNN
F 2 "TO_SOT_Packages_SMD:TSOT-6-MK06A_Handsoldering" H 4650 6400 50  0001 C CNN
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
L GND #PWR014
U 1 1 5960060B
P 1000 6800
F 0 "#PWR014" H 1000 6550 50  0001 C CNN
F 1 "GND" H 1000 6650 50  0000 C CNN
F 2 "" H 1000 6800 50  0000 C CNN
F 3 "" H 1000 6800 50  0000 C CNN
	1    1000 6800
	1    0    0    -1  
$EndComp
$Comp
L R R3
U 1 1 59605E4D
P 5400 5900
F 0 "R3" V 5480 5900 50  0000 C CNN
F 1 "100k" V 5400 5900 50  0000 C CNN
F 2 "Resistor_mw:Resistor_SMD+THTuniversal_0805to1206_RM10_HandSoldering" V 5330 5900 50  0001 C CNN
F 3 "" H 5400 5900 50  0000 C CNN
	1    5400 5900
	1    0    0    -1  
$EndComp
Text GLabel 5400 5750 1    60   Input ~ 0
LOAD
$Comp
L GND #PWR015
U 1 1 59606172
P 3350 6650
F 0 "#PWR015" H 3350 6400 50  0001 C CNN
F 1 "GND" H 3350 6500 50  0000 C CNN
F 2 "" H 3350 6650 50  0000 C CNN
F 3 "" H 3350 6650 50  0000 C CNN
	1    3350 6650
	1    0    0    -1  
$EndComp
Text GLabel 6450 1150 2    60   Input ~ 0
VBAT_IN
Text GLabel 6650 1700 2    60   Input ~ 0
VBAT_OUT
$Comp
L CONN_01X08 P2
U 1 1 59606AFB
P 10300 3700
F 0 "P2" H 10300 4150 50  0000 C CNN
F 1 "CONN_01X08" V 10400 3700 50  0000 C CNN
F 2 "Connectors_Phoenix:PhoenixContact_MCV-G_08x5.08mm_Vertical" H 10300 3700 50  0001 C CNN
F 3 "" H 10300 3700 50  0000 C CNN
	1    10300 3700
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR016
U 1 1 59606B5C
P 9200 3850
F 0 "#PWR016" H 9200 3600 50  0001 C CNN
F 1 "GND" H 9200 3700 50  0000 C CNN
F 2 "" H 9200 3850 50  0000 C CNN
F 3 "" H 9200 3850 50  0000 C CNN
	1    9200 3850
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR017
U 1 1 59606B9D
P 9300 3350
F 0 "#PWR017" H 9300 3200 50  0001 C CNN
F 1 "+5V" H 9300 3490 50  0000 C CNN
F 2 "" H 9300 3350 50  0000 C CNN
F 3 "" H 9300 3350 50  0000 C CNN
	1    9300 3350
	1    0    0    -1  
$EndComp
$Comp
L +3.3V #PWR018
U 1 1 59606BF0
P 9600 3750
F 0 "#PWR018" H 9600 3600 50  0001 C CNN
F 1 "+3.3V" H 9600 3890 50  0000 C CNN
F 2 "" H 9600 3750 50  0000 C CNN
F 3 "" H 9600 3750 50  0000 C CNN
	1    9600 3750
	1    0    0    -1  
$EndComp
Text GLabel 2000 3600 0    60   Input ~ 0
A1
Text GLabel 10100 3650 0    60   Input ~ 0
A1
Text GLabel 10100 3550 0    60   Input ~ 0
A2
Text GLabel 2000 3700 0    60   Input ~ 0
A2
Text GLabel 10100 3850 0    60   Input ~ 0
D6
Text GLabel 3700 4400 2    60   Input ~ 0
V_POWER
Text GLabel 3700 4300 2    60   Input ~ 0
D6
Text GLabel 3700 4100 2    60   Input ~ 0
D10
Text GLabel 10100 4050 0    60   Input ~ 0
D10
$Comp
L R R6
U 1 1 59617861
P 9100 5350
F 0 "R6" V 9180 5350 50  0000 C CNN
F 1 "10.54k" V 9100 5350 50  0000 C CNN
F 2 "Resistor_mw:Resistor_SMD+THTuniversal_0805to1206_RM10_HandSoldering" V 9030 5350 50  0001 C CNN
F 3 "" H 9100 5350 50  0000 C CNN
	1    9100 5350
	0    1    1    0   
$EndComp
$Comp
L R R7
U 1 1 596178D4
P 8950 5750
F 0 "R7" V 9030 5750 50  0000 C CNN
F 1 "3.74k" V 8950 5750 50  0000 C CNN
F 2 "Resistor_mw:Resistor_SMD+THTuniversal_0805to1206_RM10_HandSoldering" V 8880 5750 50  0001 C CNN
F 3 "" H 8950 5750 50  0000 C CNN
	1    8950 5750
	1    0    0    -1  
$EndComp
Text GLabel 8850 4900 0    60   Input ~ 0
VBAT_IN
Text GLabel 8600 5500 0    60   Input ~ 0
BATT
Text GLabel 2000 3800 0    60   Input ~ 0
BATT
Text GLabel 10400 5050 2    60   Input ~ 0
V_POWER
Text GLabel 2000 4400 0    60   Input ~ 0
D0
$Comp
L R R5
U 1 1 59617F72
P 9450 4600
F 0 "R5" H 9530 4600 50  0000 C CNN
F 1 "10k" V 9450 4600 50  0000 C CNN
F 2 "Resistor_mw:Resistor_SMD+THTuniversal_0805to1206_RM10_HandSoldering" V 9380 4600 50  0001 C CNN
F 3 "" H 9450 4600 50  0000 C CNN
	1    9450 4600
	0    1    1    0   
$EndComp
$Comp
L GND #PWR019
U 1 1 596183C8
P 8950 5900
F 0 "#PWR019" H 8950 5650 50  0001 C CNN
F 1 "GND" H 8950 5750 50  0000 C CNN
F 2 "" H 8950 5900 50  0000 C CNN
F 3 "" H 8950 5900 50  0000 C CNN
	1    8950 5900
	1    0    0    -1  
$EndComp
$Comp
L IRF9540N Q2
U 1 1 59618880
P 9450 5100
F 0 "Q2" H 9700 5175 50  0000 L CNN
F 1 "IPP45P03P4L-11" H 9700 5100 50  0000 L CNN
F 2 "TO_SOT_Packages_THT:TO-220_Neutral123_Vertical" H 9700 5025 50  0001 L CIN
F 3 "" H 9450 5100 50  0000 L CNN
	1    9450 5100
	-1   0    0    1   
$EndComp
$Comp
L +3.3V #PWR020
U 1 1 59619B8A
P 9100 4600
F 0 "#PWR020" H 9100 4450 50  0001 C CNN
F 1 "+3.3V" H 9100 4740 50  0000 C CNN
F 2 "" H 9100 4600 50  0000 C CNN
F 3 "" H 9100 4600 50  0000 C CNN
	1    9100 4600
	1    0    0    -1  
$EndComp
Text Notes 9600 4500 0    60   ~ 0
Voltage measurement
Text Notes 3300 5750 0    60   ~ 0
Low battery protection
Text Notes 5800 4600 0    60   ~ 0
Ultrasonic range detector power circuit
Text Notes 6600 3150 0    60   ~ 0
External watchdog circuit
Text Notes 5650 700  0    60   ~ 0
Solar charging circuit
Text Notes 1600 1950 0    60   ~ 0
Ultrasonic range detector
$Comp
L MCP112-300 U6
U 1 1 5972B815
P 1800 6450
F 0 "U6" H 1800 6350 50  0000 C CNN
F 1 "MCP112-300" H 1800 6550 50  0000 C CNN
F 2 "TO_SOT_Packages_THT:TO-92_Inline_Wide" H 1800 6450 50  0001 C CNN
F 3 "DOCUMENTATION" H 1800 6450 50  0001 C CNN
	1    1800 6450
	-1   0    0    1   
$EndComp
$Comp
L +3.3V #PWR021
U 1 1 5977FE2D
P 5950 3950
F 0 "#PWR021" H 5950 3800 50  0001 C CNN
F 1 "+3.3V" H 5950 4090 50  0000 C CNN
F 2 "" H 5950 3950 50  0000 C CNN
F 3 "" H 5950 3950 50  0000 C CNN
	1    5950 3950
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X01 J1
U 1 1 597911DD
P 9650 1250
F 0 "J1" H 9650 1350 50  0000 C CNN
F 1 "CONN_01X01" V 9750 1250 50  0000 C CNN
F 2 "Mounting_Holes:MountingHole_3.2mm_M3_DIN965_Pad" H 9650 1250 50  0001 C CNN
F 3 "" H 9650 1250 50  0001 C CNN
	1    9650 1250
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X01 J4
U 1 1 5979146A
P 9800 1650
F 0 "J4" H 9800 1750 50  0000 C CNN
F 1 "CONN_01X01" V 9900 1650 50  0000 C CNN
F 2 "Mounting_Holes:MountingHole_3.2mm_M3_DIN965_Pad" H 9800 1650 50  0001 C CNN
F 3 "" H 9800 1650 50  0001 C CNN
	1    9800 1650
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X01 J2
U 1 1 597914C6
P 10150 1150
F 0 "J2" H 10150 1250 50  0000 C CNN
F 1 "CONN_01X01" V 10250 1150 50  0000 C CNN
F 2 "Mounting_Holes:MountingHole_3.2mm_M3_DIN965_Pad" H 10150 1150 50  0001 C CNN
F 3 "" H 10150 1150 50  0001 C CNN
	1    10150 1150
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X01 J3
U 1 1 59791523
P 10500 1650
F 0 "J3" H 10500 1750 50  0000 C CNN
F 1 "CONN_01X01" V 10600 1650 50  0000 C CNN
F 2 "Mounting_Holes:MountingHole_3.2mm_M3_DIN965_Pad" H 10500 1650 50  0001 C CNN
F 3 "" H 10500 1650 50  0001 C CNN
	1    10500 1650
	1    0    0    -1  
$EndComp
Wire Wire Line
	6800 2650 6800 2800
Wire Wire Line
	2000 3100 1750 3100
Wire Wire Line
	7650 2250 7400 2250
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
	6950 1300 6950 1000
Wire Wire Line
	6950 1000 6450 1000
Wire Wire Line
	6450 1250 6450 1600
Wire Wire Line
	6450 1600 6400 1600
Wire Wire Line
	6650 1700 6400 1700
Wire Wire Line
	4200 4200 3700 4200
Wire Wire Line
	4200 4600 3700 4600
Wire Wire Line
	7400 2650 7550 2650
Wire Wire Line
	6800 2250 6500 2250
Wire Wire Line
	6450 900  6800 900 
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
	7650 1250 7650 2250
Wire Wire Line
	4700 4800 4700 4500
Connection ~ 4700 4500
Wire Wire Line
	4700 5100 4700 5300
Wire Wire Line
	5600 4450 5600 5100
Wire Wire Line
	5600 4050 6150 4050
Wire Wire Line
	2550 6550 2550 7150
Wire Wire Line
	5400 6050 5400 6300
Wire Wire Line
	2550 7150 6100 7150
Wire Wire Line
	6100 7150 6100 6400
Wire Wire Line
	6100 6400 5400 6400
Wire Wire Line
	5550 6500 5400 6500
Wire Wire Line
	3350 6300 3350 6650
Wire Wire Line
	3900 6300 3350 6300
Wire Wire Line
	9200 3450 10100 3450
Wire Wire Line
	10100 3350 9300 3350
Wire Wire Line
	10100 3750 9600 3750
Wire Wire Line
	8950 5600 8950 5350
Wire Wire Line
	8600 5500 8950 5500
Connection ~ 8950 5500
Wire Wire Line
	9650 5050 10400 5050
Wire Wire Line
	9350 5300 9350 5350
Wire Wire Line
	9350 5350 9250 5350
Wire Wire Line
	9300 4600 9100 4600
Wire Wire Line
	9600 4600 9750 4600
Wire Wire Line
	9750 4600 9750 5050
Connection ~ 9750 5050
Wire Wire Line
	2550 6450 2950 6450
Wire Wire Line
	2950 6450 2950 5750
Wire Wire Line
	2550 6350 2550 5900
Wire Wire Line
	2550 5900 900  5900
Wire Wire Line
	900  5900 900  6800
Wire Wire Line
	900  6800 1000 6800
Wire Wire Line
	9200 3850 9200 3450
$Comp
L 2N7002 Q1
U 1 1 5979BE6F
P 5500 4250
F 0 "Q1" H 5700 4325 50  0000 L CNN
F 1 "2N7002" H 5700 4250 50  0000 L CNN
F 2 "TO_SOT_Packages_SMD:TSOT-23" H 5700 4175 50  0001 L CIN
F 3 "" H 5500 4250 50  0001 L CNN
	1    5500 4250
	1    0    0    -1  
$EndComp
$Comp
L JSN-SR40T S2
U 1 1 597A9F74
P 4650 1650
F 0 "S2" H 4650 1550 50  0000 C CNN
F 1 "JSN-SR40T v2" H 4650 1750 50  0000 C CNN
F 2 "jsn--sr04t:JSN-SR04T" H 4650 1650 50  0001 C CNN
F 3 "DOCUMENTATION" H 4650 1650 50  0001 C CNN
F 4 "Ultrasonic measuring device" H 4650 1650 50  0001 C CNN "Type"
	1    4650 1650
	1    0    0    -1  
$EndComp
Text GLabel 3700 1600 0    60   Input ~ 0
TRIGGER
Text GLabel 3650 1700 0    60   Input ~ 0
ECHO
Wire Wire Line
	2900 1800 3900 1800
Wire Wire Line
	3900 1500 3700 1500
Wire Wire Line
	3700 1500 3700 1200
Wire Wire Line
	3700 1600 3900 1600
Wire Wire Line
	3650 1700 3900 1700
Text Notes 1700 750  0    60   ~ 0
Ultrasonic range detector power circuit
$Comp
L 2N7002 Q3
U 1 1 597AA159
P 2800 2300
F 0 "Q3" H 3000 2375 50  0000 L CNN
F 1 "2N7002" H 3000 2300 50  0000 L CNN
F 2 "TO_SOT_Packages_SMD:TSOT-23" H 3000 2225 50  0001 L CIN
F 3 "" H 2800 2300 50  0001 L CNN
	1    2800 2300
	1    0    0    -1  
$EndComp
Wire Wire Line
	3700 4500 4850 4500
Text GLabel 5300 4300 0    60   Input ~ 0
US
Text GLabel 4850 4500 2    60   Input ~ 0
US
Text GLabel 2600 2350 0    60   Input ~ 0
US
$Comp
L GND #PWR023
U 1 1 597AA8ED
P 2900 2500
F 0 "#PWR023" H 2900 2250 50  0001 C CNN
F 1 "GND" H 2900 2350 50  0000 C CNN
F 2 "" H 2900 2500 50  0000 C CNN
F 3 "" H 2900 2500 50  0000 C CNN
	1    2900 2500
	1    0    0    -1  
$EndComp
Wire Wire Line
	2900 2100 2900 1800
$Comp
L +3.3V #PWR?
U 1 1 597AAB28
P 3700 1200
F 0 "#PWR?" H 3700 1050 50  0001 C CNN
F 1 "+3.3V" H 3700 1340 50  0000 C CNN
F 2 "" H 3700 1200 50  0000 C CNN
F 3 "" H 3700 1200 50  0000 C CNN
	1    3700 1200
	1    0    0    -1  
$EndComp
Text GLabel 10100 3950 0    60   Input ~ 0
A0
Text GLabel 2000 3500 0    60   Input ~ 0
A0
Wire Notes Line
	5400 2750 600  2750
Wire Notes Line
	600  2750 600  600 
Wire Notes Line
	600  600  5400 600 
Wire Notes Line
	5400 600  5400 2750
Wire Notes Line
	600  2800 5000 2800
Wire Notes Line
	5000 2800 5000 5550
Wire Notes Line
	5000 5550 600  5550
Wire Notes Line
	600  5550 600  2800
Wire Notes Line
	600  5600 6350 5600
Wire Notes Line
	6350 5600 6350 7400
Wire Notes Line
	6350 7400 700  7400
Wire Notes Line
	700  7400 700  5600
Wire Notes Line
	5600 2050 7400 2050
Wire Notes Line
	7400 2050 7400 600 
Wire Notes Line
	7400 600  5550 600 
Wire Notes Line
	5550 600  5550 2050
Wire Notes Line
	5550 2050 5650 2050
Wire Notes Line
	6050 2100 6050 3250
Wire Notes Line
	6050 3250 8850 3250
Wire Notes Line
	8850 3250 8850 2550
Wire Notes Line
	8850 2550 9200 2550
Wire Notes Line
	9200 2550 9200 800 
Wire Notes Line
	9200 800  7450 800 
Wire Notes Line
	7450 800  7450 2100
Wire Notes Line
	7450 2100 6050 2100
Wire Notes Line
	6050 2200 6100 2200
Wire Wire Line
	9350 4900 8850 4900
Wire Notes Line
	8100 4350 8100 6400
Wire Notes Line
	8100 6400 11050 6400
Wire Notes Line
	11050 6400 11050 4350
Wire Notes Line
	11050 4350 8100 4350
Wire Notes Line
	5050 5300 5050 3400
Wire Notes Line
	5050 3400 7900 3400
Wire Notes Line
	7900 3400 7900 5200
Wire Notes Line
	7900 5200 5050 5200
Wire Notes Line
	5050 5200 5050 5250
Wire Notes Line
	9100 4250 10750 4250
Wire Notes Line
	10750 4250 10750 3000
Wire Notes Line
	10750 3000 9000 3000
Wire Notes Line
	9000 3000 9000 4250
Wire Notes Line
	9000 4250 9150 4250
Text Notes 9750 700  0    60   ~ 0
Mounting holes
Text Notes 9500 3150 0    60   ~ 0
Spare connections
Wire Notes Line
	9300 600  9300 2100
Wire Notes Line
	9300 2100 11100 2100
Wire Notes Line
	11100 2100 11100 600 
Wire Notes Line
	11100 600  9300 600 
$EndSCHEMATC
