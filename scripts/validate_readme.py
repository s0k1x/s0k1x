from pathlib import Path
root = Path(__file__).resolve().parents[1]
readme = (root / "README.md").read_text(encoding="utf-8")
required = ["<!-- AUTO-GENERATED:START -->", "<!-- AUTO-GENERATED:END -->", "<!-- STATUS:START -->", "<!-- STATUS:END -->", "NEON ARCADE", "CYBER SNAKE"]
missing = [item for item in required if item not in readme]
if missing:
    raise SystemExit("README validation failed; missing: " + ", ".join(missing))
print("README validation passed.")
