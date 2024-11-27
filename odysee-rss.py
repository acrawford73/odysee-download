#!bin/python3

# Date: ~2024
# Author: github.com/acrawford73

# Acquire uploads from Odysee RSS feed
# Gets the Title, Description, Thumbnail, Video
# Encodes to MP4:
#  Video: 720p, 29.97fps, q=26
#  Audio: 44.1Khz, 128kbps, stereo

import os
import re
import sys
import json
import shutil
import subprocess
import datetime,time
from time import strftime
from datetime import datetime
from os.path import splitext
# Third party
from tqdm import tqdm
import requests
import feedparser


# Remove all special characters except spaces and alphanumeric characters
# Hyphens, commas, periods allowed
def clean_title(text):
	text = text.replace('&amp;','&')
	clean = re.sub(r'[^a-zA-Z0-9\s\,\-\.\~\&\/]', '', text)
	clean = clean.replace('~','-')
	cleaned = clean.replace('/','-')
	return cleaned.strip()


### BEGIN HERE
if __name__ == "__main__":
	print()

	links_file_init = False


	## Options
	save_links = True
	download_files = True
	encode_video = False


	# Get the list of Feed URLs to grab
	feed_urls = []
	with open('rss.txt' ,'r') as dld:
		for line in dld.readlines():
			if not line in ['\n','\r\n'] and not line.strip().startswith("#"):
				if line.startswith('https'):
					feed_urls.append(line.strip())
	dld.close()


	# Process each RSS feed
	for url in feed_urls:
		print();print(f'Requesting RSS... {url}');print()
		
		# Get Odysee RSS Feed
		rss_feed = feedparser.parse(url)
		
		if rss_feed.bozo:
			print(f"Couldn't acquire RSS feed from {url}")
			continue
		else:
			if len(rss_feed.entries) == 0:
				print("No items found in the RSS feed.")
				continue
			else:
				print("Number of items:", str(len(rss_feed.entries)))

				# ASK HOW MANY
				print("How many RSS items to process for this feed?")
				rss_item_count = int(input())
				print("Processing " + str(rss_item_count) + " RSS items...");print()

				# Only get the most recent items
				#while rss_item_count >= 0:
				count = 1
				for item in rss_feed.entries:

					#print("Processing RSS item # " + str(rss_item_count-1))
					#item = rss_feed.entries

					etype = item.enclosures[0].type

					# process only video posts
					if etype.split('/')[0] != 'video':
						continue

					# Thu, 21 Nov 2024 07:27:41 GMT
					published = datetime.strptime(item.published, '%a, %d %b %Y %H:%M:%S GMT')
					published_file = published.strftime("%b %-d %Y").lower()  # nov 1 2024
					published_link = published.strftime("%B %-d %Y")  # November 1 2024

					title_for_links = item.title    # as-is
					title = clean_title(item.title) # cleanup for filenames
					thumb = item.image.href
					video = item.enclosures[0].href
					description = item.summary_detail.value
					description = description.split('</p>')[1].replace('<br />', '\n')

					print()
					print("Published:      " + str(published))
					print("Published File: " + published_file)
					print("Published Link: " + published_link)
					print("Title:       " + title)
					print("Thumb URL:   " + thumb)
					print("Video URL:   " + video)
					print("Description: " + description)
					print()


					## LINKS
					if save_links:
						# Create the new links file unless already created
						if not links_file_init:
							links_filename = "Links " + published_link + ".txt"
							print();print("Links file: " + links_filename)
							with open(links_filename, 'w') as nf:
								nf.write("Links " + published_link + '\n\n')
							nf.close()
							links_file_init = True

						# Append current description to links file
						with open(links_filename, 'a') as lf:
							lf.write(title_for_links + '\n\n')
							lf.write(description + '\n\n\n')
						lf.close()


					## DOWNLOAD FILES
					if download_files:

						# Prep downloads folder
						downloads_dir = 'downloads'
						if not os.path.exists(downloads_dir):
							os.makedirs(downloads_dir)

						chunk_size = 1024

						# GET THUMB
						try:
							thumb = "https://thumbnails.odycdn.com/card/s:1280:720/quality:85/plain/" + thumb
							print(f'Downloading Thumbnail: {thumb}')
							rs = requests.Session()
							response = rs.get(thumb, timeout=20, allow_redirects=True)
							response.raise_for_status()
							total_size = int(response.headers.get('content-length', 0))

							new_fn = title + " " + published_file + '.jpg'
							#filename = thumb.split('/')[-1]
							#file, ext = os.path.splitext(filename)
							#new_fn = title + " " + published_file + ext
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


						# GET VIDEO
						try:
							print(f'Downloading Video: {video}')
							rs = requests.Session()
							response = rs.get(video, timeout=20, stream=True, allow_redirects=True)
							response.raise_for_status()
							total_size = int(response.headers.get('content-length', 0))
							
							filename = video.split('/')[-1]
							file, ext = os.path.splitext(filename)
							new_fn = title + " " + published_file + ext
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


					# CHECK ITEM LIMIT
					if count == rss_item_count:
						break
					else:
						count+=1

	
	## ENCODE VIDEOS
	print()
	if not encode_video:
		quit()

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



	print();quit(0)	
