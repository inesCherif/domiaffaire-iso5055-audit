"""Chapter 9: the whole DomiAffaire (api + chatapp + web client) in ONE analysis, and what is different.

python ch9.py a | b | c ...
"""
import subprocess, sys, time
import pyautogui
from rec3 import Clip, find, guard, type_unicode
from ch6 import sonar_done

R = r"C:\Users\juba839\dev\demo\rec"
ROOT = r"C:\Users\juba839\dev\demo\DomiAffaire"
TERM = (456, 120, 1450, 870)
Y0, LH = 147, 22


def goto(url):
    guard("Chrome")
    pyautogui.hotkey("ctrl", "l"); time.sleep(0.3)
    type_unicode(url, 0.01); pyautogui.press("enter"); time.sleep(5)


def part_a():
    goto("localhost:9000/projects")
    pyautogui.moveTo(1500, 900)
    with Clip(R + r"\ch9a.mp4") as c:
        c.wait(1)
        c.say("Chapter nine: a question you will surely ask. DomiAffaire has three parts: the web client, the API, and a "
              "small chat service. What happens if we analyze everything at once, as one single project? "
              "Do we get the same results? Let's try. We create a third project, the same way as before.")
        c.click(1794, 232)
        c.wait(1.2)
        c.click(1675, 298)
        c.wait(3)
        c.click(484, 380)
        c.type("domiaffaire-all", 0.1)
        c.wait(0.6)
        c.say("We call it domiaffaire dash all. Next, the default new code, Create project, and Locally.",
              box=(265, 325, 440, 300))
        c.click(400, 697)
        c.wait(3)
        c.click(610, 518)
        c.wait(0.8)
        c.click(424, 736)
        c.wait(4)
        c.click(466, 771)
        c.wait(3)
        c.say("A new project token: Generate, then copy it, and Continue.", box=(1142, 595, 111, 45))
        c.blur_on("token", (420, 480, 1370, 200))
        c.click(1197, 617)
        c.wait(3)
        c.move(960, 520)
        pyautogui.doubleClick(); c.mark("click", x=960, y=520); c.wait(0.6)
        c.key("ctrl", "c")
        c.wait(0.8)
        c.click(521, 664)
        c.wait(3)
        c.blur_off("token")
        c.blur_on("tok1", (1000, 435, 800, 60))
        c.say("This project mixes Java and TypeScript, so we use the general scanner again, Other, with Docker. "
              "Let's go to the terminal.", box=(1094, 674, 225, 46))
        c.click(1205, 696)
        c.wait(1.5)
        c.blur_on("cmd", (430, 560, 1345, 460))
        c.wait(1)


SCAN = ['docker run --rm `',
        '  -e SONAR_HOST_URL="http://host.docker.internal:9000" `',
        '  -e SONAR_TOKEN `',
        '  -v "${PWD}:/usr/src" `',
        '  sonarsource/sonar-scanner-cli `',
        '  -D"sonar.projectKey=domiaffaire-all" `',
        '  -D"sonar.sources=api/src/main,chatapp/src/main,web-client" `',
        '  -D"sonar.exclusions=web-client/src/assets/**,web-client/cypress/**,**/*.spec.ts" `',
        '  -D"sonar.java.binaries=api/target/classes,chatapp/target/classes" `',
        '  -D"sonar.java.libraries=api/target/dependency/*.jar,chatapp/target/dependency/*.jar"']
EXPL = {
    5: "The new project key, domiaffaire dash all.",
    6: "Sources: now three folders, separated by commas: the main code of the API, of the chat service, and the web client.",
    7: "The same exclusions as before, with the folder name in front.",
    8: "Java binaries: where the compiled classes are, for the API and for the chat service. Without Maven, the "
       "scanner does not know it, so we must tell it.",
    9: "And Java libraries: the jar files that we just copied. They help the analyzer understand Spring and the other "
       "libraries. Press Enter."}


def scanner_running():
    out = subprocess.run(["docker", "ps", "--filter", "ancestor=sonarsource/sonar-scanner-cli", "-q"],
                         capture_output=True, text=True).stdout
    return bool(out.strip())


