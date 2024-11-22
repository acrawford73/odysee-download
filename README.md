# odysee-download
Odysee post grabber.

From a list of Odysee video post URLs (placed in urls.txt file), this script grabs the title, thumbnail, and video of Odysee video posts. It will then encode the video based on a preset configuration. The script will also grab any links given in the description and comments sections.

Some Odysee accounts upload uncompressed video direct from their PC or mobile device. These files are really large so the encoding feature can reduce the file size on average by about 75%. The encoding feature uses HandBrake-CLI to compress the video.

The downloaded files are automatically renamed to the video title (metadata 'name' field) with the published date added. 

Special characters are removed from the filenames, except commas, periods, and hyphens.

## Install

This script is intended for Ubuntu Linux with Python 3.

```code
sudo apt-get install python3 python3-pip virtualenv handbrake-cli

git clone https://github.com/acrawford73/odysee-download.git

virtualenv -p /usr/bin/python3 odysee-download
cd odysee-download
source bin/activate
pip install bs4 requests tqdm playwright
playwright install
playwright install-deps
```

## URLs

Add one Odysee URL per line into file called: urls.txt

## Run

```code
./odysee.py
```

## Output

The links filename format is: "Links November 1 2024.txt"

Thumbnails and Videos are downloaded to 'odysee-download/downloads'

Encoded video is placed in 'odysee-download/encodes'

## Encoding

The video encoding feature is disabled by default. If you wish to encode the downloaded videos, set the option "encode_video" to True.

From:

```code
encode_video = False
```

To:

```code
encode_video = True
```
