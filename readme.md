# PZ Outfit Maker

A quick and dirty XML formatter for Project Zomboid outfits
Currently only working on Windows with the default location for Steam and PZ.
If you need to use it on any other system, or with PZ installed in any other directory, change `self.folder_path` on line 6 in `PZXMLGuidReader.py`.

## Installation

1. Clone the repository or download the files
2. Install python (if you haven't already)
3. Navigate to the folder containing `main.py` in a terminal.
4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the script:
```bash
python main.py
```
A window will open and you will get a list of all vanilla clothing items.

From here, you can select any item in the Available Items list and press the plus button between the left and middle lists to add it to your outfit.
If you want to remove an item, select it in the Main Clothes list in the middle and press the now active minus button to the left of the list.
If you want to add alternatives to a clothing item, select the item in the middle Main Clothes list (you'll see the label on the right Alt list change to the item name) and select the items you want to add as an alternative in the Available Items list, then press the now active plus button to the RIGHT of the Main Clothes list.
To remove an alternative clothing item, select the Main Clothes item it is an alternative to in the Main Clothes list, then select the Alternative item in the Alt list, then press the now active minus button to the RIGHT of the Main Clothes list.

Select which gender(s) you want the outfit to apply to and give it a name at the top.

When you are done, press Export Outfit to open the save dialog. Navigate to your desired folder (for example `modname/media/clothing`) and give your file a name, then press save.
Press Export File Guid Table to generate a fileGuidTable.xml with your selected items.

If you want to add items from your own mod, press Import Clothes and navigate to `media/cloghint/clothingItems` in your own mod folder.

## What this app does

* structure an XML file with the correct male, female or both definitions
* assign a new GUID to your outfit
* give it the name you choose (or Outfit if you left name blank)
* add each item as its own m_items entry
* add each alternative item as its own subItems in its parent m_items entry
* generate a fileGuidTable file for your selected items
* allow you to import your own clothing items, or items from other mods

This gives you all the ground work for outfit making without having to check literally hundreds of tables for references.

## Contributing

Feel free to submit issues or pull requests to improve the app.

## License

This project is licensed under the MIT License.
