"""Montage of one real-screen clip: voice (Kokoro af_heart), freeze frames, zoom, highlight box, notes, subtitles,
clean cursor + click ripples, blur.

python montage.py <clip.mp4> <out.mp4> [--title "Chapter 1 - Get SonarQube"]

Reads <clip>.events.json and <clip>.cursor.json written by rec3.Clip.
At every `say` event the picture freezes, the voice speaks, overlays appear; then the real action continues.
"""
import argparse, json, re, subprocess, sys, wave
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "v2"))
import tts  # noqa: E402  (Kokoro wrapper from session 3)
import imageio_ffmpeg  # noqa: E402

FF = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS, SR = 1920, 1080, 30, 24000
ACCENT = (255, 138, 0)                       # orange (RGB)
F_SUB = ImageFont.truetype(r"C:\Windows\Fonts\segoeuisl.ttf" if Path(r"C:\Windows\Fonts\segoeuisl.ttf").exists()
                           else r"C:\Windows\Fonts\segoeui.ttf", 40)
F_NOTE = ImageFont.truetype(r"C:\Windows\Fonts\seguisb.ttf", 38)
F_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\seguisb.ttf", 46)
tts.SAY.update({"yml": "Y M L", "docker-compose": "docker compose", "GitHub": "Git Hub", "s q with postgres": "S Q with postgres",
                "SonarSource": "Sonar Source", "Antigravity": "Anti gravity", "localhost": "local host"})
ZOOM_IN = 0.6                                # seconds of zoom animation


def ease(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


# ---------- overlay pictures (RGBA numpy, drawn once) ----------
def rgba(w, h):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))


def wrap(text, font, maxw):
    lines = []
    for para in text.split("\n"):
        cur = ""
        for word in para.split():
            t = (cur + " " + word).strip()
            if font.getlength(t) <= maxw:
                cur = t
            else:
                lines.append(cur); cur = word
        lines.append(cur)
    return lines


def subtitle_img(text):
    lines = wrap(text, F_SUB, 1640)
    lh = 52
    h = lh * len(lines) + 28
    im = rgba(W, h)
    d = ImageDraw.Draw(im)
    wmax = max(F_SUB.getlength(l) for l in lines)
    x0 = (W - wmax) / 2 - 28
    d.rounded_rectangle((x0, 0, W - x0, h), 14, fill=(10, 10, 14, 215))
    for i, l in enumerate(lines):
        d.text((W / 2, 14 + i * lh + lh / 2), l, font=F_SUB, fill=(255, 255, 255, 255), anchor="mm")
    return np.array(im)


def note_img(text):
    lines = wrap(text, F_NOTE, 760)
    lh = 50
    wmax = max(F_NOTE.getlength(l) for l in lines)
    w, h = int(wmax + 64), lh * len(lines) + 34
    im = rgba(w + 8, h + 8)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((6, 6, w + 6, h + 6), 16, fill=(0, 0, 0, 110))           # shadow
    d.rounded_rectangle((0, 0, w, h), 16, fill=(255, 250, 235, 250))
    d.rounded_rectangle((0, 0, 12, h), 6, fill=ACCENT + (255,))
    for i, l in enumerate(lines):
        d.text((36, 17 + i * lh + lh / 2), l, font=F_NOTE, fill=(25, 25, 30, 255), anchor="lm")
    return np.array(im)


def title_img(text):
    w = int(F_TITLE.getlength(text) + 80)
    im = rgba(w, 92)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, 92), 18, fill=(15, 15, 20, 230))
    d.rounded_rectangle((0, 0, 14, 92), 7, fill=ACCENT + (255,))
    d.text((44, 46), text, font=F_TITLE, fill=(255, 255, 255, 255), anchor="lm")
    return np.array(im)


_badges = {}


def ff_badge(sp):
    if sp not in _badges:
        txt = f"▶▶  x{sp}"
        im = rgba(220, 76)
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 0, 220, 76), 16, fill=(15, 15, 20, 220))
        d.text((110, 38), txt, font=F_TITLE, fill=ACCENT + (255,), anchor="mm")
        _badges[sp] = np.array(im)
    return _badges[sp]


def cursor_img(scale=1.25):
    s = scale * 1.6
    pts = [(0, 0), (0, 17), (4, 13), (7, 20), (10, 19), (7, 12), (12, 12)]
    pts = [(2 + x * s, 2 + y * s) for x, y in pts]
    im = rgba(int(16 * s) + 6, int(23 * s) + 6)
    d = ImageDraw.Draw(im)
    d.polygon(pts, fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=2)
    return np.array(im)


