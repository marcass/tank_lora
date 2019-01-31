# tank_lora
Meaure water tank levels with and send signal with LoRa radio on on private network with alerts

## Hardware overview
Using an ATMega brain, a lora radio implemented by AI Thinker, an ultrasonic distance measuring device and powering with solar we will send signal from remote locations to a hub and publish water levels to a web accessable platform
* 6-2.7V power rail to supply
   * LoRa module (on board Buck converts to 3.3v for supplying radio and ATMega chip)
 * 3.3V rail to supply everything (avoiding 5V)

### Power
6V, 3W solar panel to supply power rail (2.75 to 6V) with storage that will have at least a battery and possibly a supercap. Conservaton stratagies include:
* Using a TPL5010 as a watchdog timer
   * Sends a wake pulse that can be programmed to be up to every 2hrs by varying resistance to Prog pin
   * Needs a 'done' pulse sent from MCU at least 20ms prior to next wake pulse or it will send a reset to MCU
   * Savings on changing fuses for watchdog and brownout detection are not of great benefit. Doing this would save some power (see page 397 in http://www.atmel.com/Images/Atmel-7766-8-bit-AVR-ATmega16U4-32U4_Datasheet.pdf )
      * 0.5microA in power down mode with WDT disabled vs 6microA with WDT enabled
* Disabling DC-DC converter (uses ~35microA)
   *  Would need to use somthing like a latching transistor circuit for TPL5010 to trigger, like http://m.eet.com/media/1151168/24527-112300di.pdf, then MCU feeds the TPL5010 the done pulse prior to shutting down
      * This would mean we can't power TPL5010 from LoRa module 3.3v rail causing it to use 43nA at 5v
   * counclusion: Just put LoRa radio and MCU to sleep adn allow TPL5010 to manage brownout as it operates as low as 1.8v

#### Battery protection
Low voltage protection provided by https://electronics.stackexchange.com/questions/148586/to-protect-a-lipo-cell-from-undervoltage-how-low-current-is-low-enough (top of page circuit)

Overvoltage protection provided by solar charger like adafruuit solar charger

### Parts
* Lora radios with ATMega32u4 https://www.aliexpress.com/item/5PCS-lot-LoRa32u4-RA-02-433M-Lora-Wireless-WIFI-Module-Long-Range-communication-1KM-LiPo-Atmega328/32812205344.html?spm=2114.13010608.0.0.r6qCKR
   * Similar to adafruit feather LoRa https://learn.adafruit.com/adafruit-feather-32u4-radio-with-lora-radio-module/power-management
   * Better range than nRF
* Charging circuit from 6V 3W panel https://www.aliexpress.com/item/MCP73871-PowerBoost-USB-5V-DC-Solar-Lipoly-Lithium-Lon-Polymer-Charger-Board-3-7V-4-2V/32795379739.html?spm=2114.13010208.99999999.264.vDACyf
   * Similar to MPTT charge circuit
* Solar panels https://www.aliexpress.com/item/Solar-Panel-Module-for-Light-Battery-Cell-Phone-Charger-Portable-6V-2W-330MA-DIY/32408341015.html?spm=2114.13010608.0.0.j91m7t
* 3.3V Ultrasound range detection
* TPL5010 for watchdog timer http://www.ti.com/lit/ds/symlink/tpl5010.pdf
   * 35nA at 2.8v

## Software overview

Program LoRa board with onboard ATMega32u4 chip with arduino IDE

### Flashing

* Change nodeID on each sketch prior to Flashing
* Flash remote stations with 'sensor_node'
* Flash nodes that are only forwarders duplex_forwarder (specifying which nodes can be forwarded), or duplex_all_forwarder if you are forwarding all signal, or sensor_duplex if taking readings off a tank too. Alter prefix of forwarder for tracking if necessary
* Node attached to base station (Rpi) flashed with master node

### Libraries
* NewPing http://playground.arduino.cc/Code/NewPing (NewPing not working with 3.3V range detectors so using custom script)
   * Can also use measure echo pin pulse using a while loop or PulseIn builtin
* LoRa http://www.arduinolibraries.info/libraries/lo-ra

## Lora gateway
* Using a raspberry pi
* mimimising writes to SD card for longevity
* using docker to speed setup on new hardware
   * https://www.containerstack.io/install-docker-on-raspbian/


### Starting services

* Starting services
 On raspberry pi: sudo systemctl [start][stop][status][restart] serial-attach.service
* Seial listener: `sudo systemctl start serial-attach.service`
* update for flask service and web service (nginix)

## Testing

# Notes
LoRa32u4 module has connection:

Radio module | ATMega32u4 arduino pin
--- | ---
NSS |   1 or 8
RST |   4
DIO0 | 7 (PE6) https://www.arduino.cc/en/Hacking/PinMapping32u4  

These need to be set in LoRa.setPins(ss, reset, dio0); (see https://github.com/sandeepmistry/arduino-LoRa/blob/master/API.md)

# Power consumption
* Battery protection circuit:
   * 28uA when circuit above voltage?
   * 0.6uA when curcuit below voltage
* Battery testing circuit = 0uA
* LoRa module is flaky when voltages < 2.80 (when on external watcdog) supplied to 5V pin, otherwise works well.
* LoRa module uses ~387microA when in power down sleep mode
* Solar charger uses 26uA as quiescent current
* Totoal consumption with led resistor removed from LoRa32u4 is 1.2mA on assembled board. (4 predicted, but still OK)

NOTE: TPL 5010 with ~90k Ohm resistor gives 26min between wakes
