"""Chapter 10: clean up (revoke the tokens, stop SonarQube, what happens to the data, start it again).

python ch10.py a | b | ...
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
    goto("localhost:9000/projects")
    pyautogui.moveTo(1500, 900)
    with Clip(R + r"\ch10a.mp4") as c:
        c.wait(1)
        c.say("Chapter ten, the last one: cleaning up. First, the tokens. When you do not need a token any more, "
              "revoke it, so nobody can use it. Click your account, the letter A, at the top right.",
              box=(1850, 125, 40, 40))
        c.click(1869, 144)
        c.wait(1.5)
        c.say("Then My Account.")
        x, y = find("my_account", 5)
        c.click(x, y)
        c.wait(3)
        c.say("Open the Security tab.", box=(10, 330, 280, 40))
        c.click(80, 341)
        c.wait(3)
        c.say("Here you can generate tokens, and you see all your tokens: our three project tokens, their project, "
              "when they were last used, and when they expire. Only their names are shown, never their value.",
              box=(406, 715, 1390, 300), note="Token list: names only, never the secret")
        c.say("Click Revoke on the first one.", box=(1690, 790, 96, 46))
        c.click(1738, 812)
        c.wait(1.5)
        c.move(1500, 650)
        c.wait(1)


def part_b():
    guard("Security")
    with Clip(R + r"\ch10b.mp4") as c:
        c.wait(0.5)
        c.say("SonarQube asks: are you sure? Click Yes. The token is deleted: any scanner that still uses it will be "
              "refused.", box=(1142, 607, 66, 44))
        c.click(1174, 629)
        c.wait(2.5)
        c.say("We do the same for the two other tokens.")
        for _ in range(2):
            c.click(1738, 812)
            c.wait(1.5)
            c.click(1174, 629)
            c.wait(2.5)
        c.move(1500, 650)
        c.say("All tokens are revoked. The token values that appeared in this tutorial are now useless.",
              box=(406, 715, 1390, 300), note="Tokens revoked ✔")
        c.wait(1)


def part_b2():
    guard("Security")
    with Clip(R + r"\ch10b2.mp4") as c:
        c.wait(0.3)
        c.click(1738, 836)
        c.wait(1.5)
        c.click(1174, 629)
        c.wait(2.5)
        c.move(1500, 650)
        c.say("All tokens are revoked. The token values that appeared in this tutorial are now useless.",
              box=(406, 715, 1390, 120), note="Tokens revoked ✔")
        c.wait(1)


def part_c():
    with Clip(R + r"\ch10c.mp4") as c:
        c.wait(0.5)
        x, y = find("ag_icon")
        c.click(x, y)
        c.wait(2)
        guard("sonarqube - Antigravity")
        c.click(1100, 700)
        c.type("cls", 0.1); c.key("enter"); c.wait(1)
        c.say("Finally, SonarQube itself. It uses about two gigabytes of memory, so stop it when you do not use it. "
              "In the terminal, go back to the sonarqube folder, where our docker compose file is.")
        c.type(r"cd C:\Users\juba839\sonarqube", 0.05); c.key("enter"); c.wait(1)
        c.type("docker compose stop", 0.09)
        c.say("Type docker compose stop. It stops the two containers, but keeps them, and keeps all the data in the volumes.",
              note="stop = pause, data kept", box=(470, 135 + 22, 700, 24))
        c.key("enter")
        c.ff_on(4)
        t0 = time.time()
        import subprocess
        while time.time() - t0 < 120:
            out = subprocess.run(["docker", "ps", "-q", "--filter", "name=sonarqube"], capture_output=True, text=True).stdout
            if not out.strip():
                break
            time.sleep(1)
        c.wait(1.5)
        c.ff_off()
        c.say("Both containers are stopped. Next time, type docker compose start, or up dash d again: your projects and "
              "your results are still there, with your password.", note="docker compose start = continue")
        c.say("Two other commands you should know. Docker compose down removes the containers but keeps the volumes, "
              "so the data is still safe. But docker compose down dash v also deletes the volumes: all your projects "
              "and results are lost. Be careful with dash v.", note="down -v = delete ALL data ⚠")
        c.say("That's it! You installed SonarQube with Docker, analyzed a TypeScript project and a Java project, "
              "read the results, linked them to ISO 5055, and saw that the configuration changes what is found. "
              "Now, try it on your own project. Thank you for watching!", note="Your turn: your own project!")
        c.wait(1.5)


if __name__ == "__main__":
    globals()["part_" + sys.argv[1]]()
