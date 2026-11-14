"""Fetch only the reviewed FR3 assets from the immutable upstream commit."""
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

HERE = Path(__file__).resolve().parent
ASSET_DIR = HERE.parents[1] / ".local" / "simulator" / "franka_fr3"
LOCK_PATH = HERE / "assets.lock.json"


def verify_assets():
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    for entry in lock["files"]:
        path = (ASSET_DIR / entry["path"]).resolve()
        if not path.is_relative_to(ASSET_DIR.resolve()):
            raise ValueError("Asset lock contains an unsafe path")
        if not path.is_file() or path.stat().st_size != entry["bytes"]:
            raise FileNotFoundError("FR3 assets missing. Run python apps/simulator/setup_assets.py")
        if hashlib.sha256(path.read_bytes()).hexdigest() != entry["sha256"]:
            raise ValueError("FR3 asset hash mismatch: " + entry["path"])
    return lock


def main():
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    base = f"https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/{lock['commit']}/franka_fr3/"
    downloaded = 0
    for entry in lock["files"]:
        target = (ASSET_DIR / entry["path"]).resolve()
        if not target.is_relative_to(ASSET_DIR.resolve()):
            raise ValueError("Unsafe path")
        if target.is_file() and hashlib.sha256(target.read_bytes()).hexdigest() == entry["sha256"]:
            continue
        with urlopen(base + entry["path"], timeout=60) as response:
            data = response.read(entry["bytes"] + 1)
        if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
            raise ValueError("Downloaded asset did not match lock: " + entry["path"])
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix(target.suffix + ".download")
        temporary.write_bytes(data)
        temporary.replace(target)
        downloaded += 1
    verify_assets()
    print(f"FR3 assets verified: {len(lock['files'])} files; {downloaded} downloaded.")


if __name__ == "__main__":
    main()
