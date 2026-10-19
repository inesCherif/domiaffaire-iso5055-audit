"""Chapter 2: create the sonarqube folder and docker-compose.yml in Antigravity, explain every block, add memory lines.

python ch2.py prep   -> Antigravity welcome window in front, Agent panel closed, clipboard = official compose file
python ch2.py        -> record
"""
import subprocess, sys, time
import pyautogui
from rec3 import Clip, type_unicode, find, activate, guard, foreground_title

OUT = r"C:\Users\juba839\dev\demo\rec\ch2.mp4"
AG = r"C:\Users\juba839\AppData\Local\Programs\Antigravity IDE\bin\antigravity-ide.cmd"
COMPOSE = r"C:\Users\juba839\dev\demo\assets\official-compose.yml"


def close_agent_panel():
    try:
        find("agent_hdr", timeout=3)
        pyautogui.click(1891, 66); time.sleep(0.8)
    except RuntimeError:
        pass


def L(n):
    """Screen y of line n in the top view of the pasted file (with the 'Run Service' hints)."""
    if n == 1:
        return 140
    if n == 2:
        return 184
    if n <= 24:
        return 208 + (n - 3) * 23.8
    return 750 + (n - 25) * 23.8


def S(n):
    """Screen y of line n after scrolling down 6 notches."""
    return 375 + (n - 25) * 23.85


def lines_box(y0, y1, x=505, w=820):
    return (x, int(y0 - 14), w, int(y1 - y0 + 28))


def prep():
    subprocess.run(["powershell", "-c", f"Get-Content -Raw '{COMPOSE}' | Set-Clipboard"], check=True)
    import pygetwindow as gw
    for w in gw.getAllWindows():                  # only Antigravity on screen
        if "Google Chrome" in w.title:
            w.minimize()
    if not any(w.title.strip() == "Antigravity IDE" for w in gw.getAllWindows()):
        subprocess.Popen(["cmd", "/c", AG, "--new-window"], creationflags=0x08000000)
        time.sleep(20)
    for w in gw.getAllWindows():                  # close restored test windows, without saving
        if "Antigravity IDE" in w.title and w.title.strip() != "Antigravity IDE":
            activate(w.title)
            pyautogui.hotkey("ctrl", "shift", "w"); time.sleep(1.5)
            if "Antigravity" in foreground_title():
                try:
                    pyautogui.click(*find("dont_save", 3))
                except RuntimeError:
                    pass
    activate("Antigravity IDE")
    close_agent_panel()
    guard("Antigravity IDE")
    pyautogui.hotkey("ctrl", "shift", "p"); time.sleep(0.8)
    guard("Antigravity IDE")
    type_unicode("Notifications: Clear All", 0.01); time.sleep(0.8); pyautogui.press("enter"); time.sleep(0.8)
    pyautogui.moveTo(1300, 600)
    print("front:", foreground_title())


