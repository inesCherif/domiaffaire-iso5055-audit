"""Chapter 5: first analysis, the Angular web client, with the scanner in Docker (Sonar's own wizard: Locally > Other).

Each part starts on a page already checked by a screenshot.  python ch5.py a | b | ...
"""
import subprocess, sys, time
import pyautogui
from rec3 import Clip, find, guard

R = r"C:\Users\juba839\dev\demo\rec"


def part_a():
    guard("create your project")
    with Clip(R + r"\ch5a.mp4") as c:
        c.wait(1)
        c.say("Chapter five: our first analysis. We start with the web part of DomiAffaire, an Angular application in "
              "TypeScript. Click Create a local project.", box=(265, 787, 423, 87))
        c.click(375, 830)
        c.wait(3)
        c.say("Step one of two. The project display name is the name you will see in SonarQube. "
              "We type domiaffaire dash web.", box=(265, 325, 440, 80))
        c.click(484, 380)
        c.type("domiaffaire-web", 0.1)
        c.wait(0.8)
        c.say("SonarQube fills the project key by itself. The key is the unique identifier of the project: "
              "the scanner will use it to send the results to the right place. Keep it simple, with no spaces.",
              box=(265, 433, 440, 80), note="Project key = unique ID")
        c.say("Main branch name is the name of your main Git branch, usually main. Click Next.",
              box=(265, 540, 440, 80))
        c.click(400, 697)
        c.wait(3)
        c.move(1400, 900)
        c.wait(1)


def part_b():
    guard("Set up new code")
    with Clip(R + r"\ch5b.mp4") as c:
        c.wait(1)
        c.say("Step two: new code. SonarQube separates new code, the code you changed recently, from overall code, "
              "all the code. The idea is called Clean as you code: you do not have to fix ten years of old problems "
              "at once, but every new change must be clean.", box=(265, 320, 800, 120),
              note="New code = recent changes")
        c.say("For our first project, the default is perfect: Follows the instance's default, which is the previous version. "
              "Click it, then click Create project.", box=(265, 470, 692, 97))
        c.click(610, 518)
        c.wait(0.8)
        c.click(424, 736)
        c.wait(4)
        c.move(1400, 900)
        c.wait(1)


def part_c():
    guard("Analysis Method")
    with Clip(R + r"\ch5c.mp4") as c:
        c.wait(1)
        c.say("Your project has been created. On the left, the project menu appears. Now SonarQube asks: "
              "how do you want to analyze your repository?", box=(1349, 925, 540, 65))
        c.say("Jenkins, GitHub Actions, GitLab, Bitbucket and Azure are CI tools: they run the analysis automatically "
              "on a server, at every push. This is what teams do in real projects.", box=(416, 454, 1390, 254),
              note="CI = automatic analysis on every push")
        c.say("For learning, and to analyze a project on your own computer, choose the last one: Locally.",
              box=(416, 738, 443, 157))
        c.click(466, 771)
        c.wait(3)
        c.move(1400, 900)
        c.wait(1)


def part_d():
    guard("Analyze your project")
    with Clip(R + r"\ch5d.mp4") as c:
        c.wait(1)
        c.say("Step one: provide a token. What is a token? The scanner, the program that reads your code, must prove to "
              "SonarQube who it is, before it can send results. Instead of your password, it uses a token: "
              "a long secret key, made only for this.", box=(437, 425, 1340, 120), note="Token = a secret key for the scanner")
        c.say("Why not the password? A token can be limited: this one is a project token, it can only analyze this one "
              "project. It expires, here in thirty days. And you can revoke it at any time, without changing your password.",
              box=(457, 560, 800, 250), note="Limited · expires · can be revoked")
        c.say("We keep the name, analyze domiaffaire web, and thirty days. Click Generate.", box=(1142, 595, 111, 45))
        c.blur_on("token", (420, 480, 1370, 200))
        c.click(1197, 617)
        c.wait(3)
        c.move(1400, 900)
        c.wait(1)


def part_e():
    guard("Analyze your project")
    with Clip(R + r"\ch5e.mp4") as c:
        c.blur_on("token", (420, 480, 1370, 80))
        c.wait(1)
        c.say("Here is our token, blurred in this video. SonarQube shows it only once, so copy it now: "
              "double-click on it to select it, and press Control and C. Keep it secret, like a password.",
              box=(437, 495, 800, 50), note="Shown only once → copy it now")
        c.move(960, 520)
        pyautogui.doubleClick(); c.mark("click", x=960, y=520); c.wait(0.6)
        c.key("ctrl", "c")
        c.wait(1)
        c.say("Then click Continue.", box=(467, 642, 110, 46))
        c.click(521, 664)
        c.wait(3)
        c.move(1400, 900)
        c.wait(1)


