# gpio-osc-trigger

A Raspberry Pi script that listens to a BERM sensor on a GPIO pin and sends a random OSC message to QLC+ whenever a passage is detected. Designed for gate-triggered automated lighting.

---

## Architecture

```
Capteur BERM (GPIO 27)
       │
       ▼
 Raspberry Pi
 auto_scene.py
       │  OSC UDP (127.0.0.1:7701)
       ▼
     QLC+
  (chasers 1–5)
```

---

## How it works

1. A BERM sensor is wired to **GPIO 27** (internal pull-up enabled).
2. `auto_scene.py` continuously monitors the sensor signal.
3. On a **falling edge** (passage detected), the script randomly selects one of 5 OSC addresses (`/chaser/1` to `/chaser/5`) and sends value `255`.
4. A **2-second debounce** prevents multiple triggers for a single passage.
5. QLC+ receives the OSC message and runs the corresponding chaser.

---

## Requirements

- Raspberry Pi with Raspbian
- Python 3
- Python libraries:
  ```bash
  pip install RPi.GPIO python-osc
  ```
- QLC+ installed and configured (see [qlc_plus/](qlc_plus/))

---

## QLC+ setup

Each chaser (`/chaser/1` to `/chaser/5`) must be **bound to an OSC button** in QLC+ so it can be triggered by the incoming signal.

1. Open QLC+ and load the `.qxw` file from the [qlc_plus/](qlc_plus/) folder.
2. Under **Inputs/Outputs**, enable the OSC plugin listening on port `7701`.
3. For each chaser, assign the OSC button to address `/chaser/N` (value `255` = trigger).

---

## Usage

```bash
python3 auto_scene.py
```

Stop cleanly with `Ctrl+C` — GPIO is released automatically.

---

## Files

| File | Description |
|---|---|
| `auto_scene.py` | Main script — BERM sensor detection + OSC dispatch |
| `qlc_plus/` | QLC+ configuration files (`.qxw`) |
