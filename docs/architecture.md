# Architecture

## Base System

Built on a released [tsOS-base](https://github.com/trackIT-Systems/tsOS-base) image (currently 2027.0.6, Raspberry Pi OS Lite, Debian Trixie), modified with [pimod](https://github.com/Nature40/pimod). tsOS-vhf adds the VHF signal detection and nothing else: the partition layout, overlayroot, network stack, web UI, MQTT broker, telemetry, logging, updates and the `root`/`pi` privilege model are tsOS-base's, see its [architecture](https://github.com/trackIT-Systems/tsOS-base/blob/main/docs/architecture.md).

## Data Flow

```
RTL-SDR dongles ──USB──> radiotracking ──> /data/<host>/radiotracking/*.csv
                         (one process        │
                          per SDR)           └──> mosquitto (localhost:1883)
                                                   <host>/radiotracking/...
                                                     ├──> tsconfig live dashboard (/mqtt)
                                                     └──> bridge (mosquitto.d) ──> server
```

Each SDR is read and analyzed in a process of its own. The main process matches detections of the same transmission on several SDRs, watches the SDRs, and publishes signals, matched signals, SDR states and spectra. See [Radiotracking](radiotracking.md) for the outputs.

## Key Components

### Build-Time Packages

- `librtlsdr0` and `rtl-sdr` (library, udev rules, `rtl_*` tools) from the release packages of the [trackIT-Systems/librtlsdr](https://github.com/trackIT-Systems/librtlsdr) fork, pinned by `LIBRTLSDR_VERSION` (0.9.1). The fork sets the LNA, mixer and VGA gain stages of the R820T tuner separately (`rtlsdr_set_tuner_gain_ext`), and works around usbfs mmap problems and hangs on USB transfer errors.
- `python3-numpy`, `python3-scipy`, `python3-schedule`, `python3-setuptools`: the dependencies of the Python packages below, from apt.

### Python Packages

Installed from git submodules under `/usr/local/src` with `pip install --no-deps -e`:
- `pyradiotracking` - signal detection, matching, CSV and MQTT output ([trackIT-Systems/pyradiotracking](https://github.com/trackIT-Systems/pyradiotracking))
- `pyrtlsdr` - Python bindings for librtlsdr, mainline v0.5.0 ([pyrtlsdr/pyrtlsdr](https://github.com/pyrtlsdr/pyrtlsdr))

### Systemd Services

- `radiotracking.service` - runs `/usr/local/bin/radiotracking` as `pi`, see [Radiotracking](radiotracking.md#service)

The service is in tsOS-base's polkit allowlist, so `pi` (and tsconfig) can start, stop and restart it.

### Hardware Support

- **RTL-SDR dongles** (Rafael Micro R820T tuner): raw USB devices, opened through `/dev/bus/usb` with the udev rules of the `rtl-sdr` package
- **usbfs memory**: the kernel's limit for USB buffers is removed at boot ([etc/tmpfiles.d/usbfs.conf](../etc/tmpfiles.d/usbfs.conf)), so several dongles can use large sample buffers
- Everything else (WittyPi 4, GPS, LTE, watchdog) as in [tsOS-base](https://github.com/trackIT-Systems/tsOS-base/blob/main/docs/architecture.md#hardware-support)

## Configuration Points

- `/boot/firmware/radiotracking.ini` - radiotracking's configuration ([default](../boot/firmware/radiotracking.ini)). Editable on the card (root-owned at runtime) or in tsconfig, which keeps it in its `config_dir` (`/boot/firmware`). The service does not start without it.
- `/boot/firmware/mosquitto.d/` - the bridge that forwards `<host>/radiotracking/...` to a server (tsOS-base)
- `/boot/firmware/cmdline.txt` - the hostname (`systemd.hostname=`), which is also the station name in topics and file names (tsOS-base)

## Security

`radiotracking.service` runs as `pi`, not as root, with a sandbox like tsOS-base's other daemons (see tsOS-base's [Security Design](https://github.com/trackIT-Systems/tsOS-base/blob/main/docs/security.md)):

- `ProtectSystem=strict`, `ProtectHome`, `PrivateTmp`, `NoNewPrivileges`; writes only to `/data`
- `PrivateDevices` is off so the dongles are visible; `DevicePolicy=closed` with `DeviceAllow=char-usb_device rw` limits it to raw USB devices
- `RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6 AF_NETLINK`: libusb enumerates USB devices through a netlink socket (without it: `No supported devices found`)
- No kernel tunables/modules/logs, no cgroup writes, no namespaces

A compromised `radiotracking` therefore has `pi`'s rights, held back by this sandbox. It parses no input from the network: it reads the SDRs and the configuration file and only publishes to the broker.

`/usr/local/src` is `root:root` and not group/world-writable, as in tsOS-base: `pi` can read the source trees, not change them.
