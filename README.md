# odysee-download
Odysee post grabber.

From a list of Odysee URLs (urls.txt file), this script grabs the title, thumbnail, and video of an Odysee video post. It will then encode the video based on the preset configuration. 

Some Odysee accounts upload uncompressed video direct from their PC or mobile device. These files are really large so the encoding feature can reduce the file size on average by 75%. The encoding feature uses Handbrake to compress the video.

The downloaded files are automatically renamed to the video title, with the published date added. 

Special characters are removed from the filenames.

## Install

This script is intended for Ubuntu Linux with Python 3.

```code
sudo apt-get install python3 virtualenv python3-pip handbrake-cli
```

## PIP Installs

```code
virtualenv -p /usr/bin/python3 odysee-download
cd odysee-download
source bin/activate
pip install bs4 requests tqdm
```

## URLs

Add one URL per line to file called: urls.txt

## Run

```code
./odysee.py
```

## Output

Thumbnails and Videos are downloaded to 'odysee-download/downloads'

Encoded video is placed in 'odysee-download/encodes'

## Encoding

The video encoding feature is enabled by default. If you wish to skip encoding the downloaded videos, then uncomment line 167.

From:

```code
# quit()
```

To:

```code
quit()
```