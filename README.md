# tank_lora
Meaure water tank levels with and send signal with LoRa radion on private network

## Hardware overview
Using an ATMega brain, a lora radio implemented by AI Thinker, an ultrasonic distance measuring device and powering with solar we will send signal from remote locations to a hub and publish water levels to the web
* 5V power rail to supply
   * LoRa module (this Buck converts to 3.3v for supplying radio and ATMega chip)
   * Ultraasonic range detector
 * 3.3V rail to supply TPL5010

### Power
6V, 3W solar panel to supply 5V power rail with storage that will have at least a battery and possibly a supercap. Conservaton stratagies include:
* Using a TPL5010 as a watchdog timer
   * Sends a wake pulse that can be programmed to be up to every 2hrs by varying resistance to Prog pin
   * Needs a 'done' pulse sent from MCU at least 20ms prior to next wake pulse or it will send a reset to MCU
   * This means we don't need to power a watchdog or brownout detection on MCU saving some power (see page 397 in http://www.atmel.com/Images/Atmel-7766-8-bit-AVR-ATmega16U4-32U4_Datasheet.pdf )
      * 0.5microA in power down mode with WDT disabled vs 6microA with WDT enabled
* Disabling DC-DC converter (uses ~100microA)
   *  Would need to use somthing like a latching transistor circuit for TPL5010 to trigger, like http://m.eet.com/media/1151168/24527-112300di.pdf, then MCU feeds the TPL5010 the done pulse prior to shutting down
      * This would mean we can't power TPL5010 from LoRa module 3.3v rail causing it to use 43nA at 5v

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
* LoRa http://www.arduinolibraries.info/libraries/lo-ra

## Testing

# Notes
LoRa32u4 module has connection:

Radio module | ATMega32u4
--- | ---
NSS |   1
RST |   4
DIO0 | 7 (PE6) - this is an assumption it is pin 7 as per https://www.arduino.cc/en/Hacking/PinMapping32u4  

These need to be set in LoRa.setPins(ss, reset, dio0); (see https://github.com/sandeepmistry/arduino-LoRa/blob/master/API.md)