CURSOR = cursor_img()


def blend(frame, img, x, y, alpha=1.0):
    """Alpha-blend RGBA img onto RGB frame at (x, y), clipped to the frame."""
    h, w = img.shape[:2]
    x, y = int(x), int(y)
    x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, W), min(y + h, H)
    if x0 >= x1 or y0 >= y1:
        return
    sub = img[y0 - y:y1 - y, x0 - x:x1 - x]
    a = sub[:, :, 3:4].astype(np.float32) / 255 * alpha
    reg = frame[y0:y1, x0:x1].astype(np.float32)
    frame[y0:y1, x0:x1] = (reg * (1 - a) + sub[:, :, :3] * a).astype(np.uint8)


# ---------- geometry ----------
def fit169(box, margin=0.12):
    x, y, w, h = box
    cx, cy = x + w / 2, y + h / 2
    w, h = w * (1 + 2 * margin), h * (1 + 2 * margin)
    if w / h < W / H:
        w = h * W / H
    else:
        h = w * H / W
    w, h = min(w, W), min(h, H)
    x = min(max(cx - w / 2, 0), W - w)
    y = min(max(cy - h / 2, 0), H - h)
    return x, y, w, h


def lerp_rect(a, b, u):
    return tuple(a[i] + (b[i] - a[i]) * u for i in range(4))


def apply_view(frame, view):
    """view = (x, y, w, h) crop of the screen shown full size."""
    x, y, w, h = view
    if w >= W - 1:
        return frame
    m = np.float32([[W / w, 0, -x * W / w], [0, H / h, -y * H / h]])
    return cv2.warpAffine(frame, m, (W, H), flags=cv2.INTER_CUBIC)


def to_view(pt, view):
    x, y, w, h = view
    return (pt[0] - x) * W / w, (pt[1] - y) * H / h


# ---------- audio ----------
def synth_all(events, workdir):
    workdir.mkdir(parents=True, exist_ok=True)
    out = []
    for i, e in enumerate(events):
        if e["ev"] != "say":
            continue
        wav = workdir / f"say{i:02d}.wav"
        key = workdir / f"say{i:02d}.txt"
        if not (wav.exists() and key.exists() and key.read_text(encoding="utf-8") == e["text"]):
            tts.synth(e["text"], wav)
            key.write_text(e["text"], encoding="utf-8")
        with wave.open(str(wav)) as w:
            data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16 if w.getsampwidth() == 2 else np.int32)
            if w.getsampwidth() == 4:
                data = (data / 65536).astype(np.int16)
        out.append((i, data))
    return dict(out)


def read_wav_any(path):
    import soundfile as sf
    d, sr = sf.read(str(path), dtype="float32")
    return d


def chunks(text, dur):
    """Split narration into subtitle pieces with times proportional to length."""
    parts = []
    for s in re.split(r"(?<=[.!?:])\s+", text.strip()):
        while len(s) > 95:
            cut = s.rfind(",", 0, 95)
            cut = cut if cut > 30 else s.rfind(" ", 0, 90)
            parts.append(s[:cut + 1].strip()); s = s[cut + 1:].strip()
        if s:
            parts.append(s)
    total = sum(len(p) for p in parts)
    t, res = 0.0, []
    for p in parts:
        d = dur * len(p) / total
        res.append((t, t + d, p)); t += d
    return res


