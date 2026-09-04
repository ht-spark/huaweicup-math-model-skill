#!/usr/bin/env python3
"""Validate Humanizer Chinese's portable package surfaces without external dependencies."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
README = (ROOT / "README.md").read_text(encoding="utf-8")
PLUGIN = json.loads(
    (ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
)
MARKETPLACE = json.loads(
    (ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")
)


def require(match: re.Match[str] | None, message: str) -> re.Match[str]:
    if match is None:
        raise SystemExit(message)
    return match


frontmatter = require(
    re.match(r"\A---\n(.*?)\n---\n", SKILL, re.DOTALL),
    "SKILL.md must start with YAML frontmatter",
).group(1)

for nonportable_key in ("compatibility:", "allowed-tools:"):
    if re.search(rf"(?m)^{re.escape(nonportable_key)}", frontmatter):
        raise SystemExit(f"Remove nonportable frontmatter key: {nonportable_key[:-1]}")

skill_version = require(
    re.search(r'(?m)^\s+version:\s*["\']([^"\']+)["\']\s*$', frontmatter),
    "SKILL.md metadata.version is missing",
).group(1)
skill_name = require(
    re.search(r"(?m)^name:\s*([a-z0-9-]+)\s*$", frontmatter),
    "SKILL.md name is missing or invalid",
).group(1)
readme_version = require(
    re.search(r"(?m)^- \*\*([0-9]+\.[0-9]+\.[0-9]+)\*\*", README),
    "README version history is missing",
).group(1)

versions = {skill_version, readme_version, str(PLUGIN.get("version", ""))}
if len(versions) != 1:
    raise SystemExit(f"Version mismatch: {sorted(versions)}")

marketplace_plugins = MARKETPLACE.get("plugins", [])
package_names = {
    skill_name,
    str(PLUGIN.get("name", "")),
    str(MARKETPLACE.get("name", "")),
    str(marketplace_plugins[0].get("name", "")) if marketplace_plugins else "",
}
if len(package_names) != 1:
    raise SystemExit(f"Package name mismatch: {sorted(package_names)}")

PATTERN_COUNT = 36

pattern_numbers = [
    int(number)
    for number in re.findall(r"(?m)^### ([0-9]+)\. ", SKILL)
]
if pattern_numbers != list(range(1, PATTERN_COUNT + 1)):
    raise SystemExit(f"Expected patterns 1-{PATTERN_COUNT}, found {pattern_numbers}")

readme_numbers = {
    int(number) for number in re.findall(r"(?m)^\| ([0-9]+) \|", README)
}
if readme_numbers != set(range(1, PATTERN_COUNT + 1)):
    raise SystemExit(f"README pattern table must contain patterns 1-{PATTERN_COUNT}")

if len(SKILL.splitlines()) > 500:
    raise SystemExit("SKILL.md exceeds the 500-line portability budget")

section_contracts = ROOT / "references" / "section-contracts.md"
if not section_contracts.is_file():
    raise SystemExit("Missing references/section-contracts.md")
if "references/section-contracts.md" not in SKILL:
    raise SystemExit("SKILL.md must route full-report work to the section contracts")

print(f"{skill_name} package v{skill_version} is valid")
