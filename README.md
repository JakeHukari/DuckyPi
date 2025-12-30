# DuckyPi
DuckyPi Harvester payload for the 'HackyPi device from SB Components
# Setup

1. Plug in the hackypi and wait for filesystem to mount.

2. Copy code.py, and lib folder to the root of the Hackypi filesystem.

3. Plug a micro sd card into computer and copy both folders inside of 'sd_card_assests' (assets and fonts) onto the sd card.

4. Plug a seperate usb or drive into computer and rename it to: 'DUCKYPI'. (ensure it is formatted to FAT32)

5. Unplug hackypi, micro sd card, and DUCKYPI usb drive.

# Execution
1. Plug sd card into the sd card slot on the hackypi.  
2. Plug hackypi back into computer.
3. Plug DUCKYPI usb drive into computer.
Upon boot, the hackypi will begin harvesting.

The hackypi will harvest all stored wifi usernames and passwords, system information, and stored browser data. (saved login data, browsing history, cookies, etc from any browser recognized by the hackypi (chrome, firefox, edge))

The hackypi will compress all harvested data into a zip file and copy it to the DUCKYPI usb drive.

The hackypi will then delete the harvested data from the system, it will only remain on the 'DUCKYPI' usb drive. 

# Loot Retrieval
Once harvest is complete there will be a date and time stamped zip file on the 'DUCKYPI' usb drive.
Unzip the file and you will find the harvested data.
Wifi credentials and system info will be stored in plaintext file format. (txt)
Browser information will be stored in database format (sqlite & json), some browser information might be encrypted or hashed, you will need to decrypt it to view the data.

# Modifications
To modify the images on the HackyPi screen you will need to ensure you convert your images to a .bmp format. 
Normal Bitmap (24-bit) will not work. You need to convert them to indexed color BMPs (8-bit or less with a color palette), not standard 24-bit RGB BMPs. If the images are standard 24-bit color, they will fail to load on the HackyPi screen.

You will also need to ensure the images are the correct size for the screen. (240x135)
(HackyPi will NOT auto resize images)

If you would like to change the font (vt323_12 from Google Fonts by default) you can upload any standard ttf font but the ttf (TrueType font) will need to be converted to a .bdf font format. 
(HackyPi will NOT auto convert ttf to bdf)

# WARNING
This payload is for educational purposes only. Unauthorized access to computer systems is illegal and can result in serious legal consequences. Use this tool responsibly and only with proper authorization.