## **3. Functional Overview**

This shield is designed as a development-focused platform that
integrates multiple functional blocks into a single hardware solution.
Its architecture supports rapid prototyping, educational applications,
and system validation by combining control, visualization, interaction,
and expansion capabilities. The board consolidates essential features
such as relay control, display interfaces, signal modulation, and
modular connectivity, enabling users to build complete embedded systems
without requiring extensive external hardware.

### **3.1 Relay Control Section**

The board integrates two relay channels designed for switching external
loads through isolated control signals. These relays allow the
microcontroller to safely interface with higher-power devices by
separating the control domain from the load domain. Each channel
provides standard switching terminals, enabling flexible connection to
external systems such as lighting, actuators, or low-power AC/DC
equipment. This section is positioned to maintain clear separation
between signal routing and load paths, improving reliability during
operation.

![](tools/datasheet/assets/media/image22.png){width=3.48073in}

### **3.2 Display and Visualization Section**

A dedicated display interface area is provided to support visual output
devices, including I²C-based OLED displays and compatible TFT modules.
The layout is optimized to simplify integration and minimize signal
complexity, enabling stable communication for real-time data
visualization. This section is intended for implementing user
interfaces, diagnostics, and monitoring systems within embedded
applications.

![](tools/datasheet/assets/media/image19.png){width=3.60417in}


### **3.3 PWM and Signal Control Section**

The board includes PWM-capable outputs intended for variable signal
control. These outputs enable applications such as brightness
regulation, proportional control, and signal-based interfacing with
external driver stages. The routing ensures accessibility and
compatibility with standard control requirements, allowing integration
with a wide range of peripherals that rely on pulse-width modulation.

![](tools/datasheet/assets/media/image17.png){width=3.89583in}

### **3.4 User Interaction and Feedback Section**

Integrated interaction elements include a 5×5 RGB LED matrix, multiple
push buttons, and status indicator LEDs. These components provide a
direct interface for user input and system feedback without requiring
additional hardware. The arrangement supports intuitive interaction,
making the board suitable for demonstration systems, user interfaces,
and rapid validation of embedded behaviors.

![](tools/datasheet/assets/media/image24.png){width=2.29167in}

### **3.5 DevLab / QWIIC Connectivity Section**

The board incorporates multiple JST 1 mm connectors aligned with QWIIC
and STEMMA QT standards, enabling simplified I²C-based expansion. These
connectors support plug-and-play integration of compatible modules such
as sensors and displays, reducing the need for manual wiring. The
distributed placement across the board facilitates modular design and
efficient system scaling.

![](tools/datasheet/assets/media/image13.png){width=2.96875in}



### **3.6 Platform Compatibility Section**

The central layout is organized into multiple compatibility zones to
support a variety of development platforms, including Feather, Pi Pico,
Devkit V4, Pulsar/Nano, XIAO/QT, and MikroBus formats. Each zone exposes
the required pin mappings for proper integration, allowing the shield to
function as a universal interface across different ecosystems. The
silkscreen serves as a reference for correct placement and alignment.

![](tools/datasheet/assets/media/image11.png){width=6.26772in}

### **3.7 Expansion and Prototyping Section**

A prototyping area is included to support custom circuit development
directly on the board. This section provides access to power rails and
signal points, enabling quick integration of additional components
without external prototyping tools. It is designed to complement the
modular nature of the board, allowing flexible experimentation and
system extension.

| ![](tools/datasheet/assets/media/image14.png){width=2.82292in}    | ![](tools/datasheet/assets/media/image7.png){width=1.8125in}    |
|-----------------------------------------------|----------------------------------------------|

### **3.8 Sensor Interface Section**

Gravity-style connectors are integrated to support the rapid connection
of sensors and peripheral modules. These connectors simplify wiring and
provide standardized access to power and signal lines, making them
suitable for data acquisition and educational applications where
multiple sensors are used simultaneously.

![](tools/datasheet/assets/media/image8.png){width=3.91667in}

### **3.9 Power Distribution Section**

The board integrates a flexible power distribution architecture designed
to support operation from both USB-C Power Delivery (PD) and external
power sources. The system distributes energy across independent 5 V and
3.3 V domains, allowing compatibility with mixed-voltage peripherals,
embedded platforms, and expansion modules.

The power subsystem includes dedicated voltage regulators, protection
circuitry, source-selection logic, and configurable routing headers.
This architecture allows the board to operate under different supply
conditions while maintaining stable voltage regulation and controlled
power distribution across the system.

The design supports three primary operating modes:

- USB-C Power Delivery operation

- External supply operation

- Simultaneous PD and external supply operation with automatic source
  priority

The board also integrates MOSFET-based protection circuitry to prevent
reverse current conditions and undesired interaction between power
sources.

