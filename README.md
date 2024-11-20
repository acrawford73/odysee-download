# odysee-download
Odysee post grabber.

From a list of Odysee URLs, this script grabs the title, thumbnail, and video of an Odysee video post.

Encodes the video to preset configuration.

## Install

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

Add urls to file called: urls.txt

## Run

```code
./odysee.py
```

## Output

Thumbnails and Videos are downloaded to 'odysee-download/downloads'

Encoded video is placed in 'odysee-download/encodes'

## Encoding

The encoding of video is enabled by default. If you wish to encode the downloaded videos, then uncomment line 167.

```code
# quit()
```