import tkinter
from tkinter import *
from tkinter import ttk


class VesselEntry:
    def __init__(self, vessel_name, weight_empty):
        self.name = vessel_name
        self.full_weight_var = tkinter.StringVar()
        self.weight_empty = weight_empty
        self.error_var = tkinter.StringVar()

        self.label = tkinter.Label(finished_frame, text=self.name)
        self.full_weight_entry = tkinter.Entry(finished_frame, textvariable=self.full_weight_var)
        self.empty_weight_entry = tkinter.Entry(finished_frame, textvariable=self.weight_empty) # Set the default value
        self.error_label = tkinter.Label(finished_frame, textvariable=self.error_var)

    def grid(self, row):
        self.label.grid(row=row, column=0)
        self.full_weight_entry.grid(row=row, column=1)
        self.empty_weight_entry.grid(row=row, column=2)
        self.error_label.grid(row=row, column=3)




root = tkinter.Tk()
root.title = ("Test Window")
#calculator = BrewCalculator(root)

# Create the finished_frame *outside* the loop
finished_frame = tkinter.LabelFrame(root, text="Finished Brew Info")
finished_frame.grid(row=0, column=0)

full_vessel_label = tkinter.Label(finished_frame, text="Full Vessel Weight (g)")
full_vessel_label.grid(row=0, column=1)
empty_vessel_label = tkinter.Label(finished_frame, text="Empty Vessel Weight (g)")
empty_vessel_label.grid(row=0, column=2)
error_label = tkinter.Label(finished_frame, text="Error")
error_label.grid(row=0, column=3)

vessel_array = []

vessel_array.append(VesselEntry("BrewMonk 1", "400"))
vessel_array.append(VesselEntry("BrewMonk 2", "420"))
vessel_array.append(VesselEntry("Glass Jar", "360"))

for i in range (0, len(vessel_array)):
    vessel_array[i].grid(i + 1)  # Start grid at row 1

    print(vessel_array[i].name, "Empty(g):", vessel_array[i].weight_empty)


    print(vessel_array[i].name, "Empty(g):", vessel_array[i].weight_empty)


root.mainloop()