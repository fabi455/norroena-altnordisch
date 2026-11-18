#!/usr/bin/env python3
"""Create local MP3 pronunciation approximations based on a modern Icelandic voice."""
import json, re, subprocess
from pathlib import Path
root = Path(__file__).resolve().parents[1]
source = (root / "content.js").read_text(encoding="utf-8")
match = re.search(r"window\.NORROENA_CONTENT\s*=\s*(\[[\s\S]*?\]);", source)
if not match:
    raise RuntimeError("Lerninhalt in content.js nicht gefunden")
lessons = json.loads(match.group(1))
(root / "content.json").write_text(json.dumps(lessons, ensure_ascii=False, indent=2), encoding="utf-8")
audio = root / "audio"
audio.mkdir(parents=True, exist_ok=True)
items = {item["id"]: item["term"] for lesson in lessons for item in lesson["words"] + lesson["phrases"]}
for id, phrase in items.items():
    dest = audio / (id + ".mp3")
    if dest.exists() and dest.stat().st_size > 500:
        continue
    wav = audio / (id + ".wav")
    subprocess.run(["espeak", "-v", "is", "-s", "125", "-a", "165", "-w", str(wav), phrase], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-ar", "22050", "-ac", "1", "-codec:a", "libmp3lame", "-q:a", "6", str(dest)], check=True)
    wav.unlink()
print(f"{len(lessons)} Lektionen; {len(items)} MP3-Hörbeispiele")
