# tank_lora
Meaure water tank levels with and send signal with LoRa radio on on private network with alerts

## Hardware overview
Using an ATMega brain, a lora radio implemented by AI Thinker, an ultrasonic distance measuring device and powering with solar we will send signal from remote locations to a hub and publish water levels to a web accessable platform
* 6-2.7V power rail to supply
   * LoRa module (this Buck converts to 3.3v for supplying radio and ATMega chip)
 * 3.3V rail to supply:
   * External watchdog (TPL5010)
   * Boost module for distance detector

### Power
6V, 3W solar panel to supply 5V power rail with storage that will have at least a battery and possibly a supercap. Conservaton stratagies include:
* Using a TPL5010 as a watchdog timer
   * Sends a wake pulse that can be programmed to be up to every 2hrs by varying resistance to Prog pin
   * Needs a 'done' pulse sent from MCU at least 20ms prior to next wake pulse or it will send a reset to MCU
   * Savings on changing fuses for watchdog and brownout detection are not of great benefit. Doing this would save some power (see page 397 in http://www.atmel.com/Images/Atmel-7766-8-bit-AVR-ATmega16U4-32U4_Datasheet.pdf )
      * 0.5microA in power down mode with WDT disabled vs 6microA with WDT enabled
* Disabling DC-DC converter (uses ~35microA)
   *  Would need to use somthing like a latching transistor circuit for TPL5010 to trigger, like http://m.eet.com/media/1151168/24527-112300di.pdf, then MCU feeds the TPL5010 the done pulse prior to shutting down
      * This would mean we can't power TPL5010 from LoRa module 3.3v rail causing it to use 43nA at 5v
   * counclusion: Just put LoRa radio and MCU to sleep adn allow TPL5010 to manage brownout as it operates as low as 1.8v

#### 5V rail
Solar charger like https://learn.adafruit.com/usb-dc-and-solar-lipoly-charger/using-the-charger will give up to full voltage output of panel to load so we may need to limit that (turns out we don't have to). So to get a  5V rail for ultrasonic module use boost converter from 3.3v rail on LoRa32u4 board and power it by saturating a NPN transistor with a digital pin

Uses https://www.diodes.com/assets/Datasheets/AP2112.pdf as DC-DC converter and will accept 2.5-6.5V so can manage load from solar panel

#### Battery protection
Low voltage protection provided by https://electronics.stackexchange.com/questions/148586/to-protect-a-lipo-cell-from-undervoltage-how-low-current-is-low-enough (top of page circuit)

Overvoltage protection provided by solar charger like adafruuit solar charger

### Parts
* Lora radios with ATMega32u4 https://www.aliexpress.com/item/5PCS-lot-LoRa32u4-RA-02-433M-Lora-Wireless-WIFI-Module-Long-Range-communication-1KM-LiPo-Atmega328/32812205344.html?spm=2114.13010608.0.0.r6qCKR
   * Similar to adafruit feather LoRa https://learn.adafruit.com/adafruit-feather-32u4-radio-with-lora-radio-module/power-management
   * Better range than nRF
* Charging circuit from 6V 3W panel https://www.aliexpress.com/item/MCP73871-PowerBoost-USB-5V-DC-Solar-Lipoly-Lithium-Lon-Polymer-Charger-Board-3-7V-4-2V/32795379739.html?spm=2114.13010208.99999999.264.vDACyf
   * Similar to MPTT charge circuit
* DC-DC boost 1-5V -> 5V https://www.aliexpress.com/item/5V-DC-DC-Converter-Step-Up-Power-Supply-DC-DC-Booster-Boost-Buck-Converter-Board-Step/32635991770.html?spm=2114.13010608.0.0.r6qCKR
   * Need this to run ultrasound sensor because it requires 5v and 30mA when measuing
* Solar panels https://www.aliexpress.com/item/Solar-Panel-Module-for-Light-Battery-Cell-Phone-Charger-Portable-6V-2W-330MA-DIY/32408341015.html?spm=2114.13010608.0.0.j91m7t
* Ultrasound range detection https://www.aliexpress.com/item/J34-Free-Shipping-DC-5V-Ultrasonic-Module-Distance-Measuring-Transducer-Sensor-Perfect-Waterproof/32400424410.html?spm=2114.13010608.0.0.KSTWmM
* TPL5010 for watchdog timer http://www.ti.com/lit/ds/symlink/tpl5010.pdf
   * 35nA at 2.8v

## Software overview

Program LoRa board with onboard ATMega32u4 chip with arduino IDE

### Libraries
* NewPing http://playground.arduino.cc/Code/NewPing
   * Can also use measure echo pin pulse using a while loop or PulseIn builtin
* LoRa http://www.arduinolibraries.info/libraries/lo-ra

### Starting services

* Starting services
 On raspberry pi: sudo systemctl start[stop][status][restart] <service name>
* Seial listener: `sudo systemctl start serial-attach.service`
* Bot: `sudo systemctl start telegram-bot.service`


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
* Battery testing circuit = 0uA. However, the P-channel mosfet will not switch when battery gets below 3.3V (damnit)
* LoRa module is flaky when voltages < 2.80 (when on external watcdog) supplied to 5V pin, otherwise works well.
* LoRa module uses ~387microA when in power down sleep mode
* Solar charger uses 26uA as quiescent current

NOTE: TPL 5010 with ~90k Ohm resistor gives 26min between wakes



