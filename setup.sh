#!/bin/bash

apt update
apt upgrade -y
apt install -y python3 python3-pycurl handbrake-cli

source bin/activate
pip install bs4
pip install requests
pip install tqdm