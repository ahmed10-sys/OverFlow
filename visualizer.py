#!/usr/bin/env python3
"""
Visualizer v3: Complete Static HTML Generator for Repo Blueprints
Parses repo_blueprint.json and injects:
1. Hero & Tech Stack Badges
2. Native Mermaid Architecture Flowchart
3. Execution Pipeline Cards (with Code Anchors)
4. Core Data Model Cards (Schema Tables)
5. Component Directory (File Roles & LOC Metrics)
6. Setup & Verification Playbook (Prerequisites + Copyable Command Blocks)
"""

import html
import json
import os
import sys
from pathlib import Path


def render_tech_stack_badges(tech_stack: list) -> str:
    """Render tech stack items as styled HTML pill badges."""
    if not isinstance(tech_stack, list) or not tech_stack:
        return '<span class="text-xs text-slate-500 italic">No technologies listed</span>'

    category_styles = {
        "runtime": "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
        "web-framework": "bg-sky-500/10 text-sky-400 border-sky-500/20",
        "asgi-server": "bg-indigo-500/10 text-indigo-400 border-indigo-500/20",
        "data-validation": "bg-amber-500/10 text-amber-400 border-amber-500/20",
        "llm-client": "bg-purple-500/10 text-purple-400 border-purple-500/20",
        "speech-to-text": "bg-rose-500/10 text-rose-400 border-rose-500/20",
        "text-to-speech": "bg-fuchsia-500/10 text-fuchsia-400 border-fuchsia-500/20",
        "audio-io": "bg-teal-500/10 text-teal-400 border-teal-500/20",
        "config": "bg-slate-500/10 text-slate-400 border-slate-500/20",
        "realtime-transport": "bg-cyan-500/10 text-cyan-400 border-cyan-500/20",
    }

    badges = []
    for item in tech_stack:
        if not isinstance(item, dict):
            continue
        name = html.escape(str(item.get("name", "Unknown")))
        version = html.escape(str(item.get("version", "")))
        category = str(item.get("category", "tool")).lower()
        
        style = category_styles.get(category, "bg-slate-800 text-slate-300 border-slate-700")
        
        ver_span = f'<span class="opacity-60 font-mono text-[11px]">{version}</span>' if version else ""
        cat_span = f'<span class="text-[9px] uppercase tracking-wider px-1.5 py-0.5 rounded bg-black/30 opacity-75">{html.escape(category)}</span>' if category else ""
        
        badges.append(
            f'<div class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium border {style} shadow-sm">'
            f'<span class="font-semibold text-white">{name}</span>'
            f'{ver_span}'
            f'{cat_span}'
            f'</div>'
        )
    return "\n".join(badges)


