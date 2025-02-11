import tkinter
from tkinter import *
from tkinter import ttk

window = tkinter.Tk()
window.title("Continuous Kombucha Brewing Calculator")

tabControl = ttk.Notebook(window)
calculator = ttk.Frame(tabControl)
constants = ttk.Frame(tabControl)

tabControl.add(calculator, text='Calculator')
tabControl.add(constants, text='Constants')

tabControl.pack(expand=1, fill="both")

def update_brew(*args):
    try:
        vsl1_fw = float(vessel1_fullweight.get())
        vsl1_ew = float(vessel1_emptyweight.get())
        vsl2_fw_str = vessel2_fullweight.get()
        vsl2_ew_str = vessel2_emptyweight.get()

        if vsl2_fw_str and vsl2_ew_str:
            vsl2_fw = float(vessel2_fullweight.get())
            vsl2_ew = float(vessel2_emptyweight.get())

            if vsl1_fw>vsl1_ew and vsl2_fw>vsl2_ew:
                print("vsl1_fw:", vsl1_fw, "vsl1_ew", vsl1_ew)
                print("vsl2_fw:", vsl2_fw, "vsl2_ew", vsl2_ew)

                vsl_fw = int(vsl1_fw + vsl2_fw)
                vsl_ew = int(vsl1_ew + vsl2_ew)
                brewed_kombucha = vsl_fw - vsl_ew
                total_kvolume_finished.config(text=f"{int(brewed_kombucha)}")
                kvolume_20percent.config(text=f"{int(brewed_kombucha*0.25)}")
            elif vsl1_fw>vsl1_ew:
                vsl_fw = int(vsl1_fw)
                vsl_ew = int(vsl1_ew)
                brewed_kombucha = vsl_fw - vsl_ew
                total_kvolume_finished.config(text=f"{int(brewed_kombucha)}")
                kvolume_20percent.config(text=f"{int(brewed_kombucha*0.25)}")
            else:
                total_kvolume_finished.config(text="")
                kvolume_20percent.config(text="")
    except:
        total_kvolume_finished.config(text="Invalid Input")
        kvolume_20percent.config(text="")

    vsl1_fw = float(vessel1_fullweight.get())
    vsl2_fw = float(vessel2_fullweight.get())
    vsl_fw = int(vsl1_fw + vsl2_fw)

    vsl1_empty = float(vessel1_emptyweight.get())
    vsl2_empty = float(vessel2_emptyweight.get())
    vsl_empty = int(vsl1_empty + vsl2_empty)

    brewed_kombucha = vsl_fw - vsl_empty
    total_kvolume_finished.config(text=f"{int(brewed_kombucha)}")

frame = tkinter.Frame(window)
frame.pack()

# Finished Brewing
finished_frame = tkinter.LabelFrame(calculator, text="Finished Brew Info")
finished_frame.grid(row=0, column=0)

full_vessel_label = tkinter.Label(finished_frame, text="Full Vessel Weight (g)",)
full_vessel_label.grid(row=0, column=1)
empty_vessel_label = tkinter.Label(finished_frame, text="Empty Vessel Weight (g)",)
empty_vessel_label.grid(row=0, column=2)


default_v1_weight = tkinter.StringVar()
default_v2_weight = tkinter.StringVar()
default_v1_weight.set("500")
default_v2_weight.set("501")

vessel1_label = tkinter.Label(finished_frame, text="Vessel 1")
vessel2_label = tkinter.Label(finished_frame, text="Vessel 2")
vessel1_fullweight = tkinter.Entry(finished_frame)
vessel2_fullweight = tkinter.Entry(finished_frame)
vessel1_emptyweight = tkinter.Entry(finished_frame, textvariable=default_v1_weight)
vessel2_emptyweight = tkinter.Entry(finished_frame, textvariable=default_v2_weight)

total_kvolume_finished_label = tkinter.Label(finished_frame, text="Total Kombucha (ml)")
total_kvolume_finished = tkinter.Label(finished_frame, text="")
kvolume_20percent_label = tkinter.Label(finished_frame, text="20% Continuous Brew (ml)")
kvolume_20percent = tkinter.Label(finished_frame, text="")

num_theoretical_brew = tkinter.StringVar()

testvar = tkinter.StringVar()

vessel1_fullweight["textvariable"] = testvar
print("Testvar:", testvar)


vessel1_label.grid(row=1, column=0)
vessel2_label.grid(row=2, column=0)
vessel1_fullweight.grid(row=1, column=1)
vessel2_fullweight.grid(row=2, column=1)
vessel1_emptyweight.grid(row=1, column=2)
vessel2_emptyweight.grid(row=2, column=2)
total_kvolume_finished_label.grid(row=0,column=3)
total_kvolume_finished.grid(row=1 ,column=3, rowspan=2)
kvolume_20percent_label.grid(row=0 ,column=4)
kvolume_20percent.grid(row=1 ,column=4, rowspan=2)

vessel1_fw_update = tkinter.StringVar()
vessel1_ew_update = tkinter.StringVar(value="502")
vessel2_fw_update = tkinter.StringVar()
vessel2_ew_update = tkinter.StringVar(value="504")

vessel1_fullweight["textvariable"]  = vessel1_fw_update
vessel1_emptyweight["textvariable"] = vessel1_ew_update
vessel2_fullweight["textvariable"]  = vessel2_fw_update
vessel2_emptyweight["textvariable"] = vessel2_ew_update

vessel1_fw_update.trace("w", update_brew) # "w" means write (changes to the variable)
vessel1_ew_update.trace("w", update_brew) # "w" means write (changes to the variable)
vessel2_fw_update.trace("w", update_brew) # "w" means write (changes to the variable)
vessel2_ew_update.trace("w", update_brew) # "w" means write (changes to the variable)

for widget in finished_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Brewing
brewing_frame = tkinter.LabelFrame(calculator, text="Brewing Calculator")
brewing_frame.grid(row=1, column=0)

theoretical_brew_label = tkinter.Label(brewing_frame, text="Kombucha to Replace")
theoretical_brew_label.grid(row=0, column=0)
theoretical_brew_value = tkinter.Label(brewing_frame, text="Ingredient:")
theoretical_brew_value.grid(row=1, column=0)

# Bottling
bottling_frame = tkinter.LabelFrame(calculator, text="Bottle Calculator")
bottling_frame.grid(row=2, column=0)

total_kvolume_label = tkinter.Label(bottling_frame, text="Brewed Kombucha")
total_kvolume_label.grid(row=0, column=0)

total_kvolume_entry = tkinter.Entry(bottling_frame)
total_kvolume_entry.grid(row=1, column=0)


total_kvolume_entry["textvariable"] = num_theoretical_brew
num_theoretical_brew.trace("w", update_brew) # "w" means write (changes to the variable)

#Test Button
button = tkinter.Button(calculator, text="Submit", command="")
button.grid(row=3, column=0, sticky="news", padx=20, pady=10)

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

window.mainloop()