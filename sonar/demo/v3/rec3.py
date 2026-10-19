"""Real-screen recording helpers: ffmpeg records the desktop, pyautogui moves the real cursor.

ffmpeg records WITHOUT the cursor (gdigrab draws the text cursor as a white box); instead the real cursor position
is sampled 30x/s into <clip>.cursor.json and drawn again, cleanly, in the montage.
Every action is written to <clip>.events.json with its time (seconds since recording start), so the montage knows
where to freeze, zoom and put notes.  `say(...)` marks where the voice explains something.
"""
import ctypes, json, subprocess, threading, time
from ctypes import wintypes
from pathlib import Path
import imageio_ffmpeg
import pyautogui

FF = imageio_ffmpeg.get_ffmpeg_exe()
pyautogui.FAILSAFE = True          # mouse to a screen corner = emergency stop
pyautogui.PAUSE = 0.05
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROFILE = r"C:\Users\juba839\dev\demo\chrome-ines"


class Clip:
    def __init__(self, path):
        self.path = Path(path)
        self.events, self.cursor = [], []
        self.t0 = None
        self._stop = threading.Event()

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.proc = subprocess.Popen(
            [FF, "-y", "-loglevel", "error", "-f", "gdigrab", "-framerate", "30", "-draw_mouse", "0",
             "-i", "desktop", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "16", "-pix_fmt", "yuv420p",
             str(self.path)], stdin=subprocess.PIPE)
        time.sleep(1.5)                # ffmpeg warm-up
        self.t0 = time.time()
        threading.Thread(target=self._sample, daemon=True).start()
        self.mark("start")
        return self

    def _sample(self):
        while not self._stop.is_set():
            x, y = pyautogui.position()
            self.cursor.append([round(time.time() - self.t0, 3), x, y])
            time.sleep(1 / 30)

    def __exit__(self, *exc):
        self.mark("end")
        time.sleep(1.0)
        self._stop.set()
        self.proc.stdin.write(b"q"); self.proc.stdin.flush()
        self.proc.wait(timeout=60)
        self.path.with_suffix(".events.json").write_text(json.dumps(self.events, indent=1))
        self.path.with_suffix(".cursor.json").write_text(json.dumps(self.cursor))

    def now(self):
        return round(time.time() - self.t0, 2) if self.t0 else 0

    def mark(self, ev_name, **info):
        self.events.append({"t": self.now(), "ev": ev_name, **info})

    def say(self, text, zoom=None, box=None, note=None, blur=None):
        """The voice says `text` here; the picture freezes on this frame as long as needed.
        zoom/box/blur = (x, y, w, h) in screen pixels; note = short on-screen text."""
        self.mark("say", text=text, zoom=zoom, box=box, note=note, blur=blur)
        time.sleep(0.4)

    def blur_on(self, name, box):
        """Blur screen area box=(x, y, w, h) from now until blur_off(name)."""
        self.mark("blur_on", name=name, box=list(box))

    def blur_off(self, name):
        self.mark("blur_off", name=name)

    def ff_on(self, speed=8):
        """In the montage, play from here at `speed` x (long downloads, waiting)."""
        self.mark("ff_on", speed=speed)

    def ff_off(self):
        self.mark("ff_off")

    def wait(self, s):
        time.sleep(s)

    def move(self, x, y, dur=0.9):
        pyautogui.moveTo(x, y, duration=dur, tween=pyautogui.easeInOutQuad)

    def click(self, x, y, dur=0.9, **info):
        self.move(x, y, dur)
        time.sleep(0.25)
        pyautogui.click()
        self.mark("click", x=x, y=y, **info)
        time.sleep(0.4)

    def click_on(self, name, dx=0, dy=0, dur=0.9, timeout=10):
        """Find the picture tpl/<name>.png on screen and click its centre (+dx, dy). Returns the centre."""
        x, y = find(name, timeout)
        self.click(x + dx, y + dy, dur, target=name)
        return x, y

    def scroll(self, clicks, x=None, y=None, step=1, delay=0.04):
        """Smooth scroll: `clicks` wheel notches (negative = down), sent one small notch at a time."""
        if x is not None:
            self.move(x, y, 0.6)
        n = abs(clicks)
        for _ in range(n // step):
            pyautogui.scroll(-120 * step if clicks < 0 else 120 * step)
            time.sleep(delay)

    def scroll_to(self, tpl, target_y=420, x=1100, y=700, max_notches=150):
        """Scroll down one notch at a time until tpl/<tpl>.png is at or above target_y. Returns its centre."""
        self.move(x, y, 0.5)
        for _ in range(max_notches):
            try:
                cx, cy = find(tpl, timeout=0)
                if cy <= target_y:
                    time.sleep(0.6)
                    return find(tpl, timeout=2)
            except RuntimeError:
                pass
            pyautogui.scroll(-40)
            time.sleep(0.2)
        raise RuntimeError(f"scroll_to: '{tpl}' not reached")

    def type(self, text, interval=0.05):
        self.mark("type", text=text)
        type_unicode(text, interval)

    def key(self, *keys):
        pyautogui.hotkey(*keys)
        self.mark("key", keys=list(keys))
        time.sleep(0.3)


def foreground_title():
    u = ctypes.windll.user32
    h = u.GetForegroundWindow()
    buf = ctypes.create_unicode_buffer(512)
    u.GetWindowTextW(h, buf, 512)
    return buf.value


def activate(part, maximize=True):
    """Bring the window whose title contains `part` to the front (maximized) and check it really is in front."""
    import pygetwindow as gw
    wins = [w for w in gw.getAllWindows() if part in w.title and (w.width > 200 or w.isMinimized)]
    if not wins:
        raise RuntimeError(f"no window with '{part}' in its title")
    w = wins[0]
    if w.isMinimized:
        w.restore()
    pyautogui.press("alt")
    try:
        w.activate()
    except Exception:
        pass
    time.sleep(0.6)
    if maximize and not w.isMaximized:
        w.maximize(); time.sleep(0.5)
    if part not in foreground_title():
        raise RuntimeError(f"'{part}' is not in front (front = '{foreground_title()}')")
    return w


def guard(part):
    """Stop if the window in front is not the expected one (never click into the wrong app)."""
    if part not in foreground_title():
        raise RuntimeError(f"expected '{part}' in front, found '{foreground_title()}'")


TPL = Path(r"C:\Users\juba839\dev\demo\rec\tpl")


def find(name, timeout=10, threshold=0.85):
    """Centre (x, y) of the template picture tpl/<name>.png on the real screen; waits until it appears."""
    import cv2, numpy as np
    from PIL import ImageGrab
    tpl = cv2.cvtColor(cv2.imread(str(TPL / f"{name}.png")), cv2.COLOR_BGR2GRAY)
    h, w = tpl.shape
    end = time.time() + timeout
    while True:
        scr = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2GRAY)
        res = cv2.matchTemplate(scr, tpl, cv2.TM_CCOEFF_NORMED)
        _, score, _, (x, y) = cv2.minMaxLoc(res)
        if score >= threshold:
            return x + w // 2, y + h // 2
        if time.time() > end:
            raise RuntimeError(f"'{name}' not found on screen (best score {score:.2f})")
        time.sleep(0.5)


