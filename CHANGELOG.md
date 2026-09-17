# Changelog

All notable changes to [tsOS-vhf](https://github.com/trackIT-Systems/tsOS-vhf) are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project uses calendar-based release tags (`YYYY.M.P`).

tsOS-vhf images are built on [tsOS-base](https://github.com/trackIT-Systems/tsOS-base). Base-image changes that ship in a vhf release are listed here and attributed to the corresponding tsOS-base version.

This repository was previously published as **tRackIT OS** (and, for a period, also built **BatRack OS** images). Those historical tags are included below. 

## [Unreleased]

### Changed

- Tag releases use the matching `CHANGELOG.md` section as the GitHub release body (fall back to generated notes if that heading is missing)

## [2026.5.1] - 2026-05-08

Field Release III / 2026. Adds an explicit tuner-bandwidth setting and SDR metrics for configuration in challenging RF environments.

### Added

- `tuner-bandwidth` parameter for radiotracking (defaults to twice the sample rate)
- SDR metrics reporting (`peak`, `rms`, `snr`) for local configuration

## [2026.4.1] - 2026-04-15

Field Release II / 2026. Tested with 1.2 MHz sampling rate and 1024 FFT size on Raspberry Pi 4-based vhf:trackers. Setting the signal threshold too low increases load and can exhaust station resources.

### Added

- Ringbuffer for SDR data to decouple I/O from CPU
- Update artifacts for both the previous release and the previous stable release

### Changed

- radiotracking runs without a bash wrapper and at higher priority (`Nice=-10`)
- Smaller image by removing `*.pyc` files during build
- Based on [tsOS-base 2026.4.1](https://github.com/trackIT-Systems/tsOS-base/releases/tag/2026.4.1) (WiFi priority-based station/hotspot mode, dedicated tsconfig feature flags, background services at `Nice=10`, updates applied by default)

### Fixed

- Hang-ups that could occur during SDR termination

## [2026.3.2] - 2026-03-03

Field Release I / 2026. Mission-critical fixes and improvements for the 2026 field season; most of them come from tsOS-base.

### Changed

- Based on [tsOS-base 2026.3.2](https://github.com/trackIT-Systems/tsOS-base/releases/tag/2026.3.2)
- GitHub image builds run only on tags

### Added (via tsOS-base 2026.3.2)

- Default reporting to `tsos.trackit-system.de`
- Solarlife solar charger readout
- tsconfig reset / wipe option
- Reporting of tsOS version and modem status to the backend

### Changed (via tsOS-base 2026.3.2)

- Using `wpa_supplicant` as the WiFi backend

### Fixed (via tsOS-base 2026.3.2)

- WittyPi 4 power readout
- VE.Direct serial readout
- Memory leak in Solarlife mqttutil usage

## [2026.1.2] - 2026-01-28

Field Candidate III. Further improvements after the first 2026 field candidate.

### Added

- pidiff-based update tarball between consecutive images (`.pidiffignore` for `*.pyc`, shadow files, and `.DS_Store`)

### Changed

- Based on [tsOS-base 2026.1.2](https://github.com/trackIT-Systems/tsOS-base/releases/tag/2026.1.2)
- tsconfig pyradiotracking summary

### Fixed

- Correct termination of radiotracking, allowing lower power consumption
- tsschedule support for Raspberry Pi 5 Compute Module (via tsOS-base)
- Install `rpiboot` for tsflash support (via tsOS-base)

## [2026.1.1] - 2026-01-21

Field Candidate II. Git tag only; no GitHub Releases page was published for this version.

### Changed

- Based on [tsOS-base 2026.1.1](https://github.com/trackIT-Systems/tsOS-base/releases/tag/2026.1.1)

### Added (via tsOS-base 2026.1.1)

- tsflash SD-card flashing tool

### Changed (via tsOS-base 2026.1.1)

- `chronyd-restricted.service` removed in favor of `chrony.service`
- tsconfig updated for tsupdate support
- filebrowser serves `/data` instead of `/media`

### Fixed (via tsOS-base 2026.1.1)

- Network configuration via NetworkManager connection files (instead of netplan)
- Continue `devmon` mounting after `fsck` error (`errors=continue`)

## [2025.12.6] - 2026-01-05

Field Candidate I. Core radiotracking behavior is unchanged; the image picks up the tsOS-base field-candidate platform (5-partition layout, overlayroot, updates).

### Changed

- Based on [tsOS-base 2025.12.6](https://github.com/trackIT-Systems/tsOS-base/releases/tag/2025.12.6)

### Added (via tsOS-base 2025.12.6)

- Samba file sharing
- 5-partition boot layout
- overlayroot booting
- Persistent systemd journal

### Changed (via tsOS-base 2025.12.6)

- Upgrade to Raspberry Pi OS trixie
- Bluetooth enabled on all hardware revisions

### Fixed (via tsOS-base 2025.12.6)

- Reduced image size
- WPA2 authentication with iwd

## [2025.11.4] - 2025-11-14

Pre-release. tsOS-base version bump.

### Changed

- Based on [tsOS-base 2025.11.4](https://github.com/trackIT-Systems/tsOS-base/releases/tag/2025.11.4)

## [2025.11.3] - 2025-11-13

Pre-release.

### Changed

- Based on [tsOS-base 2025.11.3](https://github.com/trackIT-Systems/tsOS-base/releases/tag/2025.11.3)
- `os-release` version codename now follows the configured Debian suite (`trixie`) instead of a leftover `bookworm`/`trixie` mismatch
- radiotracking systemd description set to a full service summary
- radiotracking now `Requires=time-sync.target`

### Removed

- Embedded SSH keys from `home/pi/.ssh/` (authorized keys and a baked-in ed25519 identity)

## [2024.10.4] - 2025-10-29

Pre-release, despite the `2024.10.4` tag name. Renovates the image for Raspberry Pi OS trixie and tsconfig-based configuration.

### Changed

- Based on [tsOS-base 2025.10.4](https://github.com/trackIT-Systems/tsOS-base/releases/tag/2025.10.4)
- Build uses a newer pimod and runs the GitHub workflow on ARM
- radiotracking is installed with `--no-deps` pip flags aligned with the trixie image

### Removed

- `radiotracking-config.service` (configuration moves to tsconfig)
- Bundled bootstrap / Font Awesome assets from the local HTML tree

## [2025.6.1] - 2025-06-10

Field Release III / 2025.

### Added

- Submodule git directories installed into the image (`librtlsdr`, `pyradiotracking`, `pyrtlsdr`) so the shipped sources match the build
- Third `datafs` exFAT partition created on first boot (via [tsOS-base 2025.6.2](https://github.com/trackIT-Systems/tsOS-base/releases/tag/2025.6.2))

### Changed

- Based on tsOS-base 2025.6.2
- Updated pyradiotracking
- Fixed CPU frequency pinning disabled; default scheduler remains in use (via tsOS-base)

### Fixed

- Boot time reduced from ~130 s to ~20 s (via tsOS-base)
- `vedirect_dump` bugfixes (via tsOS-base)

## [2025.4.1] - 2025-04-09

Field Release II / 2025 (with `vga_gain` fix). First field release published under the tsOS-vhf name.

### Changed

- Based on [tsOS-base 2025.3.3](https://github.com/trackIT-Systems/tsOS-base/releases/tag/2025.3.3)
- Default `vga_gain` is now `7`
- Default `signal_threshold_dbw` is now `-95.0`
- New GitHub releases are created as prereleases until promoted

### Fixed

- Termination status used a timezone-naive timestamp, which could produce a CBOR error (fix completed in 2025.3.2; defaults corrected here)

## [2025.3.2] - 2025-03-28

Field Release I / 2025 (with termination fix).

### Fixed

- radiotracking termination status no longer writes a timezone-naive timestamp (avoids CBOR errors on shutdown)

## [2025.3.1] - 2025-03-18

Field Release I / 2025.

### Added

- Timezone configuration via bootfs, WittyPi update, and `authorized_keys` via bootfs (via [tsOS-base 2025.3.2](https://github.com/trackIT-Systems/tsOS-base/releases/tag/2025.3.2))

### Changed

- Based on tsOS-base 2025.3.2
- pyrtlsdr v0.3.0 (compatible with librtlsdr 0.6.0–0.9.0)
- Default `vga_gain` set to `3`
- Default `signal_threshold_dbw` lowered to `-100.0`
- Default `snr_threshold_db` lowered to `3.0`
- radiotracking timestamps are timezone-aware

## [2025.1.dev2] - 2025-01-28

### Changed

- Based on [tsOS-base 2025.1.2](https://github.com/trackIT-Systems/tsOS-base/releases/tag/2025.1.2)
- Default RTL-SDR mixer stages: `lna_gain = 15`, `mixer_gain = 14`, `vga_gain = 15`
- tsOS-base repository rename reflected in the build `FROM` URL

### Added

- GitHub release badge on the project readme

## [2025.1.dev1] - 2025-01-23

### Changed

- Rebranded tRackIT OS to **tsOS-vhf**
- Based on tsOS-Base 2025.1.1
- Updated pimod

### Removed

- BatRack OS image and related build/configuration files

## [2024.10.1] - 2024-10-25

Last tRackIT OS-branded image.

### Changed

- Updated pyradiotracking; AGC is disabled

## [2024.09.1] - 2024-09-26

### Added

- Build against the [librtlsdr fork](https://github.com/librtlsdr/librtlsdr) (R802T gain stages `lna_gain`, `mixer_gain`, `vga_gain`; PLL lock)
- pyrtlsdr as a first-class submodule

### Changed

- Based on tsOS-Base 2024.09.2
- Default `center_freq` is `150155000` Hz
- Default `signal_max_duration_ms` is `50.0`

### Removed

- BatRack OS build target from the primary workflow (files remained until 2025.1.dev1)

## [2024.05.2] - 2024-05-08

### Changed

- Based on [tsOS-Base 2024.05.1](https://github.com/trackIT-Systems/tsOS-base/releases/tag/2024.05.1)

## [2024.05.1] - 2024-05-02

Field Season Update II.

### Changed

- Based on tsOS-Base 2024.04.2

### Fixed

- Startup time-sync issue (via tsOS-Base)

## [2024.04.1] - 2024-04-23 [YANKED]

Field Season Update I. Do not use: this image does not reach `time-sync.target` in some cases. Use [2024.05.1](#2024051---2024-05-02) or later.

### Changed

- Based on [tsOS-Base 2024.04.1](https://github.com/trackIT-Systems/tsOS-base/releases/tag/2024.04.1)

### Fixed

- Protect `resolv.conf` so WiFi / LTE changes do not leave networking unusable (via tsOS-Base)
- WittyPi: file-open leak with mqttutil (I2C bus handle not closed, hitting the open-file limit) (via tsOS-Base)

## [2024.03.1] - 2024-03-05

Field Season Release.

### Added

- WittyPi schedule management (via [tsOS-Base 2024.03.1](https://github.com/trackIT-Systems/tsOS-base/releases/tag/2024.03.1))
- Brovi E3372-325 support on boot (via tsOS-Base)

### Changed

- Based on tsOS-Base 2024.03.1
- Improved huaweicheck handling and software reset (via tsOS-Base)

## [2024.02.1] - 2024-02-21

Workshop Release.

### Added

- WiFi client on `wlan1` (configure via `/boot/firmware/wlan1.conf`)
- Driver for RTL 8822bu WiFi (Amolove AC1200)

### Changed

- Raspberry Pi OS bookworm via [tsOS-Base 2024.02.3](https://github.com/trackIT-Systems/tsOS-base/releases/tag/2024.02.3)

## [2024.01.1] - 2024-01-02

First image built on the split tsOS-Base / tRackIT OS structure.

### Changed

- Build consumes a pre-built tsOS-Base image instead of assembling the whole stack from Raspberry Pi OS in this repository
- Boot configuration moved under `/boot/firmware/`
- Raspberry Pi OS and packages updated (2023-11)

### Added

- I2S microphone module
- Relocate radiotracking files recovered from `lost+found`

### Removed

- In-tree `huaweicheck.py` (logic lives in the base image)

## [BatRack-OS-2023.07.1] - 2023-07-03

BatRack OS image from this repository.

### Added

- Relocate radiotracking files recovered from `lost+found`

## [tRackIT-OS-2023.05.3] - 2023-05-31

Final May 2023 tRackIT OS release; focused on connectivity stability.

### Added

- Internet connectivity via the `usb0` interface (Brovi E3372-325)
- mqttutil queries additional Huawei status fields
- huaweicheck enabled and updated (USB-hub power-cycle recovery)

### Changed

- Sysdweb interface cleanup
- Avahi HTTP service name uses the hostname

## [BatRack-OS-2023.05.3] - 2023-05-30

### Added

- Additional Huawei modem status in mqttutil
- Internet access via `usb0` (Brovi E3372-325)

## [BatRack-OS-2023.05.2] - 2023-05-26

### Fixed

- pybatrack bugfixes

## [BatRack-OS-2023.05.1] - 2023-05-17

### Changed

- Updated BatRack / pybatrack and default configuration
- Raspberry Pi camera exposed on the Caddy frontend

## [2023.05.1] - 2023-05-08

### Changed

- Raspberry Pi OS updated to the 2023-05-03 bullseye lite image
- armhf builds supported
- Caddy updated

### Removed

- Legacy apt-testing import

## [2023.04.1] - 2023-04-17

### Changed

- Updated pyradiotracking: read the exact SDR frequency back from the device (needed for 1 MHz sampling stations)

### Fixed

- mosquitto starts only after time sync

## [2023.03.3] - 2023-03-31

### Changed

- mqttutil waits for time sync
- SmartSolar runs as a process rather than a Python module

## [2023.03.2] - 2023-03-20

### Added

- gpsd started by default (time sync for stations without internet)

### Changed

- Release image renamed to `tRackIT-OS-*.img`

## [2023.03.1] - 2023-03-06

Tag `2023.03.1-beta1` points at the same commit.

### Changed

- Raspberry Pi OS updated to the 2023-02-21 bullseye lite image

### Added

- Huawei E3372 status via the local API

## [2023.02.1] - 2023-02-21

First calendar-tagged tRackIT OS image of 2023, based on Raspberry Pi OS bullseye (2022-09-22). The image already included the radiotracking stack, MQTT logging, GPS/chrony time sync, Victron Energy SmartSolar readout (`pysmartsolar`), Huawei/Brovi E7720-325 support, Avahi services, a landing page, and `flash.sh` for writing SD cards.

[Unreleased]: https://github.com/trackIT-Systems/tsOS-vhf/compare/2026.5.1...HEAD
[2026.5.1]: https://github.com/trackIT-Systems/tsOS-vhf/compare/2026.4.1...2026.5.1
[2026.4.1]: https://github.com/trackIT-Systems/tsOS-vhf/compare/2026.3.2...2026.4.1
[2026.3.2]: https://github.com/trackIT-Systems/tsOS-vhf/compare/2026.1.2...2026.3.2
[2026.1.2]: https://github.com/trackIT-Systems/tsOS-vhf/compare/2026.1.1...2026.1.2
[2026.1.1]: https://github.com/trackIT-Systems/tsOS-vhf/compare/2025.12.6...2026.1.1
[2025.12.6]: https://github.com/trackIT-Systems/tsOS-vhf/compare/2025.11.4...2025.12.6
[2025.11.4]: https://github.com/trackIT-Systems/tsOS-vhf/compare/2025.11.3...2025.11.4
[2025.11.3]: https://github.com/trackIT-Systems/tsOS-vhf/compare/2024.10.4...2025.11.3
[2024.10.4]: https://github.com/trackIT-Systems/tsOS-vhf/compare/2025.6.1...2024.10.4
[2025.6.1]: https://github.com/trackIT-Systems/tsOS-vhf/compare/2025.4.1...2025.6.1
[2025.4.1]: https://github.com/trackIT-Systems/tsOS-vhf/compare/2025.3.2...2025.4.1
[2025.3.2]: https://github.com/trackIT-Systems/tsOS-vhf/compare/2025.3.1...2025.3.2
[2025.3.1]: https://github.com/trackIT-Systems/tsOS-vhf/compare/2025.1.dev2...2025.3.1
[2025.1.dev2]: https://github.com/trackIT-Systems/tsOS-vhf/compare/2025.1.dev1...2025.1.dev2
[2025.1.dev1]: https://github.com/trackIT-Systems/tsOS-vhf/compare/2024.10.1...2025.1.dev1
[2024.10.1]: https://github.com/trackIT-Systems/tsOS-vhf/compare/2024.09.1...2024.10.1
[2024.09.1]: https://github.com/trackIT-Systems/tsOS-vhf/compare/2024.05.2...2024.09.1
[2024.05.2]: https://github.com/trackIT-Systems/tsOS-vhf/compare/2024.05.1...2024.05.2
[2024.05.1]: https://github.com/trackIT-Systems/tsOS-vhf/compare/2024.04.1...2024.05.1
[2024.04.1]: https://github.com/trackIT-Systems/tsOS-vhf/compare/2024.03.1...2024.04.1
[2024.03.1]: https://github.com/trackIT-Systems/tsOS-vhf/compare/2024.02.1...2024.03.1
[2024.02.1]: https://github.com/trackIT-Systems/tsOS-vhf/compare/2024.01.1...2024.02.1
[2024.01.1]: https://github.com/trackIT-Systems/tsOS-vhf/compare/BatRack-OS-2023.07.1...2024.01.1
[BatRack-OS-2023.07.1]: https://github.com/trackIT-Systems/tsOS-vhf/compare/tRackIT-OS-2023.05.3...BatRack-OS-2023.07.1
[tRackIT-OS-2023.05.3]: https://github.com/trackIT-Systems/tsOS-vhf/compare/BatRack-OS-2023.05.3...tRackIT-OS-2023.05.3
[BatRack-OS-2023.05.3]: https://github.com/trackIT-Systems/tsOS-vhf/compare/BatRack-OS-2023.05.2...BatRack-OS-2023.05.3
[BatRack-OS-2023.05.2]: https://github.com/trackIT-Systems/tsOS-vhf/compare/BatRack-OS-2023.05.1...BatRack-OS-2023.05.2
[BatRack-OS-2023.05.1]: https://github.com/trackIT-Systems/tsOS-vhf/compare/2023.05.1...BatRack-OS-2023.05.1
[2023.05.1]: https://github.com/trackIT-Systems/tsOS-vhf/compare/2023.04.1...2023.05.1
[2023.04.1]: https://github.com/trackIT-Systems/tsOS-vhf/compare/2023.03.3...2023.04.1
[2023.03.3]: https://github.com/trackIT-Systems/tsOS-vhf/compare/2023.03.2...2023.03.3
[2023.03.2]: https://github.com/trackIT-Systems/tsOS-vhf/compare/2023.03.1...2023.03.2
[2023.03.1]: https://github.com/trackIT-Systems/tsOS-vhf/compare/2023.02.1...2023.03.1
[2023.02.1]: https://github.com/trackIT-Systems/tsOS-vhf/releases/tag/2023.02.1
