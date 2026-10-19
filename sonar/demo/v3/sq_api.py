"""Small helper: GET a SonarQube Web API path as admin (password read from the local file, never printed)."""
import base64, json, sys, urllib.request
from pathlib import Path
PW = Path(r"C:\Users\juba839\dev\demo\assets\sonar-admin.txt").read_text().strip()


def get(path):
    req = urllib.request.Request("http://localhost:9000" + path)
    req.add_header("Authorization", "Basic " + base64.b64encode(f"admin:{PW}".encode()).decode())
    return json.load(urllib.request.urlopen(req))


if __name__ == "__main__":
    print(json.dumps(get(sys.argv[1]), indent=1)[:6000])
