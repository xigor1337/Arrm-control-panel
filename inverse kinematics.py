import math
import tkinter as tk
import serial
import time
import numpy as np

arduino = serial.Serial('COM4', 9600, timeout=1)
time.sleep(2)

inputs = []
labels = []

previous_values = [90, 90, 90, 90, 90, 70]
sliders = []

root = tk.Tk()
root.title("Big arm control panel")
root.geometry("800x600")

for i in range(1):
    frame = tk.Frame(root)
    frame.pack(pady=5)

    prev_label = tk.Label(frame, text=f"Previous: {previous_values[i]}")
    prev_label.pack(side="left")
    labels.append(prev_label)

    slider = tk.Scale(frame, from_=1, to=24, orient="horizontal")
    slider.set(20)
    slider.pack(side="left")
    inputs.append(slider)

def move_to_position():
    rotation = 90
    r = inputs[0].get()
    lost1 = 90
    lost2 = 70

    arm = 12
    distance = 22

    b = math.sqrt(distance**2 + r**2)
    print("b =", b)

    Pabc = (distance * r) / 2
    print("Pabc =", Pabc)

    b1 = (b - arm) / 2
    print("b1 =", b1)

    h = math.sqrt(arm**2 - b1**2)
    print("h =", h)

    Pafe = (b1 * h) / 2
    print("Pafe =", Pafe)

    Pgcd = (b1 * h) / 2
    print("Pgcd =", Pgcd)

    alfa1 = round(math.asin((2 * Pabc) / (b * distance)) * (180 / math.pi))
    print("alfa1 =", alfa1)

    alfa2 = round(math.asin((2 * Pafe) / (b1 * arm)) * (180 / math.pi))
    print("alfa2 =", alfa2)

    alfa = alfa1 + alfa2
    print("alfa =", alfa)

    beta = 180 - alfa2 - 90
    print("beat =", beta)

    gamma = 180 - alfa2 - 90
    print("gamma =", gamma)

    print(previous_values, [rotation, alfa, revers_angle(beta), lost1, gamma, lost2])
    send_to_arduino(previous_values, [rotation, alfa, revers_angle(beta), lost1, gamma, lost2])

send_button = tk.Button(root, text="Send to Arduino", command=move_to_position)
send_button.pack(pady=30)

def revers_angle(angle):
    return 180 - angle

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