# ---- layout-independent typing (works with AZERTY): SendInput KEYEVENTF_UNICODE ----
ULONG_PTR = ctypes.c_size_t
class KEYBDINPUT(ctypes.Structure):
    _fields_ = [("wVk", wintypes.WORD), ("wScan", wintypes.WORD), ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD), ("dwExtraInfo", ULONG_PTR)]
class _U(ctypes.Union):
    _fields_ = [("ki", KEYBDINPUT), ("pad", ctypes.c_byte * 32)]
class INPUT(ctypes.Structure):
    _fields_ = [("type", wintypes.DWORD), ("u", _U)]
KEYEVENTF_UNICODE, KEYEVENTF_KEYUP = 0x0004, 0x0002


def _send(scan, flags):
    i = INPUT(type=1)
    i.u.ki = KEYBDINPUT(0, scan, flags, 0, 0)
    ctypes.windll.user32.SendInput(1, ctypes.byref(i), ctypes.sizeof(INPUT))


def type_unicode(text, interval=0.05):
    for ch in text:
        if ch == "\n":
            pyautogui.press("enter")
        else:
            _send(ord(ch), KEYEVENTF_UNICODE)
            _send(ord(ch), KEYEVENTF_UNICODE | KEYEVENTF_KEYUP)
        time.sleep(interval)


def open_chrome(url=None):
    args = [CHROME, f"--user-data-dir={PROFILE}", "--no-first-run", "--no-default-browser-check",
            "--start-maximized", "--disable-features=Translate"]
    if url:
        args.append(url)
    return subprocess.Popen(args)
