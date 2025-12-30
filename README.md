# DuckyPi
DuckyPi Harvester payload for the 'HackyPi device from SB Components
# Setup
Plug in the hackypi and wait for filesystem to mount.
Copy code.py, and lib folder to the root of the Hackypi filesystem.
Plug a micro sd card into computer and copy both folders inside of 'sd_card_assests' (assets and fonts) onto the sd card.

Plug a seperate usb or drive into computer and rename it to: 'DUCKYPI'. (ensure it is formatted to FAT32)

Unplug hackypi, micro sd card, and DUCKYPI usb drive.
Plug sd card into the sd card slot on the hackypi.  
Plug hackypi back into computer.
Plug DUCKYPI usb drive into computer.
Upon boot, the hackypi will begin harvesting.

The hackypi will harvest all stored wifi usernames and passwords, system information, and stored browser data. (saved login data, browsing history, cookies, etc from any browser recognized by the hackypi (chrome, firefox, edge))

The hackypi will compress all harvested data into a zip file and copy it to the DUCKYPI usb drive.

The hackypi will then delete the harvested data from the system, it will only remain on the 'DUCKYPI' usb drive. 

# Loot Retrieval
Once harvest is complete there will be a date and time stamped zip file on the 'DUCKYPI' usb drive.
Unzip the file and you will find the harvested data.
Some browser information might be encrypted and will be stored in database format, you may need to decrypt it to view the data.

# WARNING
This payload is for educational purposes only. Unauthorized access to computer systems is illegal and can result in serious legal consequences. Use this tool responsibly and only with proper authorization.