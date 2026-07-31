## **2 Ratings**

### **2.1 Recommended Operating Conditions**

| **Symbol**  | **Description**                         | **Min**   | **Typ**               | **Max**                  | **Unit** |
|-------------|-----------------------------------------|-----------|-----------------------|--------------------------|----------|
| VIN_PD      | USB-C PD Input Voltage                  | 5         | 5 / 9 / 12 / 15 / 20  | 20                       | V        |
| VIN_EXT     | External Supply Input Voltage           | 5.0       | 5.0                   | 5.5                      | V        |
| VOUT_5V     | Regulated 5V Output Rail                | 4.85      | 5.0                   | 5.15                     | V        |
| VOUT_3V3    | Regulated 3.3V Output Rail              | 3.20      | 3.30                  | 3.40                     | V        |
| IOUT_5V     | Recommended 5V Rail Output Current      | 1.2       | 1.6                   | 2.0                      | A        |
| IOUT_3V3    | Recommended 3.3V Rail Output Current    | 1.2       | 1.6                   | 2.0                      | A        |
| TA          | Operating Ambient Temperature           | 0         | 25                    | 70                       | °C       |
| VIH         | Digital Input High Level                | 0.7 × VDD | —                     | VDD                      | V        |
| VIL         | Digital Input Low Level                 | 0         | —                     | 0.3 × VDD                | V        |
| FI2C        | I²C Bus Frequency                       | 100       | 400                   | 1000                     | kHz      |
| VQWIIC      | QWIIC/STEMMA Connector Supply Voltage   | 3.3       | 3.3 / 5.0             | 5.0                      | V        |
| VRELAY      | Relay Coil Supply Voltage               | 4.75      | 5.0                   | 5.25                     | V        |
| IRELAY      | Relay Coil Current (per channel)        | —         | 21.1                  | —                        | mA       |
| VLOAD_RELAY | Relay Switched Load Voltage             | —         | —                     | 30 (DC) / 125 (AC)       | V        |
| ILOAD_RELAY | Relay Switched Load Current             | —         | —                     | 1 @ 30VDC / 0.5 @ 125VAC | A        |
| VPWM        | PWM Output Load Voltage                 | 0         | VDD                   | 30                       | V        |
| IPWM        | PWM Load Current                        | —         | Application-defined   | 10                       | A        |
| VLED_MATRIX | WS2812B LED Matrix Supply Voltage       | 4.5       | 5.0                   | 5.5                      | V        |
| ILED_MATRIX | WS2812B Matrix Current (5×5 Full White) | —         | Application-dependent | 200                      | mA       |
| VLED_IO     | WS2812B Data Input Logic Level          | —         | 3.3 / 5.0             | VDD                      | V        |
| ILED_IND    | Status LED Current                      | —         | 2–10                  | —                        | mA       |
| VBUZZ       | PWM Buzzer Operating Voltage            | 3.0       | 3.3 / 5.0             | 5.0                      | V        |
| FBUZZ       | PWM Buzzer Drive Frequency              | 0.5       | \-                    | 500                      | kHz      |
| VBTN        | Push Button Logic Voltage               | 0         | VDD                   | VDD                      | V        |
| VADC        | ADC Input Voltage Range                 | 0         | —                     | VDD_ADC                  | V        |
| RVR         | Trimpot Resistance                      | —         | 10                    | —                        | kΩ       |
