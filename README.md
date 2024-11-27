# odysee-download
Odysee post grabber.

Purpose: To archive Odysee video posts.

From a list of Odysee video post URLs or RSS feed URL, these scripts grab the title, thumbnail, and video of Odysee video posts. It will then encode the video based on a preset configuration. The script also grabs any links in the description and comments areas and saves them to a file. The RSS feed does not provide comment data.

Some Odysee accounts upload uncompressed video direct from their PC or mobile device. These files can be really large so the encoding feature can reduce the file size on average by about 75%. HandBrake-CLI is used to encode all videos to MP4 format.

The downloaded thumbnail and video files are automatically renamed to the post title (metadata 'name' field) with the published date added. 

Special characters are removed from the filenames, except commas, periods, and hyphens.

Playwright for Python is used for loading the React based Odysee pages. [Playwright-Python](https://github.com/microsoft/playwright-python).

NOTE: At this time there is a bug in acquiring Odysee posts, sometimes the description and comment sections do not load into the browser simulator. I think it is due to Odysee performance because Odysee has loading issues often. The RSS feed capture is the best option at this time.

## Install

This script is intended for Ubuntu Linux with Python 3. Tested on Ubuntu 22.04 LTS.

```code
sudo apt-get install python3 python3-pip virtualenv handbrake-cli

git clone https://github.com/acrawford73/odysee-download.git

virtualenv -p /usr/bin/python3 odysee-download
cd odysee-download
source bin/activate
pip install bs4 requests tqdm playwright feedparser
playwright install-deps
playwright install
```

## URLs

Before using odysee-rss.py, add one Odysee RSS Feed URL into file called: rss.txt

Before using odysee.py, add one Odysee URL per line into file called: urls.txt

## Run

- For capturing content from the RSS feed, enter this command:

```code
./odysee-rss.py

```
Then enter the number of posts you wish to capture.

- For capturing content from the RSS feed, enter this command:

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
