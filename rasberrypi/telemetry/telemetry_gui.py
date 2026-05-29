# telemetry/telemetry_gui.py

```python
import tkinter as tk
from tkinter import ttk
import serial
import json
from telemetry_parser import parse_telemetry

SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 115200

ser = serial.Serial(
    SERIAL_PORT,
    BAUD_RATE,
    timeout=1
)

root = tk.Tk()

root.title("UAV Ground Control Station")
root.geometry("1024x600")

title = tk.Label(
    root,
    text="LoRa UAV Ground Control Station",
    font=("Arial", 20, "bold")
)

title.pack(pady=10)

telemetry_frame = tk.Frame(root)
telemetry_frame.pack(pady=20)

labels = {}

fields = [
    "Latitude",
    "Longitude",
    "Altitude",
    "Roll",
    "Pitch",
    "Yaw",
    "Battery",
    "RSSI",
    "FlightMode"
]

for field in fields:

    frame = tk.Frame(telemetry_frame)
    frame.pack(anchor="w")

    label_name = tk.Label(
        frame,
        text=f"{field}: ",
        font=("Arial", 14)
    )

    label_name.pack(side=tk.LEFT)

    label_value = tk.Label(
        frame,
        text="---",
        font=("Arial", 14, "bold")
    )

    label_value.pack(side=tk.LEFT)

    labels[field] = label_value


def update_telemetry():

    if ser.in_waiting:

        line = ser.readline().decode().strip()

        telemetry = parse_telemetry(line)

        if telemetry:

            labels["Latitude"].config(
                text=telemetry["latitude"]
            )

            labels["Longitude"].config(
                text=telemetry["longitude"]
            )

            labels["Altitude"].config(
                text=telemetry["altitude"]
            )

            labels["Roll"].config(
                text=telemetry["roll"]
            )

            labels["Pitch"].config(
                text=telemetry["pitch"]
            )

            labels["Yaw"].config(
                text=telemetry["yaw"]
            )

            labels["Battery"].config(
                text=telemetry["batteryVoltage"]
            )

            labels["RSSI"].config(
                text=telemetry["rssi"]
            )

            labels["FlightMode"].config(
                text=telemetry["flightMode"]
            )

    root.after(100, update_telemetry)


update_telemetry()

root.mainloop()
```

---

# telemetry/telemetry_parser.py

```python
import json


def parse_telemetry(data):

    try:

        telemetry = json.loads(data)

        return telemetry

    except Exception as e:

        print("Telemetry Parse Error:", e)

        return None
```

---

# telemetry/gps_display.py

```python
import folium
import webbrowser

MAP_FILE = "uav_map.html"


def generate_map(latitude, longitude):

    uav_map = folium.Map(
        location=[latitude, longitude],
        zoom_start=16
    )

    folium.Marker(
        [latitude, longitude],
        popup="UAV Position"
    ).add_to(uav_map)

    uav_map.save(MAP_FILE)

    webbrowser.open(MAP_FILE)


if __name__ == "__main__":

    generate_map(
        28.6139,
        77.2090
    )
```

---

# telemetry/battery_monitor.py

```python
def battery_percentage(voltage):

    min_voltage = 9.0
    max_voltage = 12.6

    percentage = (
        (voltage - min_voltage)
        /
        (max_voltage - min_voltage)
    ) * 100

    percentage = max(
        0,
        min(100, percentage)
    )

    return round(percentage, 2)


if __name__ == "__main__":

    voltage = 11.4

    print(
        "Battery:",
        battery_percentage(voltage),
        "%"
    )
```

---

# mavlink/

```python
