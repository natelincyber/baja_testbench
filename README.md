
## **Test Suites & Subsystem Integration**

Each test suite validates a specific drivetrain subsystem through the HIL environment. Tests run through the FastAPI test runner and interface with hardware via O-Drive motor drivers, actuator mechanisms, CAN simulation, and sensor emulation modules.

---

### **Actuator Response Validation (ECVT System)**

**Purpose:** Validate that the mock ECVT actuator reaches commanded belt positions within a defined tolerance and timing window.

**How the test works:**

1. The backend sends position commands over UART/CAN to the O-Drive driving the actuator.
2. Encoder feedback is streamed over telemetry to the test runner.
3. Error metrics (overshoot, settle time, steady-state error) are computed.
4. Results are logged and graphed via frontend.

**Subsystems Integrated:**

| Component                   | Team Responsible      | Role                             |
| --------------------------- | --------------------- | -------------------------------- |
| ECVT actuator mock hardware | Drivetrain/Mechanical | Provides physical movement       |
| O-Drive                     | Controls/Electrical   | Executes motor position commands |
| Encoder feedback lines      | Controls              | Supplies position measurements   |
| Telemetry over ESP32/WiFi   | Embedded              | Streams live data                |

**Dependencies:**

* ODrive Python library
* Encoder calibration values
* Power stage + mechanical load present
* Pi → ODrive comms functioning

**Validated Functionality:**

* Closed-loop control correctness
* Position accuracy under dynamic setpoints
* Safety cutout triggers on runaway conditions

---

### ** Center-Lock Engagement Test**

**Purpose:** Ensure mechanical dog clutch engages/disengages reliably under simulated torque loads.

**How the test works:**

1. Mock torque input is provided by hardware load emulator.
2. Actuator drives engagement motion.
3. Limit switches + encoder verify engagement state.
4. Test cycles through various load profiles (idle, ramp, shock).

**Subsystems Integrated:**

| Component                         | Team                    | Role                          |
| --------------------------------- | ----------------------- | ----------------------------- |
| Center-lock clutch mock           | Drivetrain              | Provides engagement mechanics |
| Load emulator (motor or brake)    | Mechanical + Electrical | Simulates engine torque       |
| Position sensors / limit switches | Controls                | Detect slip/failure           |
| Data capture pipeline             | Software                | Logs force vs engagement time |

**Dependencies:**

* Load emulator must exist and be controllable
* Sensor inputs must be mapped
* Safety interlocks configured

**Validated Functionality:**

* Engagement latency
* Slip vs torque threshold
* Ability to fail safe if jammed or misaligned

---

### **### O-Drive Fault Tolerance Tests**

**Purpose:** Ensure unsafe commands and noisy input do not produce uncontrolled behavior.

**Faults Injected:**

| Fault                    | Expected System Behavior |
| ------------------------ | ------------------------ |
| Invalid velocity command | Ignore + log error       |
| Dropped packets          | Hold last safe setpoint  |
| Corrupted CRC            | Reject + safe mode       |
| Latency spikes           | Graceful degradation     |

**Subsystems Integrated:**

* ODrive bus
* Safety controller
* Test runner injection hooks

**Dependencies:**

* CAN/UART monitor
* Software hooks to override payloads

**Validated Functionality:**

* No runaway motion
* Safe fallback modes
* Resilient command parsing

---

### **Sensor Simulation Sanity Tests**

**Purpose:** Verify simulated drivetrain signals mimic real-world behavior so higher-level software can be tested without the real vehicle.

**Signals Simulated:**

| Signal       | Source                      | Consumer                   |
| ------------ | --------------------------- | -------------------------- |
| Engine RPM   | Pi → DAC/CAN                | ECU controls logic         |
| Wheel speed  | Software waveform generator | Telemetry + traction logic |
| Temp sensors | GPIO ADC mock               | Thermal constraints        |

**How the test works:**

* Pi generates waveforms representing acceleration, stall, braking profiles.
* Verification script compares generated signals to expected model curves.

**Dependencies:**

* CAN injection hardware
* Lookup tables for RPM curves
* Calibration files

**Validated Functionality:**

* Correct scaling
* Smooth transitions
* PID loop stability using synthetic feedback

---

### **Telemetry Integrity Test**

**Purpose:** Validate that the telemetry stack can stream high-frequency data without corruption or packet loss.

**How the test works:**

* Synthetic telemetry streamed continuously
* Pi counts checksum errors + throughput metrics
* UI plots packet statistics

