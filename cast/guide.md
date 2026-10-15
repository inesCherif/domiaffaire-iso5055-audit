# CAST Imaging: step-by-step guide for the DomiAffaire analysis

**For:** Ines (and anyone who repeats the demo). **Product:** CAST Imaging Express (cloud, free trial).

CAST is the only vendor that documents native ISO/IEC 5055 support. This guide prepares **one** analysis, because the trial
allows a single application. Each step says **what to click**, **why**, and **what you should see**. The menu names come
from CAST's official documentation. Where the docs do not name a button, the step says *(name to confirm in rehearsal)*.

> **Official facts (doc.castsoftware.com/imagingexpress):**
> - **Trial limits:** 30 days, **1 application**, **less than 250k lines of code**.
> - **What leaves your PC:** the analyzer runs on your PC, and **only the structural analysis results** are uploaded.
> - **What CAST shows:** "critical violations based on ISO-5055 standards", listed by quality factor.
> - **Coverage:** Java with Spring (Boot, MVC, Data, Security), Spring Data MongoDB, and Angular 2–17 / TypeScript are covered.
> - **Possible gap:** CAST's video library shows ISO-5055 views for **Security, Performance Efficiency and Reliability**,
>   not Maintainability. Check this during the rehearsal (Part A).

---

## Part A: Rehearsal on CAST's demo application (no risk, does not use your slot)

*Why:* you learn the screens and the clicks before the one-shot analysis, and I write the real menu names into this guide.

