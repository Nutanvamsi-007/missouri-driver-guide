#!/usr/bin/env python3
"""Re-parse Driver_Guide.pdf at line/span level and patch guide_data.json + data.js.

Adds a structured `content` list to every chapter (headings, paragraphs, list
items with levels, callouts, tables) with paragraphs/bullets joined across
line and page breaks. Existing keys (pages, blocks, figures, questions...) are
left untouched for backward compatibility.
"""
import json
import re
import shutil
import sys
from pathlib import Path

import fitz

ROOT = Path(__file__).parent
PDF = ROOT / "Driver_Guide.pdf"
RIGHT_LIMIT = 343.8
TABLE_DIR = ROOT / "assets" / "tables"
TWO_COL_PAGES = set(range(48, 57))  # sign-card pages (chapter 7)
SKIP_CHAPTERS = {"index", "contacts"}

CALLOUT_RE = re.compile(r"^\s*(?:\*\*)?(Tip!|IMPORTANT NOTE:|Note:|NOTE:|WARNING:|Caution:)(?:\*\*)?\s*")
BULLETS = {"•": 1, "○": 2, "◦": 2, "▪": 2, "\x07": 1}


def clean(t):
    t = t.replace("\x07", "•").replace("\u2002", " ").replace("\u00ad", "").replace("\t", " ")
    t = t.replace("\u2019", "’")
    return t


def fix_text(t):
    t = t.replace("•", " ")
    t = re.sub(r"\*\*([^*]*?)\*\*", lambda m: (" " if m.group(1)[:1].isspace() else "") + ("**" + m.group(1).strip() + "**" if m.group(1).strip() else "") + (" " if m.group(1)[-1:].isspace() else ""), t)
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"\*\*\s*\*\*", " ", t)
    t = re.sub(r"(?<=\w)\. (?=(?:mo|com|org|gov|net)\b)", ".", t)
    t = re.sub(r"(?<=\.)\s+(?=(?:mo|gov|com|org)\.)", "", t)
    t = re.sub(r"dor\.\s*mo\.\s*gov", "dor.mo.gov", t)
    t = re.sub(r"\. (php|html?|aspx?|pdf)\b", r".\1", t)
    t = re.sub(r"(\d{3})\. (\d{3})", r"\1.\2", t)
    t = re.sub(r"\b([a-z]{3,}[.!?])(?=[A-Z][a-z])", r"\1 ", t)
    t = re.sub(r"\s+([,.;:!?])(?=\s|$)", r"\1", t)
    return t


def page_lines(page, x_range=None, skip_rects=()):
    """Return merged visual lines [{x0,x1,y,spans,...}] for the page."""
    d = page.get_text("dict")
    raw = []
    for b in d["blocks"]:
        if b.get("type") != 0:
            continue
        for ln in b["lines"]:
            spans = [s for s in ln["spans"] if s["text"].strip(" \t\x07\u2002") or "\x07" in s["text"]]
            spans = [s for s in spans if s["color"] != 0xFFFFFF]
            if not spans:
                continue
            x0, y0, x1, y1 = ln["bbox"]
            cy = (y0 + y1) / 2
            if any(r.x0 - 1 <= (x0 + x1) / 2 <= r.x1 + 1 and r.y0 - 1 <= cy <= r.y1 + 1 for r in skip_rects):
                continue
            raw.append({"spans": spans, "x0": x0, "x1": x1, "y": cy})
    raw.sort(key=lambda l: (l["y"], l["x0"]))
    merged = []
    for l in raw:
        if merged and abs(merged[-1]["y"] - l["y"]) < 2.2 and l["x0"] >= merged[-1]["x0"]:
            m = merged[-1]
            m["spans"] += l["spans"]
            m["x1"] = max(m["x1"], l["x1"])
        else:
            merged.append(l)
    out = []
    for l in merged:
        if x_range and not (x_range[0] <= l["x0"] < x_range[1]):
            continue
        spans = sorted(l["spans"], key=lambda s: s["bbox"][0])
        text = ""
        bold_chars = 0
        total = 0
        bullet = None
        first_text_x = None
        parts = []
        # peel leading bullet-only spans
        while len(spans) > 1 and re.fullmatch(r"[\s•○◦▪\x07\u2002]*", spans[0]["text"]):
            if any(c in spans[0]["text"] for c in "•○◦▪\x07") and bullet is None:
                bullet = 1 if l["x0"] < 42 else 2
            spans = spans[1:]
        for s in spans:
            st = clean(s["text"])
            bold = bool(s["flags"] & 16) or "Bold" in s["font"]
            if not parts:
                mb = re.match(r"^[\s•○◦▪\x07\u2002]*", s["text"])
                lead = mb.group(0)
                if any(c in lead for c in "•○◦▪\x07") or lead:
                    if any(c in lead for c in "•○◦▪\x07") and bullet is None:
                        bullet = 1 if l["x0"] < 42 else 2
                    st = clean(s["text"][len(lead):])
                    if not st.strip():
                        continue
            if not st.strip():
                parts.append((" ", False))
                continue
            if first_text_x is None:
                first_text_x = s["bbox"][0] + (len(st) - len(st.lstrip())) * 0
            parts.append((st, bold))
            n = len(st.strip())
            total += n
            if bold:
                bold_chars += n
        if not total:
            continue
        s = ""
        for st, bold in parts:
            s += f"**{st}**" if bold and st.strip() else st
        s = fix_text(s)
        plain = s.replace("**", "").strip()
        if re.fullmatch(r"(\d{1,3})\1?", plain) and l["y"] > 555:
            continue
        out.append({
            "x0": l["x0"], "x1": l["x1"], "y": l["y"], "text": s, "plain": plain,
            "bullet": bullet, "all_bold": bold_chars >= total - 1, "bold_frac": bold_chars / total,
            "tx": (l["x0"] + 11) if bullet else l["x0"],
        })
    return out


