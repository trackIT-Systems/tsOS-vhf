# tRackIT OS
[![Build tRackIT OS](https://github.com/tRackIT-Systems/tRackIT-OS/actions/workflows/build_trackit_os.yml/badge.svg)](https://github.com/tRackIT-Systems/tRackIT-OS/actions/workflows/build_trackit_os.yml)
[![Build BatRack OS](https://github.com/tRackIT-Systems/tRackIT-OS/actions/workflows/build_batrack_os.yml/badge.svg)](https://github.com/tRackIT-Systems/tRackIT-OS/actions/workflows/build_batrack_os.yml)

tRackIT OS is an open-source software for reliable VHF radio tracking of (small) animals in their wildlife habitat. tRackIT OS is an operating system distribution for tRackIT stations that receive signals emitted by VHF tags mounted on animals and are built from low-cost commodity-off-the-shelf hardware. tRackIT OS provides software components for VHF signal processing, system monitoring, configuration management, and user access. In particular, it records, stores, analyzes, and transmits detected VHF signals and their descriptive features, e.g., to calculate bearings of signals emitted by VHF radio tags mounted on animals or to perform animal activity classification. 


## Download

The image of tRackIT OS can be downloaded in the [GitHub Releases](https://github.com/tRackIT-Systems/tRackIT-OS/releases) section of this repository. 
## Build tRackIT OS

The base tRackIT OS build consists of two stages. First, a `Base.img` is built, which installs all required software and might take some time to be build. Secondly the custom software components and configuration files are copied and installed and `tRackIT-OS.img` is built. 

```sh
$ docker-compose run --rm pimod pimod.sh Base.Pifile
### FROM https://downloads.raspberrypi.org/raspios_lite_arm64/images/raspios_lite_arm64-2023-05-03/2023-05-03-raspios-bullseye-arm64-lite.img.xz
Using cache: .cache/downloads.raspberrypi.org/raspios_lite_arm64/images/raspios_lite_arm64-2023-05-03/2023-05-03-raspios-bullseye-arm64-lite.img.xz
### TO Base-arm64.img
Moving temporary /tmp/tmp.vvqN5fe4xU to Base-arm64.img
...

$ docker-compose run --rm pimod pimod.sh tRackIT-OS.Pifile
### FROM Base-arm64.img
Copying Base-arm64.img to tRackIT-OS.img.
...
```

### Targets

As of May 2023, two versions of tRackIT OS exist, build for armhf and arm64. The reasoning behind that is, that some camera software requires 32-bit libraries, which in turn are required by BatRack. 

`Base.Pifile` and `tRackIT-OS.Pifile` are using arm64 as their primary target. However there exist `-armhf` versions which create their 32-bit counterparts. `BatRack-OS.Pifile` depends on `tRackIT-OS-armhf.img`, hence this image needs to be build first.

## Build BatRack OS

BatRack OS requires three stages of building, as it is based upon tRackIT OS. As the camera drivers only work in the 32-bit OS, the stages differ slightly:

```sh
$ docker-compose run --rm pimod pimod.sh Base-armhf.Pifile 
### FROM https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2023-05-03/2023-05-03-raspios-bullseye-armhf-lite.img.xz
Using cache: .cache/downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2023-05-03/2023-05-03-raspios-bullseye-armhf-lite.img.xz
### TO Base-armhf.img
Moving temporary /tmp/tmp.7JMz4fdunp to Base-armhf.img
...

$ docker-compose run --rm pimod pimod.sh tRackIT-OS-armhf.Pifile
### FROM Base-armhf.img
### TO tRackIT-OS-armhf.img
Copying Base-armhf.img to tRackIT-OS-armhf.img.
...

$ docker-compose run --rm pimod pimod.sh -d BatRack-OS.Pifile
### FROM tRackIT-OS-armhf.img
### TO BatRack-OS.img
Copying tRackIT-OS-armhf.img to BatRack-OS.img.
...
```

## Configuration

The system can be configured through different files in the `/boot` partition.

### `/boot/firmware/cmdline.txt`

`cmdline.txt` holds the kernel boot commandline, which allows to configure the hostname in newer systemd versions. This behavioud is emulated and a hostname can be configured by setting `systemd.hostname=tRackIT-00001`

### [`/boot/firmware/radiotracking.ini`](boot/radiotracking.ini)

Hold the configuration of `pyradiotracking`, [see example config](https://github.com/tRackIT-Systems/pyradiotracking/blob/master/etc/radiotracking.ini).

### [`/boot/firmware/mqttutil.conf`](boot/mqttutil.conf)

Mqttutil reports system statistics via MQTT, [see example config](https://github.com/tRackIT-Systems/pymqttutil/blob/main/etc/mqttutil.conf).


### `/boot/firmware/wireguard.conf`

A wireguard configuration can be set using this configuration file. 

### [`/boot/firmware/mosquitto.d/`](boot/mosquitto.d/)

Files in this directory are loaded by mosquitto. E.g. mqtt brokers for reporting can be set using files in this folder.

## Scientific Usage & Citation

If you are using tRackIT OS in academia, we'd appreciate if you cited our [scientific research paper](https://jonashoechst.de/assets/papers/hoechst2021tRackIT.pdf). Please cite as "Höchst & Gottwald et al."

> J. Höchst, J. Gottwald, P. Lampe, J. Zobel, T. Nauss, R. Steinmetz, and B. Freisleben, “tRackIT OS: Open-source Software for Reliable VHF Wildlife Tracking,” in 51. Jahrestagung der Gesellschaft für Informatik, Digitale Kulturen, INFORMATIK 2021, Berlin, Germany, 2021.

```bibtex
@inproceedings{hoechst2021tRackIT,
  title = {{tRackIT OS: Open-source Software for Reliable VHF Wildlife Tracking}},
  author = {Höchst, Jonas and Gottwald, Jannis and Lampe, Patrick and Zobel, Julian and Nauss, Thomas and Steinmetz, Ralf and Freisleben, Bernd},
  booktitle = {51. Jahrestagung der Gesellschaft f{\"{u}}r Informatik, Digitale Kulturen, {INFORMATIK} 2021, Berlin, Germany},
  series = {{LNI}},
  publisher = {{GI}},
  month = sep,
  year = {2021}
}
```
