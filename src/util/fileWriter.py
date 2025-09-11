import xml.etree.ElementTree as ET
from tkinter import filedialog
import uuid

class FileWriter:
    def __init__(self, name, selected_items, item_list, subitem_list):
        self.name = name
        self.selected_items = selected_items
        self.item_list = item_list
        self.subitem_list = subitem_list
        self.name_to_guid = {name: guid for name, guid in self.item_list}

    def generate_guid(self):
        return str(uuid.uuid4())
    
    def write_guidtable(self, file_path):
        if file_path:
            
            with open(file_path, "w", encoding="utf-8") as f:
                root = ET.Element('fileGuidTable')
                for name in self.selected_items:
                    files_element = ET.SubElement(root, "files")
                    path_element = ET.SubElement(files_element, "path")
                    path_element.text = "media/clothing/clothingItems/" + name + ".xml"
                    guid_element = ET.SubElement(files_element, "guid")
                    guid_element.text = self.name_to_guid.get(name)
                for entry in self.subitem_list:
                        for name in self.subitem_list[entry]:
                            files_element = ET.SubElement(root, "files")
                            path_element = ET.SubElement(files_element, "path")
                            path_element.text = "media/clothing/clothingItems/" + name + ".xml"
                            guid_element = ET.SubElement(files_element, "guid")
                            guid_element.text = self.name_to_guid.get(name)

                f.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
                f.write(ET.tostring(root, encoding="unicode"))
    
    def write_outfit(self, file_path, male, female):
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                guid = self.generate_guid()
                root = ET.Element('outfitManager')
                outfit_name = self.name.strip() or "Outfit"
                if male:
                    male_outfit_element = ET.SubElement(root, 'm_MaleOutfits')
                    name_element = ET.SubElement(male_outfit_element, "m_Name")
                    name_element.text = outfit_name
                    guid_element = ET.SubElement(male_outfit_element, "m_Guid")
                    guid_element.text = guid
                    for name in self.selected_items:
                        items_element = ET.SubElement(male_outfit_element, "m_items")
                        item_guid_element = ET.SubElement(items_element, "itemGUID")
                        item_guid_element.text = self.name_to_guid.get(name)
                        if name in self.subitem_list:
                            for subname in self.subitem_list[name]:
                                subitems_element = ET.SubElement(items_element, "subItems")
                                subitem_guid_element = ET.SubElement(subitems_element, "itemGUID")
                                subitem_guid_element.text = self.name_to_guid.get(subname)
                if female:
                    female_outfit_element = ET.SubElement(root, 'm_FemaleOutfits')
                    name_element = ET.SubElement(female_outfit_element, "m_Name")
                    name_element.text = outfit_name
                    guid_element = ET.SubElement(female_outfit_element, "m_Guid")
                    guid_element.text = guid
                    for name in self.selected_items:
                        items_element = ET.SubElement(female_outfit_element, "m_items")
                        item_guid_element = ET.SubElement(items_element, "itemGUID")
                        item_guid_element.text = self.name_to_guid.get(name)
                        if name in self.subitem_list:
                            for subname in self.subitem_list[name]:
                                subitems_element = ET.SubElement(items_element, "subItems")
                                subitem_guid_element = ET.SubElement(subitems_element, "itemGUID")
                                subitem_guid_element.text = self.name_to_guid.get(subname)
                
                f.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
                f.write(ET.tostring(root, encoding="unicode"))