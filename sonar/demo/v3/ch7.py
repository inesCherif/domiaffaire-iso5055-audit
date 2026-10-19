"""Chapter 7: read the results (overview, issues, one issue in detail, hotspots, measures, code, profiles, gates).

python ch7.py a | b | ...
"""
import sys, time
import pyautogui
from rec3 import Clip, find, guard, type_unicode

R = r"C:\Users\juba839\dev\demo\rec"


def goto(url):
    guard("Chrome")
    pyautogui.hotkey("ctrl", "l"); time.sleep(0.3)
    type_unicode(url, 0.01); pyautogui.press("enter"); time.sleep(5)


def part_a():
    goto("localhost:9000/project/overview?id=domiaffaire-web")
    pyautogui.moveTo(1500, 900)
    with Clip(R + r"\ch7a.mp4") as c:
        c.wait(1)
        c.say("Chapter seven: let's read the results, starting with the web project. This is its Overview page. "
              "At the top, the project health dashboard gives four numbers.", box=(406, 395, 1390, 70))
        c.say("First, the quality gate: Passed. The quality gate is a list of conditions, and by default they apply to "
              "the new code. Our project is new for SonarQube, so all of it is still old code, and the gate passes. "
              "It does not mean that the code is perfect!", box=(426, 565, 322, 258),
              note="Passed ≠ perfect: the gate checks NEW code")
        c.say("Open issues: 122 problems were found. Duplications: 18 percent of the lines are copied somewhere else. "
              "And coverage: the part of the code executed by tests, zero here, because we did not run tests.",
              box=(768, 565, 1006, 258))
        x, y = c.scroll_to("snap_sec")
        c.say("Below, there is one snapshot for each software quality. First, Security: 3 issues. The pie shows their "
              "severity: blocker in red, and medium.", box=(426, y - 22, 1346, 500), note="Security = can be attacked")
        c.say("On the right, the top rules. The first one, Angular built-in sanitization bypass, two issues: the code "
              "turns off Angular's protection against cross site scripting, X S S. We will open it in a moment.",
              box=(1338, y + 50, 436, 200))
        x, y = c.scroll_to("snap_rel")
        c.say("Reliability, 107 issues. Reliability means: will the code behave correctly? Here, most of them come from one "
              "rule: 67 form fields have no label. It is an accessibility bug: a blind user with a screen reader "
              "does not know what to type in the field.", box=(426, y - 22, 1346, 500), note="Reliability = works correctly")
        x, y = c.scroll_to("snap_main")
        c.say("And Maintainability, 43 issues: code that works, but that is harder to read and to change, "
              "for example HTML elements that are not used correctly, or Angular classes that could be simpler.",
              box=(426, y - 22, 1346, 500), note="Maintainability = easy to change")
        c.wait(1)


def part_b():
    guard("Overview")
    with Clip(R + r"\ch7b.mp4") as c:
        c.wait(0.5)
        c.say("To see every problem, open Issues, in the menu on the left.", box=(41, 411, 239, 40))
        c.click(78, 431)
        c.wait(4)
        c.say("This is the list of all 122 issues. SonarQube also estimates the effort to fix them all: one day and two "
              "hours. By default they are sorted by priority, so the most dangerous ones come first.",
              box=(1360, 356, 510, 46))
        c.say("Each card is one issue. The title says what is wrong. Above it, the file. Below, the software quality, "
              "here Security, and the severity: Blocker, the highest. On the right, the line in the file, L 82, "
              "and the estimated time to fix it, thirty minutes.", box=(706, 430, 1165, 208),
              note="Title · quality · severity · line · effort")
        c.say("The tags on the right help to search. Here, c w e: this issue is linked to a C W E, an entry in the "
              "Common Weakness Enumeration, the international list of software weaknesses. "
              "Remember this word: we need it for ISO 5055.", box=(1664, 526, 192, 28), note="CWE = Common Weakness Enumeration")
        c.say("On the left, the filters. Software quality: 3 security, 107 reliability and 43 maintainability. "
              "Click on a line to see only those issues.", box=(321, 740, 315, 175))
        c.click(400, 811)
        c.wait(3)
        c.say("Now we only see the 3 security issues. Click again to remove the filter.", box=(1360, 356, 510, 46))
        c.click(400, 811)
        c.wait(3)
        c.scroll(-6, 480, 800)
        c.wait(1.5)
        c.say("Below, there are many more filters: severity, code attribute, status, language, rule, tag, and Compliance category, where you find the security standards, like OWASP Top 10 and C W E. You can combine them.", box=(321, 330, 315, 690))
        c.scroll(6, 480, 800)
        c.wait(1)


