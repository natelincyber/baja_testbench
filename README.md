# Baja SAE Hardware‑in‑the‑Loop (HIL) Testbench
## Spec
The goal of the Testcases Team is to design, document, and implement a comprehensive suite of automated tests that validate the behavior of drivetrain-related electromechanical mock subsystems (ECVT actuator and center‑lock clutch) within the HIL environment. These tests ensure that software, controls, and communication layers behave correctly before vehicle integration.

## Updates
### WEEK 1: Initial Test Case Concepts

* **Actuator Response Validation**: Make sure the mock ECVT actuator reaches commanded positions within acceptable tolerance and response time.
* **Center-Lock Engagement Test**: Verify the dog teeth engage and disengage reliably under varying simulated loads.
* **O-Drive Fault Tolerance**: Inject invalid commands, noisy signals, or communication delays to confirm safe fallback behavior.
* **Sensor Simulation Sanity Checks**: Confirm simulated RPM, wheel speed, and temperature values follow expected patterns.
* **Telemetry Data Integrity**: Validate that ESP32 data packets arrive without corruption or drops under continuous operation.
---

## Timeline

*Note: This timeline is flexible and depends heavily on the progress of the hardware, controls, and electrical teams. Milestones may shift as other subsystems are developed and integrated.*

### Weeks 1–3: Test Case ideation

* Define all major test categories for drivetrain subsystems.
* Identify edge cases, fault conditions, and safety constraints.
* Draft the complete test suite outline.

### Weeks 4–10: Test Case Implementation

* Build the Python-based test harness on the Raspberry Pi.
* Implement actuator tests for ECVT and center-lock mock systems.
* Integrate O-Drive library usage within the test framework.
* Develop full sensor simulation suite (RPM, wheel speed, temperature, etc.).
* Implement fault-injection and robustness tests.
* Conduct incremental integration tests as other teams finish components.
* Finalize documentation and validation criteria.
---

## Documentation

Add links to relevant documentation as they become available:
