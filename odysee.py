#!bin/python3

# Date: ~2024
# Author: anonymoose

# Acquire uploads from Odysee
# Prepare urls.txt file of Odysee links first
# Gets the Title, Thumbnail URL, Video URL
# Encode:
#  Video: 720p, 29.97fps, q=26
#  Audio: 44.1Khz, 128kbps, stereo

import os
import sys
import json
import datetime,time
from datetime import datetime
from time import strftime
import subprocess
import shutil
from bs4 import BeautifulSoup
from os.path import splitext
from tqdm import tqdm
import requests
import re


def clean_text(text):
    # Removes all special characters except spaces and alphanumeric characters
    cleaned = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return cleaned


downloads_dir = 'downloads'
if not os.path.exists(downloads_dir):
	os.makedirs(downloads_dir)


# get the list of URLs to grab
dld_urls = []
with open('urls.txt' ,'r') as dld:
	for line in dld.readlines():
		if not line in ['\n','\r\n'] and not line.strip().startswith("#"):
			if line.startswith('https'):
				dld_urls.append(line.strip())
dld.close()


# Get metadata from urls
for url in dld_urls:
	try:
		rs = requests.Session()
		response = rs.get(url, timeout=20)
		response.raise_for_status()
		content = response.content
		rs.close()
	except requests.exceptions.HTTPError as err:
		print(f'HTTP Error: {err}')
	except requests.exceptions.ConnectionError as errc:
		print(f'Error Connecting: {errc}')
	except requests.exceptions.Timeout as errt:
		print(f'Timeout Error: {errt}')
	except requests.exceptions.RequestException as errr:
		print(f'OOps: Something Else: {errr}')				
	finally:
		rs.close()

	# If no metadata then goto next url
	if not content:
		continue

	# Parse webpage with bs4
	soup = BeautifulSoup(content, 'html.parser')
	script_tag = soup.find('script', {'type': 'application/ld+json'})
	if script_tag:
		json_content = json.loads(script_tag.string)
	else:
		print;print('Script tag content not found.');print

	#print(json_content)

	chunk_size = 1024

	# Parse
	title = json_content['name']
	title = clean_text(title)
	title = title.strip()
	thumb = json_content['thumbnailUrl']
	video = json_content['contentUrl']
	upload_date = json_content['uploadDate']

	print()
	print("Title: " + title)
	print("Thumb: " + thumb)
	print("Video: " + video)

	uploaded = datetime.strptime(upload_date, '%Y-%m-%dT%H:%M:%S.%fZ')
	created = uploaded.strftime("%b %-d %Y").lower()

	# Thumb
	try:
		rs = requests.Session()
		response = rs.get(thumb, timeout=20, allow_redirects=True)
		response.raise_for_status()
		total_size = int(response.headers.get('content-length', 0))

		print(f'Downloading Thumbnail: {url}')
		
		filename = thumb.split('/')[-1]
		new_fn = title + " " + created + '.jpg'

		with open(new_fn, 'wb') as file, tqdm(desc='Progress', total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as bar:
			for chunk in response.iter_content(chunk_size=chunk_size):
				if chunk:
					file.write(chunk)
					bar.update(len(chunk))
		shutil.move(new_fn, os.path.join(downloads_dir, new_fn))
		file.close()

	except requests.exceptions.HTTPError as err:
		print(f'HTTP Error: {err}')
	except requests.exceptions.ConnectionError as errc:
		print(f'Error Connecting: {errc}')
	except requests.exceptions.Timeout as errt:
		print(f'Timeout Error: {errt}')
	except requests.exceptions.RequestException as errr:
		print(f'Oops: Something Else: {errr}')				
	finally:
		rs.close()

	
	# Video
	try:
		rs = requests.Session()
		response = rs.get(video, timeout=20, stream=True, allow_redirects=True)
		response.raise_for_status()
		total_size = int(response.headers.get('content-length', 0))
		
		print(f'Downloading Video: {url}')

		filename = video.split('/')[-1]
		file, ext = os.path.splitext(filename)
		new_fn = title + " " + created + ext
		
		with open(new_fn, 'wb') as file, tqdm(desc='Progress', total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as bar:
			for chunk in response.iter_content(chunk_size=chunk_size):
				if chunk:
					file.write(chunk)
					bar.update(len(chunk))
		
		shutil.move(new_fn, os.path.join(downloads_dir, new_fn))
		file.close()

	except requests.exceptions.HTTPError as err:
		print(f'HTTP Error: {err}')
	except requests.exceptions.ConnectionError as errc:
		print(f'Error Connecting: {errc}')
	except requests.exceptions.Timeout as errt:
		print(f'Timeout Error: {errt}')
	except requests.exceptions.RequestException as errr:
		print(f'Oops: Something Else: {errr}')
	finally:	
		rs.close()

print()

# quit()


### Encode Video Files ###

# Directory with video files
output_dir = 'encodes'

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
	os.makedirs(output_dir)

# Supported file extensions
video_extensions = ['.qt', '.mov', '.mp4']

# Get list of video files
video_files = [f for f in os.listdir(downloads_dir) if os.path.splitext(f)[1].lower() in video_extensions]


# Transcode each video file using HandBrakeCLI
for video_file in video_files:
	input_file = os.path.join(downloads_dir, video_file)
	output_file = os.path.join(output_dir, os.path.splitext(video_file)[0] + '.mp4')

	# HandBrakeCLI command for transcoding
	command = [
		'HandBrakeCLI',
		'-i', input_file,
		'-o', output_file,
		'--preset', 'Very Fast 720p30',
		'-e', 'x264',
		'-q', '26',
		'-r', '29.97',
		'-R', '44.1',
		'--ab', '128'
	]

	print(f"Transcoding {video_file}...")

	try:
		# Run the command
		subprocess.run(command, check=True)
		print(f"Transcoded {video_file} successfully.")
	except subprocess.CalledProcessError as e:
		print(f"Failed to transcode {video_file}. Error: {e}")

print()