def part_c():
    goto("localhost:9000/project/issues?id=domiaffaire-web&issueStatuses=OPEN%2CCONFIRMED")
    pyautogui.moveTo(1850, 950)
    with Clip(R + r"\ch7c.mp4") as c:
        c.wait(1)
        c.say("Let's open the most important issue. Click on its title.", box=(706, 466, 1165, 64))
        c.click(1017, 498)
        c.wait(4)
        c.scroll(3, 1300, 850)
        c.wait(1.5)
        c.say("The issue opens. At the top: the rule, typescript S 6268, Angular built-in sanitization should not be "
              "disabled. The line, 82, the effort, and on the right the quality, Security, Blocker.",
              box=(706, 365, 1166, 115))
        c.say("The first tab, Where is the issue, shows the code. On line 82, the function sanitize H T M L calls "
              "bypass security trust H T M L. This tells Angular: trust this H T M L, do not clean it.",
              box=(706, 948, 1166, 44), note="Line 82: bypassSecurityTrustHtml(html)")
        c.click(1018, 615)
        c.wait(2)
        c.say("Why is this an issue? SonarQube explains the risk: if an attacker controls this H T M L, they can inject "
              "JavaScript into the page. This is cross site scripting, X S S: they can steal a session, or act as the "
              "victim.", box=(706, 650, 1180, 260), note="XSS = attacker's script runs in your page")
        c.click(1210, 615)
        c.wait(2)
        c.say("How can I fix it? Here SonarQube shows code examples: the code that is not compliant, in red, and the "
              "compliant solution. For example, let Angular sanitize the content, or clean it with a trusted library first.",
              box=(706, 650, 1166, 360))
        c.click(1459, 615)
        c.wait(2)
        c.say("More info lists the standards. C W E 79: Improper Neutralization of Input During Web Page Generation. "
              "And OWASP Top 10, A3, Injection. This C W E number is the bridge to ISO 5055, in the next chapter.",
              box=(706, 700, 1060, 180),
              note="CWE-79 → ISO 5055")
        c.wait(1)


def part_d():
    guard("Issues")
    with Clip(R + r"\ch7d.mp4") as c:
        c.wait(0.5)
        c.say("In the menu there is also Security hotspots. Older versions of SonarQube showed some security risks "
              "here, as hotspots to review by a human.", box=(20, 456, 260, 40))
        c.click(124, 476)
        c.wait(4)
        c.say("In this new version, the yellow message says that the concept is deprecated: those findings now appear "
              "directly as security issues in the Issues page. This is why our X S S issue had the tag former hotspot.",
              box=(330, 205, 1560, 110), note="Hotspots → now in Issues (tag former-hotspot)")
        c.say("Now let's look at the Java project. Click Projects, at the top.", box=(330, 125, 108, 40))
        c.click(384, 144)
        c.wait(4)
        c.move(1500, 900)
        c.wait(1)


