import tkinter
from tkinter import *
from tkinter import ttk
import sqlite3

#========================#
# Initialise Tkinter GUI
#========================#

# Start Tkinter Window & Name it
window = tkinter.Tk()
window.title("Continuous Kombucha Brewing Calculator")

# Start Tabs
tabControl = ttk.Notebook(window)
calculator = ttk.Frame(tabControl)
constants = ttk.Frame(tabControl)
database_tab = ttk.Frame(tabControl)

# Name New Tabs
tabControl.add(calculator, text='Calculator')
tabControl.add(constants, text='Constants')
tabControl.add(database_tab, text='Vessels')

tabControl.pack(expand=1, fill="both")

class FinishedBrewInfo():
    def __init__(self, eweight):
        self.eweight = eweight
        
#========================#
# FUNCTIONS
#========================#
        
def update_brew(*args):
    vsl_fw = 0
    vsl_ew = 0

    try:
        vsl1_fw = float(vessel1_fullweight.get())
        vsl1_ew = float(vessel1_emptyweight.get())
        if vsl1_fw>vsl1_ew:
            vsl_fw += vsl1_fw
            vsl_ew += vsl1_ew

    except ValueError:
        pass # Do nothing if there is an error

    try:
        vsl2_fw = float(vessel2_fullweight.get())
        vsl2_ew = float(vessel1_emptyweight.get())
        if vsl2_fw>vsl2_ew:
            vsl_fw += vsl2_fw
            vsl_ew += vsl2_ew

    except ValueError:
        pass

    brewed_kombucha = vsl_fw - vsl_ew
    total_kvolume_finished.config(text=f"{int(brewed_kombucha)}")
    kvolume_20percent.config(text=f"{int(brewed_kombucha*0.25)}")
        
def old_update_brew(*args):
    try:
        vsl1_fw = float(vessel1_fullweight.get())
        vsl1_ew = float(vessel1_emptyweight.get())
        vsl2_fw_str = vessel2_fullweight.get()
        vsl2_ew_str = vessel2_emptyweight.get()

        if vsl2_fw_str and vsl2_ew_str:
            vsl2_fw = float(vessel2_fullweight.get())
            vsl2_ew = float(vessel2_emptyweight.get())

            default_v2_weight.config(text=f"{int(vsl2_fw)}")

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
    
#----------------------
# Database Function(s)
#----------------------

# Create Query Function
def query():
    conn = sqlite3.connect('KombuchaCalculator.db')
    c = conn.cursor()

    c.execute("SELECT *, oid FROM F1Vessels")
    records = c.fetchall()

    # Create the Text widget (do this ONCE, outside the query function if possible)
    try:
        for item in query_tree.get_children():
            query_tree.delete(item)
    except:
        pass

    for record in records:
        query_tree.insert("", END, values=(record[2], record[0], record[1]))

    conn.commit()
    conn.close()

# Create Function to Submit a New DB Entry
def submit():
    conn = sqlite3.connect('KombuchaCalculator.db')
    c = conn.cursor()

    c.execute("INSERT INTO F1Vessels VALUES (:name,:weight)",
              {'name': name.get(), 'weight': weight.get()})

    conn.commit()  # Commit *inside* the submit function

    # Clear the Textboxes
    name.delete(0, END)
    weight.delete(0, END)

    conn = sqlite3.connect('KombuchaCalculator.db')
    c = conn.cursor()

    c.execute("SELECT *, oid FROM F1Vessels")
    records = c.fetchall()

    # Create the Text widget (do this ONCE, outside the query function if possible)
    try:
        for item in query_tree.get_children():
            query_tree.delete(item)
    except:
        pass

    for record in records:
        query_tree.insert("", END, values=(record[2], record[0], record[1]))

    conn.commit()
    conn.close()
    query()

# Create Function to Delete a Record
def delete():
    conn = sqlite3.connect('KombuchaCalculator.db')
    c = conn.cursor() # Cursor

    # Delete a record
    c.execute("DELETE from F1Vessels WHERE oid=" + change_box.get())

    change_box.delete(0, END)

    # Commit Changes and Close Connection
    conn.commit()
    conn.close()

    query()

#----------------------------#
# Pop-up Edit Window Functions
#----------------------------#

