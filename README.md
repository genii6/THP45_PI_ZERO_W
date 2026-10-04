## Blockout Routine

The following describes how to setup the THP45 scripts to configure the hot water system blockout times at fixed times each day.
2PM Everyday:
Set to peak

9PM Everyday:
Set to overnight

8AM Everyday:
Set to overnight-free

## Daily crontab

Install the project at `~/THP45_PI_ZERO_W` on the Raspberry Pi. Initialize its
database once from that directory:

```sh
cd "$HOME/THP45_PI_ZERO_W"
/usr/bin/python3 setup.py
```

Add these entries with `crontab -e`. They run using the Raspberry Pi's local
time and append command output to `blockout-cron.log` in the project directory:

```bash
0 8  * * * python3 ~/THP45_PI_ZERO_W/main.py overnight-free >> ~/THP45_PI_ZERO_W/blockout-cron.log 2>&1
0 14 * * * python3 ~/THP45_PI_ZERO_W/main.py peak           >> ~/THP45_PI_ZERO_W/blockout-cron.log 2>&1
0 21 * * * python3 ~/THP45_PI_ZERO_W/main.py overnight      >> ~/THP45_PI_ZERO_W/blockout-cron.log 2>&1
```

## WIFI Connectivity Checks

Create this with :
```sh
sudo vim /usr/local/bin/netcheck.sh
```

```bash
#!/bin/bash
LOG=/var/log/netcheck
TARGET=8.8.8.8   # or your router, e.g. 10.0.0.1

log() { echo "$(date '+%Y-%m-%d %H:%M:%S') $*" >> "$LOG"; }

if ping -c 3 -W 5 "$TARGET" >/dev/null 2>&1; then
    log "OK ping $TARGET"
    exit 0
fi

log "FAIL ping $TARGET, restarting wifi"
nmcli radio wifi off; sleep 5; nmcli radio wifi on
sleep 30

if ping -c 3 -W 5 "$TARGET" >/dev/null 2>&1; then
    log "OK recovered after wifi restart"
else
    log "FAIL still down, rebooting"
    sync
    /sbin/reboot
fi
```

Make it executable:
```sh
sudo chmod +x /usr/local/bin/netcheck.sh
```

Add this entry with `sudo crontab -e`. This runs netcheck every 5 minutes.
```bash
*/5 * * * * /usr/local/bin/netcheck.sh >> /var/log/netcheck 2>&1
```