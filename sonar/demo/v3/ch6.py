"""Chapter 6: second analysis, the Java API (Spring Boot) with Maven, following the wizard's Maven command.

python ch6.py a | b | ...
"""
import subprocess, sys, time
import pyautogui
from rec3 import Clip, find, guard

R = r"C:\Users\juba839\dev\demo\rec"
API = r"C:\Users\juba839\dev\demo\DomiAffaire\api"


def part_a():
    guard("Projects")
    with Clip(R + r"\ch6a.mp4") as c:
        c.wait(1)
        c.say("Chapter six: the Java part. DomiAffaire's back end is a Spring Boot application, built with Maven. "
              "For Java, the scanner needs the compiled code, so the analysis works a bit differently. "
              "We are on the Projects page. A small tip appears; we close it.", box=(1424, 618, 80, 46))
        c.click(1463, 640)
        c.wait(1)
        c.say("Our first project, domiaffaire web, is here, with its grades for security, reliability and maintainability. "
              "Now we create a second project. Click Create Project, at the top right.",
              box=(530, 360, 1360, 212))
        c.click(1794, 232)
        c.wait(1.5)
        c.move(1500, 800)
        c.wait(1)


def part_b():
    guard("Projects")
    with Clip(R + r"\ch6b.mp4") as c:
        c.wait(0.5)
        c.say("The menu offers Local project, or Import from DevOps platforms. Choose Local project, like before.",
              box=(1608, 272, 280, 52))
        c.click(1675, 298)
        c.wait(3)
        c.click(484, 380)
        c.type("domiaffaire-api", 0.1)
        c.wait(0.8)
        c.say("We name it domiaffaire dash api. The key is filled automatically, and the branch is main. Click Next.",
              box=(265, 325, 440, 300))
        c.click(400, 697)
        c.wait(3)
        c.say("Same choice as before for new code: follow the instance's default. Then Create project.",
              box=(265, 470, 692, 97))
        c.click(610, 518)
        c.wait(0.8)
        c.click(424, 736)
        c.wait(4)
        c.say("And again, we analyze it Locally.", box=(416, 738, 443, 157))
        c.click(466, 771)
        c.wait(3)
        c.move(1400, 900)
        c.wait(1)


def part_c():
    guard("Analyze your project")
    with Clip(R + r"\ch6c.mp4") as c:
        c.wait(0.5)
        c.say("This project needs its own token, because a project token works for one project only. Click Generate.",
              box=(1142, 595, 111, 45))
        c.blur_on("token", (420, 480, 1370, 200))
        c.click(1197, 617)
        c.wait(3)
        c.say("Copy the new token, with a double-click and Control C, then click Continue.", box=(437, 495, 800, 50))
        c.move(960, 520)
        pyautogui.doubleClick(); c.mark("click", x=960, y=520); c.wait(0.6)
        c.key("ctrl", "c")
        c.wait(0.8)
        c.click(521, 664)
        c.wait(3)
        c.move(1400, 900)
        c.wait(1)


TOKEN_TOP = (1000, 435, 800, 60)
TOKEN_LINE = (440, 940, 1100, 30)        # last line of the Maven command block


def part_d():
    guard("Analyze your project")
    with Clip(R + r"\ch6d.mp4") as c:
        c.blur_on("tok1", TOKEN_TOP)
        c.blur_on("tok2", TOKEN_LINE)
        c.wait(0.5)
        c.say("This time, our project is built with Maven, so we choose Maven. For Java, this is the recommended way: "
              "the Maven plugin knows where the compiled classes and the libraries are.", box=(437, 674, 97, 46))
        c.click(485, 696)
        c.wait(1.5)
        c.say("SonarQube gives us one command, to run in the project folder. Mvn clean verify builds the project: "
              "it compiles the code and runs the tests. Then sonar maven plugin, colon sonar, runs the analysis.",
              zoom=(436, 820, 1330, 180), box=(450, 845, 760, 24))
        c.say("The other lines are the same settings as for the web project: the project key, the project name, "
              "the server address, and the token, which is blurred here.",
              zoom=(436, 820, 1330, 180), box=(450, 868, 600, 100))
        c.say("Why does Java need a build? The Java analyzer reads the compiled dot class files too, to understand the "
              "types and the libraries. Without compiled code, the analysis of Java fails. Let's run it.",
              note="Java analysis needs the compiled .class files")
        c.wait(1)


def sonar_done(key, after):
    """True when SonarQube has processed a report for `key` submitted after time `after` (epoch seconds)."""
    import base64, json, urllib.request
    from datetime import datetime
    from pathlib import Path
    pw = Path(r"C:\Users\juba839\dev\demo\assets\sonar-admin.txt").read_text().strip()
    req = urllib.request.Request(f"http://localhost:9000/api/ce/activity?component={key}")
    req.add_header("Authorization", "Basic " + base64.b64encode(f"admin:{pw}".encode()).decode())
    tasks = json.load(urllib.request.urlopen(req))["tasks"]
    for t in tasks:
        sub = datetime.strptime(t["submittedAt"], "%Y-%m-%dT%H:%M:%S%z").timestamp()
        if sub >= after - 5 and t["status"] in ("SUCCESS", "FAILED"):
            return t["status"]
    return None