TOKEN_TOP = (1000, 435, 800, 60)       # where the token is shown at the top right of step 1


def part_f():
    guard("Analyze your project")
    with Clip(R + r"\ch5f.mp4") as c:
        c.blur_on("token", TOKEN_TOP)
        c.wait(1)
        c.say("Step two: run analysis on your project. SonarQube asks: what option best describes your project? "
              "Maven and Gradle are for Java, dot NET for C sharp, and so on.", box=(437, 674, 882, 46))
        c.click(690, 696)
        c.wait(1.5)
        c.say("Our web client is TypeScript, so JS TS and Web looks right. But this option uses the npm scanner, "
              "which needs Node js installed on your computer. We want nothing to install, so we will use Docker instead.",
              box=(437, 740, 1330, 110), note="npm scanner needs Node.js")
        c.click(1205, 696)
        c.wait(1.5)
        c.scroll(-3, 1100, 800)
        c.wait(1.5)
        x, y = find("os_label")
        c.blur_on("cmd", (430, y + 240, 1345, 260))
        c.say("Other is the general SonarScanner, which works for every language. SonarQube asks for our operating "
              "system. We are on Windows.", box=(x - 72, y + 18, 210, 44))
        c.click(x + 75, y + 38)
        c.wait(1.5)
        c.say("SonarQube tells us to download and unzip the scanner, then to run this command in the project folder. "
              "The command is blurred here because it contains our token. Look at what it gives the scanner: "
              "the project key, the source folder, the address of the server, and the token.",
              box=(430, y + 70, 1345, 420), note="key · sources · server URL · token")
        c.say("Good news: SonarSource also publishes this same scanner as a Docker image, called sonar scanner c l i. "
              "So instead of downloading it, we run it with Docker, with exactly the same settings. Let's go to the terminal.",
              note="Same scanner, in Docker: sonarsource/sonar-scanner-cli")
        c.wait(1)


WEB = r"C:\Users\juba839\dev\demo\DomiAffaire\web-client"
TERM = (456, 120, 1450, 870)            # the maximized terminal panel in Antigravity
LH = 22                                 # terminal line height (px)
Y0 = 147                                # first terminal line after cls


def scanner_running():
    out = subprocess.run(["docker", "ps", "--filter", "ancestor=sonarsource/sonar-scanner-cli", "-q"],
                         capture_output=True, text=True).stdout
    return bool(out.strip())


SCAN_LINES = ['docker run --rm `',
              '  -e SONAR_HOST_URL="http://host.docker.internal:9000" `',
              '  -e SONAR_TOKEN `',
              '  -v "${PWD}:/usr/src" `',
              '  sonarsource/sonar-scanner-cli `',
              '  -D"sonar.projectKey=domiaffaire-web" `',
              '  -D"sonar.sources=." `',
              '  -D"sonar.exclusions=src/assets/**,cypress/**,**/*.spec.ts"']
SCAN_EXPL = [
    "docker run starts a container. Dash dash r m removes it when it is finished: the scanner is only needed "
    "during the analysis.",
    "SONAR HOST URL is the address of our server. Inside a container, local host means the container itself, "
    "so we use host dot docker dot internal: this is the name Docker Desktop gives to your computer.",
    "Dash e SONAR TOKEN passes our token variable to the scanner, without writing it.",
    "Dash v gives our code to the scanner: the current folder, P W D, is shared with the folder slash u s r "
    "slash s r c inside the container. This is where the scanner looks for the code.",
    "Then the name of the image: sonarsource slash sonar scanner c l i, the official scanner.",
    "Then the same settings as in SonarQube's wizard. The project key: domiaffaire dash web, exactly the key "
    "of our project.",
    "Sonar sources equals dot: analyze the code from this folder.",
    "And exclusions: the files we do not want to analyze. Here, src slash assets contains a purchased template "
    "with jQuery and Bootstrap: it is not our code. We also skip the test files. Now press Enter."]


