"""Chapter 3: start SonarQube with docker compose (terminal in Antigravity), then see it in Docker Desktop.

python ch3.py a   -> part A: terminal + Docker Desktop containers list
python ch3.py b   -> part B: the sonarqube container logs until 'SonarQube is operational'
"""
import subprocess, sys, time
import pyautogui
from rec3 import Clip, find, activate, guard

R = r"C:\Users\juba839\dev\demo\rec"


def docker(*args):
    return subprocess.run(["docker", *args], capture_output=True, text=True).stdout


def wait_up(timeout=1500):
    """Wait until both containers exist, postgresql is healthy and sonarqube is running."""
    end = time.time() + timeout
    while time.time() < end:
        st = docker("ps", "--format", "{{.Names}} {{.Status}}")
        if "postgresql" in st and "healthy" in st and "sonarqube Up" in st:
            return
        time.sleep(3)
    raise RuntimeError("containers did not start: " + st)


def part_a():
    activate("sonarqube - Antigravity")
    with Clip(R + r"\ch3a.mp4") as c:
        c.wait(1)
        x, y = find("dd_icon")
        c.say("Chapter three: we start SonarQube. Before anything, Docker Desktop must be running on your computer. "
              "You can see its whale icon here, in the taskbar.", box=(x - 22, y - 22, 44, 44))
        c.say("We open a terminal inside the editor. Click the Terminal menu, then New Terminal.",
              box=(366, 8, 74, 28))
        c.click(403, 22)
        c.wait(0.8)
        guard("sonarqube - Antigravity")
        c.click(450, 57)
        c.wait(6)
        c.say("A PowerShell terminal opens at the bottom. Look at the path: we are already in our sonarqube folder, "
              "next to our file. This matters, because docker compose reads the file in the current folder.",
              box=(460, 660, 330, 30), note="PS C:\\Users\\...\\sonarqube>")
        c.say("To see better, we make the terminal bigger with this button.", box=(1843, 582, 30, 30))
        c.click(1858, 597)
        c.wait(1.5)
        c.click(1100, 600)
        c.type("docker compose up -d", 0.09)
        c.wait(0.5)
        c.say("Type: docker compose up dash d. Docker compose reads our file. Up means: create and start everything "
              "that the file describes. Dash d means detached: the containers keep running in the background, "
              "and we get our terminal back. Press Enter.",
              zoom=(430, 50, 900, 160), note="docker compose up -d")
        c.key("enter")
        c.wait(4)
        c.say("The first time, Docker downloads the SonarQube image from Docker Hub. It is big, several hundred megabytes, "
              "so it can take a few minutes, depending on your internet. We speed up the video here. "
              "PostgreSQL was already on my computer, so Docker does not download it again.",
              note="First time only: download")
        c.ff_on(16)
        wait_up()
        c.wait(4)
        c.ff_off()
        rest(c)


def part_a2():
    """Continuation (the first clip stopped during the download): fast-forward, then the rest of part A."""
    guard("sonarqube - Antigravity")
    with Clip(R + r"\ch3a2.mp4") as c:
        c.ff_on(16)
        wait_up()
        c.wait(4)
        c.ff_off()
        rest(c)


def part_a3():
    guard("sonarqube - Antigravity")
    with Clip(R + r"\ch3a3.mp4") as c:
        c.wait(1)
        rest(c)


def part_b():
    guard("Docker Desktop")
    with Clip(R + r"\ch3b.mp4") as c:
        c.wait(1)
        c.click(590, 665)
        c.wait(3)
        c.say("Click on the sonarqube container. Docker Desktop opens its page. At the top, you see its image, "
              "its port link nine thousand, and its status: Running. The first tab, Logs, shows everything SonarQube "
              "writes while it starts.", box=(360, 160, 1530, 90))
        c.move(1100, 700)
        x, y = find("operational", 15)
        c.say("SonarQube starts three parts: the search engine, the web server, and the compute engine. "
              "We wait for one sentence: SonarQube is operational. Here it is. It means SonarQube is ready to use.",
              zoom=(340, y - 160, 1100, 300), box=(x - 120, y - 13, 240, 26), note="SonarQube is operational = ready")
        c.say("If you see an error here instead, the most common reason is a lack of memory: close other big programs, "
              "and keep the three memory lines of our file. "
              "Our SonarQube is running. In the next chapter, we open it in the browser and log in for the first time.")
        c.wait(1)


def rest(c):
    if True:
        c.say("Done. Docker created a network, the volumes for our data, and the two containers. "
              "First postgresql becomes Healthy, which means the database is ready, and then sonarqube is Started.",
              zoom=(430, 50, 1100, 520))
        c.click(1100, 700)
        c.type("docker compose ps", 0.09)
        c.key("enter")
        c.wait(3)
        c.say("To check, type docker compose p s. It lists our two containers, their image, their status, Up, and their ports. "
              "Look at sonarqube: port nine thousand of the computer goes to port nine thousand of the container.",
              zoom=(430, 50, 1460, 700), note="STATUS = Up · PORTS = 9000->9000")
        x, y = find("dd_icon")
        c.click(x, y)
        c.wait(3)
        guard("Docker Desktop")
        c.say("We can see the same thing in Docker Desktop. Open it from the taskbar: we are on the Containers page.")
        c.say("There is a new line called sonarqube. It is the name of our folder: Docker compose uses it as the "
              "project name. Click the small arrow to open it.", box=(360, 540, 1510, 50))
        c.click(437, 565)
        c.wait(2)
        c.say("Inside, we find our two containers: postgresql, the database, and sonarqube. "
              "On the sonarqube line, the port nine thousand colon nine thousand is a link that opens it in the browser. "
              "But SonarQube needs one or two minutes to start completely. Let's look at its logs.",
              box=(360, 540, 1510, 150))
        c.wait(1)


if __name__ == "__main__":
    {"a": part_a, "a2": part_a2, "a3": part_a3, "b": part_b}[sys.argv[1]]()
