from tkinter import *
from tkinter import ttk
import sqlite3
import main

#==============#
# Databases
#==============#

# Create a Database or Connect to One
conn = sqlite3.connect('KombuchaCalculator.db')
c = conn.cursor() # Cursor

# Create table if it doesn't exist
c.execute("""
CREATE TABLE IF NOT EXISTS F1Vessels ( -- Use IF NOT EXISTS
    name TEXT,
    empty_weight INTEGER
)
""")
conn.commit()

#========================#
# FUNCTIONS
#========================#

#----------------------------#
# Pop-up Edit Window Functions
#----------------------------#

# Create a window Used to Update a Record
def update():
    update = Tk()
    update.title('Update a Record')
    update.geometry("1200x400")

    # Create text boxes
    name_update = Entry(update, width=15)
    name_update.grid(row=0, column=1, padx=15, pady=(20,0))
    weight_update = Entry(update, width=15)
    weight_update.grid(row=0, column=3, padx=15, pady=(20,0))

    # Create text box labels
    name_label_update = Label(update, text="Vessel name")
    name_label_update.grid(row=0, column=0, padx=10, pady=(10,0))
    eweight_label_update = Label(update, text="Weight of Empty Vessel")
    eweight_label_update.grid(row=0, column=2, padx=10, pady=(10,0))

    # Create a Save Button to Save Records
    edit_btn = Button(update, text="Save Changes", command=lambda: edit(main.change_box, name_update, weight_update, update))
    edit_btn.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=50)

    record_id = main.change_box.get()

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
def edit(change_box, name_update, weight_update, update):
    record_id = change_box.get()

    try:
        conn = sqlite3.connect('KombuchaCalculator.db')
        c = conn.cursor()

        new_name = name_update.get()
        new_weight = weight_update.get()

        try:
            c.execute("UPDATE F1Vessels SET name =?, empty_weight =? WHERE oid =?", (new_name, new_weight, record_id))
            conn.commit()
            update.destroy()  # Close the update window *after* commit
            main.query(main.query_tree)
        except Exception as e:
            print("Error in updating record:", e)

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        # Handle the error appropriately

    finally:  # Ensure connection is closed only once
        if 'conn' in locals() and conn: # Check if the connection exists before closing
            conn.close()
            main.query(main.query_tree)       

#---------------------------#
# Database Window Functions
#---------------------------#

# Create Function to Delete a Record
def delete():
    conn = sqlite3.connect('KombuchaCalculator.db')
    c = conn.cursor() # Cursor

    # Delete a record
    c.execute("DELETE from F1Vessels WHERE oid= " + main.change_box.get())

    main.change_box.delete(0, END)


    # Commit changes
    conn.commit()
    # Close Connection
    conn.close()

# Submit Function for Database
def submit():
    global name, weight
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
        for item in main.query_tree.get_children():
            main.query_tree.delete(item)
    except:
        pass

    for record in records:
        main.query_tree.insert("", END, values=(record[2], record[0], record[1]))

    conn.commit()
    conn.close()