def first_word_width(line):
    w = line["plain"].split(" ")[0]
    font = "hebo" if line["all_bold"] or line["text"].startswith("**") else "helv"
    return fitz.get_text_length(w, fontname=font, fontsize=9)


def ended(prev, line, cur_type="p"):
    if prev is None:
        return True
    if cur_type == "callout" and line["x0"] < prev["x0"] - 3:
        return True
    if cur_type == "p":
        if prev["all_bold"] and not line["all_bold"]:
            return True
        if line["all_bold"] and prev["bold_frac"] < 0.3 and len(line["plain"]) < 80:
            return True
    gap = RIGHT_LIMIT - prev["x1"]
    if gap < first_word_width(line) + 4.5:
        return False
    # Forced line break mid-sentence: no terminal punctuation and lowercase continuation
    if not prev["all_bold"] and not re.search(r"[.!?:;)]\s*$", prev["plain"]):
        if line["plain"][:1].islower() or line["plain"][:1] in "($" or re.match(r"[A-Z]\b(?!\.)", line["plain"]):
            return False
    return True


def indent_level(x0):
    return 0 if x0 < 42 else (1 if x0 < 52 else 2)


class Assembler:
    def __init__(self):
        self.items = []
        self.cur = None
        self.prev = None

    def close(self):
        self.cur = None
        self.prev = None

    def start(self, typ, line, page, **kw):
        it = {"type": typ, "text": line["text"], "page": page, **kw}
        it["_x0"] = line["x0"]
        it["_tx"] = line["tx"]
        self.items.append(it)
        self.cur = it
        self.prev = line
        return it

    def join(self, it, line):
        a, b = it["text"], line["text"]
        if re.search(r"[A-Za-z]-$", a.replace("**", "")) and b[:1].islower():
            it["text"] = fix_text(a + b) if not a.endswith("**") else a + b
        else:
            it["text"] = fix_text(a + " " + b)
        self.prev = line

    def feed(self, line, page):
        m = CALLOUT_RE.match(line["text"])
        cur, prev = self.cur, self.prev
        if line["bullet"]:
            self.start("li", line, page, level=line["bullet"])
            return
        if m:
            kind = {"tip!": "tip", "important note:": "note", "note:": "note", "warning:": "warning",
                    "caution:": "warning"}[m.group(1).lower()]
            it = self.start("callout", line, page, kind=kind)
            it["text"] = fix_text(CALLOUT_RE.sub("", line["text"], 1))
            it["bold_chars"] = line["bold_frac"]
            return
        if cur is not None and not ended(prev, line, cur["type"]):
            if cur["type"] in ("li",):
                if line["x0"] >= cur["_x0"] - 1:
                    self.join(cur, line)
                    return
            elif cur["type"] == "callout":
                self.join(cur, line)
                return
            else:
                self.join(cur, line)
                return
        self.start("p", line, page, indent=indent_level(line["x0"]))


def card_items(page, pno):
    """Sign-card pages: one item group per PyMuPDF text block (title + description)."""
    d = page.get_text("dict")
    blocks = []
    for b in d["blocks"]:
        if b.get("type") != 0:
            continue
        rows = []
        for ln in b["lines"]:
            parts = []
            for sp in ln["spans"]:
                if sp["color"] == 0xFFFFFF:
                    continue
                st = clean(sp["text"])
                if not st.strip():
                    parts.append((" ", False))
                    continue
                parts.append((st, bool(sp["flags"] & 16) or "Bold" in sp["font"]))
            txt = "".join(f"**{t}**" if bd else t for t, bd in parts)
            plain = re.sub(r"\*\*", "", txt).strip()
            if not plain or (re.fullmatch(r"(\d{1,3})\1?", plain) and ln["bbox"][1] > 555):
                continue
            allb = all(bd for t, bd in parts if t.strip())
            rows.append((fix_text(txt), allb))
        if rows:
            blocks.append((b["bbox"], rows))
    blocks.sort(key=lambda t: (round(t[0][1] / 10), t[0][0]))
    out = []
    for bbox, rows in blocks:
        title = []
        while rows and rows[0][1]:
            title.append(rows.pop(0)[0])
        if title:
            out.append({"type": "h", "page": pno, "text": fix_text(" ".join(title)).replace("**", "")})
        if rows:
            out.append({"type": "p", "page": pno, "indent": 0, "text": fix_text(" ".join(r[0] for r in rows))})
    return out


