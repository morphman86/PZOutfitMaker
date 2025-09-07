# PZ Outfit Maker

A quick and dirty XML formatter for Project Zomboid outfits
Currently only working on Windows with the default location for Steam and PZ.
If you need to use it on any other system, or with PZ installed in any other directory, change `self.folder_path` on line 6 in `PZXMLGuidReader.py`.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/pyutils.git
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the script:
```bash
python PZOutfitMaker.py
```
A window will open and you will get a list of all vanilla clothing items.

From here, you can select any item in the left list and press the right arrow to add it to your outfit.
If you want to remove an item, select it in the right list and press the left arrow.
Select which gender you want the outfit to apply to at the top, and give it a name at the bottom.

When you are done, press File > Save to open the save dialog. Navigate to your desired folder (for example `modname/media/clothing`) and give your file a name, then press save.

## What this app does

It will read all vanilla clothing item XML files and give you all the names and GUIDs of those.
When saving it will
* structure an XML file with the correct male, female or both definitions
* assign a new GUID to your outfit
* give it the name you choose (or Outfit if you left name blank)
* add each item as its own m_items entry

This gives you all the ground work for outfit making without having to check literally hundreds of tables for references.

## What it will not do

This app can currently not
* add probability for an item
* assign items for the same slot as subitems (variants)
* load previously saved files

If you want these features, you can still edit the XML file once saved, but remember that this will be overwritten if you modify the file through this app again.

## Contributing

Feel free to submit issues or pull requests to improve the app.

## License

This project is licensed under the MIT License.