![](tools/datasheet/assets/media/image10.png){width=3.625in}

#### **3.9.1 USB-C Power Delivery Section**

The USB-C power stage is based on the HUSB238 USB Power Delivery
controller. This device negotiates voltage profiles directly from
compatible USB-C PD chargers and exposes the negotiated voltage to the
main VIN distribution rail.

Unlike fixed USB 5 V systems, the HUSB238 allows dynamic voltage
selection through a resistor configuration network connected to the
configuration pins of the controller. The selected voltage depends on
the installed resistor or selector configuration.

Supported Power Delivery profiles include:

| **PD Profile** | **Output Voltage** |
|----------------|--------------------|
| 5 V            | Selectable         |
| 9 V            | Selectable         |
| 12 V           | Selectable         |
| 15 V           | Selectable         |
| 18 V           | Selectable         |
| 20 V           | Selectable         |

The PD voltage is not fixed by default and depends entirely on the
selected configuration and charger capabilities. The negotiated voltage
is routed to the VIN rail and can subsequently feed the onboard
regulators to generate regulated system voltages.

##### **Recommended Power Supply Configuration**

For standard operation using USB-C PD:

- Configure jumper: **VUSB → VREG**

This configuration routes the negotiated PD voltage through the onboard
regulator stages, enabling stable generation of:

- Regulated 5 V rail

- Regulated 3.3 V rail

![](tools/datasheet/assets/media/image15.png){width=4.64739in}

This mode is recommended for general embedded applications and
mixed-voltage peripheral systems.

#### **3.9.2 Voltage Regulation Stage**

The board integrates two independent TPS54302DDCT synchronous buck
regulators to generate regulated voltage domains from the VIN
distribution rail.

The regulation subsystem is divided into:

| **Rail** | **Purpose**                    |
|----------|--------------------------------|
| 5 V      | Peripheral and expansion power |
| 3.3 V    | Logic and low-voltage devices  |

Each regulator stage includes:

- Input filtering capacitors

- Bootstrap capacitor

- Feedback compensation network

- Inductor output filtering

- Output bulk capacitors

This architecture provides stable operation under varying input voltages
and dynamic load conditions.

##### **5 V Regulation Stage**

The first TPS54302 regulator generates the regulated 5 V rail used for
peripheral distribution and external interfaces.

Features include:

- Wide input voltage compatibility

- High-efficiency synchronous conversion

- Stable regulation under PD input conditions

The regulator output is distributed to:

- Expansion headers

- Peripheral connectors

- System 5 V rail

- Secondary regulation stages

##### **3.3 V Regulation Stage**

The second TPS54302 regulator generates the regulated 3.3 V rail used
for logic-level devices and low-voltage peripherals.

This rail powers:

- Microcontroller logic

- I2C peripherals

- Sensors

- Communication interfaces

- Low-voltage expansion modules

The regulation stage is isolated from the main VIN rail through
controlled routing and filtering to improve stability and noise
performance.

#### **3.9.3 External Supply Section**

The board also supports direct external power injection through the
terminal block interface. This mode allows operation without requiring a
USB-C PD source.

The external supply input is designed primarily for regulated 5 V
operation.

When operating from the external supply input, the onboard regulation
stages can still generate the required 3.3 V rail depending on the
selected jumper configuration.

##### **Recommended External Supply Configuration**

For external 5 V operation:

- Configure jumper: **5V → 3V3 regulator enabled**

In this configuration:

- The external 5 V rail powers the system directly

- The onboard regulator generates the 3.3 V logic rail

- Peripheral distribution remains active

This configuration is recommended for standalone systems or applications
powered from laboratory supplies, batteries, or industrial power
systems.

#### **3.9.4 Source Selection and Protection Circuitry**

The board integrates automatic source-selection circuitry to manage
coexistence between USB-C PD and external power sources.

The source-selection stage uses an AO3407 MOSFET array combined with
passive protection circuitry to implement the following:

- Reverse current protection

- Source isolation

- Automatic voltage path selection

- Controlled current flow

- Priority management

The MOSFET stage prevents undesired backfeeding between power sources
and protects the regulators during transitions between supply modes.

##### **Power Path Operation**

When a USB-C PD source is connected:

- The PD source becomes the primary power source

- The AO3407 stage isolates the external supply path

- System power is routed from the negotiated PD rail

When the PD source is disconnected:

- The external supply path automatically becomes active

- Power transitions without manual intervention

- System operation continues from the external source

This architecture allows uninterrupted operation and improves system
reliability under mixed-source conditions.

#### **3.9.5 Power Configuration Cases**

##### **Case 1. USB-C Power Delivery Operation**

This mode uses USB-C PD as the primary power source.

###### **Recommended Configuration**

