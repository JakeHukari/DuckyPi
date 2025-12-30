# DuckyPi
DuckyPi Harvester payload for the HackyPi device from SB Components.

Official HackyPi can be obtained from: https://shop.sb-components.co.uk/products/hackypi-compact-diy-usb-hacking-tool

# Requirements
- HackyPi device
- MicroSD card
- USB flash drive named `DUCKYPI` (FAT32 formatted)

# Setup
#### HackyPi
1. Plug in the HackyPi & wait for the filesystem to mount.
2. Copy `code.py` & the entire `lib` folder to the root of the HackyPi filesystem.
#### Micro SD card
3. Plug a MicroSD card into your computer & copy both folders inside of `sd_card_assets` (assets & fonts) onto the SD card.

(Ensure you copy the assets & fonts folders INSIDE of the sd_card_assets folder NOT the entire sd_card_assets folder itself)

#### DUCKYPI USB drive (this will be the loot storage device)
4. Plug a separate USB drive into your computer & rename it exactly: `DUCKYPI` (ensure it is formatted to FAT32).

(If you want the use a different name for your loot storage device, ensure you also change the name in the code.py file (line 354))
#### Final step
5. Unplug the HackyPi, MicroSD card, & DUCKYPI USB drive.
6. Insert the MicroSD card into the HackyPi.

# Safe Mode 
DuckyPi has a built-in `Safe Mode` function that can be enabled by pressing `Caps Lock` while the HackyPi is booting.

Once the DuckyPi code is placed on the HackyPi device you can enable `Caps Lock` during boot or t-5 second countdown to enter `Safe Mode` to prevent the device from executing HID functions.

Safe Mode allows you to modify the HackyPi filesystem without executing the payload.

# Execution
1. Plug the HackyPi into the target computer. (Ensure the sd card is inserted into the HackyPi)
2. Plug the DUCKYPI USB drive into the target computer.
3. Wait
4. Harvest Process will begin.

# Harvest Process
1. Upon boot, after the 5 second countdown (unless Safe Mode is enabled), the HackyPi will begin harvesting.

2. The HackyPi will harvest all stored WiFi usernames & passwords, system information, & stored browser data (saved login data, browsing history, cookies, etc. from Chrome, Firefox, & Edge) from the target computer.

3. The HackyPi will compress all harvested data into a zip file & copy it to your `DUCKYPI` (loot storage device) USB drive.

4. The HackyPi will then delete the harvested data from the system. It will only remain on your `DUCKYPI` (loot storage device) USB drive.

# Loot Retrieval
Once harvest is complete there will be a compressed, date & time stamped, Loot folder on your `DUCKYPI` (loot storage device) USB drive.

Unzip the folder & you will find the harvested data.

WiFi credentials & system info will be stored in plaintext file format (.txt).

Browser information will be stored in database format (sqlite & json). Some browser information may be encrypted or hashed & will need to be decrypted to view the data.

The Loot folder will also contain a log file of the harvest process. If any errors occur during the harvest process use the log to dertermine which step failed.

# Modifications
## Timers
To modify the countdown timer- change the `COUNTDOWN_SECONDS` variable in the `code.py` file (line 38). (default is 5 seconds)

To modify the delay between commands- change the `CMD_DELAY` variable in the `code.py` file (line 39). (default is 1 second)

## Images
To modify the images on the HackyPi screen you will need to ensure you convert your images to a .bmp format.

Normal Bitmap (24-bit) will not work. You need to convert them to indexed color BMPs (8-bit or less with a color palette). If the images are standard 24-bit color, they will fail to load on the HackyPi screen.

You will also need to ensure the images are the correct size for the screen (240x135).

#### The HackyPi will NOT auto-resize images.

## Fonts
To modify the font (vt323_12 from Google Fonts by default) you can upload any standard TTF font but it will need to be converted to a .bdf font format.

#### The HackyPi will NOT auto-convert TTF to BDF.

##
### If you upload images or fonts that are not compatible- the device will still execute the code.py payload but the images and font will not display.
#### (so its not really a big deal) 

# WARNING
This project is for educational purposes only. Unauthorized access to any computer systems is illegal & can result in serious legal consequences. Use this tool responsibly & only with proper authorization 😉.