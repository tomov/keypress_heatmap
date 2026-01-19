# Keyboard Heatmap Generator

A tool for logging physical keypresses and generating visual heatmaps of keyboard usage. Currently configured for a Kinesis Advantage2 with Dvorak layout.

## Prerequisites

- Ubuntu/Debian Linux
- Python 3.x

## Installation

### 1. Install system dependencies

```bash
sudo apt update
sudo apt install evtest python3-pip
```

### 2. Install Python dependencies

**Option A: Using conda (recommended)**

```bash
conda create -n keylogger python=3.11
conda activate keylogger
pip install -r requirements.txt
```

**Option B: Using pip directly**

```bash
pip install -r requirements.txt
```

### 3. Add your user to the input group

To read input devices without root privileges, add your user to the `input` group:

```bash
sudo usermod -a -G input $USER
```

**Log out and log back in** for the group change to take effect.

## Finding Your Keyboard Device

The keylogger reads from a specific input device file. You need to identify which `/dev/input/eventX` corresponds to your keyboard.

### Using evtest

1. Run evtest as root:

```bash
sudo evtest
```

2. You'll see a list of available input devices:

```
/dev/input/event0:  Power Button
/dev/input/event1:  Sleep Button
/dev/input/event2:  Video Bus
...
/dev/input/event15: Kinesis Advantage2 Keyboard
...
```

3. Find your keyboard in the list and note the device path (e.g., `/dev/input/event15`)

4. Select it by entering the number. Press some keys to verify it's the correct device - you should see output like:

```
Event: time 1234567890.123456, type 1 (EV_KEY), code 30 (KEY_A), value 1
Event: time 1234567890.234567, type 1 (EV_KEY), code 30 (KEY_A), value 0
```

5. Press `Ctrl+C` to exit evtest

### Configure the device path

Edit `keylogger.py` and update the `DEVICE_PATH` variable:

```python
DEVICE_PATH = '/dev/input/event15'  # Replace with your device
```

## Usage

### Running the Keylogger

```bash
python3 keylogger.py
```

Keypresses are logged to `physical_keys.log` with timestamps.

### Generating the Heatmap

After collecting data, generate a visualization:

```bash
python3 generate_heatmap.py
```

This creates `kinesis_heatmap.png` showing key usage frequency.

## Files

| File | Description |
|------|-------------|
| `keylogger.py` | Captures and logs keypresses from input device |
| `generate_heatmap.py` | Creates heatmap visualization from log data |
| `kinesis_layout.txt` | ASCII keyboard layout for heatmap positioning |
| `physical_keys.log` | Log file with timestamped keypresses |
| `kinesis_heatmap.png` | Generated heatmap image |

## Customization

### Different Keyboard Layouts

To use a different keyboard layout:

1. Edit `kinesis_layout.txt` with your ASCII keyboard representation
2. Update `KEY_MAP` in `generate_heatmap.py` to match your key labels

## Troubleshooting

**"Permission denied" error:**
- Ensure you've added your user to the `input` group (see Installation step 3)
- Make sure you logged out and back in after adding the group

**"Device not found" error:**
- Re-run `sudo evtest` to find the correct device path
- Device paths can change after reboots or when plugging/unplugging devices

**No events in evtest:**
- Make sure you selected the correct device (keyboards may have multiple entries)
- Try selecting a different event number for your keyboard