# ---------- main ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clip"); ap.add_argument("out"); ap.add_argument("--title", default="")
    ap.add_argument("--blur", default="", help="json file: list of {t0,t1,box:[x,y,w,h]} in clip time (live parts)")
    a = ap.parse_args()
    clip = Path(a.clip)
    events = json.loads(clip.with_suffix(".events.json").read_text())
    cur = np.array(json.loads(clip.with_suffix(".cursor.json").read_text()))
    blurs = json.loads(Path(a.blur).read_text()) if a.blur else []
    t_last = events[-1]["t"] + 5
    for e in events:                              # blur_on / blur_off markers from the recording
        if e["ev"] == "blur_on":
            off = next((f["t"] for f in events if f["ev"] == "blur_off" and f.get("name") == e["name"]
                        and f["t"] >= e["t"]), t_last)
            blurs.append({"t0": e["t"] - 0.2, "t1": off + 0.2, "box": e["box"]})
    work = clip.parent / (clip.stem + "_work")
    work.mkdir(exist_ok=True)
    import soundfile as sf
    voices = {}
    for i, e in enumerate(events):
        if e["ev"] == "say":
            wav = work / f"say{i:02d}.wav"; key = work / f"say{i:02d}.txt"
            work.mkdir(exist_ok=True)
            if not (wav.exists() and key.exists() and key.read_text(encoding="utf-8") == e["text"]):
                tts.synth(e["text"], wav); key.write_text(e["text"], encoding="utf-8")
            voices[i], sr = sf.read(str(wav), dtype="float32")
            assert sr == SR, sr
    clicks = [e for e in events if e["ev"] == "click"]
    says = [(i, e) for i, e in enumerate(events) if e["ev"] == "say"]
    t_end = next(e["t"] for e in events if e["ev"] == "end") + 0.8

    def cursor_at(t):
        k = np.searchsorted(cur[:, 0], t)
        k = min(max(k, 0), len(cur) - 1)
        return cur[k, 1], cur[k, 2]

    # Build the output plan: list of (kind, ...) pieces
    plan, t_prev = [], 0.0
    for i, e in says:
        plan.append(("live", t_prev, e["t"]))
        plan.append(("freeze", e["t"], i, len(voices[i]) / SR + 0.7))
        t_prev = e["t"]
    plan.append(("live", t_prev, t_end))

    # gdigrab delivers ~27-28 fps with real timestamps and starts ~1.5 s before t0 (warm-up):
    # resample to exact 30 fps and shift by the measured offset (video length - recorded event span).
    probe = subprocess.run([FF, "-i", str(clip)], capture_output=True, text=True).stderr
    hh, mm, ss = re.search(r"Duration: (\d+):(\d+):([\d.]+)", probe).groups()
    vdur = int(hh) * 3600 + int(mm) * 60 + float(ss)
    off = max(0.0, vdur - (t_end - 0.8 + 1.0))
    print(f"video {vdur:.2f}s, offset {off:.2f}s")
    dec = subprocess.Popen([FF, "-loglevel", "error", "-i", str(clip), "-vf", "fps=30", "-f", "rawvideo",
                            "-pix_fmt", "rgb24", "-"],
                           stdout=subprocess.PIPE)
    tmp_v = work / "video.mp4"
    enc = subprocess.Popen([FF, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
                            "-pix_fmt", "yuv420p", str(tmp_v)], stdin=subprocess.PIPE)
    src_i, last = -1, None

    def read_until(t):
        nonlocal src_i, last
        want = int(round((t + off) * FPS))
        while src_i < want:
            buf = dec.stdout.read(W * H * 3)
            if len(buf) < W * H * 3:
                break
            last = np.frombuffer(buf, np.uint8).reshape(H, W, 3).copy(); src_i += 1
        return last

    title = title_img(a.title) if a.title else None
    ffs = []                                      # fast-forward spans: ff_on(speed) ... ff_off
    for e in events:
        if e["ev"] == "ff_on":
            t1 = next((f["t"] for f in events if f["ev"] == "ff_off" and f["t"] >= e["t"]), t_end)
            ffs.append((e["t"], t1, e.get("speed", 8)))

    def speed_at(t):
        return next((sp for a0, a1, sp in ffs if a0 <= t < a1), 1)
    audio, out_t = [], 0.0                       # (start time in output, samples)
    FULL = (0, 0, W, H)

    def draw_common(fr, t_src, view, out_now):
        for b in blurs:
            if b["t0"] <= t_src <= b["t1"]:
                x, y, w, h = map(int, b["box"])
                fr[y:y + h, x:x + w] = cv2.GaussianBlur(fr[y:y + h, x:x + w], (0, 0), 18)
        return fr

    def finish(fr, t_src, view, out_now, extra=None):
        fr = apply_view(fr, view)
        if extra:
            extra(fr)
        cx, cy = to_view(cursor_at(t_src), view)
        for c in clicks:                          # click ripple
            dt = t_src - c["t"]
            if 0 <= dt < 0.45:
                px, py = to_view((c["x"], c["y"]), view)
                r = int(14 + 50 * dt / 0.45)
                ov = fr.copy()
                cv2.circle(ov, (int(px), int(py)), r, ACCENT, 5, cv2.LINE_AA)
                al = 1 - dt / 0.45
                fr[:] = cv2.addWeighted(ov, al, fr, 1 - al, 0)
        blend(fr, CURSOR, cx - 2, cy - 2)
        if title is not None and out_now < 5:
            al = min(1, out_now / 0.4, (5 - out_now) / 0.5)
            blend(fr, title, 60, H - 330, al)
        enc.stdin.write(fr.tobytes())

    for piece in plan:
        if piece[0] == "live":
            _, t0, t1 = piece
            t = t0
            while t < t1 - 1e-6:
                sp = speed_at(t)
                fr = draw_common(read_until(t).copy(), t, FULL, out_t)
                if sp > 1:
                    blend(fr, ff_badge(sp), W - 260, 40)
                finish(fr, t, FULL, out_t); out_t += 1 / FPS
                t += sp / FPS
        else:
            _, t, i, dur = piece
            e = events[i]
            base = draw_common(read_until(t).copy(), t, FULL, out_t)
            if e.get("blur"):
                x, y, w, h = map(int, e["blur"])
                base[y:y + h, x:x + w] = cv2.GaussianBlur(base[y:y + h, x:x + w], (0, 0), 18)
            target = fit169(e["zoom"]) if e.get("zoom") else FULL
            voice = voices[i]
            audio.append((out_t + 0.25, voice))
            subs = [(s0 + 0.25, s1 + 0.25, subtitle_img(txt)) for s0, s1, txt in chunks(e["text"], len(voice) / SR)]
            note = note_img(e["note"]) if e.get("note") else None
            n = int(round(dur * FPS))
            for k in range(n):
                u = k / FPS
                zin = ease(u / ZOOM_IN) if e.get("zoom") else 0
                zout = ease((u - (dur - ZOOM_IN)) / ZOOM_IN) if e.get("zoom") else 0
                view = lerp_rect(lerp_rect(FULL, target, zin), FULL, zout)
                fade = min(1, u / 0.3, max(0, (dur - u) / 0.3))

                def extra(fr, view=view, u=u, fade=fade):
                    if e.get("box"):
                        x, y, w, h = e["box"]
                        p0 = to_view((x - 8, y - 8), view); p1 = to_view((x + w + 8, y + h + 8), view)
                        if not e.get("zoom"):         # spotlight: dim the rest of the screen
                            dim = fr.copy(); dim[:] = (dim * 0.55).astype(np.uint8)
                            x0, y0 = max(int(p0[0]), 0), max(int(p0[1]), 0)
                            dim[y0:int(p1[1]), x0:int(p1[0])] = fr[y0:int(p1[1]), x0:int(p1[0])]
                            fr[:] = cv2.addWeighted(dim, fade, fr, 1 - fade, 0)
                        ov = fr.copy()
                        cv2.rectangle(ov, (int(p0[0]), int(p0[1])), (int(p1[0]), int(p1[1])), ACCENT, 6, cv2.LINE_AA)
                        fr[:] = cv2.addWeighted(ov, fade, fr, 1 - fade, 0)
                    if note is not None:
                        nh, nw = note.shape[:2]
                        if e.get("box"):
                            x, y, w, h = e["box"]
                            p1 = to_view((x + w, y + h + 8), view); p0 = to_view((x, y - 8), view)
                            ny = p1[1] + 18 if p1[1] + 18 + nh < H - 190 else p0[1] - 18 - nh
                            nx = min(max(p0[0], 30), W - nw - 30)
                        else:
                            nx, ny = W - nw - 60, 150
                        blend(fr, note, nx, max(ny, 20), fade)
                    for s0, s1, img in subs:
                        if s0 <= u < s1 + 0.15:
                            blend(fr, img, 0, H - img.shape[0] - 70)
                            break
                finish(base.copy(), t, view, out_t, extra); out_t += 1 / FPS
    enc.stdin.close(); enc.wait(); dec.kill()

    # audio track
    total = int(out_t * SR) + SR
    track = np.zeros(total, np.float32)
    for st, v in audio:
        s = int(st * SR); track[s:s + len(v)] += v[:max(0, total - s)]
    wav = work / "voice.wav"
    sf.write(str(wav), track, SR)
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", str(tmp_v), "-i", str(wav), "-c:v", "copy", "-c:a", "aac",
                    "-b:a", "160k", "-shortest", a.out], check=True)
    print(f"{a.out}: {out_t:.1f}s")


if __name__ == "__main__":
    main()
