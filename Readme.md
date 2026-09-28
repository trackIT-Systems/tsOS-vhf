# tsOS-vhf
[![Build tsOS-vhf Images](https://github.com/trackIT-Systems/tsOS-vhf/actions/workflows/build.yml/badge.svg)](https://github.com/trackIT-Systems/tsOS-vhf/actions/workflows/build.yml)
[![GitHub Release](https://img.shields.io/github/v/release/trackIT-Systems/tsOS-vhf)](https://github.com/trackIT-Systems/tsOS-vhf/releases/latest)

tsOS-vhf is a Raspberry Pi OS image for unattended VHF wildlife-tracking stations. It receives signals from VHF tags on animals, records detections and features, and forwards them for bearing estimation and activity classification.

[trackIT Systems](https://trackit.systems) supplies **vhf:tracker** stations commercially, running this image in the field.

The image is built on [tsOS-base](https://github.com/trackIT-Systems/tsOS-base) for **arm64** (Raspberry Pi 3+ / Compute Module).

## What's in the image

On top of tsOS-base:

- **[pyradiotracking](https://github.com/trackIT-Systems/pyradiotracking)** — RTL-SDR signal detection, matching, CSV/MQTT export, dashboard
- **[librtlsdr](https://github.com/librtlsdr/librtlsdr)** fork and **[pyrtlsdr](https://github.com/pyrtlsdr/pyrtlsdr)** — R802T gain stages and Python bindings
- **Caddy** route `/radiotracking/` to the dashboard (`localhost:8050`)
- **`radiotracking.service`** — starts after time sync, `Nice=-10`, writes detections to `/data`

Inherited from [tsOS-base](https://github.com/trackIT-Systems/tsOS-base/blob/main/Readme.md): tsconfig, FileBrowser Quantum, Mosquitto, mqttutil, Chrony/gpsd, WittyPi (`tsschedule`), WireGuard, Samba, LTE helpers, overlayroot.

## Download and flash

Images are published in [GitHub Releases](https://github.com/trackIT-Systems/tsOS-vhf/releases). Release notes live in [CHANGELOG.md](CHANGELOG.md).

Flash with Raspberry Pi Imager or `dd`. Default hostname is `tsos-default-name` (set `systemd.hostname=` in [`cmdline.txt`](https://github.com/trackIT-Systems/tsOS-base/blob/main/boot/firmware/cmdline.txt) on the boot partition). For backend matching, use `<planner>-<project>-<number>`; each station name must be unique.

## First access

**SSH:** user `pi`, password `natur`. Drop a public-key file at `/boot/firmware/authorized_keys` on the card; it is installed for `pi` and `root` on boot.

**Wi-Fi hotspot:** SSID follows the hostname, PSK `BirdsAndBats`. The station is `169.254.0.1`. An optional extra client network can be defined in [`wlan1.conf`](boot/firmware/wlan1.conf).

**Web:** Caddy on port 80 — tsconfig at `/`, FileBrowser Quantum at `/data/`, radiotracking dashboard at `/radiotracking/` ([Caddyfile](etc/caddy/Caddyfile)).

## Boot configuration

Runtime settings live on the VFAT boot partition (`/boot/firmware` on the Pi). Edit on the card, then reboot.

| File | Purpose |
| --- | --- |
| `cmdline.txt` | `systemd.hostname=`, `timezone=`, first-boot `repartition` |
| [`radiotracking.ini`](boot/firmware/radiotracking.ini) | pyradiotracking ([example](https://github.com/trackIT-Systems/pyradiotracking/blob/main/etc/radiotracking.ini)) |
| [`wlan1.conf`](boot/firmware/wlan1.conf) | Optional extra Wi-Fi client (`wlan1`) |
| `mqttutil.conf` | MQTT system reporting |
| `mosquitto.d/` | Extra Mosquitto broker configs (`include_dir`) |
| `wireguard.conf` | WireGuard interface |
| `authorized_keys` | SSH keys copied to `pi` and `root` |
| `tsconfig.yml` | tsconfig service config |
| `geolocation` | Static GPS coordinates |

Platform files other than `radiotracking.ini` and `wlan1.conf` come from tsOS-base. See that project's [boot configuration](https://github.com/trackIT-Systems/tsOS-base/blob/main/Readme.md#boot-configuration).

In tsconfig, saving and deploying configuration are separate actions — use **Deploy** after saving changes that should take effect on the station.

## Storage

`/data` is the station data volume (ExFAT `datafs` after first-boot repartition, or a USB disk). `radiotracking.service` writes CSV detections there. FileBrowser Quantum roots at `/data`.

## Updates

`tsupdate` applies OTA images using Raspberry Pi tryboot, with automatic rollback if the new image fails to boot. Operator overview: [tsOS-base updatability](https://github.com/trackIT-Systems/tsOS-base/blob/main/docs/updatability.md). GitHub Releases may also attach pidiff update tarballs between consecutive images.

## Hardware

- RTL-SDR dongles (R802T): staged gains `lna_gain`, `mixer_gain`, `vga_gain` via the librtlsdr fork
- USB hub power via `uhubctl` (logged on radiotracking start)
- Plus tsOS-base hardware: WittyPi 4, GPS, LTE, watchdog — [tsOS-base hardware](https://github.com/trackIT-Systems/tsOS-base/blob/main/Readme.md#hardware)

## Build

Images are two-stage: a published [tsOS-base](https://github.com/trackIT-Systems/tsOS-base/releases) zip (currently 2027.0.1), then this repo's Pifile via [pimod](https://github.com/Nature40/pimod) `v0.9.3` ([docker-compose.yml](docker-compose.yml)):

```sh
docker-compose run --rm pimod pimod.sh tsOS-vhf.Pifile
```

## Further reading

- [Quickstart](docs/index.md) — flash, configure, first checks, SDR calibration
- [Operation](docs/operation.md) — services, restarts, monitoring
- [Troubleshooting](docs/troubleshooting.md)
- [Common tasks](docs/tasks.md)
- [tsOS-base](https://github.com/trackIT-Systems/tsOS-base) — overlayroot, partitions, OTA, shared services
- [CHANGELOG.md](CHANGELOG.md)

## Citation

If you use tsOS-vhf in academia, please cite [Höchst & Gottwald et al.](https://jonashoechst.de/assets/papers/hoechst2021tRackIT.pdf)

> J. Höchst, J. Gottwald, P. Lampe, J. Zobel, T. Nauss, R. Steinmetz, and B. Freisleben, “trackIT OS: Open-source Software for Reliable VHF Wildlife Tracking,” in 51. Jahrestagung der Gesellschaft für Informatik, Digitale Kulturen, INFORMATIK 2021, Berlin, Germany, 2021.

```bibtex
@inproceedings{hoechst2021trackIT,
  title = {{trackIT OS: Open-source Software for Reliable VHF Wildlife Tracking}},
  author = {Höchst, Jonas and Gottwald, Jannis and Lampe, Patrick and Zobel, Julian and Nauss, Thomas and Steinmetz, Ralf and Freisleben, Bernd},
  booktitle = {51. Jahrestagung der Gesellschaft f{\"{u}}r Informatik, Digitale Kulturen, {INFORMATIK} 2021, Berlin, Germany},
  series = {{LNI}},
  publisher = {{GI}},
  month = sep,
  year = {2021}
}
```
