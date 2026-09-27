# OverFlow: System Architecture Tour Visualizer

> **A zero-dependency, static web generator that converts structured repository blueprints (`repo_blueprint.json`) into interactive, production-grade Architecture Tour web dashboards.**

---

## 1. Executive Summary

When developers or AI pipelines analyze a software repository, they often generate a structured JSON blueprint describing the codebase architecture, control flows, data models, entrypoints, and runbooks.

**OverFlow** is a compiler and visualization engine built in pure Python. It takes that raw machine-readable blueprint and transforms it into a self-contained, interactive single-page application (SPA). The resulting dashboard gives engineers, stakeholders, and AI agents an intuitive, visual walkthrough of how any complex software system is built and executed.

---

## 2. Key Features

- **Zero Runtime Dependencies**: The generator runs on standard Python 3.10+ without `pip install` requirements (no Jinja2, no heavy frameworks).
- **Interactive Mermaid Flowchart**: Renders dynamic system control-flow diagrams natively in dark mode.
- **Click-to-Jump Navigation**: Clicking any node inside the Mermaid SVG diagram instantly and smoothly scrolls to the exact execution card in the pipeline walkthrough and triggers an animated glowing highlight effect.
- **Deep System Diagnostics**: Visualizes primary purpose, execution control flow, invariants, edge cases, and category-badged technology stacks.
- **Schema & Data Models**: Renders Pydantic and data transfer models with types and field constraints.
- **File System Directory & LOC**: Displays file hierarchies, architectural roles, and line counts.
- **Copyable Playbook**: Step-by-step verification commands with individual and "Copy All Steps" single-click clipboard actions.
- **Instant GitHub Pages Deployment**: Fully compatible with zero-config static hosting.

---

## 3. Repository Architecture & File Breakdown

```
OverFlow/
├── visualizer.py               # Pure Python compiler & token replacement engine
├── template.html               # Base dark-mode HTML/CSS/JS shell with slot tokens
├── logo.svg                    # Custom geometric brand logo
├── README.md                   # Quickstart documentation
├── ARCHITECTURE_AND_PROJECT_GUIDE.md  # Comprehensive architectural handbook
├── .gitignore                  # Python ignore rules ensuring static output tracking
├── fixtures/                   # Test blueprint datasets
│   ├── callbridge.json         # Real-world Voice AI agent blueprint (FastAPI / Groq / AssemblyAI)
│   └── doc_indexer.json        # High-throughput vector search ETL pipeline blueprint
├── output/                     # Generated static HTML artifacts
│   ├── architecture_tour.html  # Default compiled tour (CallBridge)
│   ├── callbridge_tour.html    # Compiled CallBridge tour
│   └── doc_indexer_tour.html   # Compiled DocIndexer tour
└── index.html                  # Root entrypoint for GitHub Pages direct deployment
```

### Detailed File Responsibilities

