"""Screenshot of the real screen (full size + half size for viewing). python shot.py <name>"""
import subprocess, sys
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
name = sys.argv[1] if len(sys.argv) > 1 else "now"
out = rf"C:\Users\juba839\dev\demo\rec\shots\{name}.png"
import os; os.makedirs(os.path.dirname(out), exist_ok=True)
subprocess.run([FF, "-loglevel", "error", "-y", "-f", "gdigrab", "-i", "desktop", "-frames:v", "1", out], check=True)
print(out)
