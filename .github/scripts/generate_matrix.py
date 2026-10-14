"""Reads pins.yml and outputs a flat GitHub Actions matrix JSON."""
import json
import re
import sys
import yaml


def slugify(text):
    return re.sub(r"-+", "-", re.sub(r"[^a-zA-Z0-9]", "-", text)).strip("-").lower()


with open("pins.yml") as f:
    config = yaml.safe_load(f)

include = [
    {
        "repo": repo,
        "slug": slugify(section["title"]),
        "title": section["title"],
        "description": section["description"],
    }
    for section in config["sections"]
    for repo in section.get("repos") or []
]

if not include:
    print("Error: no repos defined in pins.yml", file=sys.stderr)
    sys.exit(1)

print(json.dumps({"include": include}))
