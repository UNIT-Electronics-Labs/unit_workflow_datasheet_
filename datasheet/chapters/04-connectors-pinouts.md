## **4 Connectors & Pinouts**

### **4.1 General Pinout**

![](datasheet/assets/media/image23.png){width=6.26772in}

*Multi-Shield General Pinout*

### **4.2 Pinout General Description**

| **Label**    | **Description**          | **Typical Use**                                |
|--------------|--------------------------|------------------------------------------------|
| GND          | Ground reference         | Common return path for all signals             |
| 3V3          | 3.3V regulated output    | Power for sensors, logic devices               |
| VIN / 5V     | Main input voltage       | External power supply, USB input               |
| SDA          | I²C Data Line            | Communication with sensors (EEPROM, IMU, etc.) |
| SCL          | I²C Clock Line           | Synchronization for I²C devices                |
| TX           | UART Transmit            | Serial communication to PC or modules          |
| RX           | UART Receive             | Serial data input                              |
| GPIO         | General Purpose I/O      | Digital input/output (buttons, LEDs)           |
| ADC          | Analog Input             | Sensor reading (voltage, temperature, etc.)    |
| PWM          | PWM Output               | Motor control, dimming LEDs, buzzer            |
| INT          | Interrupt Input          | Event-driven signals from sensors              |
| EN           | Enable Control           | Power enable/disable modules                   |
| RST          | Reset Signal             | Reset connected boards or modules              |
| QWIIC SDA    | I²C Data (JST 1mm)       | Plug-and-play I²C modules                      |
| QWIIC SCL    | I²C Clock (JST 1mm)      | Plug-and-play I²C modules                      |
| NeoPixel DIN | Data input for LED       | Control WS2812 LED strips/matrix               |
| BTN1         | Button Input             | User interaction                               |
| BTN2         | Button Input             | User interaction                               |
| VOUT         | Regulated output voltage | Power external circuits                        |
| USB VBUS     | USB power line           | Power from USB-C                               |
| LOAD+        | Load positive terminal   | External load connection                       |
| LOAD-        | Load negative terminal   | External load return                           |
| COM          | Relay common             | Switching circuits                             |
| NO           | Relay normally open      | Load activation                                |
| NC           | Relay normally closed    | Default load state                             |
| MOSI         | SPI Master Out           | Data to SPI devices                            |
| MISO         | SPI Master In            | Data from SPI devices                          |
| SCK          | SPI Clock                | SPI synchronization                            |
| CS           | Chip Select              | Select SPI device                              |
| BUZZ         | Buzzer Output            | Sound alerts, feedback                         |
| LED          | Status LED               | Visual indication                              |
| PROG         | Programming Pin          | Firmware flashing                              |
| ID           | Board ID / Address       | Device identification                          |
