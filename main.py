from ctypes import sizeof
import tkinter as tk
from tkinter import LAST, Menu, Label, Listbox, Entry, Button, Frame, Checkbutton, Scrollbar, BooleanVar, filedialog, NORMAL, DISABLED, END, SINGLE, MULTIPLE, X, Y, BOTH, RIGHT, LEFT, TOP, VERTICAL
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
        self.selected_item = []
        self.subitems = {}

        # Menu
        menubar = Menu(self)
        # filemenu = Menu(menubar, tearoff=0)
        menubar.add_command(label="Import Clothes", command=self.import_clothes)
        menubar.add_command(label="Export Outfit", command=self.save_outfit)
        menubar.add_command(label="Export File Guid Table", command=self.save_guidtable)
        # menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)

        # Name Textfield
        name_frame = Frame(self)
        name_frame.pack(fill=X, anchor="nw", padx=10, pady=(10, 5))
        Label(name_frame, text="Outfit Name:").pack(side=LEFT)
        self.textbox_name = Entry(name_frame)
        self.textbox_name.pack(side=LEFT, fill=X, expand=True)

        # Gender Tickboxes
        gender_frame = Frame(self)
        gender_frame.pack(anchor="nw", padx=10, pady=(0, 5))
        self.male_var = BooleanVar(value=True)
        self.female_var = BooleanVar(value=True)
        self.checkbox_male = Checkbutton(gender_frame, text="Male", variable=self.male_var)
        self.checkbox_male.pack(side=LEFT, padx=(0, 10))
        self.checkbox_female = Checkbutton(gender_frame, text="Female", variable=self.female_var)
        self.checkbox_female.pack(side=LEFT)

        # Listboxes frame
        lists_frame = Frame(self)
        lists_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        # All Clothing Listbox
        listbox_all_items_frame = Frame(lists_frame)
        listbox_all_items_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))
        Label(listbox_all_items_frame, text="Available items").pack(side=TOP)
        self.listbox_all_items = Listbox(listbox_all_items_frame, selectmode=MULTIPLE)
        self.listbox_all_items.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar_all_items = Scrollbar(listbox_all_items_frame, orient=VERTICAL, command=self.listbox_all_items.yview)
        scrollbar_all_items.pack(side=RIGHT, fill=Y)
        self.listbox_all_items.config(yscrollcommand=scrollbar_all_items.set)
        xmlreader = FileReader(self.defaultClothesPath)
        self.itemlist = xmlreader.read_guids()
        for name, guid in self.itemlist:
            self.listbox_all_items.insert(END, name)

        # Outfit Buttons
        button_frame_outfit = Frame(lists_frame)
        button_frame_outfit.pack(side=LEFT, fill=Y)
        self.button_add_to_selected = Button(button_frame_outfit, text="+", command=self.add_to_selected)
        self.button_add_to_selected.pack(pady=20)
        self.button_remove_from_selected = Button(button_frame_outfit, text="-", command=self.remove_from_selected, state=DISABLED)
        self.button_remove_from_selected.pack(pady=10)

        # Selected Clothing Listbox
        listbox_selected_items_frame = Frame(lists_frame)
        listbox_selected_items_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))
        Label(listbox_selected_items_frame, text="Main Clothes").pack(side=TOP)
        self.listbox_selected_items = Listbox(listbox_selected_items_frame, selectmode=SINGLE)
        self.listbox_selected_items.pack(side=LEFT, fill=BOTH, expand=True)
        self.listbox_selected_items.bind('<<ListboxSelect>>', self.selected_item_clicked)
        scrollbar_selected_items = Scrollbar(listbox_selected_items_frame, orient=VERTICAL, command=self.listbox_selected_items.yview)
        scrollbar_selected_items.pack(side=RIGHT, fill=Y)
        self.listbox_selected_items.config(yscrollcommand=scrollbar_selected_items.set)

        # Sub-item Buttons
        button_frame_sub = Frame(lists_frame)
        button_frame_sub.pack(side=LEFT, fill=Y)
        self.button_add_to_selected_sub = Button(button_frame_sub, text="+", command=self.add_to_selected_subitem, state=DISABLED)
        self.button_add_to_selected_sub.pack(pady=20)
        self.button_remove_from_selected_sub = Button(button_frame_sub, text="-", command=self.remove_from_selected_subitem, state=DISABLED)
        self.button_remove_from_selected_sub.pack(pady=10)

        # Sub-item Listbox
        listbox_sub_items_frame = Frame(lists_frame)
        listbox_sub_items_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0,10))
        self.label_sub_items = Label(listbox_sub_items_frame, text="Alt: [none selected]")
        self.label_sub_items.pack(side=TOP)
        self.listbox_sub_items = Listbox(listbox_sub_items_frame, selectmode=MULTIPLE)
        self.listbox_sub_items.pack(side=LEFT, fill=BOTH, expand=True)
        self.listbox_sub_items.bind('<<ListboxSelect>>', self.selected_subitem_clicked)
        scrollbar_sub_items = Scrollbar(listbox_sub_items_frame, orient=VERTICAL, command=self.listbox_sub_items.yview)
        scrollbar_sub_items.pack(side=RIGHT, fill=Y)
        self.listbox_sub_items.config(yscrollcommand=scrollbar_sub_items.set)
    
    def selected_item_clicked(self, event):
        self.button_remove_from_selected.config(state=DISABLED)
        self.listbox_sub_items.delete(0, END)
        if len(self.listbox_selected_items.curselection()) > 0:
            self.button_remove_from_selected.config(state=NORMAL)
            self.set_selected_item(self.listbox_selected_items.get(self.listbox_selected_items.curselection()[0]))
        if self.subitems and self.selected_item in self.subitems:
            for item in self.subitems[self.selected_item]:
                self.listbox_sub_items.insert(END, item)

    def selected_subitem_clicked(self, event):
        self.button_remove_from_selected_sub.config(state=DISABLED)
        if len(self.listbox_sub_items.curselection()) > 0:
            self.button_remove_from_selected_sub.config(state=NORMAL)
    def set_selected_item(self, item):
        self.selected_item = item
        if item:
            self.button_add_to_selected_sub.config(state=NORMAL)
            text=f"Alt: {self.selected_item}"
        else:
            self.button_add_to_selected_sub.config(state=DISABLED)
            text="Alt: [none selected]"
        text = text[:23]
        self.label_sub_items.config(text=text)

    def move_from_list_to_list(self, fromList, toList, selected, extras=[]):
        if selected:
            for index in reversed(selected):
                item = fromList.get(index)
                fromList.delete(index)
                toList.insert(END, item)
            for index in reversed(extras):
                toList.insert(END, index)
            self.sort_listbox(fromList)
            self.sort_listbox(toList)

    def add_to_selected(self):
        self.listbox_sub_items.delete(0, END)
        selection = self.listbox_all_items.curselection()
        self.set_selected_item(self.listbox_all_items.get(selection[0]))
        self.move_from_list_to_list(self.listbox_all_items, self.listbox_selected_items, selection)
    
    def add_to_selected_subitem(self):
        selection = self.listbox_all_items.curselection()
        if self.selected_item:
            if self.subitems and self.selected_item in self.subitems:
                    for item in self.subitems[self.selected_item]:
                        if not item in self.subitems[self.selected_item]:
                            self.listbox_sub_items.insert(END, item)
            self.move_from_list_to_list(self.listbox_all_items, self.listbox_sub_items, selection)
            self.subitems[self.selected_item] = self.listbox_sub_items.get(0, END)

    def remove_from_selected_subitem(self):
        selection = self.listbox_sub_items.curselection()
        if selection:
            self.move_from_list_to_list(self.listbox_sub_items, self.listbox_all_items, selection)
            self.subitems[self.selected_item] = self.listbox_sub_items.get(0, END)
        
    def remove_from_selected(self):
        self.button_remove_from_selected.config(state=DISABLED)
        selection = self.listbox_selected_items.curselection()
        if selection:
            extras = []
            index = 0
            if self.selected_item in self.subitems:
                for name in self.subitems[self.selected_item]:
                    extras.append(self.listbox_sub_items.get(index))
                    index += 1
                self.subitems.pop(self.listbox_selected_items.get(selection[0]))
            self.move_from_list_to_list(self.listbox_selected_items, self.listbox_all_items, selection, extras)
            self.listbox_sub_items.delete(0, END)
            self.set_selected_item(None)

    def get_selected_guids(self):
        # Convert item names in listbox_selected_items into GUIDs using itemlist from PZXMLGuidReader
        name_to_guid = {name: guid for name, guid in self.itemlist}
        items = self.listbox_selected_items.get(0, END)
        guidlist = []
        for item in items:
            guid = name_to_guid.get(item)
            if guid:
                guidlist.append(guid)
        return guidlist
    
    def sort_listbox(self, listToSort):
        items = listToSort.get(0, END)
        listToSort.delete(0, END)
        sorted_items = sorted(items)
        for item in sorted_items:
            listToSort.insert(END, item)
    
    def import_clothes(self):
        loadFolder = filedialog.askdirectory(title="Folder of clothing items (usually media/clothing/clothingItems)")
        xmlreader = FileReader(loadFolder)
        itemlist = xmlreader.read_guids()  # List of (name, guid)
        for item in itemlist:
            self.itemlist.append(item)
            self.listbox_all_items.insert(END, item[0])
            self.sort_listbox(self.listbox_all_items)

    def save_outfit(self):
        selected_items = self.listbox_selected_items.get(0, END)
        name = self.textbox_name.get()
        writer = FileWriter(name, selected_items, self.itemlist, self.subitems)

        file_path_outfit = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
        male = self.male_var.get()
        female = self.female_var.get()
        writer.write_outfit(file_path_outfit, male, female)

    def save_guidtable(self):
        selected_items = self.listbox_selected_items.get(0, END)
        name = self.textbox_name.get()
        writer = FileWriter(name, selected_items, self.itemlist, self.subitems)

        file_path_guidtable = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
        writer.write_guidtable(file_path_guidtable)


if __name__ == "__main__":
    app = PZOutfitMaker()
    app.mainloop()