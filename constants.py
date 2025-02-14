import tkinter
from tkinter import *
from tkinter import ttk
from main import constants

#Constants

brewVesselConstant_frame = tkinter.LabelFrame(constants, text="Brewing Vessel Info")
brewVesselConstant_frame.grid(row=0, column=0)

brewVessel_name = tkinter.Label(brewVesselConstant_frame, text="Vessel Name")
brewVessel_name.grid(row=0, column=0)
brewVessel_unit = tkinter.Label(brewVesselConstant_frame, text="Vessel Weight (g)")
brewVessel_unit.grid(row=0, column=1)

testbrewconstant1 = tkinter.StringVar(value="502")
testbrewconstant2 = tkinter.StringVar(value="504")

brewVesselConstant_v1_label = tkinter.Label(brewVesselConstant_frame, text="Vessel 1")
brewVesselConstant_v1_label.grid(row=1, column=0)
brewVesselConstant_v1_value = tkinter.Label(brewVesselConstant_frame, textvariable=testbrewconstant1)
brewVesselConstant_v1_value.grid(row=1, column=1)

brewVesselConstant_v2_label = tkinter.Label(brewVesselConstant_frame, text="Vessel 2")
brewVesselConstant_v2_label.grid(row=2, column=0)
brewVesselConstant_v2_value = tkinter.Label(brewVesselConstant_frame, textvariable=testbrewconstant2)
brewVesselConstant_v2_value.grid(row=2, column=1)

#Test Button
button = tkinter.Button(calculator, text="Submit", command="")
button.grid(row=3, column=0, sticky="news", padx=20, pady=10)