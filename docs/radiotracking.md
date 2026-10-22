# Radiotracking (`radiotracking.service`)

`radiotracking.service` detects the signals of VHF wildlife tracking transmitters with the station's RTL-SDR dongles and publishes them to `/data` and the local MQTT broker. The program is [pyradiotracking](https://github.com/trackIT-Systems/pyradiotracking); its [Readme](https://github.com/trackIT-Systems/pyradiotracking/blob/main/Readme.md) describes the detection algorithm, all outputs and the conversion to dBm. This page covers how tsOS-vhf runs it.

## Service

[radiotracking.service](../etc/systemd/system/radiotracking.service) runs:

```
/usr/local/bin/radiotracking --config /boot/firmware/radiotracking.ini --station %H \
    --mqtt --mqtt-host localhost --mqtt-port 1883 --csv --export-config --path /data
```

- **Station name**: the hostname (`%H`, also the directory under `/data`), so topics and file names follow `systemd.hostname=` in `cmdline.txt`. Station names must be unique for a server to tell stations apart.
- **Options on the command line override `radiotracking.ini`**: MQTT to the local broker, CSV files and the exported configuration under `/data` are always on.
- **User**: `pi`, with a sandbox, see [Architecture](architecture.md#security). `Nice=-10`, so the analysis keeps up under load.
- **Start conditions**: after `time-sync.target` (`Requires=`), `mosquitto.service` and `hostname-config.service`; only with the `/boot/firmware` and `/data` mounts; only if `/boot/firmware/radiotracking.ini` exists. tsOS-base's `chrony-wait.service` holds `time-sync.target` until chrony has synced, without a timeout. Signal times must be comparable between stations, so the service does not start with an unsynced clock.

## Configuration

`/boot/firmware/radiotracking.ini` ([default](../boot/firmware/radiotracking.ini)), edited on the card or in tsconfig. Values are Python literals (`device = ['0', '1']`). [pyradiotracking's etc/radiotracking.ini](https://github.com/trackIT-Systems/pyradiotracking/blob/main/etc/radiotracking.ini) lists every option with its default, `radiotracking -h` describes them. Changes take effect when the service restarts.

| Section | Options set by the default | Notes |
| --- | --- | --- |
| `[optional arguments]` | `verbose`, `calibrate`, `config`, `schedule` | `calibrate` marks the CSV files as a calibration run and disables MQTT, see [Files](#files). `schedule` is ignored (tsconfig writes `schedule = ['']`); power scheduling is tsOS-base's `tsschedule` |
| `[rtl-sdr]` | `device`, `calibration`, `center_freq` (150.155 MHz), `sample_rate` (300 kHz), `gain`, `lna_gain`, `mixer_gain`, `vga_gain`, `sdr_max_restart`, `sdr_timeout_s` | One `device` and `calibration` entry per SDR. The separate gain stages need the trackIT librtlsdr fork, which the image ships |
| `[analysis]` | `fft_nperseg`, `fft_window`, `signal_threshold_dbw`, `snr_threshold_db`, `signal_min_duration_ms`, `signal_max_duration_ms` | Detection thresholds |
| `[matching]` | `matching_timeout_s`, `matching_time_diff_s`, `matching_bandwidth_hz`, `matching_duration_diff_ms` | Grouping of one transmission across SDRs |
| `[publish]` | `sig_stdout`, `match_stdout`, `path`, `csv`, `export_config`, `mqtt`, `mqtt_host`, `mqtt_port` | `path`, `csv`, `export_config` and the MQTT options are overridden by the service |

### Calibration

SDRs of the same model differ in their attenuation, and a station with directional antennas compares the powers of its SDRs. Two settings exist per SDR:

- `calibration` - an offset in dB added to the SDR's powers (dBW), so that the SDRs of a station read the same power for the same transmitter.
- `fullscale_dbm` - the receiver's full scale input power, measured once per receiver. With it, powers are also published in dBm at the antenna port. See [Powers in dBm](https://github.com/trackIT-Systems/pyradiotracking/blob/main/Readme.md#powers-in-dbm).

## Outputs

### Files

`/data/<host>/radiotracking/<host>_<start time>*.csv` (`<start time>` as `YYYY-MM-DDTHHMMSS`), a new set at every start of the service:

| File | Content |
| --- | --- |
| `<host>_<start time>.csv` | signals of every SDR |
| `…-matched.csv` | matched signals: one transmission, with its power on each SDR |
| `…-calibrated.csv` | matched signals in dBm (SDRs with `fullscale_dbm`) |
| `…-gain.csv` | gain settings and dBW to dBm offset at every SDR start |
| `…-state.csv` | SDR state changes |
| `…-spectrum.csv` | noise level and SNR of every frequency bin, every `spectrum_interval_s` (300 s) |

With `--export-config`, the configuration in effect is written next to them as `<host>_<start time>.ini`. With `calibrate = True`, every file name gets the suffix `_calibration` and nothing is published over MQTT. `/data` is reachable over FileBrowser, WebDAV and SFTP (tsOS-base).

### MQTT

Published to the local broker as JSON, CSV and CBOR:

| Topic | Payload |
| --- | --- |
| `<host>/radiotracking/device/<device>/<format>` | signals of one SDR |
| `<host>/radiotracking/matched/<format>` | matched signals |
| `<host>/radiotracking/calibrated/<format>` | matched signals in dBm |
| `<host>/radiotracking/gain/<device>/<format>` | gain and dBm offset, retained |
| `<host>/radiotracking/state/<format>` | SDR states |
| `<host>/radiotracking/spectrum/<format>` | noise and SNR per frequency bin |

tsconfig's live dashboard reads `device`, `matched` and `calibrated` over `/mqtt`.

A bridge in `/boot/firmware/mosquitto.d` decides what leaves the station. Forwarding every signal plus warnings and worse of every service ([tsOS-base logging](https://github.com/trackIT-Systems/tsOS-base/blob/main/docs/logging.md#forwarding-over-mqtt)):

```
topic +/radiotracking/# out 1
topic +/tsconfig/journal/+/emerg/cbor out 1
topic +/tsconfig/journal/+/alert/cbor out 1
topic +/tsconfig/journal/+/crit/cbor out 1
topic +/tsconfig/journal/+/err/cbor out 1
topic +/tsconfig/journal/+/warning/cbor out 1
topic +/tsconfig/journalstats/cbor out 1
```

Over a cellular link, `+/radiotracking/+/cbor` and `+/radiotracking/+/+/cbor` carry the same data in its compact form.

A second radiotracking instance on the station (e.g. for debugging) needs its own `--mqtt-client-id`, otherwise it takes over the session of the service.

## Logging

radiotracking follows the [tsOS logging convention](https://github.com/trackIT-Systems/tsOS-base/blob/main/docs/logging.md): it writes to the journal with a priority, `SYSLOG_IDENTIFIER=radiotracking` and the source location, logs at `WARNING` by default, and logs nothing periodic above `DEBUG`. A working station logs nothing after its start.

- `journalctl -u radiotracking -p warning` - warnings and worse
- `journalctl -u radiotracking -o verbose` - with the source location (`CODE_FILE`, `CODE_LINE`, `CODE_FUNC`)
- `-v` (INFO) or `-vv` (DEBUG) is added to `ExecStart` temporarily with a drop-in (`systemctl edit radiotracking`, as root)

Its warnings and errors reach `<host>/tsconfig/journal/radiotracking/<level>/…` through `tstelemetry`.

## Recovery

Failures are handled in three stages, from one SDR up to the whole station:

1. **SDR restart (radiotracking)**. An SDR is restarted when no samples arrive for `sdr_timeout_s`, or when the analysis cannot keep up and the ring buffer overflows. The other SDRs keep running.
2. **Service restart (systemd)**. After `sdr_max_restart` restarts of an SDR, radiotracking exits, including the SDRs that still work: bearings need every direction, so a station does not continue incomplete. systemd restarts the service after 60 s (`Restart=always`, `RestartSec=60s`).
3. **Reboot (systemd)**. More than 10 starts within 15 minutes reboot the station (`StartLimitBurst=10`, `StartLimitIntervalSec=900s`, `StartLimitAction=reboot`), which also resets the USB stack. With `RestartSec=60s` this happens 10 minutes after the first failure at the earliest.

A hang of the whole system is covered by tsOS-base's [hardware watchdog](https://github.com/trackIT-Systems/tsOS-base/blob/main/docs/watchdog.md).

`systemctl stop radiotracking` stops the restarts and reboots, e.g. while copying data from a failing station.

### Monitoring

- **Service state** (tsconfig, `systemctl status radiotracking`): active only means the process runs. A station that restarts one SDR over and over is still active.
- **Uptime** (`system` telemetry of tsOS-base): a low uptime that keeps resetting means reboots by stage 3.
- **SDR states** (`<host>/radiotracking/state/…`): starts and stops per SDR.
- **Signals per SDR** (`<host>/radiotracking/device/<device>/…`): the most direct evidence, but only while a transmitter is in range. Matched signals alone hide a single failing SDR.
- **Journal counts** (`<host>/tsconfig/journalstats/…`): warnings and errors of `radiotracking` per interval.

## Troubleshooting

### The station keeps restarting

Check the log for which SDR is restarted.

- **The same SDR, again and again**: its USB connection, the USB hub, or the dongle itself. Replug or replace it.
- **Different SDRs at random**, often after the analysis fell behind: the system cannot keep up. Check
  - the temperature (`thermal` telemetry, below 80 °C) and the heat sink,
  - the power supply of the Raspberry Pi and the USB hub (`throttled` telemetry, `under_voltage`),
  - the configuration: raising `signal_threshold_dbw`, `snr_threshold_db` or `signal_min_duration_ms` reduces the number of signals to process. pyradiotracking's `etc/benchmark.py` times the analysis for a configuration.

### The service does not start

- **No time sync**: the service waits for `time-sync.target`. `chronyc tracking` shows whether chrony has synced. Without a network connection or GPS, check the cellular modem (`mmcli -L`, `nmcli device`) and the uplink (`ping -c4 8.8.8.8`).
- **No configuration**: `/boot/firmware/radiotracking.ini` must exist (`ConditionPathExists=`).
- **No SDR found**: `rtl_test` lists the dongles. Stop the service first, a dongle can only be opened once.

### `Failed to allocate zero-copy buffer`

The usbfs memory limit is not removed. `cat /sys/module/usbcore/parameters/usbfs_memory_mb` must print `0`; it is set at boot by [usbfs.conf](../etc/tmpfiles.d/usbfs.conf).

### The station runs but is not reachable

The LEDs are lit and the hotspot SSID is visible, but no address is assigned and WireGuard does not respond. The cause is not known; a hardware defect is suspected. Power-cycle the station.
