"""CISC 121 Project — Shuttle Stop Crowd Ranking (Merge Sort visualizer).

Counts are fictional teaching examples, not real-time campus measurements.
Core sorting is implemented below without Python's built-in sorting functions.
"""

import html
import re
from typing import Any

import gradio as gr

MAX_STOPS = 24
MAX_COUNT = 100000
SAMPLE = """Union St,45
Library,20
Residence,70
Gym,35
West Campus,55"""


def parse_stops(text: str) -> list[dict[str, Any]]:
    """Parse 'stop name,nonnegative integer' records; report actionable errors."""
    if not text or not text.strip():
        raise ValueError("Enter at least one stop, one per line: Stop name, crowd count.")
    rows = [line.strip() for line in text.splitlines() if line.strip()]
    if len(rows) > MAX_STOPS:
        raise ValueError(f"Use at most {MAX_STOPS} stops so the simulation stays readable.")
    stops = []
    seen = set()
    for line_number, line in enumerate(rows, start=1):
        if line.count(",") != 1:
            raise ValueError(f"Line {line_number}: use exactly one comma, e.g. Library,20.")
        name, count_text = (field.strip() for field in line.split(",", 1))
        if not name or len(name) > 32:
            raise ValueError(f"Line {line_number}: the stop name must be 1–32 characters.")
        if name.casefold() in seen:
            raise ValueError(f"Line {line_number}: '{name}' appears more than once.")
        if not re.fullmatch(r"[0-9]+", count_text):
            raise ValueError(f"Line {line_number}: crowd count must be a whole nonnegative number.")
        count = int(count_text)
        if count > MAX_COUNT:
            raise ValueError(f"Line {line_number}: crowd count must be at most {MAX_COUNT:,}.")
        seen.add(name.casefold())
        stops.append({"id": len(stops), "name": name, "count": count})
    return stops


