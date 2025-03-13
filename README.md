# odysee-download

Odysee post grabber.

From an Odysee RSS feed URL, this script grabs the title, thumbnail, and video of Odysee video posts. It will then encode the video based on a preset configuration. The script also grabs the description info and saves to a file. The RSS feed does not provide comment data, so comments with links must be grabbed manually.

Some Odysee accounts upload uncompressed video direct from their PC or mobile device. These files can be really large so the encoding feature can reduce the file size on average by about 75%. HandBrake-CLI is used to encode all videos to MP4 format.

The downloaded thumbnail and video files are automatically renamed to the post title (metadata 'name' field) with the published date added. 

Special characters are removed from the filenames, except commas, periods, and hyphens.

## Install

This script is intended for Ubuntu Linux with Python 3. Tested on Ubuntu 22.04 LTS.

```code
sudo apt-get install python3 python3-pip virtualenv handbrake-cli

git clone https://github.com/acrawford73/odysee-download.git

pip install bs4 requests tqdm feedparser
```

## URLs

Before using odysee-rss.py, add one Odysee RSS Feed URL into file called: rss.txt

The Odysee channels' RSS feed URL location is present inside the three button hidden menu, on the top right, then select "Copy RSS URL".

## Run

At the command prompt, enter this command:

```code
./odysee-rss.py
```

Then enter the number of consecutive recent posts you wish to capture.

Please note that 'Reposts' are not provided in the RSS data so they can be ignored. All other Odysee posts are listed in the RSS data.

Example:

You visit the channel you wish to grab videos from and you see there are four brand new Odysee posts. One of them is a repost. So when running this script and it asks for how many posts you wish to acquire, 3 is entered because the repost will not be present in the RSS data.

## Output

The links filename format is: "Links November 1 2024.txt"

Thumbnails and Videos are downloaded to 'odysee-download/downloads'

Encoded video is placed in 'odysee-download/encodes'

## Encoding

The video encoding feature is disabled by default. To enable, set the option "encode_video" to True.

From:

```code
encode_video = False
```

To:

```code
encode_video = True
```
