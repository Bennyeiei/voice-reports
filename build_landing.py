# -*- coding: utf-8 -*-
"""build_landing.py — regenerate index.html จากโฟลเดอร์งานใน site/<ชื่องาน>/

แต่ละงานต้องมี site/<ชื่องาน>/index.html (viewer) และอาจมี job.json:
  { "title": "...", "date": "...", "people": 1, "total_minutes": 8.1, "note": "..." }

ใช้:
    python build_landing.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"

TEMPLATE = """<!doctype html>
<html lang="th"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>รายงานเวลาพากย์</title>
<style>
:root{{color-scheme:dark;--bg:#070d18;--line:rgba(120,140,190,.16);--text:#e8edf7;--muted:#94a1bd;--accent:#6c8cff}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:"Segoe UI",system-ui,Arial,sans-serif;color:var(--text);
background:radial-gradient(1100px 520px at 12% -8%,rgba(108,140,255,.16),transparent 60%),linear-gradient(180deg,#0b1426,#070d18 60%);min-height:100vh}}
.wrap{{max-width:980px;margin:0 auto;padding:40px 22px 60px}}
h1{{font-size:26px;margin:0 0 6px}}
.lead{{color:var(--muted);font-size:14px;margin:0 0 26px}}
.jobs{{display:grid;gap:14px}}
.job{{display:block;text-decoration:none;color:var(--text);background:linear-gradient(180deg,rgba(24,34,58,.85),rgba(15,23,42,.75));
border:1px solid var(--line);border-radius:16px;padding:18px 20px;transition:transform .15s,border-color .15s}}
.job:hover{{transform:translateY(-2px);border-color:rgba(108,140,255,.5)}}
.jt{{font-size:19px;font-weight:700;margin-bottom:4px}}
.jt::before{{content:"\U0001F399️ "}}
.jm{{color:var(--muted);font-size:13px}}
.jn{{color:#8ea6ff;font-size:12px;margin-top:6px}}
.empty{{color:var(--muted);background:rgba(15,23,42,.6);border:1px dashed var(--line);border-radius:16px;padding:28px;text-align:center}}
.foot{{margin-top:30px;color:#5b6680;font-size:12px}}
</style></head>
<body><div class="wrap">
<h1>รายงานเวลาพากย์</h1>
<p class="lead">รวมรายงานการคิดเวลาพากย์แต่ละงาน — คลิกเข้าไปดูคลื่นเสียง ก่อน/หลังตัดเงียบ + ฟัง mp3 + viewer เต็มซูมตรวจได้</p>
<div class="jobs">
{jobs_html}
</div>
<p class="foot">สร้างด้วย audio_vad_report (silence-gate billing) · {count} งาน</p>
</div></body></html>
"""

JOB_TEMPLATE = """<a class="job" href="site/{slug}/index.html">
<div class="jt">{title}</div>
<div class="jm">{meta}</div>
{note_html}
</a>"""


def main() -> None:
    jobs = []
    if SITE.is_dir():
        for d in sorted(SITE.iterdir()):
            if not d.is_dir() or not (d / "index.html").exists():
                continue
            meta = {}
            job_json = d / "job.json"
            if job_json.exists():
                meta = json.loads(job_json.read_text(encoding="utf-8"))
            jobs.append((d.name, meta))

    if jobs:
        parts = []
        for slug, meta in jobs:
            title = meta.get("title", slug)
            bits = []
            if meta.get("date"):
                bits.append(meta["date"])
            if meta.get("people"):
                bits.append(f"{meta['people']} คน")
            if meta.get("total_minutes") is not None:
                bits.append(f"{meta['total_minutes']} นาที")
            note_html = f'<div class="jn">{meta["note"]}</div>' if meta.get("note") else ""
            parts.append(JOB_TEMPLATE.format(
                slug=slug, title=title, meta=" · ".join(bits), note_html=note_html,
            ))
        jobs_html = "\n".join(parts)
    else:
        jobs_html = '<p class="empty">ยังไม่มีรายงาน — งานใหม่จะปรากฏที่นี่อัตโนมัติเมื่อเพิ่มโฟลเดอร์งาน</p>'

    html = TEMPLATE.format(jobs_html=jobs_html, count=len(jobs))
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    print(f"wrote index.html with {len(jobs)} job(s)")


if __name__ == "__main__":
    main()
