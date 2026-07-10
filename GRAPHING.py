import io
import time

import matplotlib.pyplot as plt
import pandas as pd
import paramiko

HOST = "192.168.18.13"
PORT = 22
USERNAME = "pi"
PASSWORD = ""          # Set password here
REMOTE_FILE = "/home/pi/1.xlsx"
CHECK_INTERVAL = 300   # 5 minutes


def read_last_row():
    transport = paramiko.Transport((HOST, PORT))
    transport.connect(username=USERNAME, password=PASSWORD)
    sftp = paramiko.SFTPClient.from_transport(transport)
    with sftp.open(REMOTE_FILE, "rb") as f:
        data = f.read()
    sftp.close()
    transport.close()
    df = pd.read_excel(io.BytesIO(data))
    return df.iloc[-1]


def update_graphs():
    ax1.clear()
    ax2.clear()

    ax1.plot(times, temp_in, color="blue", marker="o", linewidth=2, label="Temp In")
    ax1.plot(times, temp_out, color="red", marker="o", linewidth=2, label="Temp Out")
    ax1.set_title("Temp in/out", fontsize=14, fontweight="bold")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Temperature (°C)")
    ax1.grid(True)
    ax1.legend()

    ax2.plot(times, humid_in, color="blue", marker="o", linewidth=2, label="Hum. In")
    ax2.plot(times, humid_out, color="red", marker="o", linewidth=2, label="Hum. Out")
    ax2.set_title("Humid. in/out", fontsize=14, fontweight="bold")
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Humidity (%)")
    ax2.grid(True)
    ax2.legend()

    ax1.tick_params(axis="x", rotation=45)
    ax2.tick_params(axis="x", rotation=45)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.draw()
    plt.pause(0.1)


plt.ion()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
fig.canvas.manager.set_window_title("Temperature & Humidity Monitor")
fig.suptitle("Indoor / Outdoor Environment Monitoring",
             fontsize=16, fontweight="bold")

times = []
temp_in = []
temp_out = []
humid_in = []
humid_out = []

row = read_last_row()
last_timestamp = str(row.iloc[1])

times.append(last_timestamp)
temp_in.append(float(row.iloc[2]))
temp_out.append(float(row.iloc[4]))
humid_in.append(float(row.iloc[5]))
humid_out.append(float(row.iloc[6]))

update_graphs()

print("Monitoring started...")

while True:
    time.sleep(CHECK_INTERVAL)
    try:
        row = read_last_row()
        timestamp = str(row.iloc[1])

        if timestamp != last_timestamp:
            last_timestamp = timestamp

            times.append(timestamp)
            temp_in.append(float(row.iloc[2]))
            temp_out.append(float(row.iloc[4]))
            humid_in.append(float(row.iloc[5]))
            humid_out.append(float(row.iloc[6]))

            # Keep last 100 points
            if len(times) > 100:
                times = times[-100:]
                temp_in = temp_in[-100:]
                temp_out = temp_out[-100:]
                humid_in = humid_in[-100:]
                humid_out = humid_out[-100:]

            update_graphs()
            print("New data:", timestamp)
        else:
            print("No new row.")

    except Exception as e:
        print("Error:", e)
