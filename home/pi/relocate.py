#!/usr/bin/env python3

import argparse
import datetime
import logging
import pathlib
import shutil

parser = argparse.ArgumentParser(description="Relocate lost+found files of tsOS-vhf to their original filenames")
parser.add_argument("hostname", help="original hostname")
parser.add_argument("-o", "--outpath", help="path to copy files to", type=pathlib.Path, default=".")
parser.add_argument("-i", "--inpath", help="path to find files in", type=pathlib.Path, default=".")
parser.add_argument("-p", "--prefix", help="prefix of files to find", default="#")
parser.add_argument("-v", "--verbose", action="store_true")

HEADERS = {
    "[optional arguments]": ".ini",
    "Device;Time;Frequency;Duration;max (dBW);avg (dBW);std (dB);noise (dBW);snr (dB)": ".csv",
    "Time;Frequency;Duration;0": "-matched.csv",
    "Device;Time;State": "-state.csv",
}


args = parser.parse_args()
if args.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

logging.debug(args.__dict__)

for path in args.inpath.glob(f"{args.prefix}*"):
    logging.debug("Handling file        %s", path)

    # get creation time
    unix_ts = pathlib.Path(path).stat().st_ctime
    ts = datetime.datetime.fromtimestamp(unix_ts)
    logging.debug("Creation:            %s", ts)

    # get header
    with open(path) as f:
        head = f.readline()[:-1]
        logging.debug("Head:                %s", head)

    # lookup file extension
    try:
        ext = HEADERS[head]
        logging.debug("Extension:           %s", ext)
    except KeyError:
        logging.warning('No extension found for header "%s", skipping', head)
        continue

    # build path
    dest_name = f"{args.hostname}_{ts:%Y-%m-%dT%H%M%S}{ext}"
    logging.debug("Destination:          %s", dest_name)

    dest_path = args.outpath / dest_name
    logging.info("Copying %s to %s", path, dest_path)
    shutil.copy(path, dest_path)
