#!/usr/bin/env python3
"""Restore the 127 original, voice-consistent Gunnar MP3s from Norrœna 1.1.

Original lesson terms and IDs must match to avoid mismatched spoken content.
"""
import json
import os
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REPO=os.getenv("GITHUB_REPOSITORY","fabi455/norroena-altnordisch")
RUN="44766250203"
ARTIFACT="Norroena-1.1-Neural-APK"

def valid(data):
    return len(data)>1800 and (data[:3]==b"ID3" or (len(data)>1 and data[0]==255 and data[1]&224==224))

def entries(lessons):
    lookup={}
    for l in lessons:
        for w in l["words"]+l["phrases"]:
            if w["id"] in lookup and lookup[w["id"]]!=w["term"]:raise RuntimeError("Conflicting audio IDs")
            lookup[w["id"]]=w["term"]
    return lookup

def main():
    new=json.loads((ROOT/"content.json").read_text("utf8"))
    if len(new)!=16:raise RuntimeError("Expected 16 lessons")
    current=entries(new)
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(
            ["gh","run","download",RUN,"--repo",REPO,"--name",ARTIFACT,"--dir",tmp],
            check=True
        )
        apk=next(iter(Path(tmp).rglob("*.apk")),None)
        if apk is None:raise RuntimeError("Original Gunnar APK not found in artifact")
        out=ROOT/"audio";out.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(apk) as z:
            if "assets/content.json" not in z.namelist():
                raise RuntimeError("Original APK had no source text for comparing audio")
            old=json.loads(z.read("assets/content.json"))
            old_map=entries(old)
            if len(old)!=8 or len(old_map)!=127:
                raise RuntimeError("Unexpected historic APK contents")
            found=0
            for id,term in old_map.items():
                if current.get(id)!=term:raise RuntimeError(f"Old lesson changed: {id}")
                key="assets/audio/"+id+".mp3"
                if key not in z.namelist():raise RuntimeError(f"Original Gunnar clip missing: {id}")
                data=z.read(key)
                if not valid(data):raise RuntimeError(f"Bad Gunnar MP3: {id}")
                (out/(id+".mp3")).write_bytes(data)
                found+=1
        if found!=127:raise RuntimeError("Expected 127 Gunnar recordings")
        print(f"Reused {found} original Gunnar-Neural recordings; all IDs and texts unchanged.",flush=True)

if __name__=="__main__":
    main()