def record():
    guard("Antigravity IDE")
    with Clip(OUT) as c:
        c.blur_on("recent", (750, 450, 475, 330))          # my recent workspaces list
        c.wait(1)
        c.say("Chapter two. Now we create the configuration file on our own computer. You can use any code editor: "
              "VS Code, Notepad plus plus, or even the Windows Notepad. Here I use Antigravity. "
              "First, we make an empty folder that will hold our SonarQube setup. Click Open Folder.",
              box=(756, 285, 460, 55), note="Any editor works: VS Code, Notepad++, Notepad")
        c.click(985, 313)
        c.wait(2.5)
        guard("Open Folder")
        c.blur_off("recent")
        c.say("A window opens on your user folder. At the top, click New folder.", box=(123, 106, 108, 32))
        c.click(178, 122)
        c.wait(1.2)
        c.type("sonarqube", 0.12)
        c.wait(0.6)
        c.say("We call the folder sonarqube, in small letters, and we press Enter.")
        c.key("enter")
        c.wait(1)
        c.say("The folder is created and selected. Now click Select folder, to open it in the editor.",
              box=(674, 538, 130, 32))
        c.click(738, 553)
        c.wait(4)
        guard("sonarqube - Antigravity")
        x, y = find("trust_yes", 10)
        c.say("The editor asks if we trust the files in this folder. This is our own new folder, and it is empty, "
              "so it is safe: click Yes, I trust the authors.", box=(x - 130, y - 18, 260, 36))
        c.click(x, y)
        c.wait(2)
        try:
            find("agent_hdr", timeout=3)
            c.say("We do not need the AI agent panel on the right, so we close it.", box=(1876, 51, 30, 30))
            c.click(1891, 66)
        except RuntimeError:
            pass
        c.wait(1)
        c.say("Our folder sonarqube is open, on the left, and it is empty. Now we create the file. "
              "Right-click in the empty area, and choose New File.", box=(55, 90, 370, 26))
        c.move(200, 400)
        pyautogui.rightClick(); c.mark("click", x=200, y=400); c.wait(1.2)
        c.click(273, 425)
        c.wait(1)
        c.type("docker-compose.yml", 0.08)
        c.say("Type the name exactly: docker-compose dot yml. Docker compose looks for this name. Then press Enter.",
              box=(55, 115, 370, 28), note="docker-compose.yml")
        c.key("enter")
        c.wait(2)
        c.say("The empty file is open. Now paste the file we copied from GitHub, with Control and V.")
        c.key("ctrl", "v")
        c.wait(1)
        c.key("ctrl", "home")
        c.wait(4)
        c.move(1400, 600)
        # ---- explain the sonarqube service ----
        c.say("Let's read it together, block by block. Under services, there are two containers. "
              "The first one is called sonarqube. Its image is sonarqube colon community: this is the free Community "
              "Build, and Docker downloads it automatically from Docker Hub.",
              zoom=lines_box(L(1), L(3)), box=lines_box(L(1), L(3)))
        c.say("Hostname and container name give the container a fixed name, sonarqube, that we will see in Docker Desktop. "
              "Read only true makes the files of the container read-only, which is safer.",
              zoom=lines_box(L(4), L(6)), box=lines_box(L(4), L(6)))
        c.say("Depends on, d b, condition service healthy: SonarQube waits until the database is really ready before it starts.",
              zoom=lines_box(L(7), L(9)), box=lines_box(L(7), L(9)))
        c.say("Environment gives SonarQube the address of its database, with a user name and a password. "
              "Here both are just sonar. They are only used between the two containers, inside Docker. "
              "On a real shared server, you would choose a strong password.",
              zoom=lines_box(L(10), L(13)), box=lines_box(L(10), L(13)), note="Database address + login")
        c.say("Volumes are folders that Docker keeps outside the container. SonarQube stores its data, its plugins "
              "and its logs there, so nothing is lost when you stop or update the container.",
              zoom=lines_box(L(14), L(18)), box=lines_box(L(14), L(18)), note="Volumes = your data survives restarts")
        c.say("T m p f s is a small temporary folder kept in memory. You do not need to change it.",
              zoom=lines_box(L(19), L(20)), box=lines_box(L(19), L(20)))
        c.say("Ports is very important. 9000 colon 9000 means: port 9000 of the container is opened on port 9000 of your "
              "computer. This is why we will open SonarQube at local host colon 9000 in the browser.",
              zoom=lines_box(L(21), L(22)), box=lines_box(L(21), L(22)), note="localhost:9000")
        c.say("Networks puts the container on a small private network, so that SonarQube and its database can talk to each other.",
              zoom=lines_box(L(23), L(24)), box=lines_box(L(23), L(24)))
        # ---- the database service ----
        c.scroll(-6, 1400, 600)
        c.wait(1.5)
        c.say("The second container is called d b. It uses the official PostgreSQL image, version 17. "
              "The health check asks the database every ten seconds: are you ready? This is the check that SonarQube waits for.",
              zoom=lines_box(S(25), S(31), w=800), box=lines_box(S(25), S(31), w=800), note="PostgreSQL 17 = the database")
        c.say("Then the database gets its own names, the same user, password and database name, sonar, as we gave "
              "to SonarQube above, and a volume, so your results are saved on your disk.",
              zoom=lines_box(S(32), S(41)), box=lines_box(S(32), S(41)), note="Must match the SonarQube settings")
        c.say("At the bottom, the file declares the volumes and the networks that we used above. You can leave all of this as it is.",
              zoom=lines_box(S(43), S(50), w=500), box=lines_box(S(43), S(50), w=500))
        # ---- add the memory lines ----
        c.key("ctrl", "home")
        c.wait(1.5)
        c.say("One more thing, very useful on a laptop. SonarQube runs three Java programs inside the container, and by "
              "default they can use a lot of memory. Sonar's documentation lets us limit them with three environment "
              "variables. We add them under the database password. Click at the end of line thirteen.",
              zoom=lines_box(L(10), L(13)), box=lines_box(L(13), L(13)))
        c.click(860, int(L(13)))
        c.key("end")
        c.key("enter")
        c.type('SONAR_SEARCH_JAVAOPTS: "-Xms384m -Xmx384m"', 0.05)
        c.key("enter")
        c.type('SONAR_WEB_JAVAOPTS: "-Xmx384m"', 0.05)
        c.key("enter")
        c.type('SONAR_CE_JAVAOPTS: "-Xmx512m"', 0.05)
        c.wait(1)
        c.say("Search is the search engine, Web is the website, and C E, the compute engine, is the part that processes "
              "your analysis reports. With these limits, SonarQube runs with about two gigabytes of memory. "
              "Be careful: keep the same spaces at the start of the lines as the lines above, because in a yml file the spaces matter.",
              zoom=lines_box(L(10), L(16)), box=lines_box(L(14), L(16), w=560), note="Indentation matters in YAML")
        c.key("ctrl", "s")
        c.wait(1.5)
        c.say("Save with Control and S. The white dot on the tab disappears: the file is saved. "
              "Our setup is ready. In the next chapter, we start SonarQube with one command.",
              box=(435, 46, 220, 34))
        c.wait(1)


if __name__ == "__main__":
    if "prep" in sys.argv:
        prep()
    else:
        record()
