"""Chapter 8: ISO/IEC 5055 with SonarQube (CISQ list of CWEs, Sonar's cwe tag, what matches, what does not).

python ch8.py a | b | ...
"""
import sys, time
import numpy as np
import pyautogui
from PIL import ImageGrab
from rec3 import Clip, find, guard, type_unicode

R = r"C:\Users\juba839\dev\demo\rec"


def orange_box():
    """Bounding box of Chrome's orange 'find in page' highlight (current match)."""
    a = np.array(ImageGrab.grab()).astype(int)
    m = (a[:, :, 0] > 230) & (a[:, :, 1] > 120) & (a[:, :, 1] < 170) & (a[:, :, 2] < 80)
    m[:110, :] = False
    m[1015:, :] = False
    ys, xs = np.nonzero(m)
    if len(xs) < 20:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max() - xs.min()), int(ys.max() - ys.min())


def find_on_page(c, text, say_text, note=None):
    pyautogui.hotkey("ctrl", "a")
    c.type(text, 0.09)
    c.key("enter")
    c.wait(1.5)
    b = orange_box()
    box = (b[0] - 10, b[1] - 8, 900, b[3] + 16) if b else (1372, 112, 440, 40)
    c.say(say_text, box=box, note=note)


def part_a():
    guard("CODE QUALITY RULES")
    pyautogui.press("home"); time.sleep(1)
    pyautogui.moveTo(1850, 950)
    with Clip(R + r"\ch8a.mp4") as c:
        c.wait(1)
        c.say("Chapter eight: ISO 5055. ISO slash IEC 5055 is the international standard that measures the structural "
              "quality of source code. It comes from CISQ, the Consortium for Information and Software Quality. "
              "This is CISQ's official page with the list: it-cisq dot org, Code quality rules.",
              box=(150, 60, 400, 40), note="ISO/IEC 5055 = CISQ code quality standard")
        c.say("The standard has four characteristics: Reliability, Performance Efficiency, Security, and Maintainability. "
              "Each one is defined as a list of software weaknesses, identified by their C W E numbers. "
              "To measure ISO 5055, a tool counts how many times each weakness occurs in your code.",
              box=(230, 580, 1440, 160), note="4 characteristics = lists of CWEs")
        c.say("Remember the two C W E numbers we found in SonarQube. Let's search them in this page, with Control and F.")
        c.key("ctrl", "f")
        c.wait(0.8)
        find_on_page(c, "CWE-476",
                     "C W E 476, NULL pointer dereference: found, in the Reliability list. So the 45 null pointer issues "
                     "that SonarQube found in our Java code are ISO 5055 reliability weaknesses.",
                     note="CWE-476 ∈ ISO 5055 Reliability")
        find_on_page(c, "CWE-79:",
                     "C W E 79, cross site scripting: found, number 3 in the Security list. So our two X S S issues "
                     "are ISO 5055 security weaknesses.", note="CWE-79 ∈ ISO 5055 Security")
        pyautogui.hotkey("ctrl", "a")
        c.type("CWE-352", 0.09)
        c.key("enter")
        c.wait(1.5)
        c.say("And C W E 352, the C S R F issue of our API? Zero results. It is not in ISO 5055. "
              "SonarQube found it, and it can be a real risk, but it does not count for the standard.",
              box=(1372, 112, 440, 40), note="CWE-352: not in ISO 5055")
        c.key("escape")
        c.wait(1)


def part_b():
    guard("Issues")
    pyautogui.hotkey("ctrl", "l"); time.sleep(0.3)
    type_unicode("localhost:9000/issues?issueStatuses=OPEN%2CCONFIRMED", 0.01); pyautogui.press("enter")
    time.sleep(5)
    pyautogui.moveTo(1850, 950)
    with Clip(R + r"\ch8b.mp4") as c:
        c.wait(1)
        c.say("Now let's do the same from SonarQube's side. Click Issues, at the top: this page shows the issues of all "
              "projects together, 172 in total.", box=(1240, 210, 600, 46))
        c.say("SonarQube adds the tag c w e to every rule that is linked to a C W E. So we can filter on this tag. "
              "Scroll down the filters on the left, to Tag.")
        c.move(180, 800)
        for _ in range(4):
            pyautogui.scroll(-480); time.sleep(0.8)
        x, y = find("facet_tag", 5)
        c.click(x, y)
        c.wait(2)
        c.move(180, 800)
        pyautogui.scroll(-480); time.sleep(1.2)
        x, y = find("tag_cwe", 5)
        c.say("The tags are listed with their counts. Click c w e.", box=(10, y - 20, 330, 40))
        c.click(x, y)
        c.wait(3)
        c.say("52 issues are linked to a C W E. Now open the Rule filter, to see which rules they come from.",
              box=(1240, 210, 600, 46))
        x, y = find("facet_rule", 5)
        c.click(x, y)
        c.wait(2.5)
        c.say("Seven rules. Now we compare each one with the ISO list. Null pointers should not be dereferenced, 36 issues, "
              "and Optional value should only be accessed after is present, 9 issues: both are C W E 476, "
              "so they are in ISO 5055 Reliability.", box=(10, 295, 330, 85), note="36 + 9 = 45 → ISO Reliability (CWE-476)")
        c.say("Angular built-in sanitization, 2 issues: C W E 79, in ISO 5055 Security.", box=(10, 422, 330, 40),
              note="2 → ISO Security (CWE-79)")
        c.say("The other four rules: debugging features, C W E 489; C S R F, C W E 352; CORS, C W E 942; and the "
              "pseudorandom number generator, C W E 338. They are real security advice, but these C W E numbers are not in "
              "the ISO 5055 lists. So they do not count.", box=(10, 380, 330, 200), note="5 issues: CWE not in ISO 5055")
        c.wait(1)


def part_c():
    guard("Issues")
    with Clip(R + r"\ch8c.mp4") as c:
        c.wait(0.5)
        c.say("What about the two other ISO characteristics? Let's go back to the CISQ page.", box=(350, 8, 300, 34))
        c.click(470, 25)
        c.wait(2)
        guard("CODE QUALITY RULES")
        c.key("ctrl", "f")
        c.wait(0.6)
        find_on_page(c, "PERFORMANCE EFFICIENCY",
                     "Performance Efficiency: for example, resources that are never released, or expensive operations inside "
                     "loops. SonarQube has no Performance quality, so this characteristic is not covered at all.",
                     note="Performance: not in SonarQube")
        find_on_page(c, "CWE-1041",
                     "And Maintainability: here, C W E 1041, use of redundant code, copy paste. SonarQube measures "
                     "duplication, 18 percent in our web project, but its maintainability rules have no C W E number. "
                     "So you must match them by hand, one by one.", note="Maintainability: close, but no CWE tags")
        c.key("escape")
        c.wait(0.5)
        c.say("So, to summarize. SonarQube is not an ISO 5055 tool: it does not claim to measure the standard. "
              "But it gives a useful partial view. With the c w e tag, we found 47 ISO weaknesses in DomiAffaire: "
              "45 in Reliability, and 2 in Security.", note="ISO 5055 via SonarQube: Reliability 45 · Security 2")
        c.say("Performance is missing, and Maintainability needs manual work. An ISO 5055 measurement also needs a tool "
              "that looks for all the C W Es of the lists. This is why we compared SonarQube with other tools in our "
              "project, like CAST Imaging.", note="Performance — · Maintainability: manual")
        c.wait(1)


if __name__ == "__main__":
    globals()["part_" + sys.argv[1]]()
