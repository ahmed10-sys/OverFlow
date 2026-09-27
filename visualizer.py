"""
Visualizer: Static HTML Generator for Repo Blueprints
Transforms repo_blueprint.json schema into an interactive Architecture Tour.
"""

import json
import os
import sys
from pathlib import Path


def load_blueprint(blueprint_path: str | Path) -> dict:
    """Load and parse the JSON blueprint file."""
    with open(blueprint_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_architecture_tour(blueprint_path: str | Path, template_path: str | Path, output_path: str | Path) -> None:
    """Generate static architecture tour HTML from blueprint and template."""
    blueprint = load_blueprint(blueprint_path)
    
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # Stub: inject raw JSON or placeholder render
    rendered = template.replace("{{BLUEPRINT_DATA}}", json.dumps(blueprint, indent=2))
    rendered = rendered.replace("{{PROJECT_NAME}}", blueprint.get("project_metadata", {}).get("name", "Architecture Tour"))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"[+] Successfully generated: {output_path}")


def main():
    base_dir = Path(__file__).parent
    blueprint_path = base_dir / "fixtures" / "callbridge.json"
    template_path = base_dir / "template.html"
    output_path = base_dir / "output" / "architecture_tour.html"

    if len(sys.argv) > 1:
        blueprint_path = Path(sys.argv[1])
    if len(sys.argv) > 2:
        output_path = Path(sys.argv[2])

    build_architecture_tour(blueprint_path, template_path, output_path)


if __name__ == "__main__":
    main()
