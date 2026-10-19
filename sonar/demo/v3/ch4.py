"""Chapter 4: open SonarQube in the browser, first login (admin/admin), forced password change, tour of the empty server.

python ch4.py a | b | c
"""
import sys, time
from pathlib import Path
import pyautogui
from rec3 import Clip, find, activate, guard

R = r"C:\Users\juba839\dev\demo\rec"
PW = Path(r"C:\Users\juba839\dev\demo\assets\sonar-admin.txt").read_text().strip()   # never printed


def load(c, tpl, tries=4):
    """Wait for the page (template tpl); if Chrome hangs on 'Loading...', reload it with F5."""
    for _ in range(tries):
        try:
            return find(tpl, 10)
        except RuntimeError:
            guard("Chrome")
            pyautogui.press("f5")
    return find(tpl, 20)


def part_a():
    activate("Google Chrome")
    with Clip(R + r"\ch4a.mp4") as c:
        c.wait(1)
        c.say("Chapter four: we open SonarQube for the first time. Go back to your browser and open a new tab.")
        c.key("ctrl", "t")
        c.wait(1)
        guard("Chrome")
        c.type("localhost:9000", 0.1)
        c.say("Type local host colon nine thousand. Local host means: this computer. Nine thousand is the port that "
              "we opened in our docker compose file. Press Enter.", box=(150, 60, 400, 40), note="localhost:9000")
        c.key("enter")
        c.ff_on(4)
        load(c, "login_user")
        c.ff_off()
        c.wait(1)
        c.say("This is the SonarQube login page. A new SonarQube always has one user, the administrator. "
              "Its user name is admin, and its password is also admin. Everybody knows this password, "
              "so SonarQube will force us to change it right away.",
              box=(250, 500, 500, 190), note="First login: admin / admin")
        c.click(500, 565)
        c.type("admin", 0.12)
        c.click(480, 662)
        c.type("admin", 0.12)
        c.wait(0.5)
        c.say("Type admin in both fields, then click Log in.", box=(250, 715, 500, 40))
        c.click(500, 735)
        c.wait(10)
        c.move(1400, 900)
        c.wait(1)


def part_b():
    guard("Update password")
    with Clip(R + r"\ch4b.mp4") as c:
        c.wait(1)
        c.say("SonarQube opens the page: Update your password. The yellow message says it: this account should not use "
              "the default password. If your browser offers to save the password, you can say no thanks for now.",
              box=(714, 184, 492, 64))
        c.say("Why is this so important? The administrator can do everything in SonarQube: see all the code, change all "
              "the rules, and create users. With admin admin, anybody on your network could log in. "
              "So we choose a strong password, and we keep it in a password manager.",
              box=(714, 270, 440, 400), note="Admin = full control → strong password")
        c.click(930, 361)
        c.type("admin", 0.12)
        c.say("First, the old password: admin.", box=(714, 339, 437, 45))
        c.blur_on("pw1", (714, 447, 437, 45))
        c.click(930, 469)
        c.type(PW, 0.06)
        c.wait(0.8)
        c.say("Then the new password. While we type, SonarQube checks its rules: at least twelve characters, "
              "one upper case letter, one lower case letter, one number and one special character. "
              "All the checks are green.", box=(714, 500, 440, 180), note="12+ chars · A-Z · a-z · 0-9 · !?#")
        c.blur_on("pw2", (714, 744, 437, 45))
        c.click(930, 766)
        c.type(PW, 0.06)
        c.wait(0.5)
        c.say("Type the same password again, to confirm it. We blur it in this video, and so should you: "
              "never show a real password on screen. Click Update.", box=(714, 819, 82, 40),
              note="Never share your password")
        c.click(754, 839)
        c.wait(6)
        c.blur_off("pw1"); c.blur_off("pw2")
        c.move(1400, 900)
        c.wait(1)


def part_b2():
    guard("Update password")
    with Clip(R + r"\ch4b2.mp4") as c:
        c.blur_on("pw", (714, 447, 437, 152))
        c.click(754, 649)
        c.wait(8)
        c.blur_off("pw")
        c.move(1400, 900)
        c.wait(1)


def part_c():
    guard("create your project")
    with Clip(R + r"\ch4c.mp4") as c:
        c.blur_on("popup", (1252, 100, 565, 475))
        c.wait(0.5)
        c.say("The password is changed, and we are in! Chrome asks again to save the password. We click No thanks, "
              "and we also close this message at the bottom, with Dismiss.", box=(1674, 444, 116, 48))
        c.click(1731, 468)
        c.blur_off("popup")
        c.wait(1)
        c.click(1806, 940)
        c.wait(1.5)
        c.say("This is SonarQube, still empty. At the top left, it says SonarQube community: the free version. "
              "At the bottom, you can see the exact version: Community Build, 26 point 10.",
              box=(30, 115, 210, 60), note="SonarQube Community Build 26.10")
        c.say("Let's look at the menu at the top. Projects is the list of all the projects that you analyze.",
              box=(282, 125, 86, 40))
        c.move(410, 145)
        c.say("Issues shows all the problems found, in all projects, with filters.", box=(376, 125, 70, 40))
        c.move(487, 145)
        c.say("Rules is the catalogue of all the checks that SonarQube knows: thousands of rules, for each language.",
              box=(456, 125, 62, 40))
        c.move(599, 145)
        c.say("Quality profiles decide which rules are used for each language. The default one is called Sonar way.",
              box=(527, 125, 144, 40))
        c.move(744, 145)
        c.say("Quality gates are the pass or fail conditions for your code, for example: no new bugs. "
              "We will see them in the results.", box=(681, 125, 128, 40))
        c.move(887, 145)
        c.say("And Administration is for the settings of the server, the users and the plugins. Only the admin sees it.",
              box=(818, 125, 140, 40))
        c.move(1869, 144)
        c.say("At the top right, the letter A is your account. This is where we will create a token in the next chapter.",
              box=(1850, 125, 40, 40))
        c.move(1000, 600)
        c.say("In the middle, SonarQube asks: how do you want to create your project? You can import it from a DevOps "
              "platform, like GitHub or GitLab, but this needs extra configuration. For a project on your own computer, "
              "the simplest is: Create a local project. This is what we do in the next chapter.",
              box=(265, 787, 423, 87), note="Your own PC → Create a local project")
        c.wait(1)


if __name__ == "__main__":
    {"a": part_a, "b": part_b, "b2": part_b2, "c": part_c}[sys.argv[1]]()
