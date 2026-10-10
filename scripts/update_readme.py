#!/usr/bin/env python3
"""Update the repository table and status using GitHub's public API."""
import json, os, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
USERNAME = "s0k1x"

def github_json(url):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "s0k1x-nebula-profile-bot", "X-GitHub-Api-Version": "2022-11-28"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response)

def replace_section(text, start, end, content):
    if start not in text or end not in text:
        raise RuntimeError(f"Missing README markers: {start} / {end}")
    before, rest = text.split(start, 1)
    _, after = rest.split(end, 1)
    return before + start + "\n" + content + "\n" + end + after

def main():
    text = README.read_text(encoding="utf-8")
    repos = github_json(f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=updated&type=owner")
    repos = sorted((r for r in repos if not r.get("fork") and not r.get("private")), key=lambda r: r["name"].lower())
    rows = ["| Repository | Language | Stars | Updated (UTC) |", "|---|---:|---:|---|"]
    for r in repos:
        updated = (r.get("updated_at") or "—").replace("T", " ").replace("Z", "")[:16]
        rows.append(f'| [{r["name"]}](https://github.com/{USERNAME}/{r["name"]}) | {r.get("language") or "—"} | ⭐ {r.get("stargazers_count", 0)} | {updated} |')
    text = replace_section(text, "<!-- AUTO-GENERATED:START -->", "<!-- AUTO-GENERATED:END -->", "\n".join(rows))
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    status = f"> **Last profile update:** `{now}` · **Public repositories scanned:** `{len(repos)}`"
    text = replace_section(text, "<!-- STATUS:START -->", "<!-- STATUS:END -->", status)
    README.write_text(text, encoding="utf-8")
    print(f"Scanned {len(repos)} public repositories; updated README at {now}.")

if __name__ == "__main__":
    main()
