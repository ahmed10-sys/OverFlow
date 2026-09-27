# Repo Architecture Tour Visualizer

A lightweight, zero-dependency static HTML generator that parses structured `repo_blueprint.json` schemas into interactive, self-contained Architecture Tour web dashboards. It visualizes high-level system metadata, real-time Mermaid diagrams, execution step flows with code anchors, core data models, API interfaces, directory layouts, and onboarding verification runbooks into a single deployable artifact.

## Quickstart

Run the visualizer against any blueprint:

```bash
python visualizer.py fixtures/callbridge.json output/architecture_tour.html
```

Open `output/architecture_tour.html` directly in any browser or host it via GitHub Pages.
