"""Renders README.md from readme.md.j2 + pins.yml + downloaded SVG assets."""
import os
import re

import yaml
from jinja2 import Environment, FileSystemLoader


def slugify(text):
    return re.sub(r"-+", "-", re.sub(r"[^a-zA-Z0-9]", "-", text)).strip("-").lower()


repo_owner = os.environ["REPO_OWNER"]

with open("pins.yml") as f:
    config = yaml.safe_load(f)

sections = []
for section in config["sections"]:
    slug = slugify(section["title"])
    section_dir = f"assets/{slug}"
    svgs = [
        {"name": repo, "path": f"assets/{slug}/{repo}.svg"}
        for repo in section.get("repos") or []
        if os.path.isfile(f"assets/{slug}/{repo}.svg")
    ]
    sections.append({**section, "svgs": svgs})

env = Environment(
    loader=FileSystemLoader(".github/scripts"),
    keep_trailing_newline=True,
    trim_blocks=True,
    lstrip_blocks=True,
)
readme = env.get_template("readme.md.j2").render(repo_owner=repo_owner, sections=sections)

with open("README.md", "w") as f:
    f.write(readme)