def render_flow_cards(execution_flow: list) -> str:
    """Render numbered pipeline execution stages with code anchors and IO contracts."""
    if not isinstance(execution_flow, list) or not execution_flow:
        return '<p class="text-sm text-slate-500 p-4">No execution flow stages defined.</p>'

    cards = []
    for idx, stage in enumerate(execution_flow, 1):
        if not isinstance(stage, dict):
            continue

        stage_id = html.escape(str(stage.get("stage_id", f"flow-{idx:02d}")))
        step_number = html.escape(str(stage.get("step_number", idx)))
        name = html.escape(str(stage.get("name", f"Stage {step_number}")))
        module_file = html.escape(str(stage.get("module_file", "unknown.py")))
        symbol_invoked = html.escape(str(stage.get("symbol_invoked", "")))
        mechanism = html.escape(str(stage.get("mechanism", "No mechanism description provided.")))
        input_contract = html.escape(str(stage.get("input_contract", "")))
        output_contract = html.escape(str(stage.get("output_contract", "")))

        # Code anchor info
        code_anchor = stage.get("code_anchor", {})
        if not isinstance(code_anchor, dict):
            code_anchor = {}
        
        anchor_file = html.escape(str(code_anchor.get("file", module_file)))
        anchor_lines = html.escape(str(code_anchor.get("lines", "")))
        anchor_snippet = html.escape(str(code_anchor.get("snippet", "# No snippet provided")))

        caption = f"{anchor_file}" + (f":{anchor_lines}" if anchor_lines else "")

        # IO Contracts block
        contracts_html = ""
        if input_contract or output_contract:
            in_row = f'<div class="p-2.5 rounded-lg bg-black/40 border border-slate-800/80"><span class="text-emerald-400 font-semibold select-none">IN:</span> <span class="text-slate-300 ml-1">{input_contract}</span></div>' if input_contract else ""
            out_row = f'<div class="p-2.5 rounded-lg bg-black/40 border border-slate-800/80"><span class="text-sky-400 font-semibold select-none">OUT:</span> <span class="text-slate-300 ml-1">{output_contract}</span></div>' if output_contract else ""
            contracts_html = f"""
            <div class="space-y-2 pt-2 border-t border-white/5 text-xs font-mono">
              {in_row}
              {out_row}
            </div>
            """

        symbol_html = f'<span class="text-indigo-400">&rarr;</span> <span class="text-sky-300">{symbol_invoked}</span>' if symbol_invoked else ""

        cards.append(f"""
        <div id="stage-{stage_id}" class="glass-panel p-6 rounded-2xl border border-slate-800 hover:border-indigo-500/30 transition-all flex flex-col justify-between space-y-4 shadow-lg group scroll-mt-24">
          <div class="space-y-3">
            <div class="flex items-center justify-between gap-2 flex-wrap">
              <span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-mono font-bold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                Step {step_number}
              </span>
              <div class="text-xs font-mono text-slate-400 truncate flex items-center gap-1.5">
                <span class="text-slate-300 font-semibold">{module_file}</span>
                {symbol_html}
              </div>
            </div>

            <h3 class="text-base font-bold text-white group-hover:text-sky-300 transition-colors">
              {name}
            </h3>

            <p class="text-xs text-slate-300 leading-relaxed">
              {mechanism}
            </p>
          </div>

          {contracts_html}

          <!-- Code Anchor Snippet with Caption -->
          <div class="rounded-xl overflow-hidden border border-slate-800/80 bg-[#06090f] mt-2">
            <div class="flex items-center justify-between px-3 py-1.5 bg-slate-900/60 border-b border-slate-800/80 text-[11px] font-mono text-slate-400">
              <span class="flex items-center gap-1.5">
                <svg class="w-3.5 h-3.5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"/></svg>
                Anchor: <strong class="text-slate-300">{caption}</strong>
              </span>
              <span class="text-[10px] uppercase font-semibold text-slate-500 tracking-wider">Python</span>
            </div>
            <pre class="p-3 text-xs font-mono overflow-x-auto text-sky-200/90 leading-snug"><code class="language-python">{anchor_snippet}</code></pre>
          </div>
        </div>
        """)

    return "\n".join(cards)