**VUSB → VREG**

###### **Operation**

- HUSB238 negotiates the configured PD voltage

- VIN rail receives negotiated voltage

- Regulators generate stable 5 V and 3.3 V rails

- Recommended for standard operation

This mode provides maximum flexibility and allows operation from
high-voltage USB-C PD chargers.

##### **Case 2. External 5 V Supply Operation**

This mode uses the external terminal block as the primary power source.

###### **Recommended Configuration**

**5V → 3V3 regulator enabled**

###### **Operation**

- External 5 V source powers the system

- 3.3 V rail generated locally by regulator

- Suitable for battery systems and laboratory supplies

This configuration allows operation without requiring USB-C PD
negotiation.

##### **Case 3. USB-C PD + External Supply**

This mode allows simultaneous connection of both power sources.

###### **Operation**

- USB-C PD source receives priority

- External supply acts as backup source

- Automatic switching occurs if PD power is removed

- MOSFET stage prevents reverse current flow

This configuration is useful in redundant or failover power applications
where uninterrupted operation is required.

#### **3.9.6 Power Distribution Considerations**

To ensure stable operation, the following considerations are
recommended:

- Verify jumper configuration before applying power

- Use regulated external supplies (only +5V)

- Avoid exceeding regulator thermal limits

- Ensure PD chargers support the selected voltage profile

- Use appropriate cable quality for high-current PD operation

For high-power configurations:

- Ensure adequate cooling

- Verify connector current capability

- Avoid simultaneous excessive peripheral loading

The board architecture is designed to support flexible embedded
development while maintaining safe operation across multiple voltage
domains and power-source configurations.

### **3.10 Audio Feedback Section**

An onboard PWM-controlled buzzer provides audible feedback capabilities
for system status, alerts, or interaction cues. It enables simple sound
generation controlled directly by the microcontroller, supporting
user-oriented applications and debugging scenarios.

![](tools/datasheet/assets/media/image4.png){width=1.05208in}

### **3.11 Button Interface Section**

The board integrates four user buttons designed for direct interaction
with the system. These buttons operate using a push-type mechanism and
are electrically configured for digital input detection, allowing
reliable state changes when pressed or released.

The implementation supports typical push–pull signal behavior through
the microcontroller configuration, enabling straightforward integration
for user control, menu navigation, or event triggering. This section is
intended to provide immediate manual input without requiring additional
external components, simplifying development and testing workflows.

![](tools/datasheet/assets/media/image20.png){width=1.5in}




### **3.13 Board Topology**

![](tools/datasheet/assets/media/image2.png){width=6.26772in}

Views of Topology

Table 3.2.1 - Components Overview

| **Ref.**                           | **Description**                                                    |
|------------------------------------|--------------------------------------------------------------------|
| U3, U4                             | mikroBUS™ Shield                                                   |
| U5                                 | Feather Shield                                                     |
| U6                                 | Pi Pico Shield                                                     |
| U7                                 | DevKit V4 Shield                                                   |
| U8                                 | Pulsar Shield (NANO form factor)                                   |
| U9                                 | XIAO/QT Shield                                                     |
| U10                                | UNIT CH340E USB-to-Serial Shield                                   |
| SW1                                | DIP switch for selecting PD VUSB output (5V, 9V, 12V, 15V, 20V)    |
| J1                                 | USB connector for Power Delivery (PD) input                        |
| J2                                 | Terminal block for PD VUSB output (5V, 9V, 12V, 15V, 20V)          |
| J3                                 | QWIIC connector (JST 1.0 mm pitch) for I²C – HUSB238 PD controller |
| J4, J5, J6, J7, JP3, JP4, JP5, JP6 | 2.54 mm JST Gravity-compatible connector hub                       |
| J8, J9, J10, J11, J12, J13, J14    | QWIIC connectors (JST 1.0 mm pitch) for I²C                        |
| J15                                | QWIIC parallel bus connector (JST 1.0 mm pitch) for I²C            |
| JP9, JP24                          | Auxiliary 2.54 mm pins for general-purpose use                     |
| JP20, JP21, JP22, JP23             | Auxiliary connectors for I²C or SPI LCDs/displays                  |
| SW2, SW3, SW4, SW5, JP11           | General-purpose push buttons                                       |
| JP10                               | Signal header for general-purpose LEDs and WS2812B 5x5 matrix (L2) |
| J16, J17                           | Terminal blocks for relay outputs                                  |
| J18, J19                           | Terminal blocks for PWM module outputs                             |
| VR1, JP8                           | 10k trimpot for ADC applications                                   |
| LS1, JP25                          | SMD buzzer for general-purpose use                                 |
| JP8                                | Power rail supply (3.3V, 5V, GND) for external devices             |