def table_image(page, bbox, pno):
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    pix = page.get_pixmap(matrix=fitz.Matrix(3, 3), clip=fitz.Rect(bbox) + (-3, -3, 3, 3))
    name = f"table_p{pno:03d}_{int(bbox[1])}"
    try:
        from PIL import Image
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        img.save(TABLE_DIR / f"{name}.webp", quality=88)
        return f"assets/tables/{name}.webp"
    except Exception:
        pix.save(str(TABLE_DIR / f"{name}.png"))
        return f"assets/tables/{name}.png"


def process_pages(doc, pages):
    asm = Assembler()
    for pg in pages:
        pno = pg["page_number"]
        page = doc[pno - 1]
        tables = []
        try:
            tf = page.find_tables(strategy="lines_strict")
            for t in tf.tables:
                if len(t.rows) >= 2 and len(t.header.cells if t.header else []) >= 0 and t.col_count >= 2:
                    r = fitz.Rect(t.bbox)
                    if r.width > 150 and r.height > 30 and r.height < 520:
                        tables.append((r, t))
        except Exception:
            pass
        rects = [r for r, _ in tables]
        if pno == 47:
            hits = page.search_for("Sign Colors")
            if hits:
                reg = fitz.Rect(30, hits[0].y0 - 3, 350, 574)
                tables.append((reg, None))
                rects.append(reg)
        if pno in TWO_COL_PAGES:
            asm.close()
            asm.items += card_items(page, pno)
            continue
        streams = [page_lines(page, None, rects)]
        first_on_page = True
        for si, lines in enumerate(streams):
            events = [(l["y"], "line", l) for l in lines]
            if si == 0:
                for r, t in tables:
                    events.append((r.y0, "table", (r, t)))
            events.sort(key=lambda e: e[0])
            for _, kind, obj in events:
                if kind == "table":
                    r, t = obj
                    if t is None:
                        asm.close()
                        asm.items.append({"type": "table", "page": pno, "image": table_image(page, r, pno),
                                          "text": "Sign colors and sign shapes legend", "rows": []})
                        continue
                    rows = [[(c or "").replace("\n", " ").strip() for c in row] for row in t.extract()]
                    alt = " | ".join(" ".join(x for x in row if x) for row in rows)
                    asm.close()
                    asm.items.append({"type": "table", "page": pno, "image": table_image(page, r, pno),
                                      "text": fix_text(alt), "rows": rows})
                    continue
                asm.feed(obj, pno)
    items = asm.items
    # Post-process: headings
    for it in items:
        if it["type"] == "p":
            plain = it["text"].replace("**", "")
            if it["text"].startswith("**") and it["text"].endswith("**") and it["text"].count("**") == 2 and len(plain) <= 90:
                it["type"] = "h"
                it["text"] = plain
        if it["type"] == "callout":
            if it.pop("bold_chars", 0) > 0.5 or it["text"].startswith("**"):
                it["text"] = fix_text(it["text"].replace("**", ""))
        it["text"] = it["text"].strip()
        for k in ("_x0", "_tx"):
            it.pop(k, None)
    return items


def plain_text(items):
    out = []
    for it in items:
        t = it["text"].replace("**", "")
        if it["type"] == "li":
            out.append("• " + t)
        elif it["type"] == "callout":
            label = {"tip": "Tip! ", "note": "Note: ", "warning": "Warning: "}[it["kind"]]
            out.append(label + t)
        else:
            out.append(t)
    return "\n\n".join(out)


def main():
    gd = ROOT / "guide_data.json"
    dj = ROOT / "data.js"
    for f in (gd, dj):
        bak = f.with_suffix(f.suffix + ".bak")
        if not bak.exists():
            shutil.copy(f, bak)
    data = json.loads(gd.read_text())
    doc = fitz.open(PDF)
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for ch in data["chapters"]:
        if ch["id"] in SKIP_CHAPTERS:
            continue
        if only and ch["id"] != only:
            continue
        items = process_pages(doc, ch["pages"])
        ch["content"] = items
        ft = plain_text(items)
        ch["full_text"] = ft
        ch["word_count"] = len(ft.split())
        ch["read_minutes"] = max(1, round(ch["word_count"] / 200))
        print(ch["id"], len(items), "items", ch["word_count"], "words")
    if only and "--dry" in sys.argv:
        return
    gd.write_text(json.dumps(data, ensure_ascii=False, indent=1))
    dj.write_text("// Missouri Driver Guide Data Bundle (Offline & Client-side Ready)\nwindow.MISSOURI_GUIDE_DATA = " + json.dumps(data, ensure_ascii=False) + ";\n")


if __name__ == "__main__":
    main()
