import sys
import string
import re
from collections import defaultdict

def main():
    if len(sys.argv) < 3:
        print("Usage: python processor.py <input.bin> <output.txt>")
        return

    filepath = sys.argv[1]
    outpath = sys.argv[2]
    
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return

    text = data.decode('ascii', errors='ignore')
    lines = text.split('\n')
    
    extracted_records = set()
    charge_cycles = set()
    power_stats = {}
    system_events = {}
    ota_history = set()

    for line in lines:
        clean_line = ''.join(c for c in line if c in string.printable and c not in '\r\n')
        if not clean_line:
            continue

        # App Usage
        if 'RecordTime->' in clean_line and '->' in clean_line:
            idx = clean_line.find('RecordTime->')
            if idx != -1:
                extracted_records.add(clean_line[idx:])
                
        # Charge Cycles
        elif 'Begin:20' in clean_line and 'ChargType:' in clean_line:
            idx = clean_line.find('Begin:20')
            if idx != -1:
                charge_cycles.add(clean_line[idx:])
                
        # Power Stats
        pow_match = re.search(r'(POWER(?:ON|OFF)_[A-Z0-9_]+)\s*=\s*(\d+)', clean_line)
        if pow_match:
            key, val = pow_match.groups()
            power_stats[key] = max(power_stats.get(key, 0), int(val))
            
        # System events/health
        sys_match = re.search(r'(SYSTEM_[A-Z_]+|system_app_anr|event_log)\s+->\s+(\d+)', clean_line)
        if sys_match:
            key, val = sys_match.groups()
            system_events[key] = max(system_events.get(key, 0), int(val))
            
        # OTA Updates
        elif 'Fingerprint ->' in clean_line:
            idx = clean_line.find('Fingerprint ->')
            if idx != -1:
                ota_history.add(clean_line[idx:])

    sorted_records = sorted(list(extracted_records))

    flat_data = []
    for record in sorted_records:
        parts = record.split(',')
        if not parts:
            continue
            
        time_part = parts[0]
        if time_part.startswith('RecordTime->'):
            time_val = time_part.split('->')[1]
            if not re.match(r'^\d{4}-\d{2}-\d{2}_\d{2}:\d{2}$', time_val):
                continue
            
            for app_part in parts[1:]: # Fixed indexing
                if '->' in app_part:
                    app, val = app_part.split('->', 1)
                    flat_data.append({
                        "time": time_val.replace('_', ' '),
                        "app": app
                    })

    app_last_used = {}
    for entry in flat_data:
        app = entry["app"]
        time = entry["time"]
        if app not in app_last_used or time > app_last_used[app]:
            app_last_used[app] = time

    flat_data.sort(key=lambda x: x["time"], reverse=True)
    last_100 = flat_data[:100]

    with open(outpath, 'w', encoding='utf-8') as out:
        out.write("=== INSTALLED APPS AND LAST USED DATE ===\n\n")
        for app in sorted(app_last_used.keys()):
            out.write(f"{app} | Last Used: {app_last_used[app]}\n")
            
        out.write("\n" + "="*80 + "\n\n")
        out.write("=== LAST 100 USED APPS ===\n\n")
        for idx, entry in enumerate(last_100, 1):
            out.write(f"{idx:03d}. {entry['time']} | {entry['app']}\n")
            
        out.write("\n" + "="*80 + "\n\n")
        out.write("=== OTA UPDATE & FIRMWARE HISTORY ===\n\n")
        for ota in sorted(list(ota_history)):
            out.write(f"{ota}\n")
            
        out.write("\n" + "="*80 + "\n\n")
        out.write("=== SYSTEM HEALTH & EVENT COUNTERS ===\n\n")
        for k, v in sorted(system_events.items()):
            out.write(f"{k} : {v}\n")
            
        out.write("\n" + "="*80 + "\n\n")
        out.write("=== POWER & THERMAL TIMERS ===\n\n")
        for k, v in sorted(power_stats.items()):
            out.write(f"{k} : {v}\n")

        out.write("\n" + "="*80 + "\n\n")
        out.write("=== BATTERY CHARGING CYCLES ===\n\n")
        for cycle in sorted(list(charge_cycles)):
            out.write(f"{cycle}\n")

    print(f"Summary generated at {outpath}")

if __name__ == '__main__':
    main()