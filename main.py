import tkinter as tk
from tkinter import Menu, Listbox, Button, Frame, filedialog, END, SINGLE
from src.util.fileReader import FileReader
from src.util.fileWriter import FileWriter

class PZOutfitMaker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PZ Outfit Maker")
        self.geometry("600x400")

        # Parameters
        self.itemlist = []
        self.defaultClothesPath = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\ProjectZomboid\\media\\clothing\\clothingItems"

        # Menu
        menubar = Menu(self)
        # filemenu = Menu(menubar, tearoff=0)
        menubar.add_command(label="Import Clothes", command=self.load)
        menubar.add_command(label="Export Outfit", command=self.save_outfit)
        menubar.add_command(label="Export File Guid Table", command=self.save_guidtable)
        # menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)

        # Name Textfield
        name_frame = Frame(self)
        name_frame.pack(fill=tk.X, anchor="nw", padx=10, pady=(10, 5))
        tk.Label(name_frame, text="Outfit Name:").pack(side=tk.LEFT)
        self.name_entry = tk.Entry(name_frame)
        self.name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Gender Tickboxes
        gender_frame = Frame(self)
        gender_frame.pack(anchor="nw", padx=10, pady=(0, 5))
        self.male_var = tk.BooleanVar(value=True)
        self.female_var = tk.BooleanVar(value=True)
        self.male_check = tk.Checkbutton(gender_frame, text="Male", variable=self.male_var)
        self.male_check.pack(side=tk.LEFT, padx=(0, 10))
        self.female_check = tk.Checkbutton(gender_frame, text="Female", variable=self.female_var)
        self.female_check.pack(side=tk.LEFT)

        # Listboxes and buttons frame
        lists_frame = Frame(self)
        lists_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Left Listbox with Scrollbar
        left_listbox_frame = Frame(lists_frame)
        left_listbox_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.left_listbox = Listbox(left_listbox_frame, selectmode=SINGLE)
        self.left_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        left_scrollbar = tk.Scrollbar(left_listbox_frame, orient=tk.VERTICAL, command=self.left_listbox.yview)
        left_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.left_listbox.config(yscrollcommand=left_scrollbar.set)
        xmlreader = FileReader(self.defaultClothesPath)
        self.itemlist = xmlreader.read_guids()
        for name, guid in self.itemlist:
            self.left_listbox.insert(END, name)

        # Middle Buttons
        button_frame = Frame(lists_frame)
        button_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.to_right_btn = Button(button_frame, text="→", command=self.move_right)
        self.to_right_btn.pack(pady=10)
        self.to_left_btn = Button(button_frame, text="←", command=self.move_left)
        self.to_left_btn.pack(pady=10)

        # Right Listbox
        right_listbox_frame = Frame(lists_frame)
        right_listbox_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.right_listbox = Listbox(right_listbox_frame, selectmode=SINGLE)
        self.right_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        right_scrollbar = tk.Scrollbar(right_listbox_frame, orient=tk.VERTICAL, command=self.right_listbox.yview)
        right_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.right_listbox.config(yscrollcommand=right_scrollbar.set)

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
            self.sort_left_listbox()

    def get_selected_guids(self):
        # Convert item names in right_listbox into GUIDs using itemlist from PZXMLGuidReader
        name_to_guid = {name: guid for name, guid in self.itemlist}
        items = self.right_listbox.get(0, END)
        guidlist = []
        for item in items:
            guid = name_to_guid.get(item)
            if guid:
                guidlist.append(guid)
        return guidlist
    
    def sort_left_listbox(self):
        items = self.left_listbox.get(0, END)
        self.left_listbox.delete(0, END)
        sorted_items = sorted(items)
        for item in sorted_items:
            self.left_listbox.insert(END, item)
    
    def load(self):
        loadFolder = filedialog.askdirectory(title="Folder of clothing items (usually media/clothing/clothingItems)")
        xmlreader = FileReader(loadFolder)
        itemlist = xmlreader.read_guids()  # List of (name, guid)
        for item in itemlist:
            self.itemlist.append(item)
            self.left_listbox.insert(END, item[0])
            self.sort_left_listbox()

    def save_outfit(self):
        selected_items = self.right_listbox.get(0, END)
        name = self.name_entry.get()
        writer = FileWriter(name, selected_items, self.itemlist)

        file_path_outfit = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
        male = self.male_var.get()
        female = self.female_var.get()
        writer.write_outfit(file_path_outfit, male, female)

    def save_guidtable(self):
        selected_items = self.right_listbox.get(0, END)
        name = self.name_entry.get()
        writer = FileWriter(name, selected_items, self.itemlist)

        file_path_guidtable = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
        writer.write_guidtable(file_path_guidtable)


if __name__ == "__main__":
    app = PZOutfitMaker()
    app.mainloop()