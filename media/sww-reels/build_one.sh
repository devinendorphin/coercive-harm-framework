#!/bin/bash
# build_one.sh <slug> : music -> video -> mux  ->  out/reel_<NN>_<slug>.mp4
set -e
cd "$(dirname "$0")"; . venv/bin/activate
slug=$1
read id idx < <(python -c "from content import REELS; r=[x for x in REELS if x['slug']=='$slug'][0]; print(r['id'], REELS.index(r))")
dur=$(python -c "import json;print(json.load(open('build/timing_$slug.json'))['dur']+2.6)")
python music.py $dur $idx build/music_$slug.wav
python render.py $slug
ffmpeg -loglevel error -y -i build/video_$slug.mp4 -i build/voice_$slug.wav -i build/music_$slug.wav -filter_complex \
 "[1:a]aresample=48000,pan=stereo|c0=c0|c1=c0,apad[v];[v]asplit=2[v1][v2];[2:a]volume=0.24[m];[m][v1]sidechaincompress=threshold=0.015:ratio=5:attack=20:release=600[md];[md][v2]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]" \
 -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -movflags +faststart out/reel_${id}_$slug.mp4
echo "done $id $slug"
