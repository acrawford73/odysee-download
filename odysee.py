#!bin/python3

# Date: ~2024
# Author: nanimoose

# Acquire uploads from Odysee
# Prepare urls.txt file of Odysee links first
# Gets the Title, Thumbnail URL, Video URL
# Encode:
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
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from tqdm import tqdm
import requests

print()
links_file_init = False


## Options
get_links = True
download_files = True
encode_video = False


# Get React HTML
def fetch_html(url):
	with sync_playwright() as p:
		# Launch a browser
		browser = p.firefox.launch(headless=True)  # Set headless=False if you want to see the browser
		page = browser.new_page()
		page.set_default_navigation_timeout(30000.0)
		# Watch as the traffic flys by
		page.on("request", lambda request: print(">>", request.method, request.url))
		page.on("response", lambda response: print("<<", response.status, response.url))
		# Filter out media content, not necessary for HTML parsing
		page.route(re.compile(r"\.(qt|mov|mp4|jpg|png|svg|webp|wott)$"), lambda route: route.abort()) 
		# Navigate to the desired URL
		page.goto(url)
		# Wait for the React app to load completely
		page.wait_for_load_state('networkidle')
		# Get the HTML content of the page
		html_content = page.content()
		# Close the browser
		browser.close()
		return html_content


# Remove all special characters except spaces and alphanumeric characters
# Hyphens, commas, periods allowed
def clean_text(text):
	text = text.replace('&amp;','&')
	clean = re.sub(r'[^a-zA-Z0-9\s\,\-\.\~\&\/]', '', text)
	clean = clean.replace('~','-')
	cleaned = clean.replace('/','-')
	return cleaned.strip()


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

	## Grab the HTML of the Odysee video post
	print();print();print("Grabbing Odysee HTML...")
	print(url);print()

	content = fetch_html(url)
	
	## Testing
	#content = open('test.html', 'r')

	# If no content then try next URL
	if not content:
		continue

	# Parse webpage JSON metadata
	soup = BeautifulSoup(content, 'html.parser')
	script_tag = soup.find('script', {'type': 'application/ld+json'})

	if script_tag:
		json_content = json.loads(script_tag.string)
		#print(json_content)
	else:
		print();print('Script tag for metadata not found.');print()

	# Parse
	title = json_content['name']
	title_for_links = title
	title = clean_text(title)
	thumb = json_content['thumbnailUrl']
	video = json_content['contentUrl']
	upload_date = json_content['uploadDate']

	# Grab date for filenames
	uploaded = datetime.strptime(upload_date, '%Y-%m-%dT%H:%M:%S.%fZ')
	created = uploaded.strftime("%b %-d %Y").lower()  # Format: nov 1 2024

	# Create new text file for today's links
	# Format: 'Psinergy Links Nov 1 2024.txt'
	if not links_file_init:
		created_links = uploaded.strftime("%B %-d %Y") # Format: November 1 2024
		links_filename = "Links " + created_links + ".txt"
		print();print("Links file: " + links_filename)
		with open(links_filename, 'w') as nf:
			nf.write("Psinergy Links " + created_links + '\n\n')
		nf.close()
		links_file_init = True

	# Show details for this URL
	print()
	print("Title: " + title_for_links)
	print("Thumb: " + thumb)
	print("Video: " + video)


	# Get links from HTML of each URL
	if get_links:

		# Initialize for this URL
		links = []
		
		# Description
		print();print("Description links:")
		description_element = soup.find('div', class_='markdown-preview--description')
		if not description_element:
			print("Could not find the Description class.")
		else:
			desc_links = description_element.find_all('a')
			for link in desc_links:
				link_http = link.get('href')
				if link_http.startswith('http') or link_http.startswith('https'):
					print(link.get('href'))
					links.append(link.get('href'))

		# Comments from Psinergy only:
		# Biofield Practice 0nly ~ Psinergy
		# Psinergy0Nhold
		print();print("Comments links:")
		comments_element = soup.find('ul', class_='comments')
		if not comments_element:
			print("Couldn't find any comments.")
		else:
			comment_links = comments_element.find_all('a')
			for link in comment_links:
				link_http = link.get('href')
				if link_http.startswith('http') or link_http.startswith('https'):
					print(link.get('href'))
					links.append(link.get('href'))

		# Append the links to text file from this URL
		if len(links) > 0:
			with open(links_filename, 'a') as lf:
				lf.write(title_for_links + '\n\n')
				for link in links:
					lf.write(link+'\n')
				lf.write('\n\n')
			lf.close()


	## Download files
	if download_files:

		# Prep downloads folder
		downloads_dir = 'downloads'
		if not os.path.exists(downloads_dir):
			os.makedirs(downloads_dir)

		chunk_size = 1024

		# Get Thumb
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

		
		# Get Video
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


# Move the links file to 'downloads'
#shutil.move(links_filename, os.path.join(downloads_dir, links_filename))


### Encode Video Files ###
if not encode_video:
	print();quit()

print()

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