1. **Open the demo app.** Go to https://castimaging.io, sign in, and open the preloaded demo application (for example *DemoAppPython*).
2. **Find the summary page.** Then find the architecture overview.
   - *Video (3 min):* [summary page](https://vimeo.com/1161835766) · [architecture overview](https://vimeo.com/1161830873)
3. **Find the ISO-5055 views.** Open each quality factor and one violation in it, with its rule, the impacted object, the graph and the remediation text.
   - *Videos:* [Security](https://vimeo.com/1162124322) · [Reliability](https://vimeo.com/1162133669) · [Performance efficiency](https://vimeo.com/1162128420)
4. **Check Maintainability.** Is there a **Maintainability** view? Note **yes/no**.
5. **Check exports.** Is there an **export** (CSV/Excel/report) of the ISO-5055 violations? Note where it is.
   - *Hint:* the docs list "reports / generate report" in the API, and an *Application summary report*.
6. **Test a short recording.** Make a **30-second test recording** with Snipping Tool (**Win + Shift + R**, select the browser window, mic on).

📸 **Send me screenshots of:** the summary page, the ISO-5055 list, one violation detail, and the export menu (if any).

---

## Part B: Install the CAST Imaging Analyzer (Windows)

*Why:* CAST analyses the code **on your PC**. Your PC fits the requirements: Windows 11, 16 GB RAM (8 GB minimum), x64,
and the 3 GB + 4–8 GB of disk it needs.

1. In castimaging.io click **Start analysis**, then download the **Analyzer** for Windows.
   - **Online** analyzer: uploads by itself.
   - **Offline** analyzer: about 1 GB plus a license file, and you upload by hand.
   - Use the **online** one unless it fails.
2. Run the installer and accept the defaults.
3. **Before analysing, close heavy apps.** In our earlier run the PC had only about 0.5 GB of free RAM.
   - Stop the DomiAffaire app (`Ctrl+C` in its terminals) and `docker stop domi-mongo`, or quit Docker Desktop. CAST does not need them.
   - Close Discord and extra Chrome tabs.

## Part C: Profiling (safe, nothing uploaded yet)

*Why:* profiling inventories the code (technologies, size) **before** the real analysis. It is our last check before the one shot.

The Analyzer window (**CAST Imaging Express**, Onboarding) has 3 steps in the left panel: **1 Select source code location**,
**2 Start profiling**, **3 Run deep analysis**. The first screen has a **Select folder path** field with a **Browse** button
and an **Application name** field.

1. Start the Analyzer.
2. **Source folder** (click **Browse**): `C:\Users\juba839\dev\cast\DomiAffaire`.
   - Select **this folder**, not the OneDrive one and not `app/`.
   - It is a clean copy: only `api`, `chatapp` and `web-client-07-06-2024`.
   - Removed from the copy: tests, the purchased "Midone" template (assets), jQuery/Bootstrap vendor files, the npm lock file, `node_modules`, the `.mvn` folder, the mobile app and the notebooks.
3. **Application name:** `DomiAffaire`.
4. Run the **profiling**.
5. **STOP and send me a screenshot of the profiling result.** We check together:

| Check | Expected | If not |
|---|---|---|
| Size | about 28,500 non-blank lines (Java about 5,900, TypeScript about 8,900, HTML about 10,400, CSS about 2,800). Far below 250k. | Ask me before going on |
| Technologies | Java, Spring (Boot/MVC/Data/Security), MongoDB, TypeScript/Angular, HTML/CSS | If Angular/TypeScript is missing, we decide together (backend-only analysis is acceptable) |
| Folders | 3 folders, no `node_modules`, no `assets` | Re-export the folder (I do it) |

## Part D: Deep analysis + upload (the ONE-SHOT step)

*Why:* this produces the ISO-5055 results. With the trial it can be done for one application only, so do it only after Part C is OK.

1. Run the **deep analysis**. It can take from several minutes to an hour; do not put the PC to sleep.
2. **Upload** the results.
   - Online analyzer: automatic.
   - Offline analyzer: **Upload results** (top right of castimaging.io), choosing `DomiAffaire.casticr` from `%PROGRAMDATA%\CAST\CAST-Imaging-CLI\DomiAffaire\deep-analysis`.
3. **Don't record this part.** A 10-second clip of the progress bar is enough for the video.

## Part E: Explore the results before recording

1. **Open the application.** Open *DomiAffaire* in castimaging.io, then the summary page.
2. **Write down the counts.** Open each ISO-5055 quality factor and note **the number of violations per rule** (screenshot each list).
3. **Export, if possible.** Export the violations (CSV/report) if the trial allows it, and save the file in `iso5055/cast/results/`.
4. **Look for our own findings.** Look for the weaknesses our reviews found (`reports/03-review-iso.md`); IDs in brackets:

| Factor | Look for | Where in our code |
|---|---|---|
| Security | Hard-coded key (CWE-321/798) [S04] | `api/.../utils/JwtUtil.java:65` |
| Security | Unintended path: UI → DB without authentication (CWE-424/1057) [S14] | `chatapp` service |
| Security / Reliability | Unchecked return value (CWE-252), NULL dereference (CWE-476) [R01, R02] | `DomiAffaireServiceImpl.java` |
| Reliability | Empty-handling catch (CWE-390) [R09]; uncaught declared exceptions (CWE-248) [N11] | `ReservationServiceImpl.java:129`, controllers |
| Performance | DB calls in loops (CWE-1050) [P04]; too many data accesses per method (CWE-1073) [N01]; big data elements (CWE-1043) [N04] | `DeadlineServiceImpl.java`, `DomiAffaireServiceImpl.java` |
| Maintainability (if shown) | File > 1,000 lines (CWE-1080), copy-paste (CWE-1041), dead code (CWE-561) [M01–M03] | `DomiAffaireServiceImpl.java`, controllers |

5. **Note what CAST flags that we did not.** This is the key question of the study.

📸 **Send me** the screenshots and the export. I fill the `found_CAST` column of `findings.csv` and write `reports/05-cast-vs-claude.md`.

## Part F: Record

Follow [`video-script.md`](video-script.md). Preparation:
- **Focus mode on:** no notifications. Close other tabs and Discord.
- **Browser:** zoom 125 %, full-screen window (F11).
- **Snipping Tool:** **Win + Shift + R**, select the window, then click **Record**. Click the mic icon to turn your voice on.
- **Retakes are free.** The results stay online for the 30 days, so you can record as many times as needed.

## If something goes wrong
| Problem | What to do |
|---|---|
| The analyzer refuses to start / out of memory | Close Docker Desktop and other apps, then retry |
| Profiling shows far more lines than expected | Do not continue; send me the screenshot |
| Online upload fails | Use the offline analyzer and **Upload results** by hand |
| Trial expired or refused | Plan B: SonarQube demo (step 6) + say CAST is the only native ISO 5055 tool, citing CAST's docs |

## Sources
- CAST Imaging Express documentation:
  - [initial access](https://doc.castsoftware.com/imagingexpress/getting-started/initial-access/)
  - [requirements](https://doc.castsoftware.com/imagingexpress/technical-resources/requirements/)
  - [offline mode](https://doc.castsoftware.com/imagingexpress/how-to/offline/)
  - [explore](https://doc.castsoftware.com/imagingexpress/use-cases/explore/)
  - [improve](https://doc.castsoftware.com/imagingexpress/use-cases/improve/)
  - [video library](https://doc.castsoftware.com/imagingexpress/video-library/)
- CAST covered technologies: https://doc.castsoftware.com/technologies/covered-technos/