def part_e():
    guard("Projects")
    with Clip(R + r"\ch7e.mp4") as c:
        c.wait(0.5)
        c.say("The Projects page now shows our two projects side by side. The letters are ratings, from A, the best, "
              "to E, the worst. The rating depends on the most severe issue: one blocker issue gives E, "
              "one high issue gives D, one medium gives C.", box=(530, 360, 1360, 212),
              note="A = best … E = worst (worst issue decides)")
        c.say("So the API gets D in security, and the web client E, because of its blocker X S S issue. "
              "Click domiaffaire api.", box=(530, 470, 270, 90))
        c.click(672, 394)
        c.wait(4)
        c.click(78, 431)
        c.wait(4)
        c.say("Its issues are different, because the language is different. The first one: disabling Spring Security's "
              "C S R F protection. C S R F means cross site request forgery: another website makes your browser send "
              "requests to this A P I. For an A P I that uses tokens, disabling it can be fine, so SonarQube asks a human "
              "to check.", box=(706, 466, 1165, 170), note="CSRF = cross-site request forgery")
        c.say("Then: enabling CORS, which lets other websites call the A P I. And most of the issues are reliability "
              "issues: A NullPointerException could be thrown. Thirty six times! Let's open one.",
              box=(706, 680, 1165, 330))
        c.click(1100, 990)
        c.wait(4)
        c.move(1850, 950)
        c.wait(1)


def part_f():
    guard("Issues")
    with Clip(R + r"\ch7f.mp4") as c:
        c.wait(0.5)
        c.say("This is a reliability bug, severity medium. In the file accountant controller, line 139, the code calls "
              "get content type on the uploaded image, and compares it with image slash p n g. But get content type "
              "can return null. Then Java throws a NullPointerException, and the request crashes.",
              box=(706, 360, 1166, 120), note="getContentType() may be null → crash")
        c.say("On the left, SonarQube even shows the execution flow, step by step: one, get content type can return "
              "null. Two, the result is used without a check. This is why static analysis is powerful: it follows the "
              "paths in the code without running it.", box=(321, 720, 315, 290), note="Execution flow")
        c.click(1459, 615)
        c.wait(2)
        c.say("And in More info: C W E 476, NULL Pointer Dereference. Keep this one in mind too.",
              box=(706, 760, 900, 40), note="CWE-476")
        c.wait(1)


def part_g():
    goto("localhost:9000/component_measures?id=domiaffaire-web&metric=duplicated_lines_density&view=list")
    pyautogui.moveTo(1850, 950)
    with Clip(R + r"\ch7g.mp4") as c:
        c.wait(1)
        c.say("Back to the web project. In the menu Reporting, then Measures, you find all the numbers, one category "
              "at a time. Here, duplications: 18 percent of the lines are copied.", box=(20, 546, 260, 40))
        c.say("The list shows the worst files. In accountant blogs component, 82 percent of the lines are duplicated: "
              "the same code was copied into several components. If there is a bug in it, you must fix it in every copy.",
              box=(706, 640, 1166, 340), note="Copy-paste = fix the bug N times")
        c.say("Now, who decides if a project passes or fails? The quality gate. Click Quality gates, at the top.",
              box=(745, 125, 120, 40))
        c.click(804, 144)
        c.wait(4)
        c.say("The default gate is called Sonar way. It has four conditions, all on new code: new code has zero issues, "
              "new security hotspots are reviewed, coverage of new code is at least 80 percent, and duplication of "
              "new code is at most 3 percent.", box=(560, 520, 1280, 280),
              note="Sonar way: rules on NEW code")
        c.say("Our projects are new, so they have no new code yet, and the gate passes. As soon as you change your code "
              "and analyze again, every change must respect these four conditions. You can also copy this gate and make "
              "your own, stricter one, for example on overall code.", box=(1760, 242, 80, 46))
        c.click(599, 144)
        c.wait(4)
        c.say("Last: Quality profiles. A profile is the set of rules used for one language. For each language, "
              "SonarQube has built-in profiles, and the default one is marked default. Our analyses used the default "
              "profiles, Sonar way core.", box=(20, 600, 1220, 300),
              note="Profile = which rules are checked")
        c.say("This is all we need to read the results. In the next chapter, we connect them with the ISO 5055 standard.")
        c.wait(1)


if __name__ == "__main__":
    globals()["part_" + sys.argv[1]]()
