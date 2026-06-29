# รายงานเวลาพากย์ (voice-reports)

repo แม่สำหรับรวมรายงานการคิดเวลาพากย์ทุกงาน เปิดดูออนไลน์ผ่าน GitHub Pages

- หน้ารวม (landing): `index.html` — ลิสต์ทุกงาน
- แต่ละงาน = โฟลเดอร์ย่อย `<ชื่องาน>/` (self-contained: viewer + mp3 ในตัว)

## วิธีเพิ่มงานใหม่
1. สร้าง bundle ของงานลงใน `site/<ชื่องาน>/` (index.html + viewer_*.html + mp3 ชื่อ ASCII)
2. ใส่ `site/<ชื่องาน>/job.json` (ออปชัน) เพื่อโชว์รายละเอียดบนหน้ารวม:
   ```json
   { "title": "KKN50", "date": "2026-01-15", "people": 6, "total_minutes": 73.5, "note": "ตอนที่ 1" }
   ```
3. รัน `python build_landing.py` (อยู่นอกโฟลเดอร์ site) → regenerate `index.html` ให้ลิสต์งานใหม่
4. `git add -A && git commit -m "add <งาน>" && git push` → GitHub Pages อัปเดตเอง

> ⚠️ repo นี้ **public** (จำเป็นสำหรับ GitHub Pages ฟรี) — งาน/เสียงที่ใส่จะเปิดสาธารณะ
> สร้างด้วย `audio_vad_report.py` (silence-gate billing แบบ Adobe Audition Delete Silence)
