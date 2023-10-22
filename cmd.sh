###
# Code to create audio from text
#

#!/bin/bash

if [ "$#" -ne 3 ]; then
	edge-tts -f $1 --voice ja-JP-NanamiNeural  --write-media $2
	exit 1
else
	echo "usage: ./cmd.sh [INPUT TEXT FILE] [OUTPUT MP3 FILE]"
	exit 1
fi