# Create a window Used to Update a Record
def update():
    updatewindow = Tk()
    updatewindow.title('Update a Record')
    updatewindow.geometry("1200x400")

    # Create text boxes
    name_update = Entry(updatewindow, width=15)
    name_update.grid(row=0, column=1, padx=15, pady=(20,0))
    weight_update = Entry(updatewindow, width=15)
    weight_update.grid(row=0, column=3, padx=15, pady=(20,0))

    # Create text box labels
    name_label_update = Label(updatewindow, text="Vessel name")
    name_label_update.grid(row=0, column=0, padx=10, pady=(10,0))
    eweight_label_update = Label(updatewindow, text="Weight of Empty Vessel")
    eweight_label_update.grid(row=0, column=2, padx=10, pady=(10,0))

    # Create a Save Button to Save Records
    edit_btn = Button(updatewindow, text="Save Changes", command=lambda: edit(updatewindow, name_update, weight_update))
    edit_btn.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=50)

    record_id = change_box.get()

    conn = sqlite3.connect('KombuchaCalculator.db')
    c = conn.cursor() # Cursor

    c.execute("SELECT * FROM F1Vessels WHERE oid = " + record_id)
    records = c.fetchall()

    #Loop Through Results
    for record in records:
        name_update.insert(0, record[0])
        weight_update.insert(0, record[1])
    
    # Commit changes & Close
    conn.commit()
    conn.close()

# Create Function to Update a Record
def edit(updatewindow, name_update, weight_update):
    record_id = change_box.get()

    try:
        conn = sqlite3.connect('KombuchaCalculator.db')
        c = conn.cursor()

        new_name = name_update.get()
        new_weight = weight_update.get()

        try:
            c.execute("UPDATE F1Vessels SET name =?, empty_weight =? WHERE oid =?", (new_name, new_weight, record_id))
            conn.commit()
            updatewindow.destroy()  # Close the update window *after* commit
            query()
        except Exception as e:
            print("Error in updating record:", e)

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        # Handle the error appropriately

    finally:  # Ensure connection is closed only once
        if 'conn' in locals() and conn: # Check if the connection exists before closing
            conn.close()
            query()

#========================#
# Tab 1 -Calculator
#========================#

# Frame inside the window
frame = tkinter.Frame(window)
frame.pack()

# Create frames and labels
finished_frame = tkinter.LabelFrame(calculator, text="Finished Brew Info")
finished_frame.grid(row=0, column=0)
full_vessel_label = tkinter.Label(finished_frame, text="Full Vessel Weight (g)",)
full_vessel_label.grid(row=0, column=1)
empty_vessel_label = tkinter.Label(finished_frame, text="Empty Vessel Weight (g)",)
empty_vessel_label.grid(row=0, column=2)

# Create and set Default weight Values
default_v1_weight = tkinter.StringVar()
default_v2_weight = tkinter.StringVar()
default_v1_weight.set("500")
default_v2_weight.set("501")

# Name and Initialise Data Entry for Vessel Weight
vessel1_label = tkinter.Label(finished_frame, text="Vessel 1")
vessel2_label = tkinter.Label(finished_frame, text="Vessel 2")
vessel1_fullweight = tkinter.Entry(finished_frame)
vessel2_fullweight = tkinter.Entry(finished_frame)
vessel1_emptyweight = tkinter.Entry(finished_frame, textvariable=default_v1_weight)
vessel2_emptyweight = tkinter.Entry(finished_frame, textvariable=default_v2_weight)

# Add Error Labels
weight_error_label = tkinter.Label(finished_frame, text="")
weight_error_v1 = tkinter.Label(finished_frame, text="")
weight_error_v2 = tkinter.Label(finished_frame, text="")

# Initialise Calculation Fields
total_kvolume_finished_label = tkinter.Label(finished_frame, text="Total Kombucha (ml)")
total_kvolume_finished = tkinter.Label(finished_frame, text="")
kvolume_20percent_label = tkinter.Label(finished_frame, text="20% Continuous Brew (ml)")
kvolume_20percent = tkinter.Label(finished_frame, text="")
num_theoretical_brew = tkinter.StringVar()
testvar = tkinter.StringVar()
vessel1_fullweight["textvariable"] = testvar


vessel1_label.grid(row=1, column=0)
vessel2_label.grid(row=2, column=0)
vessel1_fullweight.grid(row=1, column=1)
vessel2_fullweight.grid(row=2, column=1)
vessel1_emptyweight.grid(row=1, column=2)
vessel2_emptyweight.grid(row=2, column=2)
weight_error_v1.grid(row=1, column=3)
weight_error_v2.grid(row=2, column=3)
total_kvolume_finished_label.grid(row=0,column=4)
total_kvolume_finished.grid(row=1 ,column=4, rowspan=2)
kvolume_20percent_label.grid(row=0 ,column=5)
kvolume_20percent.grid(row=1 ,column=5, rowspan=2)

