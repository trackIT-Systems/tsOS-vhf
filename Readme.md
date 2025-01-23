# tsOS-vhf
[![Build tsOS-vhf Images](https://github.com/trackIT-Systems/tsOS-vhf/actions/workflows/build.yml/badge.svg)](https://github.com/trackIT-Systems/tsOS-vhf/actions/workflows/build.yml)

tsOS-vhf is an open-source software for reliable VHF radio tracking of (small) animals in their wildlife habitat.tsOS-vhf is an operating system distribution for trackIT stations that receive signals emitted by VHF tags mounted on animals and are built from low-cost commodity-off-the-shelf hardware.tsOS-vhf provides software components for VHF signal processing, system monitoring, configuration management, and user access. In particular, it records, stores, analyzes, and transmits detected VHF signals and their descriptive features, e.g., to calculate bearings of signals emitted by VHF radio tags mounted on animals or to perform animal activity classification. 


## Download

The image of tsOS-vhf can be downloaded in the [GitHub Releases](https://github.com/trackIT-Systems/tsOS-vhf/releases) section of this repository. 

## Build tsOS-vhf

The base tsOS-vhf build consists of two stages. First, a base image is built, which installs all required software and might take some time to be build, see [https://github.com/trackIT-Systems/tsOS-Base](tsOS-Base). Secondly the custom software components and configuration files are copied and installed and `tsOS-vhf.img` is built. 

```sh
$ docker-compose run --rm pimod pimod.sh tsOS-vhf.Pifile
### FROM https://github.com/trackIT-Systems/tsOS-Base/releases/download/2024.07.2/tsOS-Base-arm64-2024.07.2.zip
Fetching remote: https://github.com/trackIT-Systems/tsOS-Base/releases/download/2024.07.2/tsOS-Base-arm64-2024.07.2.zip
...
```

### Targets

As of September 2024, two versions of tsOS-vhf exist, build for `armhf` and `arm64`. The reasoning behind that is, that some camera software requires 32-bit libraries, which in turn are required by BatRack. 

`tsOS-vhf.Pifile` is using arm64 as their primary target. However there exist `-armhf` versions which create their 32-bit counterparts. 

## Configuration

The system can be configured through different files in the `/boot` partition.

### `/boot/firmware/cmdline.txt`

`cmdline.txt` holds the kernel boot commandline, which allows to configure the hostname in newer systemd versions. This behavioud is emulated and a hostname can be configured by setting `systemd.hostname=trackIT-00001`

### [`/boot/firmware/radiotracking.ini`](boot/firmware/radiotracking.ini)

Hold the configuration of `pyradiotracking`, [see example config](https://github.com/trackIT-Systems/pyradiotracking/blob/main/etc/radiotracking.ini).

### [`/boot/firmware/mqttutil.conf`](boot/firmware/mqttutil.conf)

Mqttutil reports system statistics via MQTT, [see example config](https://github.com/trackIT-Systems/pymqttutil/blob/main/etc/mqttutil.conf).


### `/boot/firmware/wireguard.conf`

A wireguard configuration can be set using this configuration file. 

### [`/boot/firmware/mosquitto.d/`](boot/firmware/mosquitto.d/)

Files in this directory are loaded by mosquitto. E.g. mqtt brokers for reporting can be set using files in this folder.

## Scientific Usage & Citation

If you are using tsOS-vhf in academia, we'd appreciate if you cited our [scientific research paper](https://jonashoechst.de/assets/papers/hoechst2021tRackIT.pdf). Please cite as "Höchst & Gottwald et al."

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