def part_b():
    with Clip(R + r"\ch9b.mp4") as c:
        c.wait(0.5)
        x, y = find("ag_icon")
        c.click(x, y)
        c.wait(2)
        guard("sonarqube - Antigravity")
        try:
            find("agent_hdr", timeout=2)
            c.click(1891, 66); c.wait(0.8)
        except RuntimeError:
            pass
        c.click(1100, 700)
        c.type("cls", 0.1); c.key("enter"); c.wait(1)
        c.type("cd " + ROOT, 0.04); c.key("enter"); c.wait(1)
        c.type("ls", 0.1); c.key("enter"); c.wait(2)
        c.say("This time we go to the main folder of DomiAffaire, which contains the three parts: api, chatapp and "
              "web client.", zoom=(456, 120, 900, 480))
        c.type("cls", 0.1); c.key("enter"); c.wait(1)
        c.say("Without Maven, the scanner needs the compiled Java code, and the libraries. So first we compile the two "
              "Java parts, and we copy their libraries into target slash dependency. Dash f tells Maven which pom file "
              "to use, and dash q makes it quiet.", note="Compile first: classes + libraries")
        c.type("mvn -q -f api/pom.xml compile dependency:copy-dependencies -DoutputDirectory=target/dependency", 0.03)
        c.key("enter")
        c.ff_on(8)
        time.sleep(4)
        while True:
            busy = subprocess.run(["powershell", "-c", "(Get-CimInstance Win32_Process -Filter \"Name='java.exe'\" | "
                                   "Where-Object { $_.CommandLine -like '*plexus-classworlds*' }).Count"],
                                  capture_output=True, text=True).stdout.strip()
            if busy in ("", "0"):
                break
            time.sleep(2)
        c.ff_off()
        c.type("mvn -q -f chatapp/pom.xml compile dependency:copy-dependencies -DoutputDirectory=target/dependency", 0.03)
        c.key("enter")
        c.ff_on(8)
        time.sleep(4)
        while True:
            busy = subprocess.run(["powershell", "-c", "(Get-CimInstance Win32_Process -Filter \"Name='java.exe'\" | "
                                   "Where-Object { $_.CommandLine -like '*plexus-classworlds*' }).Count"],
                                  capture_output=True, text=True).stdout.strip()
            if busy in ("", "0"):
                break
            time.sleep(2)
        c.ff_off()
        c.say("Both are compiled. Now the token of the new project, in the variable, and we clear the screen.")
        c.blur_on("tokline", TERM)
        c.type('$env:SONAR_TOKEN = "', 0.06)
        c.key("ctrl", "v"); c.wait(0.4)
        c.type('"', 0.1); c.key("enter"); c.wait(1)
        c.type("cls", 0.1); c.key("enter"); c.wait(1.2)
        c.blur_off("tokline")
        c.say("The command starts like the one for the web client. The differences are at the end.")
        for i, ln in enumerate(SCAN):
            c.type(ln, 0.03)
            if i in EXPL:
                c.say(EXPL[i], box=(470, Y0 + i * LH - 12, 1300, 24), zoom=(456, Y0 - 30, 1440, 300))
            if i < len(SCAN) - 1:
                c.key("enter")
        start = time.time()
        c.key("enter")
        c.wait(3)
        c.say("Two minutes of analysis: we speed up.")
        c.ff_on(12)
        while not scanner_running() and time.time() - start < 120:
            time.sleep(1)
        while scanner_running():
            time.sleep(2)
        c.wait(2)
        c.ff_off()
        c.say("ANALYSIS SUCCESSFUL. Let's compare the results.", zoom=(456, 640, 1450, 350))
        c.wait(1)


def part_c():
    guard("sonarqube - Antigravity")
    with Clip(R + r"\ch9c.mp4") as c:
        c.wait(0.5)
        c.click(1376, 1050)
        c.wait(2.5)
        guard("Chrome")
        c.say("Here are our three projects. domiaffaire all has 28 thousand lines: the web client, 22 thousand, "
              "plus the API, 5.6 thousand, plus the small chat service.", box=(530, 360, 1360, 212))
        c.say("Now compare the issues. Security: 9 for the whole project, but 4 plus 3, so 7, for the two projects "
              "together. Reliability: 155, instead of 46 plus 107, so 153. Maintainability: 43 in both cases.",
              box=(540, 480, 360, 80), note="Security 9 vs 7 · Reliability 155 vs 153")
        c.say("So the whole analysis found four more issues. The chat service brings no issue at all, so where do they "
              "come from? Let's look at the security issues of domiaffaire all.", box=(530, 360, 1360, 212))
        c.click(672, 394)
        c.wait(4)
        c.click(78, 431)
        c.wait(4)
        c.click(400, 811)
        c.wait(3)
        c.move(1300, 800)
        for _ in range(2):
            pyautogui.scroll(-480); time.sleep(1)
        c.wait(1)
        x, y = find("app_props", 5)
        c.say("Here they are: two issues in the file application dot properties, the configuration of the Spring API. "
              "The maximum upload size is ten megabytes, more than the recommended eight: an attacker could upload "
              "huge files and fill the memory or the disk.", box=(x - 250, y - 20, 1200, 470),
              note="Only found by the whole analysis")
        c.say("Why did the Maven analysis miss them? Because the Maven scanner only reads the Java code and the pom file "
              "by default. It never opened the properties file in s r c slash main slash resources. In the whole "
              "analysis, we gave the full s r c slash main folder, so the configuration was analyzed too.",
              note="Maven: src/main/java only · Docker: all of src/main")
        c.say("And the two extra reliability issues are two more Optional get calls, C W E 476, in the API. Same code, same rule, but the analyzer ran with a different setup: other compiled classes, other libraries. Even a small difference in configuration changes the results.",
              note="+2 CWE-476: different setup")
        c.say("The lesson: the results depend on what you give to the scanner. Check the number of files analyzed in "
              "the log, include your configuration files, and give Java its compiled classes and libraries. "
              "Otherwise, problems stay hidden, and SonarQube cannot tell you.", note="Results depend on the configuration")
        c.wait(1)


if __name__ == "__main__":
    globals()["part_" + sys.argv[1]]()
