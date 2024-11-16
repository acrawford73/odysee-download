#!/bin/bash

if test -d "downloads"; then
	rm -rf downloads
	echo "Downloads folder deleted."
else
	echo "Downloads folder not found."
fi

if test -d "encodes"; then
	rm -rf encodes
	echo "Encodes folder deleted."
else
	echo "Encodes folder not found."
fi

echo ""