def render_data_models(core_data_models: list) -> str:
    """Render core data model schema cards with field tables."""
    if not isinstance(core_data_models, list) or not core_data_models:
        return '<p class="text-sm text-slate-500 p-4">No data models defined.</p>'

    cards = []
    for model in core_data_models:
        if not isinstance(model, dict):
            continue

        entity_name = html.escape(str(model.get("entity_name", "DataModel")))
        defined_in = html.escape(str(model.get("defined_in", "models.py")))
        fields = model.get("fields", [])

        field_rows = []
        if isinstance(fields, list):
            for field in fields:
                if not isinstance(field, dict):
                    continue
                fname = html.escape(str(field.get("name", "")))
                ftype = html.escape(str(field.get("type", "Any")))
                fdesc = html.escape(str(field.get("description", "")))

                field_rows.append(f"""
                <tr class="border-b border-slate-800/60 last:border-0 hover:bg-slate-800/30 transition">
                  <td class="py-2.5 px-3 font-mono text-xs font-semibold text-white whitespace-nowrap">{fname}</td>
                  <td class="py-2.5 px-3 font-mono text-[11px] whitespace-nowrap">
                    <span class="px-2 py-0.5 rounded bg-emerald-950/60 text-emerald-300 border border-emerald-800/40">{ftype}</span>
                  </td>
                  <td class="py-2.5 px-3 text-xs text-slate-300 leading-relaxed">{fdesc}</td>
                </tr>
                """)

        table_body = "\n".join(field_rows) if field_rows else '<tr><td colspan="3" class="p-3 text-xs text-slate-500">No fields listed</td></tr>'

        cards.append(f"""
        <div class="glass-panel rounded-2xl p-5 border border-slate-800 shadow-lg flex flex-col justify-between space-y-4">
          <div class="space-y-3">
            <div class="flex items-center justify-between border-b border-white/5 pb-3">
              <h3 class="text-base font-bold text-white font-mono flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
                {entity_name}
              </h3>
              <span class="text-xs font-mono text-slate-400 bg-slate-800/60 px-2 py-0.5 rounded border border-slate-700/60">
                {defined_in}
              </span>
            </div>

            <div class="overflow-x-auto rounded-xl border border-slate-800/80 bg-[#06090f]">
              <table class="w-full text-left border-collapse">
                <thead>
                  <tr class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider border-b border-slate-800 bg-slate-900/60">
                    <th class="py-2 px-3">Field</th>
                    <th class="py-2 px-3">Type</th>
                    <th class="py-2 px-3">Description</th>
                  </tr>
                </thead>
                <tbody>
                  {table_body}
                </tbody>
              </table>
            </div>
          </div>
        </div>
        """)

    return "\n".join(cards)


def render_directory_table(file_system_directory: list) -> str:
    """Render repository directory tables with file roles and LOC counts."""
    if not isinstance(file_system_directory, list) or not file_system_directory:
        return '<p class="text-sm text-slate-500 p-6">No directory breakdown available.</p>'

    sections = []
    for dir_info in file_system_directory:
        if not isinstance(dir_info, dict):
            continue

        directory = html.escape(str(dir_info.get("directory", "./")))
        purpose = html.escape(str(dir_info.get("purpose", "")))
        key_files = dir_info.get("key_files", [])

        file_rows = []
        total_loc = 0
        if isinstance(key_files, list):
            for kf in key_files:
                if not isinstance(kf, dict):
                    continue
                file_name = html.escape(str(kf.get("file", "")))
                role = html.escape(str(kf.get("role", "")))
                loc = kf.get("loc", "-")
                if isinstance(loc, int):
                    total_loc += loc

                file_rows.append(f"""
                <tr class="border-b border-slate-800/60 last:border-0 hover:bg-slate-800/30 transition">
                  <td class="py-3 px-4 font-mono text-xs font-bold text-sky-300 flex items-center gap-2 whitespace-nowrap">
                    <svg class="w-4 h-4 text-slate-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
                    {file_name}
                  </td>
                  <td class="py-3 px-4 text-xs text-slate-300">{role}</td>
                  <td class="py-3 px-4 font-mono text-xs text-amber-400 font-semibold text-right whitespace-nowrap">{loc}</td>
                </tr>
                """)

        table_body = "\n".join(file_rows) if file_rows else '<tr><td colspan="3" class="p-3 text-xs text-slate-500">No key files listed</td></tr>'
        loc_badge = f'<span class="text-xs font-mono text-amber-300/80 bg-amber-950/40 border border-amber-800/40 px-2 py-0.5 rounded">Total: {total_loc} LOC</span>' if total_loc > 0 else ""

        sections.append(f"""
        <div class="p-6 border-b border-slate-800 last:border-0">
          <div class="flex flex-wrap items-center justify-between gap-3 mb-4">
            <div class="flex items-center gap-2.5">
              <span class="px-2.5 py-1 rounded-md bg-amber-500/10 text-amber-400 border border-amber-500/20 font-mono text-xs font-bold">
                {directory}
              </span>
              <span class="text-xs text-slate-300">{purpose}</span>
            </div>
            {loc_badge}
          </div>

          <div class="overflow-x-auto rounded-xl border border-slate-800 bg-[#06090f]">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider border-b border-slate-800 bg-slate-900/80">
                  <th class="py-2.5 px-4">File Name</th>
                  <th class="py-2.5 px-4">Architecture Function & Role</th>
                  <th class="py-2.5 px-4 text-right">LOC</th>
                </tr>
              </thead>
              <tbody>
                {table_body}
              </tbody>
            </table>
          </div>
        </div>
        """)

    return "\n".join(sections)


