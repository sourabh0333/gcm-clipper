"""A single local page to watch the ranked clips and keep or reject each one. Decisions stay in the
browser until exported; the exported JSON is labelled data for improving the detector."""

import html
import json


def _fmt(seconds):
    seconds = int(seconds)
    return f"{seconds // 3600}:{seconds // 60 % 60:02d}:{seconds % 60:02d}"


def build(job_name, info, clips):
    cards = []
    for clip in clips:
        verdict = clip.get("judge") or {}
        title = verdict.get("title") or clip["type"].replace("_", " ")
        reasons = ", ".join(clip.get("reasons", [])) or "loud moment"
        summary = verdict.get("summary", "")
        weak = verdict.get("weak_points", "")
        cards.append(f"""
<article class="card" data-id="{clip['id']}">
  <video src="clips/{html.escape(clip['file'])}" controls preload="metadata" playsinline></video>
  <div class="meta">
    <p class="rank">#{clip['rank']} · {html.escape(clip['type'].replace('_', ' '))} · score {clip['final_score']}</p>
    <h2>{html.escape(title)}</h2>
    {f'<p>{html.escape(summary)}</p>' if summary else ''}
    <p class="why">Why: {html.escape(reasons)}</p>
    {f'<p class="weak">Weak points: {html.escape(weak)}</p>' if weak else ''}
    <p class="time">{_fmt(clip['start'])} – {_fmt(clip['end'])} in the source</p>
    <div class="actions">
      <button data-v="keep">Keep</button><button data-v="reject">Reject</button>
      <input placeholder="Why? (optional)" aria-label="Reason">
    </div>
  </div>
</article>""")

    data = json.dumps({"job": job_name, "source": info.get("webpage_url") or info.get("path"),
                       "clips": [{k: c[k] for k in ("id", "rank", "start", "end", "type", "final_score")}
                                 for c in clips]})
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI-GCM review</title>
<style>
:root {{ --bg:#f6f7f8; --card:#fff; --ink:#15181c; --muted:#5b6470; --line:#dde1e6; --keep:#137a3f; --reject:#b3261e; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#111315; --card:#1b1e21; --ink:#eef0f2; --muted:#9aa3ad; --line:#2c3136; }} }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--ink); font:15px/1.45 system-ui,sans-serif; }}
header {{ padding:20px 16px; border-bottom:1px solid var(--line); display:flex; flex-wrap:wrap; gap:12px; align-items:center; justify-content:space-between; }}
h1 {{ font-size:20px; margin:0; }} h2 {{ font-size:17px; margin:4px 0 8px; }}
main {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:16px; padding:16px; }}
.card {{ background:var(--card); border:1px solid var(--line); border-radius:12px; overflow:hidden; }}
.card.keep {{ outline:3px solid var(--keep); }} .card.reject {{ opacity:.55; outline:3px solid var(--reject); }}
video {{ width:100%; aspect-ratio:9/16; background:#000; display:block; }}
.meta {{ padding:12px 14px 14px; }} .meta p {{ margin:4px 0; }}
.rank,.time,.why {{ color:var(--muted); font-size:13px; }} .weak {{ color:var(--reject); font-size:13px; }}
.actions {{ display:flex; flex-wrap:wrap; gap:8px; margin-top:10px; }}
button {{ min-height:40px; padding:0 16px; border-radius:8px; border:1px solid var(--line); background:var(--card); color:var(--ink); font:inherit; cursor:pointer; }}
button[data-v=keep].on {{ background:var(--keep); color:#fff; }} button[data-v=reject].on {{ background:var(--reject); color:#fff; }}
input {{ flex:1 1 140px; min-height:40px; padding:0 10px; border-radius:8px; border:1px solid var(--line); background:transparent; color:var(--ink); font:inherit; }}
</style></head><body>
<header><div><h1>{html.escape(info.get('title') or job_name)}</h1>
<p style="margin:4px 0 0;color:var(--muted)">{len(clips)} clips, best first. Keep or reject each, then export.</p></div>
<button id="export">Export decisions</button></header>
<main>{''.join(cards)}</main>
<script>
const DATA = {data};
const KEY = 'aigcm-review-' + DATA.job;
let state = {{}};
try {{ state = JSON.parse(localStorage.getItem(KEY) || '{{}}'); }} catch (e) {{}}
const save = () => {{ try {{ localStorage.setItem(KEY, JSON.stringify(state)); }} catch (e) {{}} }};
document.querySelectorAll('.card').forEach(card => {{
  const id = card.dataset.id, input = card.querySelector('input');
  const paint = () => {{
    const v = (state[id] || {{}}).verdict;
    card.classList.toggle('keep', v === 'keep'); card.classList.toggle('reject', v === 'reject');
    card.querySelectorAll('button').forEach(b => b.classList.toggle('on', b.dataset.v === v));
  }};
  input.value = (state[id] || {{}}).reason || '';
  card.querySelectorAll('button').forEach(b => b.addEventListener('click', () => {{
    state[id] = {{ ...(state[id] || {{}}), verdict: b.dataset.v }}; save(); paint();
  }}));
  input.addEventListener('input', () => {{ state[id] = {{ ...(state[id] || {{}}), reason: input.value }}; save(); }});
  paint();
}});
document.getElementById('export').addEventListener('click', () => {{
  const out = {{ ...DATA, clips: DATA.clips.map(c => ({{ ...c, ...(state[c.id] || {{}}) }})) }};
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([JSON.stringify(out, null, 2)], {{ type: 'application/json' }}));
  a.download = DATA.job + '-decisions.json'; a.click();
}});
</script></body></html>
"""
