import tkinter as tk
from tkinter import ttk
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

team="GRIPS"
broker_address="localhost"
client = mqtt.Client(CallbackAPIVersion.VERSION1, "mps_gui")
client.connect(broker_address, 1883)

def dispose_base(side: str, color: str):
    client.publish(team + "/prepare/BS/" + side, color)

def retrieve_cap(station: str):
    client.publish(team + "/prepare/" + station, "RetrieveCap")

def mount_cap(station: str):
    client.publish(team + "/prepare/" + station, "MountCap")
def mount_ring(station: str, color: str):
    client.publish(team + "/prepare/" + station, color)

def prepare_ds(orderId: str):
    client.publish(team + "/prepare/DS", orderId)


# Create the main application window
root = tk.Tk()

root.title("Button Click GUI")

# Create a tab control
tab_control = ttk.Notebook(root)

# Create tabs for different groups
groups = ["CS1", "CS2", "RS1", "RS2", "BS", "DS"]
tabs = {}
for group in groups:
    tabs[group] = ttk.Frame(tab_control)
    tab_control.add(tabs[group], text=group)

# Pack the tab control
tab_control.pack(expand=1, fill="both")

# Create RetrieveCap and MountCap buttons for CS1 group
retrieve_cap_button_cs1 = tk.Button(tabs["CS1"], text="RetrieveCap", command=lambda: retrieve_cap("CS1"))
retrieve_cap_button_cs1.pack(pady=10)
mount_cap_button_cs1 = tk.Button(tabs["CS1"], text="MountCap", command=lambda: mount_cap("CS1"))
mount_cap_button_cs1.pack(pady=10)

# Create RetrieveCap and MountCap buttons for CS2 group
retrieve_cap_button_cs2 = tk.Button(tabs["CS2"], text="RetrieveCap", command=lambda: retrieve_cap("CS2"))
retrieve_cap_button_cs2.pack(pady=10)
mount_cap_button_cs2 = tk.Button(tabs["CS2"], text="MountCap", command=lambda: mount_cap("CS2"))
mount_cap_button_cs2.pack(pady=10)

# Create MountOrange and MountGreen buttons for RS1 group
mount_orange_button_rs1 = tk.Button(tabs["RS1"], text="MountOrange", command=lambda: mount_ring("RS1", "Orange"))
mount_orange_button_rs1.pack(pady=10)
mount_green_button_rs1 = tk.Button(tabs["RS1"], text="MountGreen", command=lambda: mount_ring("RS1", "Green"))
mount_green_button_rs1.pack(pady=10)

# Create MountYellow and MountBlue buttons for RS2 group
mount_yellow_button_rs2 = tk.Button(tabs["RS2"], text="MountYellow", command=lambda: mount_ring("RS2", "Yellow"))
mount_yellow_button_rs2.pack(pady=10)
mount_blue_button_rs2 = tk.Button(tabs["RS2"], text="MountBlue", command=lambda: mount_ring("RS2", "Blue"))
mount_blue_button_rs2.pack(pady=10)

# Create Silver, Red, and Black buttons for BS group
mount_silver_button_bs = tk.Button(tabs["BS"], text="Silver", command=lambda: dispose_base("output", "Silver"))
mount_silver_button_bs.pack(pady=10)
mount_red_button_bs = tk.Button(tabs["BS"], text="Red", command=lambda: dispose_base("output", "Red"))
mount_red_button_bs.pack(pady=10)
mount_black_button_bs = tk.Button(tabs["BS"], text="Black", command=lambda: dispose_base("output", "Black"))
mount_black_button_bs.pack(pady=10)

# Create a text field and a Prepare button for DS group
text_field = tk.Entry(tabs["DS"])
text_field.pack(pady=10)
prepare_button_ds = tk.Button(tabs["DS"], text="Prepare", command=lambda: prepare_ds(text_field.get()))
prepare_button_ds.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()