def render_setup_commands(playbook: dict) -> str:
    """Render prerequisites checklist and copyable commands."""
    if not isinstance(playbook, dict):
        playbook = {}

    prerequisites = playbook.get("prerequisites", [])
    commands = playbook.get("commands", [])

    # Prerequisites list
    prereq_items = []
    if isinstance(prerequisites, list):
        for p in prerequisites:
            prereq_items.append(
                f'<li class="flex items-start gap-2 text-xs text-slate-300">'
                f'<svg class="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>'
                f'<span>{html.escape(str(p))}</span>'
                f'</li>'
            )
    prereq_html = "\n".join(prereq_items) if prereq_items else '<li class="text-xs text-slate-500 italic">None specified</li>'

    # Build all commands string for "Copy All"
    all_cmds_list = []
    cmd_cards = []

    if isinstance(commands, list):
        for idx, cmd in enumerate(commands, 1):
            if not isinstance(cmd, dict):
                continue
            step_num = html.escape(str(cmd.get("step", idx)))
            title = html.escape(str(cmd.get("title", f"Step {step_num}")))
            raw_command = str(cmd.get("command", ""))
            escaped_command = html.escape(raw_command)

            all_cmds_list.append(f"# Step {step_num}: {title}\n{raw_command}")

            cmd_cards.append(f"""
            <div class="rounded-xl overflow-hidden border border-slate-800 bg-[#06090f] shadow-md">
              <div class="flex items-center justify-between px-4 py-2 bg-slate-900/80 border-b border-slate-800">
                <div class="flex items-center gap-2">
                  <span class="w-5 h-5 rounded-full bg-rose-500/20 text-rose-400 text-xs font-mono font-bold flex items-center justify-center">
                    {step_num}
                  </span>
                  <span class="text-xs font-semibold text-white">{title}</span>
                </div>
                <button class="copy-btn px-2.5 py-1 text-[11px] font-semibold text-slate-300 bg-slate-800 hover:bg-slate-700 hover:text-white rounded border border-slate-700 transition flex items-center gap-1" data-clipboard="{html.escape(raw_command, quote=True)}">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>
                  Copy
                </button>
              </div>
              <pre class="p-3 text-xs font-mono overflow-x-auto text-emerald-300"><code class="language-bash">{escaped_command}</code></pre>
            </div>
            """)

    all_commands_combined = "\n\n".join(all_cmds_list)
    copy_all_btn = f"""
    <button class="copy-btn px-3 py-1.5 text-xs font-semibold text-sky-400 bg-sky-950/60 hover:bg-sky-900/60 rounded-lg border border-sky-800/60 transition flex items-center gap-1.5 shadow-sm" data-clipboard="{html.escape(all_commands_combined, quote=True)}">
      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/></svg>
      Copy All Steps
    </button>
    """ if all_cmds_list else ""

    return f"""
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <div class="lg:col-span-1 space-y-4">
        <h3 class="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
          <svg class="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          Prerequisites
        </h3>
        <ul class="space-y-2.5 p-4 rounded-xl bg-slate-900/60 border border-slate-800">
          {prereq_html}
        </ul>
      </div>

      <div class="lg:col-span-2 space-y-4">
        <div class="flex items-center justify-between">
          <h3 class="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <svg class="w-4 h-4 text-sky-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"/></svg>
            Verification Playbook
          </h3>
          {copy_all_btn}
        </div>
        <div class="space-y-3">
          {"".join(cmd_cards)}
        </div>
      </div>
    </div>
    """


