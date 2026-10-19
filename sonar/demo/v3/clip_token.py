"""Put a saved demo token back on the clipboard (never prints it).  python clip_token.py token-web.txt"""
import subprocess, sys
from pathlib import Path

p = Path(r"C:\Users\juba839\dev\demo\assets") / sys.argv[1]
tok = p.read_text(encoding="ascii").strip()
subprocess.run(["clip"], input=tok.encode("ascii"), check=True)
back = subprocess.run(["powershell", "-c", "Get-Clipboard"], capture_output=True, text=True).stdout.strip()
print("clipboard holds the token:", back == tok, "| starts with sqp_:", tok.startswith("sqp_"))
