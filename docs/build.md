# Build System

## Overview

tsOS-vhf is built in two stages: tsOS-base builds its image from Raspberry Pi OS Lite and publishes it as a release, and tsOS-vhf modifies that released image with [pimod](https://github.com/Nature40/pimod), as defined in `tsOS-vhf.Pifile`.

## Build Files

- `tsOS-vhf.Pifile` - arm64 build (Raspberry Pi 3+)
- `.inspect.Pifile` - opens a shell in a built image (see [Inspecting an Image](#inspecting-an-image))
- `docker-compose.yml` - pimod build environment

## Build Process

1. **Base Image**: Downloads the tsOS-base release zip (`FROM`)
2. **Modifications**: Applies changes via Pifile commands:
   - File installation (`INSTALL`)
   - Package installation (`RUN apt-get install`)
   - Python packages (`RUN python3 -m pip install`)
   - Service enablement (`RUN systemctl enable`)
3. **Output**: Produces `tsOS-vhf-arm64.img`

## Pifile Structure

### Key Sections

1. **Base Image** (`FROM`): tsOS-base release, `PUMP 500M` expands the image by 500 MB
2. **OS Metadata** (`RUN tee /etc/os-release`): `VARIANT="VHF"`, version from git tags
3. **Custom Files** (`INSTALL`): Copies `boot`, `etc` and `usr` to the image
4. **Git Submodules**: Installs the `.git` directories of `pyradiotracking` and `pyrtlsdr`
5. **Permissions**: `/usr/local/src` root-owned, `git safe.directory` for each source tree
6. **Root Password** (optional): `TSOS_ROOT_PASSWORD`, see below
7. **Services**: librtlsdr packages, Python packages, `radiotracking.service`
8. **Cleanup** (`ZERO`, `SHRINK`): Removes apt lists and caches, zero-fills unused space and shrinks the image

### Important Build Details

- **Base version**: Pinned in the `FROM` URL. Updating tsOS-base means changing that URL and listing the base changes in [CHANGELOG.md](../CHANGELOG.md).
- **Versioning**: Uses `git describe --tags --always` for `VERSION_ID`
- **Python Packages**: Installed with `--no-deps` (dependencies come from apt)
- **librtlsdr**: `.deb` packages downloaded from the trackIT-Systems/librtlsdr release `v${LIBRTLSDR_VERSION}`; no build toolchain is installed
- **Root password**: `TSOS_ROOT_PASSWORD` (from the environment, never committed) sets root's password and enables password SSH for root, as in tsOS-base. If unset, the base image's root account is left as it is.

## Building Locally

```sh
docker-compose run --rm pimod pimod.sh tsOS-vhf.Pifile
```

With a root password:

```sh
TSOS_ROOT_PASSWORD=... docker-compose run --rm -e TSOS_ROOT_PASSWORD pimod pimod.sh tsOS-vhf.Pifile
```

### Inspecting an Image

```sh
IMG=tsOS-vhf-arm64.img docker-compose run --rm pimod pimod.sh .inspect.Pifile
```

opens a shell in the image, changes are written to it (`INPLACE`).

### Flashing

```sh
sudo ./flash.sh tsOS-vhf-arm64.img /dev/<disk>
```

unmounts the card and writes the image with `pv` and `dd`.

## CI/CD

GitHub Actions builds on tag push ([.github/workflows/build.yml](../.github/workflows/build.yml)):
- Creates a pre-release, with the tag's section of [CHANGELOG.md](../CHANGELOG.md) as release notes (generated notes if there is none)
- Builds the image with `Nature40/pimod@v0.9.3`, with submodules
- Packages the image as `tsOS-vhf-arm64-<tag>.zip` and uploads it to the release
- Generates delta updates with `pidiff` (partition 2, excluding [.pidiffignore](../.pidiffignore)) from the latest release and from the latest stable release, uploaded as `tsOS-vhf-arm64-update-<from>-to-<tag>.tar`

### Delta Baseline

`DELTA_BASELINE` in the workflow is the oldest release a delta update is generated from. tsOS-base 2027.0.2 changed the `root`/`pi` privilege model, so devices on earlier images are reflashed, and no delta crosses that boundary.

## Adding Components

### New Package

Add to the `RUN apt-get install` section in the Pifile.

### New Service

1. Add the service file to `etc/systemd/system/`
2. Enable in Pifile: `RUN systemctl enable <service>.service`
3. Run it as `pi` with a sandbox, like `radiotracking.service`
4. To let `pi` control it, add it to tsOS-base's polkit allowlist (`20-tsos-systemctl.rules`)

### New Python Package

1. Add as git submodule in `usr/local/src/`
2. Install its `.git` directory in the Pifile, like `pyradiotracking`
3. Install in Pifile: `RUN python3 -m pip install --no-deps -e /usr/local/src/<package>`
4. Install apt dependencies separately if needed

### Custom Files

Place files in directory structure matching target filesystem:
- `boot/` → `/boot/`
- `etc/` → `/etc/`
- `usr/` → `/usr/`