def merge_sort_steps(stops: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Return descending crowd ranking and recorded Merge Sort teaching steps.

    Tie handling: original order is preserved by choosing left on equality.
    This is a stable Merge Sort, NOT a call to a built-in sorting function.
    """
    working = [item.copy() for item in stops]
    history = []

    def record(action: str, detail: str, focus=(), segment=None):
        history.append({
            "action": action,
            "detail": detail,
            "items": [item.copy() for item in working],
            "focus": list(focus),
            "segment": list(segment) if segment is not None else None,
        })

    record("Start", "Original input order. We will rank the busiest stop first.")

    def split_and_merge(left: int, right: int) -> None:
        if right - left <= 1:
            return
        middle = (left + right) // 2
        record("Split", f"Divide positions {left + 1}–{right} into two smaller groups.",
               segment=(left, right))
        split_and_merge(left, middle)
        split_and_merge(middle, right)

        left_items = working[left:middle]
        right_items = working[middle:right]
        merged = []
        i = j = 0
        while i < len(left_items) and j < len(right_items):
            a = left_items[i]
            b = right_items[j]
            record("Compare", f"Compare {a['name']} ({a['count']}) with {b['name']} ({b['count']}).",
                   focus=(a["id"], b["id"]), segment=(left, right))
            if a["count"] >= b["count"]:
                merged.append(a)
                i += 1
            else:
                merged.append(b)
                j += 1
        # Copy remaining elements into the merged group.
        while i < len(left_items):
            merged.append(left_items[i]); i += 1
        while j < len(right_items):
            merged.append(right_items[j]); j += 1
        working[left:right] = merged
        record("Merge", f"Merged positions {left + 1}–{right} in descending crowd order.",
               focus=[item["id"] for item in merged], segment=(left, right))

    split_and_merge(0, len(working))
    record("Finished", "All groups are merged. The largest crowd is first.")
    return working, history


def render_bars(frame: dict[str, Any]) -> str:
    items = frame["items"]
    max_count = max((x["count"] for x in items), default=1) or 1
    focus = set(frame["focus"])
    segment = frame["segment"]
    bar_rows = []
    for position, item in enumerate(items):
        chosen = item["id"] in focus
        in_segment = segment is not None and segment[0] <= position < segment[1]
        color = "#0f766e" if chosen else ("#617dd6" if in_segment else "#94a3b8")
        width = max(3, round(item["count"] / max_count * 100)) if item["count"] else 0
        name = html.escape(item["name"])
        count = item["count"]
        bar_rows.append(
            f'<div class="crowd-row"><div class="crowd-name" style="color:#0f172a !important;opacity:1 !important">{position + 1}. {name}</div>'
            f'<div class="crowd-track"><div class="crowd-fill" style="width:{width}%;background:{color}"></div></div>'
            f'<div class="crowd-value" style="color:#0f172a !important;opacity:1 !important">{count}</div></div>'
        )
    action = html.escape(frame["action"])
    return (
        '<div class="crowd-wrap">'
        f'<div class="crowd-action">{action}</div>'
        + "".join(bar_rows)
        + '<p class="crowd-legend"><span style="color:#0f766e">■</span> compared / merged'
          ' &nbsp; <span style="color:#617dd6">■</span> active group'
          ' &nbsp; <span style="color:#94a3b8">■</span> other items</p></div>'
    )


def ranking_markdown(ranked: list[dict[str, Any]]) -> str:
    if not ranked:
        return "No ranking yet."
    lines = ["| Rank | Shuttle stop | Estimated riders |", "|---:|---|---:|"]
    for index, item in enumerate(ranked, start=1):
        # Escape characters that would interfere with markdown tables.
        clean = item["name"].replace("|", "\\|")
        lines.append(f"| {index} | {clean} | {item['count']} |")
    top_count = ranked[0]["count"]
    busiest = [x["name"] for x in ranked if x["count"] == top_count]
    lines.append(f"\n**Dispatch recommendation:** prioritize **{', '.join(busiest)}** "
                 f"({top_count} estimated riders). These are user-entered estimates, not live counts.")
    return "\n".join(lines)


def step_output(state: dict[str, Any], index: int):
    if not state or not state.get("frames"):
        return "No simulation yet.", "Enter stops and select **Run Merge Sort**.", "", 0
    frames = state["frames"]
    index = max(0, min(int(index), len(frames) - 1))
    frame = frames[index]
    description = (f"**Step {index + 1} of {len(frames)} — {frame['action']}**\n\n"
                   + frame["detail"])
    return render_bars(frame), description, ranking_markdown(state["ranked"]), index


def start_sort(text: str):
    try:
        stops = parse_stops(text)
    except ValueError as exc:
        raise gr.Error(str(exc)) from exc
    ranked, frames = merge_sort_steps(stops)
    state = {"ranked": ranked, "frames": frames}
    bars, desc, ranking, index = step_output(state, 0)
    return state, bars, desc, ranking, gr.update(minimum=0, maximum=len(frames)-1, value=index)


def show_step(state: dict[str, Any], index: float):
    bars, desc, ranking, _ = step_output(state, int(index))
    return bars, desc, ranking


def next_step(state: dict[str, Any], index: float, delta: int):
    max_index = len(state.get("frames", [])) - 1 if state else 0
    next_index = max(0, min(max_index, int(index) + delta))
    bars, desc, ranking, _ = step_output(state, next_index)
    return gr.update(value=next_index), bars, desc, ranking


def go_last(state: dict[str, Any]):
    index = max(0, len(state.get("frames", [])) - 1) if state else 0
    bars, desc, ranking, _ = step_output(state, index)
    return gr.update(value=index), bars, desc, ranking


def add_stop(text: str, name: str, count: float):
    name = (name or "").strip()
    if not name or len(name) > 32 or "," in name or "\n" in name:
        raise gr.Error("Stop name must be 1–32 characters without commas.")
    if count is None or count < 0 or count > MAX_COUNT or int(count) != count:
        raise gr.Error("Crowd count must be a whole number from 0 to 100,000.")
    new_text = (text.rstrip() + "\n" if text and text.strip() else "") + f"{name},{int(count)}"
    try:
        parse_stops(new_text)
    except ValueError as exc:
        raise gr.Error(str(exc)) from exc
    return new_text, "", 0


CSS = """
.crowd-wrap {background:#f8fafc;border:1px solid #e2e8f0;border-radius:16px;padding:20px;color:#0f172a}
.crowd-action {font-weight:750;font-size:16px;margin-bottom:16px;color:#0f172a}
.crowd-row {display:grid;grid-template-columns:145px 1fr 56px;align-items:center;gap:12px;margin:11px 0}
.crowd-name {font-size:13px;overflow-wrap:anywhere;color:#0f172a !important}
.crowd-track {height:22px;background:#e2e8f0;border-radius:6px;overflow:hidden}
.crowd-fill {height:100%;border-radius:6px;transition:width .18s ease}
.crowd-value {font-weight:700;font-variant-numeric:tabular-nums;text-align:right;color:#0f172a !important}
.crowd-legend {font-size:12px;color:#475569;margin-top:18px}
@media(max-width:620px){.crowd-row{grid-template-columns:100px 1fr 40px;gap:6px}.crowd-wrap{padding:12px}}
"""


def build_app():
    with gr.Blocks(title="Shuttle Stop Crowd Ranking — Merge Sort") as demo:
        gr.Markdown("# 🚌 Shuttle Stop Crowd Ranking\n"
                    "**Learn Merge Sort by ranking campus shuttle stops from busiest to quietest.** "
                    "All starting numbers are fictional examples; replace them with your own estimates.")
        state = gr.State({})
        with gr.Row():
            with gr.Column(scale=1):
                stops_input = gr.Textbox(label="Stop data (one per line: name,count)",
                                         value=SAMPLE, lines=8,
                                         info="Nonnegative whole numbers, unique names, maximum 24 stops.")
                with gr.Accordion("Add one stop", open=False):
                    new_name = gr.Textbox(label="Stop name", placeholder="Example: Student Centre")
                    new_count = gr.Number(label="Estimated rider count", value=25, precision=0)
                    add_button = gr.Button("Add stop to input")
                run_button = gr.Button("Run Merge Sort", variant="primary")
                gr.Markdown("**How to use:** Edit the stops, click **Run Merge Sort**, "
                            "then use **Next**, **Previous**, the slider, or **Final result**. "
                            "A new run is needed after editing input.")
            with gr.Column(scale=2):
                chart = gr.HTML(value='<div class="crowd-wrap">Click <b>Run Merge Sort</b> to begin.</div>')
                detail = gr.Markdown("The step explanation will appear here.")
                step_slider = gr.Slider(minimum=0, maximum=1, value=0, step=1, label="Simulation step")
                with gr.Row():
                    previous = gr.Button("◀ Previous")
                    following = gr.Button("Next ▶")
                    final = gr.Button("Final result ⏭")
        gr.Markdown("## Final crowd ranking")
        ranking = gr.Markdown("No ranking yet. Run the algorithm to view the result.")
        gr.Markdown("*Teaching note:* Merge Sort recursively divides the records, compares their crowd counts, "
                    "and merges them. Equal counts keep their original relative order (stable sorting). "
                    "Crowd estimates are illustrative; dispatch decisions should use reliable live data in practice.")

        add_button.click(add_stop, inputs=[stops_input, new_name, new_count],
                         outputs=[stops_input, new_name, new_count])
        run_button.click(start_sort, inputs=stops_input,
                         outputs=[state, chart, detail, ranking, step_slider])
        step_slider.input(show_step, inputs=[state, step_slider], outputs=[chart, detail, ranking])
        previous.click(lambda s, i: next_step(s, i, -1), inputs=[state, step_slider],
                       outputs=[step_slider, chart, detail, ranking])
        following.click(lambda s, i: next_step(s, i, 1), inputs=[state, step_slider],
                        outputs=[step_slider, chart, detail, ranking])
        final.click(go_last, inputs=state, outputs=[step_slider, chart, detail, ranking])
    return demo


if __name__ == "__main__":
    build_app().launch(css=CSS)
