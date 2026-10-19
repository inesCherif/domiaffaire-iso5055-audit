"""20-second test: open the clean Chrome profile, go to the Sonar docs, move the cursor around."""
import time
from rec3 import Clip, open_chrome

OUT = r"C:\Users\juba839\dev\demo\rec\test.mp4"
with Clip(OUT) as c:
    c.move(960, 540, dur=1.2)
    open_chrome("https://www.sonarsource.com/products/sonarqube/")
    c.mark("chrome_opened")
    c.wait(6)
    c.move(400, 300, dur=1.5)
    c.move(1400, 500, dur=1.5)
    c.move(960, 700, dur=1.2)
    c.wait(2)
