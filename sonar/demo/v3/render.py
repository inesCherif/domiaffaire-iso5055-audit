"""Render chapters: montage every part, then join the parts into one video per chapter.

python render.py 1 2 3      (chapter numbers; default: all known)
Output: presentation/sonarqube/v3/chN-<slug>.mp4
"""
import subprocess, sys
from pathlib import Path
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
HERE = Path(__file__).resolve().parent
REC = Path(r"C:\Users\juba839\dev\demo\rec")
OUT = HERE.parents[2] / "presentation" / "sonarqube" / "v3"

CHAPTERS = {
    1: ("get-sonarqube", "Chapter 1 · Get SonarQube", ["ch1"]),
    2: ("docker-compose-file", "Chapter 2 · Write docker-compose.yml", ["ch2"]),
    3: ("start-sonarqube", "Chapter 3 · Start SonarQube in Docker", ["ch3a", "ch3a2", "ch3a3", "ch3b"]),
    4: ("first-login", "Chapter 4 · First login", ["ch4a", "ch4b", "ch4b2", "ch4c"]),
    5: ("analyze-web-client", "Chapter 5 · Analyze a TypeScript project",
        ["ch5a", "ch5b", "ch5c", "ch5d", "ch5e", "ch5f", "ch5g", "ch5g2", "ch5h"]),
    6: ("analyze-java-maven", "Chapter 6 · Analyze a Java project with Maven", ["ch6a", "ch6b", "ch6c", "ch6d", "ch6e", "ch6f"]),
    7: ("read-results", "Chapter 7 · Read the results", ["ch7a", "ch7b", "ch7c", "ch7d", "ch7e", "ch7f", "ch7g"]),
    8: ("iso-5055", "Chapter 8 · ISO/IEC 5055 with SonarQube", ["ch8a", "ch8b", "ch8c"]),
    9: ("whole-project", "Chapter 9 · The whole project in one analysis", ["ch9a", "ch9b", "ch9c"]),
    10: ("clean-up", "Chapter 10 · Clean up", ["ch10a", "ch10b", "ch10b2", "ch10c"]),
}


def join_all():
    files = [OUT / f"ch{n}-{CHAPTERS[n][0]}.mp4" for n in CHAPTERS]
    lst = REC / "all-concat.txt"
    lst.write_text("".join(f"file '{f.as_posix()}'\n" for f in files if f.exists()))
    final = OUT / "sonarqube-beginner-tutorial.mp4"
    subprocess.run([FF, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy",
                    str(final)], check=True)
    print("OK", final, flush=True)


def render(n):
    slug, title, parts = CHAPTERS[n]
    OUT.mkdir(parents=True, exist_ok=True)
    done = []
    for i, p in enumerate(parts):
        dst = REC / f"{p}-final.mp4"
        if dst.exists() and dst.stat().st_mtime > (REC / f"{p}.events.json").stat().st_mtime:
            done.append(dst); continue
        args = [sys.executable, str(HERE / "montage.py"), str(REC / f"{p}.mp4"), str(dst)]
        if i == 0:
            args += ["--title", title]
        print("render", p, flush=True)
        for attempt in range(3):              # the voice model sometimes fails to load when memory is short
            r = subprocess.run(args, env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"})
            if r.returncode == 0 and dst.exists():
                break
            print("retry", p, flush=True)
        else:
            raise RuntimeError(f"montage failed for {p}")
        done.append(dst)
    final = OUT / f"ch{n}-{slug}.mp4"
    lst = REC / f"ch{n}-concat.txt"
    lst.write_text("".join(f"file '{d.as_posix()}'\n" for d in done))
    subprocess.run([FF, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy",
                    str(final)], check=True)
    print("OK", final, flush=True)


if __name__ == "__main__":
    for n in (map(int, sys.argv[1:]) if sys.argv[1:] else CHAPTERS):
        render(n)
    join_all()
