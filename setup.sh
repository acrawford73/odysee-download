#!/bin/bash

apt update
apt install -y python3 handbrake-cli

source bin/activate
pip install bs4
pip install requests
pip install tqdm
