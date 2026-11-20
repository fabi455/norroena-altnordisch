#!/usr/bin/env python3
"""Generate Norrœna's 128 offline audio samples with a natural Icelandic neural voice.

CAUTION: This is modern Icelandic TTS, not reconstructed Old Norse pronunciation.
The voice is obtained at build time; the Android app has no internet dependency.
"""
import asyncio
import json
import os
import random
import re
from pathlib import Path

import edge_tts

ROOT = Path(__file__).resolve().parents[1]
AUDIO_DIR = ROOT / "audio"
VOICE = "is-IS-GunnarNeural"
RATE = "-6%"
CONCURRENCY = 2


def collect():
    source = (ROOT / "content.js").read_text("utf-8")
    m = re.search(r"window\.NORROENA_CONTENT\s*=\s*(\[[\s\S]*?\]);", source)
    if not m:
        raise RuntimeError("Norrœna Lerninhalt in content.js nicht gefunden")
    lessons = json.loads(m.group(1))
    (ROOT / "content.json").write_text(
        json.dumps(lessons, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    items = [item for lesson in lessons for item in lesson["words"] + lesson["phrases"]]
    ids = [item["id"] for item in items]
    if len(lessons) != 8 or len(items) != 128 or len(set(ids)) != len(items):
        raise RuntimeError(
            f"Erwartet: 8 Lektionen, 128 eindeutige Audios; gefunden: {len(lessons)} / {len(items)}"
        )
    if any(not item["term"].strip() for item in items):
        raise RuntimeError("Leerer Sprechertext")
    return items


def valid_mp3(path):
    if not path.exists() or path.stat().st_size < 1800:
        return False
    with path.open("rb") as f:
        h = f.read(3)
    return h == b"ID3" or (len(h) >= 2 and h[0] == 255 and (h[1] & 224) == 224)


async def one(item, semaphore):
    dest = AUDIO_DIR / (item["id"] + ".mp3")
    if valid_mp3(dest):
        return dest
    async with semaphore:
        temp = AUDIO_DIR / (item["id"] + ".partial.mp3")
        for attempt in range(5):
            try:
                temp.unlink(missing_ok=True)
                speaker = edge_tts.Communicate(item["term"], voice=VOICE, rate=RATE)
                await asyncio.wait_for(speaker.save(str(temp)), timeout=60)
                if not valid_mp3(temp):
                    raise ValueError(f"Unvollständiges MP3 für {item['id']}")
                os.replace(temp, dest)
                print(f"OK {item['id']} {item['term'][:28]} ({dest.stat().st_size} Bytes)", flush=True)
                return dest
            except Exception as exc:
                temp.unlink(missing_ok=True)
                print(f"TTS Retry {attempt+1}/5: {item['id']}: {exc}", flush=True)
                if attempt == 4:
                    raise RuntimeError(f"Neuralstimme für {item['term']!r} nicht verfügbar") from exc
                await asyncio.sleep(min(30, 2 ** attempt * 2 + random.random()))


async def main():
    items = collect()
    AUDIO_DIR.mkdir(exist_ok=True)
    semaphore = asyncio.Semaphore(CONCURRENCY)
    files = await asyncio.gather(*(one(item, semaphore) for item in items))
    if len(files) != 128 or not all(valid_mp3(p) for p in files):
        raise RuntimeError("MP3-Validierung fehlgeschlagen")
    print(
        f"OK: 128 gültige MP3-Dateien, "
        f"{sum(p.stat().st_size for p in files) / 1048576:.2f} MiB, "
        f"Neuralstimme: {VOICE}",
        flush=True,
    )


if __name__ == "__main__":
    asyncio.run(main())