vessel1_fw_update = tkinter.StringVar()
vessel1_ew_update = tkinter.StringVar(value="502")
vessel1_err_update = tkinter.StringVar()
vessel2_fw_update = tkinter.StringVar()
vessel2_ew_update = tkinter.StringVar(value="504")
vessel2_err_update = tkinter.StringVar()


vessel1_fullweight["textvariable"]  = vessel1_fw_update
vessel1_emptyweight["textvariable"] = vessel1_ew_update
weight_error_v1["textvariable"] = vessel1_err_update
vessel2_fullweight["textvariable"]  = vessel2_fw_update
vessel2_emptyweight["textvariable"] = vessel2_ew_update
weight_error_v2["textvariable"] =vessel2_err_update

vessel1_fw_update.trace("w", update_brew) # "w" means write (changes to the variable)
vessel1_ew_update.trace("w", update_brew) 
vessel2_err_update.trace("w", update_brew)
vessel2_fw_update.trace("w", update_brew) 
vessel2_ew_update.trace("w", update_brew) 
vessel2_err_update.trace("w", update_brew)

#vessel1_fw_update = tkinter.StringVar()
#vessel1_fullweight["textvariable"]  = vessel1_fw_update
#vessel1_fw_update.trace("w", update_brew) # "w" means write (changes to the variable)

#for widget in finished_frame.winfo_children():
#    widget.grid_configure(padx=10, pady=5)

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

#§§§§§§§§§§§§§§§§§§
# Databases Page
#§§§§§§§§§§§§§§§§§§

# Data Entry Frame
data_frame = tkinter.LabelFrame(database_tab, text="New Vessel")
data_frame.grid(row=0, column=0, padx= 10, ipady=5, sticky='w'+'e')

# Change Records Frame
control_frame = tkinter.LabelFrame(database_tab, text="Change Records by ID")
control_frame.grid(row=0, column=1, padx= 10, ipady=5, sticky='n'+'e'+'w'+'s')

# Data Display Frame
data_display = tkinter.LabelFrame(database_tab, text="Data")
data_display.grid(row=1, column=0, columnspan=2, padx= 10, ipady=5, ipadx=15, sticky='w'+'e')

#-----------------------------#
# New Vessel Data Entry
#-----------------------------#

# Create text box labels
name_label = Label(data_frame, text="Vessel name")
name_label.grid(row=0, column=0, padx=10)
eweight_label = Label(data_frame, text="Weight of Empty Vessel")
eweight_label.grid(row=1, column=0, padx=10)

# Create text boxes
name = Entry(data_frame, width=15)
name.grid(row=0, column=1, padx=15)
weight = Entry(data_frame, width=15)
weight.grid(row=1, column=1, padx=15)

# Create a Submit button
submit_btn = Button(data_frame, text="New Record", command=lambda: [submit()])
submit_btn.grid(row=2, column=0, columnspan=2, padx=12.5, pady=5, sticky='w'+'e')

#-----------------------------#
# Change Records Section 
#-----------------------------#

# Create text box label
change_box_label = Label(control_frame, text="ID:")
change_box_label.grid(row=0, column=0, padx=10, rowspan=1)

# Create ID Entry box
change_box = Entry(control_frame, width=15)
change_box.grid(row=0, column=1, padx=15, rowspan=2)

# Create a Delete Button
delete_btn = Button(control_frame, text="Delete Record", command=lambda: [delete(), query()])
delete_btn.grid(row=0, column=3, padx=5)

# Create an Update button
update_btn = Button(control_frame, text="Update Record", command= lambda: [update()])
update_btn.grid(row=1, column=3, padx=5, pady=5)

#-----------------------------#
# Data Display
#-----------------------------#

#Treeview Code
query_tree = ttk.Treeview(data_display, columns=("col1", "col2", "col3"), show="headings")
query_tree.heading("col1", text="ID")
query_tree.heading("col2", text="Vessel Name")
query_tree.heading("col3", text="Weight (g)")
query_tree.grid(row=2, column=0, columnspan=2, sticky="nsew")
data_display.grid_rowconfigure(2, weight=1)
data_display.grid_columnconfigure(0, weight=3)
data_display.grid_columnconfigure(1, weight=2)

query()

window.mainloop()