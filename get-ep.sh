#!/bin/bash
# Usage: ./get-all-eps.sh page-url filename.mp4

ffmpeg -i `python run.py $1` -acodec copy -vcodec copy -bsf:a aac_adtstoasc $2
