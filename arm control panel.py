import tkinter as tk
import serial
import time

arduino = serial.Serial('COM4', 9600, timeout=1)
time.sleep(2)

inputs = []
labels = []

def send_slider_to_arduino():
    data = []
    for i in range(6):
        new_value = inputs[i].get()
        pre_value = previous_values[i]
        data.append(f"{pre_value},{new_value}")
        previous_values[i] = new_value
        labels[i].config(text=f"Previous: {previous_values[i]}")

    message = ";".join(data) + "\n"
    print("\n", message)
    arduino.write(message.encode())


previous_values = [90, 90, 90, 90, 90, 70]

root = tk.Tk()
root.title("Big arm control panel")
root.geometry("800x600")

for i in range(6):
    frame = tk.Frame(root)
    frame.pack(pady=5)

    prev_label = tk.Label(frame, text=f"Previous: {previous_values[i]}")
    prev_label.pack(side="left")
    labels.append(prev_label)

    slider = tk.Scale(frame, from_=0 if i < 5 else 30, to=180 if i < 5 else 70, orient="horizontal")
    slider.set(previous_values[i])
    slider.pack(side="left")
    inputs.append(slider)

send_button = tk.Button(root, text="Send to Arduino", command=send_slider_to_arduino)
send_button.pack(pady=30)

# section about movement learning
position_locations = []
position_buttons = []

def remember_position(i):
    position_locations[i-1] = previous_values.copy()
    print(position_locations)

# small servo 0,15 s/60° -with weight
# big servo 0,2 s/60°
# 0,2s / 60° = 0,0033333333333333
# [56, 90, 90, 90, 90, 70] <- input "positions1" example
# [117, 90, 90, 90, 90, 70] <- input "positions2" example
def wait_time_calculation(positions1, positions2):
    speed = 0.004 + 0.02  # speed of a servo + delay
    wait_time = 0
    for i in range(6):
        if positions1[i] > positions2[i]:
            wait_time += speed * (positions1[i] - positions2[i])
        elif positions1[i] < positions2[i]:
            wait_time += speed * (positions2[i] - positions1[i])
    print("Wait time is =", wait_time)
    return wait_time

def send_to_arduino(positions1, positions2):
    data = []
    for i in range(len(positions1)):
        pre_value = positions1[i]
        new_value = positions2[i]
        data.append(f"{pre_value},{new_value}")
        previous_values[i] = new_value
        labels[i].config(text=f"Previous: {previous_values[i]}")

    message = ";".join(data) + "\n"
    print(message)
    arduino.write(message.encode())

def start_positional_movement():
    loops = 1
    send_to_arduino(previous_values, position_locations[0])
    time.sleep(wait_time_calculation(previous_values, position_locations[0]))
    positional_movement(loops)

def positional_movement(loops):
    for i in range(len(position_locations)):
        if i == (len(position_locations)-1):
            send_to_arduino(position_locations[i], position_locations[0])
            time.sleep(wait_time_calculation(position_locations[i], position_locations[0]))
        else:
            send_to_arduino(position_locations[i], position_locations[i+1])
            time.sleep(wait_time_calculation(position_locations[i], position_locations[i+1]))
    if loops == amount.get():
        pass
    else:
        loops += 1
        position_locations(loops)

position_frame = tk.Frame(root)
position_frame.pack(pady=5)

for i in range(1, 4):
    position_button = tk.Button(position_frame, text=f"Position {i}", command=lambda i=i: remember_position(i))
    position_button.pack(side="left")
    position_buttons.append(position_button)
    position_locations.append("none")

amount = tk.Scale(root, from_=1, to=10, orient="horizontal")
amount.pack(pady=5)

position_button = tk.Button(root, text="Positional movement", command=start_positional_movement)
position_button.pack(pady=5)

root.mainloop()