def part_g():
    with Clip(R + r"\ch5g.mp4") as c:
        c.wait(0.5)
        x, y = find("ag_icon")
        c.click(x, y)
        c.wait(2)
        guard("sonarqube - Antigravity")
        c.click(1100, 700)
        c.type("cls", 0.1); c.key("enter"); c.wait(1)
        c.say("We are back in the terminal of our editor. First, we go into the folder of the project that we want "
              "to analyze. For you, it is the folder of your own project. Here it is the web client of DomiAffaire.")
        c.type("cd " + WEB, 0.04); c.key("enter"); c.wait(1)
        c.type("ls", 0.1); c.key("enter"); c.wait(2)
        c.say("With l s, we check that we are in the right place: we see package dot json, angular dot json and the s r c "
              "folder, the source code.", zoom=(456, 120, 900, 480))
        c.type("cls", 0.1); c.key("enter"); c.wait(1)
        c.say("Now the token. We put it in a variable of this terminal, called SONAR underscore TOKEN. "
              "Type dollar env colon SONAR TOKEN equals, open the quotes, paste the token with Control V, and close the quotes.",
              note='$env:SONAR_TOKEN = "..."')
        c.blur_on("tokline", TERM)
        c.type('$env:SONAR_TOKEN = "', 0.06)
        c.key("ctrl", "v"); c.wait(0.4)
        c.type('"', 0.1); c.key("enter"); c.wait(1)
        c.say("Why a variable? This way, the token is not written inside the command, and it only lives in this "
              "terminal window: when you close it, it is gone. Then we clear the screen with c l s, so the token "
              "is not visible any more.", note="Token only lives in this terminal")
        c.type("cls", 0.1); c.key("enter"); c.wait(1.2)
        c.blur_off("tokline")
        c.say("Now the command. It is long, so we write it on several lines: in PowerShell, a back quote at the end "
              "of a line means the command continues on the next line.", note="` = continue on the next line")
        for i, (ln, ex) in enumerate(zip(SCAN_LINES, SCAN_EXPL)):
            c.type(ln, 0.035)
            yy = Y0 + i * LH
            c.say(ex, box=(470, yy - 12, 1010, 24), zoom=(456, Y0 - 30, 1100, 260))
            if i < len(SCAN_LINES) - 1:
                c.key("enter")
        c.key("enter")
        c.wait(3)
        c.say("The scanner starts. It reads the configuration, downloads the analyzers from our SonarQube server, "
              "and then reads every file. This takes a few minutes, so we speed up the video.")
        c.ff_on(10)
        t0 = time.time()
        while not scanner_running() and time.time() - t0 < 120:
            time.sleep(1)
        while scanner_running():
            time.sleep(2)
        c.wait(2)
        c.ff_off()
        c.say("At the end, the scanner writes ANALYSIS SUCCESSFUL, and EXECUTION SUCCESS. Our code has been analyzed, "
              "and the report has been sent to SonarQube. Just above, it even gives the link to see the results.",
              zoom=(456, 640, 1450, 350), note="ANALYSIS SUCCESSFUL = done")
        c.wait(1)


def part_g2():
    """Continuation of part G (the first clip stopped when the scanner started)."""
    guard("sonarqube - Antigravity")
    with Clip(R + r"\ch5g2.mp4") as c:
        c.ff_on(10)
        while scanner_running():
            time.sleep(2)
        c.wait(2)
        c.ff_off()
        c.say("At the end, the scanner writes ANALYSIS SUCCESSFUL, and EXECUTION SUCCESS. Our code has been analyzed, "
              "and the report has been sent to SonarQube. Just above, it even gives the link to see the results.",
              zoom=(456, 640, 1450, 350), note="ANALYSIS SUCCESSFUL = done")
        c.wait(1)


def part_h():
    guard("sonarqube - Antigravity")
    with Clip(R + r"\ch5h.mp4") as c:
        c.wait(0.5)
        c.say("Let's go back to the browser.")
        c.click(1293, 1050)
        c.wait(2.5)
        guard("Chrome")
        c.say("The SonarQube page has refreshed by itself, and now shows the Overview of our project. "
              "Twenty two thousand lines of code, analyzed one minute ago.", box=(220, 270, 520, 70))
        c.say("Here are the first results: the quality gate is Passed, there are 122 open issues, 18 percent of the code "
              "is duplicated, and the coverage is zero, because we did not run the tests. We will read all of this "
              "in detail in chapter seven. First, let's analyze the Java part too.",
              box=(270, 470, 930, 200), note="Quality gate · issues · duplication · coverage")
        c.wait(1)


if __name__ == "__main__":
    globals()["part_" + sys.argv[1]]()
