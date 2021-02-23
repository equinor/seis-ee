# Earthworm Service

Short description on how the Earthworm service is configured, with some useful commands.

## Systemd

To make sure earthworm restarts on system reboot, it's setup as a systemd service.  
The service file is located at `/etc/systemd/system/earthworm.service` and looks like this;

```toml
[Unit]
Description=Earthworm auto startstop
[Service]
ExecStart=/home/earthworm/ew/earthworm_7.10/bin/startstop
User=earthworm
Group=earthworm
Environment=EW_PARAMS=/home/earthworm/ew/earthworm_7.10/run/params/
Environment=EW_BITS=64
Environment=EW_DATA_DIR=/home/earthworm/ew/earthworm_7.10/run/data/
Environment=EW_VERSION=earthworm_7.10
Environment=EW_INST_ID=INST_NNSN
Environment=EW_LOG=/home/earthworm/ew/earthworm_7.10/run/log/
Environment=EW_RUN_DIR=/home/earthworm/ew/earthworm_7.10/run
Environment=EW_HOME=/home/earthworm/ew/earthworm_7.10
Environment=EW_INSTALLATION=INST_UNKNOWN
Environment=PATH=/home/earthworm/ew/earthworm_7.10/bin
Environment=SYS_NAME=localhost
[Install]
WantedBy=multi-user.target
```

If earthworm needs to be started or stopped, it can  be achived whith these commands __as root__

```bash
systemctl start earthworm
systemctl stop earthworm
systemctl restart earthworm
```

If you make changes to the earthworm.service file, run `systemctl daemon-reload` to load the new config, and then restart the service with `systemctl restart earthworm`.

To see if earthworm is running succsesfully or not, run;  

```bash
earthworm@earthworm:~$ systemctl status earthworm
* earthworm.service - Earthworm auto startstop
Loaded: loaded (/etc/systemd/system/earthworm.service; enabled; vendor preset: enabled)
Active: active (running) since Tue 2021-02-23 13:49:34 UTC; 22min ago
Main PID: 299461 (startstop)
Tasks: 22 (limit: 38530)
Memory: 272.1M
(...)
```

## Logs

To view all logs from earthworm (there can be alot):  
`journalctl -u earthworm`

To follow live logs:
```bash
earthworm@earthworm~$ journalctl -f -u earthworm
-- Logs begin at Thu 2021-02-11 10:19:09 UTC, end at Tue 2021-02-23 14:14:01 UTC. --
Feb 23 14:13:04 earthworm startstop[299471]:                                                                        Total
Feb 23 14:13:04 earthworm startstop[299471]:                   Dead Time                  Gap Length (sec)           gap
Feb 23 14:13:04 earthworm startstop[299471]:       SCNL        (dy:hr:mn)  le 0  0-.25 .25-1.1  1.1-8  8-64    >64  (sec)
Feb 23 14:13:04 earthworm startstop[299471]:       ----        ----------  ----  -----  ------  -----  ----   ----  -----
Feb 23 14:13:04 earthworm startstop[299471]: Equinor stations
Feb 23 14:13:04 earthworm startstop[299471]:  GRA01 EHZ NS 00    0:00:00      0      0      1      0      0      0      0
Feb 23 14:13:04 earthworm startstop[299471]:  OSE01 EHZ NS 00    0:00:00      0      0      0      0      1      0     10
```