| File | Type | Primary Role |
| :--- | :--- | :--- |
| [`visualizer.py`](file:///c:/Personal%20Stuff/Projects/OverFlow%202/visualizer.py) | Python Script | Loads input blueprint JSON, sanitizes text with HTML escaping, builds responsive component markup, replaces template tokens, and exports the final HTML artifact. |
| [`template.html`](file:///c:/Personal%20Stuff/Projects/OverFlow%202/template.html) | HTML5 / JS / Tailwind | The presentation shell containing dark-mode styling, sticky navigation, CDN integrations (Tailwind, Mermaid.js, Highlight.js), and client-side SVG event delegation scripts. |
| [`logo.svg`](file:///c:/Personal%20Stuff/Projects/OverFlow%202/logo.svg) | Vector Asset | Branded UI identity asset featuring glowing bracket optics embedded directly into the header navbar. |
| [`fixtures/callbridge.json`](file:///c:/Personal%20Stuff/Projects/OverFlow%202/fixtures/callbridge.json) | Test Fixture | Sample blueprint of an autonomous outbound negotiation phone agent with real-time dealbreaker interception. |
| [`fixtures/doc_indexer.json`](file:///c:/Personal%20Stuff/Projects/OverFlow%202/fixtures/doc_indexer.json) | Test Fixture | Sample blueprint of a CLI background ETL pipeline chunking documents and syncing vectors with Qdrant. |
| [`index.html`](file:///c:/Personal%20Stuff/Projects/OverFlow%202/index.html) | Generated SPA | Production root build deployed directly to GitHub Pages at `https://ahmed10-sys.github.io/OverFlow/`. |

---

## 4. End-to-End System Integration Flow

The entire workflow from raw data ingestion to live interaction operates in three stages:

```
+--------------------------+
|  repo_blueprint.json     | (Input: Machine-generated architectural schema)
+------------+-------------+
             |
             v
+--------------------------+
|      visualizer.py       | (Python Ingestion & Component Markup Builders)
|  - html.escape()         |
|  - render_tech_stack()   |
|  - render_flow_cards()   |
|  - render_data_models()  |
|  - render_directory()    |
|  - render_playbook()     |
+------------+-------------+
             |
             v
+--------------------------+
|      template.html       | (String Replacement of Slot Tokens: {{TOKEN}})
+------------+-------------+
             |
             v
+--------------------------+
|  output/architecture_tour| (Deployable Static Single-Page App)
+------------+-------------+
             |
             v
+--------------------------------------------------------------------------+
|  Browser Client Execution:                                               |
|  1. Tailwind CSS applies obsidian glassmorphism & responsive layout.    |
|  2. Mermaid.js renders SVG control graph in dark mode.                  |
|  3. Highlight.js highlights Python/Bash code blocks.                     |
|  4. JS Event Delegation connects SVG nodes -> Execution Flow Cards.      |
|  5. User clicks SVG node -> smooth scroll & cyan pulse glow animation.   |
+--------------------------------------------------------------------------+
```

---

## 5. Token Replacement System

The generator avoids heavy templating engines like Jinja2 in favor of deterministic string replacement. Each token corresponds directly to a top-level schema key in the authoritative `repo_blueprint.json`:

```
{{PROJECT_NAME}}                   <-- project_metadata.name
{{PROJECT_SLUG}}                   <-- project_metadata.slug
{{PROJECT_SUMMARY}}                <-- project_metadata.summary
{{PRIMARY_PURPOSE}}                <-- project_metadata.project_description.primary_purpose
{{ARCHITECTURE_AND_CONTROL_FLOW}}  <-- project_metadata.project_description.architecture_and_control_flow
{{EDGE_CASES}}                     <-- project_metadata.project_description.edge_cases_and_invariants
{{TECH_STACK_BADGES}}              <-- project_metadata.tech_stack (Pills with version & category)
{{MERMAID_GRAPH}}                  <-- mermaid_graph (Raw Mermaid syntax injected into <pre class="mermaid">)
{{FLOW_CARDS}}                     <-- execution_flow (Numbered cards with IO contracts & code anchors)
{{DATA_MODEL_CARDS}}               <-- core_data_models (Schema cards with field tables)
{{DIRECTORY_TABLE}}                <-- file_system_directory (File tables with roles & LOC)
{{SETUP_COMMANDS}}                 <-- setup_and_verification_playbook (Prereqs + copyable code blocks)
```

---

## 6. How the Interactive Click-to-Jump Engine Works

A standout capability of OverFlow is bidirectional visual-to-code navigation between the high-level architecture diagram and code anchors.

### Implementation Logic

1. **Native Mermaid Render**: Mermaid.js runs in dark mode and renders the flowchart as an inline SVG `<svg>` inside `.mermaid`.
2. **Container Event Delegation**: Instead of modifying Mermaid's raw syntax (which is fragile), an event listener is mounted to the `.mermaid` container.
3. **Multi-Tier Generic Heuristic Matcher**:
   When a user clicks on an SVG node (`g.node`), the script extracts the node's visible text tokens and runs a 3-tier lookup against all rendered cards:
   - **Tier 1 (Exact Symbol Match)**: Checks if any symbol (e.g. `extract_rules_from_prompt`, `evaluate_caller_turn`, `speak_text_aloud`) matches the node.
   - **Tier 2 (Token Overlap Match)**: Checks matching endpoint routes, data models, or stage titles.
   - **Tier 3 (Module File Fallback)**: Matches module filenames (e.g. `engine.py`, `app.py`, `tts_player.py`).
4. **Smooth Centered Scrolling & Pulse Glow**:
   - `scrollIntoView({ behavior: 'smooth', block: 'center' })` centers the target stage card in the viewport.
   - Adds `.highlight-active`, triggering an animated glowing cyan border and scale transition (`@keyframes card-pulse-glow`).

---

## 7. How to Run, Test, and Deploy

### Local Build Commands

```powershell
# 1. Compile default CallBridge tour
python visualizer.py fixtures/callbridge.json output/architecture_tour.html

# 2. Compile secondary DocIndexer tour
python visualizer.py fixtures/doc_indexer.json output/doc_indexer_tour.html

# 3. Generate root index for GitHub Pages
python visualizer.py fixtures/callbridge.json index.html

# 4. Preview in your default browser
start output/architecture_tour.html
```

### Deploying to GitHub Pages

```powershell
git add .
git commit -m "feat: compile and publish architecture tours"
git push origin main
```

Live URLs:
- **Root Tour**: `https://ahmed10-sys.github.io/OverFlow/`
- **CallBridge Tour**: `https://ahmed10-sys.github.io/OverFlow/output/architecture_tour.html`
- **DocIndexer Tour**: `https://ahmed10-sys.github.io/OverFlow/output/doc_indexer_tour.html`

---

## 8. Summary of Engineering Highlights

- **Zero-Dependency Architecture**: No virtual environments or external package installations required to build tours.
- **Defensive Data Ingestion**: Uses safe `.get()` calls throughout Python and JavaScript so missing fields never crash compilation or client rendering.
- **Aesthetic Excellence**: Built with a custom dark palette, responsive glassmorphic cards, glowing mesh backgrounds, and accessible high-contrast text.
- **Universal Schema Compatibility**: Verified to work out of the box with any valid `repo_blueprint.json` schema.
