#!/bin/bash

apt update
apt install -y python3 python3-pip virtualenv handbrake-cli

source bin/activate
pip install bs4 requests tqdm playwright
playwright install-deps
playwright install