**Dependencies:**

* ESP32 or direct Pi Wi-Fi
* WebSockets enabled
* Logging container running

**Failures Detected:**

* Dropped packets under load
* Latency > 50ms
* Buffering overflow conditions

---

## **Code Execution Flow**

```
User Runs Test (Frontend UI)
         │
         ▼
FastAPI REST Endpoint (/tests/run)
         │
         ▼
Test Runner executes Python test module
         │
         ├── Commands actuators (Odrive)
         ├── Reads sensors (mock + real)
         ├── Injects faults
         ▼
Results streamed via WebSockets → UI
Logs stored for replay + debugging
```

---

## **First Deliverable — FastAPI Server + Network Bridging Setup**

The first milestone for the HIL Testbench project is establishing a network-accessible backend running on the Raspberry Pi and serving system health diagnostics through FastAPI. This enables remote access, telemetry streaming, and future test execution.

### **1️⃣ Networking Setup & SSH Access**

The Raspberry Pi is assigned a **static IP** on the bridged network, allowing reliable SSH access even when connected to university Wi-Fi (Eduroam).

📌 **Connection Path**

```
Eduroam (Host Laptop Wi-Fi)
        │  (bridge)
        ▼
Host PC Ethernet Port
        │
        ▼
Raspberry Pi (eth0)
```

The host machine shares its network connection with the Pi through **Windows network bridging**, exposing the Pi to the LAN as if directly connected.

### **Raspberry Pi Network Configuration**

The Pi is configured with a static IP:

```bash
ip a show eth0
```

Output:

```
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether b8:27:eb:58:dc:cf brd ff:ff:ff:ff:ff:ff
    inet 192.168.137.50/24 brd 192.168.137.255 scope global noprefixroute eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::ff97:5ec0:9060:4761/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
```

📌 **Static IP Chosen:** `192.168.137.50`
📌 **Use Case:** SSH access + hosting web dashboard
📌 **Verification:** Pi reachable from host using:

```bash
ssh natel@192.168.137.50
```

This confirms the Pi is directly accessible on the bridged network even when the host is connected to Eduroam.

---

### **2️⃣ FastAPI Server (Initial Implementation)**

The first software deliverable is a FastAPI app that runs on Raspberry Pi and exposes system performance data.

**Purpose:**
Provide a web-hosted *System Health Dashboard* that reports:

| Metric                        | Example Sources                          |
| ----------------------------- | ---------------------------------------- |
| CPU load & thermal throttling | `/proc/cpuinfo`, `vcgencmd measure_temp` |
| RAM usage                     | `psutil`                                 |
| Voltage levels                | `vcgencmd get_throttled`                 |
| Network stats                 | `ifconfig`, `socket`, `/sys/class/net/`  |
| Disk IO + space               | `df`, `iostat`                           |

#### **Endpoint Behavior**

| Endpoint            | Method | Description                                 |
| ------------------- | ------ | ------------------------------------------- |
| `/health`           | GET    | Returns structured JSON with system metrics |
| `/dashboard`        | GET    | Serves frontend UI widget                   |
| `/ws/system-stream` | WS     | Live updating stats feed                    |

#### ** Example (Backend)**

```python
from fastapi import FastAPI
import psutil, subprocess

app = FastAPI()

@app.get("/health")
def get_health():
    return {
        "cpu_usage": psutil.cpu_percent(),
        "ram": psutil.virtual_memory()._asdict(),
        "temp": subprocess.getoutput("vcgencmd measure_temp"),
        "voltage": subprocess.getoutput("vcgencmd get_throttled"),
        "net": psutil.net_io_counters()._asdict()
    }
```

---

### **3️⃣ Frontend System Health Widget**

The Pi hosts a lightweight web dashboard served by FastAPI using static file mounting.

#### **Example UI Behavior:**

* Displays neat real-time cards for each metric
* Uses JS WebSocket stream to auto-refresh
* Future-ready component to integrate drivetrain telemetry

#### **UI Mock-up (Planned Layout)**

```
┌─────────────────────────────────────────┐
│       Raspberry Pi System Status        │
├─────────────────────────────────────────┤
│ CPU: 24% @ 1.5GHz │ Temp: 47.3°C        │
│ RAM: 612MB / 4096MB                     │
│ Voltage: OK (no throttling)             │
│ Network: 3.2 Mbps up / 8.1 Mbps down    │
└─────────────────────────────────────────┘
```

---
