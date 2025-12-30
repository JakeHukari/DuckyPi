# DuckyPi
DuckyPi Harvester payload for the HackyPi device from SB Components.

Official HackyPi can be obtained from: https://shop.sb-components.co.uk/products/hackypi-compact-diy-usb-hacking-tool

# Requirements
- HackyPi device
- MicroSD card
- USB flash drive named `DUCKYPI` (FAT32 formatted)

# Setup
1. Plug in the HackyPi & wait for the filesystem to mount.
2. Copy `code.py` & the `lib` folder to the root of the HackyPi filesystem.
3. Plug a MicroSD card into your computer & copy both folders inside of `sd_card_assets` (assets & fonts) onto the SD card.
4. Plug a separate USB drive into your computer & rename it to exactly: `DUCKYPI` (ensure it is formatted to FAT32).
5. Unplug the HackyPi, MicroSD card, & DUCKYPI USB drive.

# Safe Mode 
DuckyPi has a built-in `Safe Mode` function that can be enabled by pressing `Caps Lock` while the HackyPi is booting.

Once the DuckyPi code is placed on the HackyPi device you can press `Caps Lock` during boot or t-5 second countdown to enter `Safe Mode` to prevent the device from executing HID functions.

Safe Mode allows you to modify the HackyPi filesystem without executing the payload.

# Execution
1. Plug the HackyPi into the target computer. (Ensure the sd card is inserted into the HackyPi)
2. Plug the DUCKYPI USB drive into the target computer.
3. Wait

Upon boot (unless Safe Mode is enabled), the HackyPi will begin harvesting.

The HackyPi will harvest all stored WiFi usernames & passwords, system information, & stored browser data (saved login data, browsing history, cookies, etc. from Chrome, Firefox, & Edge).

The HackyPi will compress all harvested data into a zip file & copy it to the `DUCKYPI` USB drive.

The HackyPi will then delete the harvested data from the system. It will only remain on the `DUCKYPI` USB drive.

# Loot Retrieval
Once harvest is complete there will be a date & time stamped zip file on the `DUCKYPI` USB drive.
Unzip the file & you will find the harvested data.
WiFi credentials & system info will be stored in plaintext file format (.txt).
Browser information will be stored in database format (sqlite & json). Some browser information may be encrypted or hashed & will need to be decrypted to view the data.

# Modifications
To modify the images on the HackyPi screen you will need to ensure you convert your images to a .bmp format.
Normal Bitmap (24-bit) will not work. You need to convert them to indexed color BMPs (8-bit or less with a color palette). If the images are standard 24-bit color, they will fail to load on the HackyPi screen.

You will also need to ensure the images are the correct size for the screen (240x135).
The HackyPi will NOT auto-resize images.

If you would like to change the font (vt323_12 from Google Fonts by default) you can upload any standard TTF font but it will need to be converted to a .bdf font format.
The HackyPi will NOT auto-convert TTF to BDF.

# WARNING
This payload is for educational purposes only. Unauthorized access to computer systems is illegal & can result in serious legal consequences. Use this tool responsibly & only with proper authorization.