TERM = (456, 120, 1450, 870)
Y0, LH = 147, 22
MVN_LINES = ['mvn clean verify -DskipTests `',
             '  org.sonarsource.scanner.maven:sonar-maven-plugin:sonar `',
             '  -D"sonar.projectKey=domiaffaire-api" `',
             '  -D"sonar.projectName=domiaffaire-api" `',
             '  -D"sonar.host.url=http://localhost:9000" `',
             '  -D"sonar.token=$env:SONAR_TOKEN"']
MVN_EXPL = [
    "mvn clean verify, as in the wizard. We add dash D skip tests: the tests of this project need a running "
    "database, and we only want the analysis now. So the coverage will stay at zero.",
    "Then the Sonar Maven plugin, exactly as SonarQube wrote it.",
    "The project key, domiaffaire dash api.",
    "The project name.",
    "Here the server address is local host, because Maven runs directly on our computer, not inside a container.",
    "And the token, read from our variable. In PowerShell, we put each dash D setting in quotes, like this, "
    "so that the dots are not misread. Press Enter."]


def part_e():
    import time as _t
    with Clip(R + r"\ch6e.mp4") as c:
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
        c.say("Back in the terminal. We go to the folder of the Java project, called api, with c d and its full path. "
              "With l s, we see its pom dot xml, the Maven file, and its s r c folder.")
        c.type("cd " + API, 0.04); c.key("enter"); c.wait(1)
        c.type("ls", 0.1); c.key("enter"); c.wait(2)
        c.say("Maven must be installed on your computer, with Java. If it is not, Spring Boot projects come with "
              "the Maven wrapper, m v n w dot c m d, which you can use instead of m v n.", zoom=(456, 120, 900, 480),
              note="No Maven? use .\\mvnw.cmd")
        c.type("cls", 0.1); c.key("enter"); c.wait(1)
        c.say("We store the new token in the variable, the same way as before, and we clear the screen.")
        c.blur_on("tokline", TERM)
        c.type('$env:SONAR_TOKEN = "', 0.06)
        c.key("ctrl", "v"); c.wait(0.4)
        c.type('"', 0.1); c.key("enter"); c.wait(1)
        c.type("cls", 0.1); c.key("enter"); c.wait(1.2)
        c.blur_off("tokline")
        c.type('$env:MAVEN_OPTS = "-Xmx768m"', 0.06)
        c.say("A tip for laptops: MAVEN OPTS limits the memory of Maven to 768 megabytes, so that it does not "
              "compete too much with SonarQube.", box=(470, Y0 - 12, 600, 24))
        c.key("enter"); c.wait(1)
        c.type("cls", 0.1); c.key("enter"); c.wait(1)
        for i, (ln, ex) in enumerate(zip(MVN_LINES, MVN_EXPL)):
            c.type(ln, 0.035)
            c.say(ex, box=(470, Y0 + i * LH - 12, 1010, 24), zoom=(456, Y0 - 30, 1100, 220))
            if i < len(MVN_LINES) - 1:
                c.key("enter")
        start = _t.time()
        c.key("enter")
        c.wait(4)
        c.say("Maven downloads what it needs, compiles the code, builds the application, and then the analysis starts. "
              "We speed up the video again.")
        c.ff_on(8)
        status = None
        while status is None and _t.time() - start < 900:
            _t.sleep(4)
            status = sonar_done("domiaffaire-api", start)
        c.wait(3)
        c.ff_off()
        c.mark("status", status=status)
        c.say("BUILD SUCCESS, and the analysis report is sent to SonarQube. The Java project is analyzed too.",
              zoom=(456, 640, 1450, 350), note="BUILD SUCCESS")
        c.wait(1)


def part_f():
    guard("sonarqube - Antigravity")
    with Clip(R + r"\ch6f.mp4") as c:
        c.wait(0.5)
        c.click(1376, 1050)
        c.wait(2.5)
        guard("Chrome")
        c.say("In the browser, the page has refreshed again: this is the overview of domiaffaire api. "
              "Five thousand six hundred lines of Java, and the version, zero point zero point one snapshot, "
              "comes from the pom dot xml file.", box=(220, 270, 860, 70))
        c.say("The quality gate is passed, there are 50 open issues, 8.8 percent duplication, and zero coverage, "
              "because we skipped the tests. We now have two projects. In the next chapter, we read the results in detail.",
              box=(270, 470, 930, 200))
        c.wait(1)


if __name__ == "__main__":
    globals()["part_" + sys.argv[1]]()
