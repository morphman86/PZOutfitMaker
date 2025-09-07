import os
import xml.etree.ElementTree as ET

class PZXMLGuidReader:
    def __init__(self):
        self.folder_path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\ProjectZomboid\\media\\clothing\\clothingItems"

    def read_guids(self):
        results = []
        for filename in os.listdir(self.folder_path):
            if filename.lower().endswith('.xml'):
                file_path = os.path.join(self.folder_path, filename)
                try:
                    tree = ET.parse(file_path)
                    clothing_item = tree.getroot()
                    if clothing_item is not None:
                        guid_elem = clothing_item.find('m_GUID')
                        if guid_elem is not None and guid_elem.text:
                            name = os.path.splitext(filename)[0]
                            guid = guid_elem.text.strip()
                            results.append((name, guid))
                except ET.ParseError:
                    continue  # skip files that can't be parsed
        return results