import tkinter

class VesselEntry:
    def __init__(self, frame, vessel_number):
        self.vessel_number = vessel_number
        self.label = tkinter.Label(frame, text=f"Vessel {vessel_number}")
        self.full_weight_var = tkinter.StringVar()
        self.empty_weight_var = tkinter.StringVar(value="500") #Default value is 500
        self.full_weight_entry = tkinter.Entry(frame, textvariable=self.full_weight_var)
        self.empty_weight_entry = tkinter.Entry(frame, textvariable=self.empty_weight_var)
        self.error_var = tkinter.StringVar()
        self.error_label = tkinter.Label(frame, textvariable=self.error_var)

    def grid(self, row, column_start):
        self.label.grid(row=row, column=0)
        self.full_weight_entry.grid(row=row, column=column_start)
        self.empty_weight_entry.grid(row=row, column=column_start + 1)
        self.error_label.grid(row=row, column=column_start + 2)

class BrewCalculator(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        master.title("Kombucha Calculator")
        self.grid()

        self.vessel_entries = 0
        self.num_vessels = 2 # Start with 2 vessels

        self.create_widgets()

    def create_widgets(self):
        # Finished Brewing Frame
        finished_frame = tkinter.LabelFrame(self, text="Finished Brew Info")
        finished_frame.grid(row=0, column=0)

        full_vessel_label = tkinter.Label(finished_frame, text="Full Vessel Weight (g)")
        full_vessel_label.grid(row=0, column=1)
        empty_vessel_label = tkinter.Label(finished_frame, text="Empty Vessel Weight (g)")
        empty_vessel_label.grid(row=0, column=2)

        for i in range(self.num_vessels):
            vessel = VesselEntry(finished_frame, i + 1)
            vessel.grid(i + 1, 0)  # Start grid at row 1

            self.vessel_entries.append(vessel)
            vessel.full_weight_var.trace("w", self.update_brew)
            vessel.empty_weight_var.trace("w", self.update_brew)
            vessel.error_var.trace("w", self.update_brew) # Trace error variable too

        total_kvolume_finished_label = tkinter.Label(finished_frame, text="Total Kombucha (ml)")
        total_kvolume_finished_label.grid(row=0, column=4)
        self.total_kvolume_finished = tkinter.Label(finished_frame, text="")
        self.total_kvolume_finished.grid(row=1, column=4, rowspan=self.num_vessels)

        kvolume_20percent_label = tkinter.Label(finished_frame, text="20% Continuous Brew (ml)")
        kvolume_20percent_label.grid(row=0, column=5)
        self.kvolume_20percent = tkinter.Label(finished_frame, text="")
        self.kvolume_20percent.grid(row=1, column=5, rowspan=self.num_vessels)

    def update_brew(self, *args):
        total_full = 0
        total_empty = 0

        for vessel in self.vessel_entries:
            try:
                full = float(vessel.full_weight_var.get())
                empty = float(vessel.empty_weight_var.get())

                if full <= empty: # Error if full weight is not greater than empty weight
                    vessel.error_var.set("Full weight must be greater than empty weight")
                else:
                    vessel.error_var.set("") # Clear error if valid

                total_full += full
                total_empty += empty

            except ValueError:
                vessel.error_var.set("Invalid input") # Error message for invalid input
                # Handle error (e.g., set error message)
                pass # If there is bad input, don't stop the code

        brewed_kombucha = total_full - total_empty

        if brewed_kombucha > 0: # Only display if there is a valid kombucha amount
            self.total_kvolume_finished.config(text=f"{int(brewed_kombucha)}")
            self.kvolume_20percent.config(text=f"{int(brewed_kombucha * 0.20)}")
        else:
            self.total_kvolume_finished.config(text="")
            self.kvolume_20percent.config(text="")


root = tkinter.Tk()
calculator = BrewCalculator(root)
root.mainloop()