#!/usr/bin/env python3
"""Build Norrœna's unique offline audio with the Icelandic Gunnar Neural voice.

Speech is synthesized from *modern Icelandic* TTS as an approximation to Old
West Norse pronunciation; it is not a historical linguistic reconstruction.
Existing verified Gunnar files are reused. Never silently fall back to eSpeak.
"""
import argparse
import asyncio
import json
import os
import random
import re
from pathlib import Path

import edge_tts

ROOT=Path(__file__).resolve().parents[1]
VOICE="is-IS-GunnarNeural"
RATE="-6%"

def collect():
    source=(ROOT/"content.js").read_text("utf-8")
    m=re.search(r"window\.NORROENA_CONTENT\s*=\s*(\[[\s\S]*?\]);",source)
    if not m:raise RuntimeError("Norrœna content.js not found")
    lessons=json.loads(m.group(1))
    (ROOT/"content.json").write_text(json.dumps(lessons,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    if len(lessons)!=16:raise RuntimeError(f"Expected 16 lessons, found {len(lessons)}")
    items=[w for l in lessons for w in l["words"]+l["phrases"]]
    if len(items)!=256:raise RuntimeError(f"Expected 256 flashcard entries, found {len(items)}")
    unique={}
    for x in items:
        if not x.get("term") or not x.get("id"):raise RuntimeError("Missing text or ID")
        before=unique.get(x["id"])
        if before is not None and before["term"]!=x["term"]:
            raise RuntimeError("The same sound ID is used for different texts")
        unique[x["id"]]=x
    if len(unique)!=255:raise RuntimeError(f"Expected 255 distinct MP3 IDs, found {len(unique)}")
    return list(unique.values())

def valid(path):
    if not path.is_file() or path.stat().st_size<1800:return False
    with path.open("rb") as f:h=f.read(3)
    return h==b"ID3" or len(h)>=2 and h[0]==255 and h[1]&224==224

async def record(entry,root,retries=6):
    dest=root/(entry["id"]+".mp3")
    if valid(dest):return
    root.mkdir(parents=True,exist_ok=True)
    temp=root/(entry["id"]+".partial.mp3")
    last=None
    for i in range(retries):
        try:
            temp.unlink(missing_ok=True)
            # ǫ and œ are historic letters unfamiliar to modern Icelandic
            # synthesizers. Replace only the *spoken input* if necessary.
            spoken=entry["term"] if i<2 else entry["term"].replace("ǫ","ö").replace("œ","æ")
            await asyncio.wait_for(
                edge_tts.Communicate(spoken,voice=VOICE,rate=RATE).save(str(temp)),
                timeout=60
            )
            if not valid(temp):raise RuntimeError("Audio empty or invalid")
            os.replace(temp,dest)
            print(f"GUNNAR {entry['id']} {entry['term'][:32]} ({dest.stat().st_size} B)",flush=True)
            await asyncio.sleep(.5+random.random()*.6)
            return
        except Exception as e:
            last=e
            temp.unlink(missing_ok=True)
            print(f"Retry {i+1}/{retries} {entry['id']}: {e}",flush=True)
            if i+1<retries:
                await asyncio.sleep(min(18,2**i+random.random()))
    raise RuntimeError(f"Gunnar Neural cannot synthesize {entry['id']}: {entry['term']}") from last

async def main(args):
    all_items=collect()
    old=Path(args.reused)
    missing=[w for w in all_items if not valid(old/(w["id"]+".mp3"))]
    chosen=missing[args.part::args.parts]
    out=Path(args.output)
    out.mkdir(parents=True,exist_ok=True)
    print(f"Norrœna: {len(all_items)} distinct IDs; {len(missing)} need synthesis; group {args.part} of {args.parts}: {len(chosen)}",flush=True)
    for x in chosen:await record(x,out)
    if any(not valid(out/(x["id"]+".mp3")) for x in chosen):
        raise RuntimeError("Incomplete audio shard")
    (out/f"gunnar-shard-{args.part}.json").write_text(
        json.dumps({"voice":VOICE,"part":args.part,"parts":args.parts,
                    "ids":[w["id"] for w in chosen]},ensure_ascii=False),encoding="utf-8")
    print(f"Complete: {len(chosen)} Gunnar clips in shard {args.part}",flush=True)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--reused",default="audio")
    p.add_argument("--output",default="generated")
    p.add_argument("--part",type=int,default=0)
    p.add_argument("--parts",type=int,default=1)
    a=p.parse_args()
    if a.parts<1 or a.part<0 or a.part>=a.parts:raise SystemExit("Invalid shard parameters")
    asyncio.run(main(a))
