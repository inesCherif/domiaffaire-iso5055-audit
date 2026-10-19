"""Chapter 1: Get SonarQube (official docs -> Docker compose -> official example file -> copy it).

Before running: the clean Chrome profile is open, maximized, on the docs homepage (see prep in ch1_prep()).
"""
import sys, time
import pyautogui
from rec3 import Clip, type_unicode, find

OUT = r"C:\Users\juba839\dev\demo\rec\ch1.mp4"
HOME = "https://docs.sonarsource.com/sonarqube-community-build/"


def prep():
    """Bring the demo Chrome to a clean state: one tab, docs homepage, top of page."""
    pyautogui.click(960, 600)                     # focus Chrome (page body)
    pyautogui.hotkey("ctrl", "l"); time.sleep(0.3)
    type_unicode(HOME, 0.005); pyautogui.press("enter")
    time.sleep(6)
    pyautogui.moveTo(1200, 700)


def record():
    with Clip(OUT) as c:
        c.wait(1)
        c.say("Hi! In this tutorial, we install SonarQube on our own computer, we run it in Docker, and we analyze a real "
              "project, step by step. The only thing you need before starting is Docker Desktop. "
              "We always start from the official documentation, at docs dot sonarsource dot com. "
              "Never download SonarQube from a random website.",
              box=(150, 60, 460, 40), note="Official docs: docs.sonarsource.com")
        c.move(990, 515, 1.2)
        c.say("SonarQube Community Build is the free version of SonarQube. It reads your source code, without running it, "
              "and finds bugs, security weaknesses, and code that is hard to maintain, in more than forty languages. "
              "It runs on your own machine, so your code never leaves your computer.",
              zoom=(480, 400, 1010, 460), note="Free · 40+ languages · runs on your PC")
        c.click_on("menu_install")
        c.wait(2.5)
        c.say("To install it, open Server installation and setup, in the menu on the left. "
              "This page says there are three ways to install SonarQube: from a ZIP file, from the Docker image, "
              "or on Kubernetes. We use the Docker image: Docker gives us SonarQube already prepared and ready to run, "
              "so we install nothing else on Windows.",
              box=(500, 480, 980, 70), note="3 ways: ZIP · Docker image · Kubernetes")
        c.click_on("menu_docker")
        c.wait(2.5)
        c.say("Click From Docker image. It has four pages. The one we need is: Set up and start your container.",
              box=(510, 715, 962, 62))
        c.click_on("card_setup")
        c.wait(3)
        c.say("This page shows two ways to start the container. With docker run, you type one long command. "
              "With Docker compose, you write the whole setup in one file. We choose Docker compose, because it starts "
              "SonarQube and its database together, and later you restart everything with one short command.",
              box=(510, 545, 960, 95), note="docker run = one long command\ndocker compose = one file (our choice)")
        c.scroll(-7, 990, 700)
        c.wait(1.5)
        lx, ly = find("yml_link")
        c.say("Here is the Docker compose part. SonarSource gives an official example file. Click: yml file example.",
              zoom=(490, ly - 95, 990, 210), box=(lx - 82, ly - 16, 165, 32))
        c.click(lx, ly, target="yml_link")
        c.wait(6)
        c.say("The link opens the official GitHub repository of SonarSource, the company that makes SonarQube. "
              "We are in the folder s q with postgres, which means SonarQube with a PostgreSQL database. "
              "PostgreSQL is where SonarQube saves your projects and your results, so nothing is lost when you restart. "
              "Open the file docker-compose dot yml.",
              box=(150, 60, 830, 40), note="github.com/SonarSource = official source")
        c.click_on("gh_file")
        c.wait(4)
        cx, cy = find("gh_copy")
        c.say("This is the file we need. It describes two containers: SonarQube itself, and its database. "
              "We will explain every line in the next chapter, when we create the file on our computer. "
              "For now, click the copy button, at the top right of the file, to copy all of it.",
              box=(cx - 17, cy - 17, 34, 34), note="Copy raw file")
        c.click(cx, cy, target="gh_copy")
        c.wait(2)
        c.say("Done: the whole file is in our clipboard. In the next chapter, we create a folder for SonarQube on our "
              "computer, and we paste this file inside it.")
        c.wait(1)


if __name__ == "__main__":
    if "prep" in sys.argv:
        prep()
    else:
        record()
