# Project Structure

## Directory Layout

```
tsOS-vhf/
├── boot/
│   └── firmware/
│       └── radiotracking.ini       # radiotracking configuration (default)
├── etc/
│   ├── systemd/system/
│   │   └── radiotracking.service   # Signal detection service
│   └── tmpfiles.d/
│       └── usbfs.conf              # Removes the usbfs memory limit
├── usr/
│   └── local/
│       └── src/                    # Application git submodules
│           ├── pyradiotracking/
│           └── pyrtlsdr/
├── docs/                           # Developer documentation
├── .github/workflows/build.yml     # CI/CD workflow
├── .inspect.Pifile                 # Shell in a built image
├── .pidiffignore                   # Files excluded from delta updates
├── CHANGELOG.md                    # Release notes
├── docker-compose.yml              # Build environment
├── flash.sh                        # Writes an image to an SD card
└── tsOS-vhf.Pifile                 # Build config (arm64)
```

## Key Directories

### `boot/firmware/`

Files copied to the boot partition (root-owned at runtime, see tsOS-base's [Security Design](https://github.com/trackIT-Systems/tsOS-base/blob/main/docs/security.md)):
- `radiotracking.ini` - radiotracking's configuration, see [Radiotracking](radiotracking.md#configuration)

All other boot partition files (`cmdline.txt`, `mosquitto.d/`, `wireguard.conf`, ...) come from tsOS-base.

### `etc/`

- `systemd/system/radiotracking.service` - see [Radiotracking](radiotracking.md#service)
- `tmpfiles.d/usbfs.conf` - sets `/sys/module/usbcore/parameters/usbfs_memory_mb` to `0` at boot

### `usr/local/src/`

Git submodules containing Python packages:
- Each submodule is installed via `pip install --no-deps -e`
- `.git` directories are preserved during build
- Permissions set to `root:root`, not group/world-writable - `pi` can read but not write

## Git Submodules

Submodules in `usr/local/src/`:
- `pyradiotracking` - signal detection ([trackIT-Systems/pyradiotracking](https://github.com/trackIT-Systems/pyradiotracking))
- `pyrtlsdr` - librtlsdr bindings ([pyrtlsdr/pyrtlsdr](https://github.com/pyrtlsdr/pyrtlsdr), v0.5.0)

librtlsdr is not a submodule: it is installed from the release packages of [trackIT-Systems/librtlsdr](https://github.com/trackIT-Systems/librtlsdr).

## Build Artifacts

- `tsOS-vhf-arm64.img` - Final arm64 image
- `.cache/` - Cached base images (created by pimod)
