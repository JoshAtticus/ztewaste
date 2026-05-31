@echo off
echo Rebooting to Unisoc BROM mode (ignore if this fails)...
adb reboot autodloader
echo Waiting for device to connect in Unisoc BROM mode (if the previous step failed, power off device, then hold volume down and connect USB, release once device is detected)...
cd unisoc_brom
spd_dump.exe exec_addr 0x65012f48 fdl fdl1-dl.bin 0x65000800 fdl fdl2-dl.bin 0xb4fffe00 exec r ztepersist reset
cd ..

echo Dump complete. Processing data...
python3 processor.py unisoc_brom\ztepersist.bin zte_dump.txt

echo Done! Please check zte_dump.txt.
pause