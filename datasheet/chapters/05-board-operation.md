## **5 Board Operation**

### **5.1 Getting Started**

This section provides a complete initial procedure for operating the
Multi Hub Shield with a compatible microcontroller platform. The
objective is to validate correct hardware integration, power
distribution, and communication using a basic functional example.

The Multi Hub Shield is designed to operate with multiple development
boards, including Pulsar C6 (ESP32-C6), ESP32 DevKit V4, XIAO, and other
compatible formats. Each platform is supported through dedicated layout
zones that expose the required pin mappings for proper operation.

The initial validation is centered on establishing I²C communication and
verifying system behavior through a visual interface. For this purpose,
the use of an I²C OLED display (128×64) is recommended, as it provides
immediate feedback and simplifies debugging.

**Hardware Requirements**

- Multi Hub Shield

- Compatible development board (Pulsar C6, ESP32 DevKit V4, XIAO, or
  equivalent)

- I²C OLED display (128×64, SSD1306 recommended)

- USB-C cable for power and programming

- Optional jumper configuration or headers depending on platform

**System Assembly**

Begin by installing the selected development board into the
corresponding compatibility zone on the shield. Ensure that all pins are
correctly aligned and fully inserted. The silkscreen labeling on the
board serves as the primary reference for positioning.

If required, configure jumpers or headers to enable communication lines
such as I²C. Some platforms may require explicit routing of SDA and SCL
signals depending on the internal pin configuration.

Once the microcontroller is installed, connect the OLED display to one
of the DevLab/QWIIC connectors. These connectors provide direct access
to the I²C bus and power lines, allowing a clean and solderless
connection.

**Electrical Connections**

The QWIIC/DevLab connector provides the following signals:

- VCC (3.3 V or 5 V depending on board configuration)

- GND

- SDA (data line)

- SCL (clock line)

For the Pulsar C6, the default I²C configuration is:

- SDA → GPIO6

- SCL → GPIO7

Ensure that the display module operates within the same voltage domain
as the board. Incorrect voltage selection may prevent operation or
damage the device.

**Connection Diagram**

![](datasheet/assets/media/image25.png){width=6.26772in}

#### **Development Environment Setup**

Open the Arduino IDE and configure the following:

- Board: ESP32C6 Dev Module

- Port: Corresponding serial port

- Libraries Required:

  - Wire (included by default)

  - Adafruit SSD1306

  - Adafruit GFX

Install the required libraries using the Arduino Library Manager if they
are not already available.

#### **Initial Test Application**

The following example initializes the I²C interface and displays a basic
message on the OLED. This confirms correct communication between the
microcontroller and the display.

```cpp
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SDA_PIN 6
#define SCL_PIN 7
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

void setup() {
  Serial.begin(115200);

  // Initialize I2C
  Wire.begin(SDA_PIN, SCL_PIN);

  // Initialize display
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("OLED initialization failed");
    while (true);
  }

  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 10);
  display.println("Multi Hub Shield");
  display.println("Initialization OK");
  display.display();
}

void loop() {
  // No repeated actions required
}
```

#### **Code Description**

The program begins by initializing the serial interface for debugging
purposes. The I²C bus is then configured using the defined SDA and SCL
pins corresponding to the selected platform.

The OLED display is initialized using its default I²C address (0x3C). If
the display is not detected, the program halts execution, indicating a
hardware or connection issue.

Once initialized, the display buffer is cleared, and a simple text
message is rendered. This confirms that communication is established and
that the system is functioning correctly.

#### **Validation and Expected Behavior**

After uploading the code:

- The OLED display should power on and show the initialization message.

- The serial monitor should not report errors if the device is correctly
  connected.

- If no display output is observed, verify wiring, I²C address, and
  voltage compatibility.

This validation step confirms:

- Correct power distribution

- Functional I²C communication

- Proper platform integration

- Working development environment

#### **Next Steps**

Once the initial test is successful, the system is ready for further
development. Additional features of the Multi Hub Shield can be
progressively enabled, including:

- Relay control for external loads

- PWM signal generation for control applications

- Sensor integration through DevLab or Gravity connectors

- User interaction using buttons and LED matrix

This structured approach ensures a reliable starting point before
implementing more complex embedded applications.
