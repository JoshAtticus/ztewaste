# ZTE Diagnostics Dump Proof of Concept
Extract a concerning amount of user information from Unisoc ZTE devices using CVE-2022-38694. 

> [!CAUTION]
> Please **do not permalink here!!!!!** The repo name is almost certainly going to change in the future. Instead, provide a link to my writeup on my blog.

## Usage
1. Download appropriate Unisoc BROM tools from [https://github.com/TomKing062/CVE-2022-38694_unlock_bootloader/releases](https://github.com/TomKing062/CVE-2022-38694_unlock_bootloader/releases). For the ZTE Blade A73 5G/Optus X Pro 5G specifically, as well as other Unisoc T760 devices, use ums9620_ZTE_universal.zip
2. Extract contents of downloaded zip to the root of the `unisoc_brom` folder
3. Run diagdump_poc.bat and follow instructions

## Tested devices
Only tested on ZTE Blade A73 5G (Unisoc T760/UMS9620). 

Should work with other Unisoc T760 ZTE devices, will likely work with other Unisoc ZTE devices, needs modification for non-Unisoc ZTE devices (i.e. replacing Unisoc BROM tools with mtkclient or edl.py if the partition even exists on those devices), and will not work with non-ZTE.

## What's extracted??
- A full log of all apps used (which can be used to create a list of installed apps)
- OTA Update/Firmware Update history (build number, old build number, firmware version, install date & time, update type)
- System boot count, Recovery boot count, App Not Responding count, Crash Report count
- Total system uptime, total time charging
- Total time charging the phone at 45 and 50+ degrees celsius powered on and powered off
- Battery charge cycles (date & time device started charging, fast or normal charging, time charging in m but sometimes just a random number, battery percentage when charging started and ended, minimum battery voltage, maximum battery voltage, minimum battery current, maximum battery current, minimum temperature and maximum temperature in celsius)

## Writeup
Writeup available here: [https://blog.joshattic.us/posts/2026-05-31-your-zte-phone-is-spying-on-you](https://blog.joshattic.us/posts/2026-05-31-your-zte-phone-is-spying-on-you)
