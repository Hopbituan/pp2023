import csv
import tkinter as tk
from tkinter import filedialog, messagebox
# Define class for equipment
class Equipment:
    def __init__(self, name, description, quantity, location):
        self.name = name
        self.description = description
        self.quantity = quantity
        self.location = location

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_quantity(self):
        return self.quantity

    def get_location(self):
        return self.location

    def set_quantity(self, new_quantity):
        self.quantity = new_quantity

# Define class for equipment management system
class EquipmentManagementSystem:
    def __init__(self):
        self.equipment_list = []

    # Add new equipment to the system
    def add_equipment(self, name, description, quantity, location):
        new_equipment = Equipment(name, description, quantity, location)
        self.equipment_list.append(new_equipment)

    # Remove equipment from the system
    def remove_equipment(self, equipment_name):
        for equipment in self.equipment_list:
            if equipment.get_name() == equipment_name:
                self.equipment_list.remove(equipment)

    # Update equipment quantity
    def update_equipment_quantity(self, equipment_name, new_quantity):
        for equipment in self.equipment_list:
            if equipment.get_name() == equipment_name:
                equipment.set_quantity(new_quantity)
                return equipment
        return None
    
    # Display all equipment in the system
    def display_equipment(self, output_file=None):
        if output_file:
            with open(output_file, 'w') as f:
                for equipment in self.equipment_list:
                    f.write(f"Name: {equipment.get_name()}\nDescription: {equipment.get_description()}\nQuantity: {equipment.get_quantity()}\nLocation: {equipment.get_location()}\n\n")
        else:
            for equipment in self.equipment_list:
                print(f"Name: {equipment.get_name()}\nDescription: {equipment.get_description()}\nQuantity: {equipment.get_quantity()}\nLocation: {equipment.get_location()}\n")
    
    # Clear all the equipment in the system
    def clear_equipment_list(self):
        self.equipment_list.clear()
        
class EquipmentManagementGUI:
    def __init__(self, master):
        self.master = master
        master.title("Equipment Management System")

        self.equipment_system = EquipmentManagementSystem()

        self.create_widgets()

    def create_widgets(self):
        # Add Equipment Frame
        add_frame = tk.Frame(self.master)
        add_frame.pack()

        add_label = tk.Label(add_frame, text="Add Equipment")
        add_label.grid(row=0, column=0, columnspan=2)

        name_label = tk.Label(add_frame, text="Name:")
        name_label.grid(row=1, column=0)
        self.name_entry = tk.Entry(add_frame)
        self.name_entry.grid(row=1, column=1)

        description_label = tk.Label(add_frame, text="Description:")
        description_label.grid(row=2, column=0)
        self.description_entry = tk.Entry(add_frame)
        self.description_entry.grid(row=2, column=1)

        quantity_label = tk.Label(add_frame, text="Quantity:")
        quantity_label.grid(row=3, column=0)
        self.quantity_entry = tk.Entry(add_frame)
        self.quantity_entry.grid(row=3, column=1)

        location_label = tk.Label(add_frame, text="Location:")
        location_label.grid(row=4, column=0)
        self.location_entry = tk.Entry(add_frame)
        self.location_entry.grid(row=4, column=1)

        add_button = tk.Button(add_frame, text="Add", command=self.add_equipment)
        add_button.grid(row=5, column=1)

        # Equipment List Frame
        list_frame = tk.Frame(self.master)
        list_frame.pack()

        list_label = tk.Label(list_frame, text="Equipment List")
        list_label.grid(row=0, column=0, columnspan=2)

        self.equipment_listbox = tk.Listbox(list_frame)
        self.equipment_listbox.grid(row=1, column=0, columnspan=2)

        remove_button = tk.Button(list_frame, text="Remove", command=self.remove_equipment)
        remove_button.grid(row=2, column=0)

        update_button = tk.Button(list_frame, text="Update Quantity", command=self.update_quantity)
        update_button.grid(row=2, column=1)

        # Menu Frame
        menu_frame = tk.Frame(self.master)
        menu_frame.pack()

        display_button = tk.Button(menu_frame, text="Display Equipment", command=self.display_equipment)
        display_button.pack(side=tk.LEFT)

        save_button = tk.Button(menu_frame, text="Save Equipment List", command=self.save_equipment_list)
        save_button.pack(side=tk.LEFT)

        load_button = tk.Button(menu_frame, text="Load Equipment List", command=self.load_equipment_list)
        load_button.pack(side=tk.LEFT)

        clear_button = tk.Button(menu_frame, text="Clear Equipment List", command=self.clear_equipment_list)
        clear_button.pack(side=tk.LEFT)

    def add_equipment(self):
        name = self.name_entry.get()
        description = self.description_entry.get()
        quantity = int(self.quantity_entry.get())
        location = self.location_entry.get()
        self.equipment_system.add_equipment(name, description, quantity, location)
        self.update_equipment_listbox()

    def remove_equipment(self):
        selection = self.equipment_listbox.curselection()
        if selection:
            equipment_name = self.equipment_listbox.get(selection[0])
            self.equipment_system.remove_equipment(equipment_name)
            self.update_equipment_listbox()
        else:
            messagebox.showerror("Error", "Please select an equipment to remove.")

    def update_equipment_listbox(self):
        self.equipment_listbox.delete(0, tk.END)
        for equipment in self.equipment_system.equipment_list:
            self.equipment_listbox.insert(tk.END, equipment.name)

    def update_quantity(self):
        selection = self.equipment_listbox.curselection()
        if selection:
            equipment_name = self.equipment_listbox.get(selection[0])
            equipment = self.equipment_system.update_equipment_quantity(equipment_name, int(tk.simpledialog.askstring("Update Quantity", f"Enter new quantity for {equipment_name}:")))
            if equipment:
                self.update_equipment_listbox()
            else:
                messagebox.showerror("Error", f"{equipment_name} not found.")
    

    def display_equipment(self):
        equipment_str = ""
        for equipment in self.equipment_system.equipment_list:
            equipment_str += f"Name: {equipment.name}\nDescription: {equipment.description}\nQuantity: {equipment.quantity}\nLocation: {equipment.location}\n\n"
        messagebox.showinfo("Equipment List", equipment_str)

    def save_equipment_list(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv")
        if file_path:
            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Description", "Quantity", "Location"])
                for equipment in self.equipment_system.equipment_list:
                    writer.writerow([equipment.name, equipment.description, equipment.quantity, equipment.location])
            messagebox.showinfo("Save", f"Equipment list saved to {file_path}")

    def load_equipment_list(self):
        file_path = filedialog.askopenfilename(defaultextension=".csv")
        if file_path:
            with open(file_path, "r") as file:
                reader = csv.reader(file)
                for data in reader:
                    name = data[0]
                    description = data[1]
                    quantity = int(data[2])
                    location = data[3]
                    self.equipment_system.add_equipment(name, description, quantity, location)
            self.update_equipment_listbox()
            messagebox.showinfo("Load", f"Equipment list loaded from {file_path}")

    def clear_equipment_list(self):
        result = messagebox.askquestion("Clear Equipment List", "Are you sure you want to clear the equipment list?", icon='warning')
        if result == 'yes':
            self.equipment_system.clear_equipment_list()
            self.update_equipment_listbox()
            messagebox.showinfo("Clear", "Equipment list cleared.")
            
    
    def run(self):
        self.master.mainloop()

if __name__ == "__main__":
    master = tk.Tk()
    app = EquipmentManagementGUI(master)
    app.run()