def main():
    base_dir = Path(__file__).resolve().parent
    
    # 1. Read JSON file path from sys.argv[1] (default: fixtures/callbridge.json)
    if len(sys.argv) > 1:
        blueprint_path = Path(sys.argv[1])
    else:
        blueprint_path = base_dir / "fixtures" / "callbridge.json"

    # Default output path
    if len(sys.argv) > 2:
        output_path = Path(sys.argv[2])
    else:
        output_path = base_dir / "output" / "architecture_tour.html"

    template_path = base_dir / "template.html"

    # 2. Parse JSON into dict with defensive error handling
    if not blueprint_path.exists():
        print(f"[-] Error: Blueprint file not found at: {blueprint_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(blueprint_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[-] Error parsing JSON in {blueprint_path}: {e}", file=sys.stderr)
        sys.exit(1)

    # 3. Load template.html as string
    if not template_path.exists():
        print(f"[-] Error: Template file not found at: {template_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(template_path, "r", encoding="utf-8") as f:
            html_content = f.read()
    except Exception as e:
        print(f"[-] Error reading template file {template_path}: {e}", file=sys.stderr)
        sys.exit(1)

    # Metadata & Descriptions
    metadata = data.get("project_metadata", {})
    if not isinstance(metadata, dict):
        metadata = {}

    description = metadata.get("project_description", {})
    if not isinstance(description, dict):
        description = {}

    project_name = html.escape(str(metadata.get("name", "Project Architecture Tour")))
    project_slug = html.escape(str(metadata.get("slug", "architecture-tour")))
    project_summary = html.escape(str(metadata.get("summary", "System overview and architectural blueprint.")))

    primary_purpose = html.escape(str(description.get("primary_purpose", "No primary purpose specified.")))
    architecture_flow = html.escape(str(description.get("architecture_and_control_flow", "No architecture description specified.")))
    edge_cases = html.escape(str(description.get("edge_cases_and_invariants", "No edge cases or invariants specified.")))

    tech_stack = metadata.get("tech_stack", [])
    tech_stack_badges = render_tech_stack_badges(tech_stack)

    # Mermaid diagram raw
    mermaid_graph = str(data.get("mermaid_graph", "graph TD\n  Start[Start] --> End[End]")).strip()

    # Section Renderers
    execution_flow = data.get("execution_flow", [])
    flow_cards_html = render_flow_cards(execution_flow)

    core_data_models = data.get("core_data_models", [])
    data_models_html = render_data_models(core_data_models)

    file_system_directory = data.get("file_system_directory", [])
    directory_table_html = render_directory_table(file_system_directory)

    playbook = data.get("setup_and_verification_playbook", {})
    setup_commands_html = render_setup_commands(playbook)

    # Full Token Replacements
    replacements = {
        "{{PROJECT_NAME}}": project_name,
        "{{PROJECT_SLUG}}": project_slug,
        "{{PROJECT_SUMMARY}}": project_summary,
        "{{PRIMARY_PURPOSE}}": primary_purpose,
        "{{ARCHITECTURE_AND_CONTROL_FLOW}}": architecture_flow,
        "{{EDGE_CASES}}": edge_cases,
        "{{TECH_STACK_BADGES}}": tech_stack_badges,
        "{{MERMAID_GRAPH}}": mermaid_graph,
        "{{FLOW_CARDS}}": flow_cards_html,
        "{{DATA_MODEL_CARDS}}": data_models_html,
        "{{DIRECTORY_TABLE}}": directory_table_html,
        "{{SETUP_COMMANDS}}": setup_commands_html,
    }

    for token, val in replacements.items():
        html_content = html_content.replace(token, val)

    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
    except Exception as e:
        print(f"[-] Error writing output file {output_path}: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"[+] Successfully generated: {output_path}")


if __name__ == "__main__":
    main()
