# odysee-download
Odysee post grabber.

From a list of Odysee video post URLs (placed in urls.txt file), this script grabs the title, thumbnail, and video of Odysee video posts. It will then encode the video based on a preset configuration. 

Some Odysee accounts upload uncompressed video direct from their PC or mobile device. These files are really large so the encoding feature can reduce the file size on average by about 75%. The encoding feature uses HandBrake-CLI to compress the video.

The downloaded files are automatically renamed to the video title (metadata 'name' field) with the published date added. 

Special characters are removed from the filenames, except commas, periods, and hyphens.

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

The terminal output when the files are downloading looks similar to this:

```code
Title: Biofield practice for control
Thumb: https://thumbnails.odycdn.com/card/s:1280:720/quality:85/plain/https://thumbs.odycdn.com/a999bf52a6d85f4c441e3cee35a2b5c5.webp
Video: https://player.odycdn.com/api/v3/streams/free/trim.9932740E-E83F-4D74-AD19-B8F970152E48/adfebe73315a8d8f4752ef2b263eada02d4f289d/036365.qt
Downloading Thumbnail: https://odysee.com/@BiofieldPractice:5/trim.9932740E-E83F-4D74-AD19-B8F970152E48:a
Progress: 100%|█████████████████████████████████████████████████████████████████████████████████████| 138k/138k [00:00<00:00, 92.7MB/s]
Downloading Video: https://odysee.com/@BiofieldPractice:5/trim.9932740E-E83F-4D74-AD19-B8F970152E48:a
Progress: 100%|███████████████████████████████████████████████████████████████████████████████████| 37.0M/37.0M [00:15<00:00, 2.54MB/s]
```

The terminal output when encoding the videos is verbose so I won't show a sample in this README.

## Encoding

The video encoding feature is enabled by default. If you wish to skip encoding the downloaded videos, uncomment line 167.

From:

```code
# quit()
```

To:

```code
quit()
```
