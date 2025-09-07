import tkinter as tk
from tkinter import Menu, Listbox, Button, Frame, filedialog, END, SINGLE
import uuid
from PZXMLGuidReader import PZXMLGuidReader

class PZOutfitMaker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.add_gender_checkboxes()
        self.title("PZ Outfit Maker")
        self.geometry("600x400")

        # Menu
        menubar = Menu(self)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save", command=self.save)
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)

        # Main layout
        main_frame = Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left Listbox
        self.left_listbox = Listbox(main_frame, selectmode=SINGLE)
        self.left_listbox.grid(row=0, column=0, sticky="ns", padx=(0,10), pady=5)
        # Items
        xmlreader = PZXMLGuidReader()
        itemlist = xmlreader.read_guids()        
        for name, guid in itemlist:
            self.left_listbox.insert(END, name)

        # Middle Buttons
        button_frame = Frame(main_frame)
        button_frame.grid(row=0, column=1, sticky="ns", pady=5)
        self.to_right_btn = Button(button_frame, text="→", command=self.move_right)
        self.to_right_btn.pack(pady=10)
        self.to_left_btn = Button(button_frame, text="←", command=self.move_left)
        self.to_left_btn.pack(pady=10)

        # Right Listbox
        self.right_listbox = Listbox(main_frame, selectmode=SINGLE)
        self.right_listbox.grid(row=0, column=2, sticky="ns", padx=(10,0), pady=5)
        
        # Name Textfield
        name_frame = Frame(main_frame)
        name_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(10,0))
        tk.Label(name_frame, text="Outfit Name:").pack(side=tk.LEFT)
        self.name_entry = tk.Entry(name_frame)
        self.name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Make columns expand
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(2, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

    def move_right(self):
        selection = self.left_listbox.curselection()
        if selection:
            item = self.left_listbox.get(selection[0])
            self.left_listbox.delete(selection[0])
            self.right_listbox.insert(END, item)

    def move_left(self):
        selection = self.right_listbox.curselection()
        if selection:
            item = self.right_listbox.get(selection[0])
            self.right_listbox.delete(selection[0])
            self.left_listbox.insert(END, item)
    
    def add_gender_checkboxes(self):
        gender_frame = Frame(self)
        gender_frame.pack(side=tk.TOP, anchor="w", padx=10, pady=(0,5))

        self.male_var = tk.BooleanVar(value=True)
        self.female_var = tk.BooleanVar(value=True)

        self.male_check = tk.Checkbutton(gender_frame, text="Male", variable=self.male_var)
        self.male_check.pack(side=tk.LEFT, padx=(0,10))
        self.female_check = tk.Checkbutton(gender_frame, text="Female", variable=self.female_var)
        self.female_check.pack(side=tk.LEFT)

    def get_selected_guids(self):
        # Convert item names in right_listbox into GUIDs using itemlist from PZXMLGuidReader
        xmlreader = PZXMLGuidReader()
        itemlist = xmlreader.read_guids()  # List of (name, guid)
        name_to_guid = {name: guid for name, guid in itemlist}
        items = self.right_listbox.get(0, END)
        guidlist = []
        for item in items:
            guid = name_to_guid.get(item)
            if guid:
                guidlist.append(guid)
        return guidlist

    def save(self):
        guidlist = self.get_selected_guids()
        if not guidlist:
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                guid = self.generate_guid()
                f.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
                f.write("<outfitManager>\n")
                outfit_name = self.name_entry.get().strip() or "Outfit"
                if self.male_var.get():
                    f.write(f'  <m_MaleOutfits>\n')
                    f.write(f'    <m_Name=>{outfit_name}</m_Name>\n')
                    f.write(f'    <m_Guid=>{guid}</m_Guid>\n')
                    for item in guidlist:
                        f.write(f'    <m_items>\n')
                        f.write(f'      <itemGUID>{item}</itemGUID>\n')
                        f.write(f'    </m_items>\n')
                    f.write(f'  </m_MaleOutfits>\n')
                if self.female_var.get():
                    f.write(f'  <m_FemaleOutfits>\n')
                    f.write(f'    <m_Name=>{outfit_name}</m_Name>\n')
                    f.write(f'    <m_Guid=>{guid}</m_Guid>\n')
                    for item in guidlist:
                        f.write(f'    <m_items>\n')
                        f.write(f'      <itemGUID>{item}</itemGUID>\n')
                        f.write(f'    </m_items>\n')
                    f.write(f'  </m_FemaleOutfits>\n')
                f.write("</outfitManager>\n")

    def generate_guid(self):
        return str(uuid.uuid4())

if __name__ == "__main__":
    app = PZOutfitMaker()
    app.mainloop()