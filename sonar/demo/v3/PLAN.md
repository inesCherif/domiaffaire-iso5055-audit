# SonarQube beginner tutorial, v3 (real screen)

Audience: Ines's friends. They have Docker Desktop, but no SonarQube and no idea how it works. After this video they
must be able to do everything on their own project, with no YouTube needed.

## Decisions (Ines, 2026-10-19)
- English voice **af_heart** (Kokoro) + English burned-in subtitles (every spoken word). No AI slides.
- Real screen only: ffmpeg records the real desktop; the real Windows cursor is moved by a script (slow, visible).
  The screen **freezes** while the voice finishes explaining, then the action continues.
- Montage on top of the real screen: zoom on the important area, arrows/boxes, short on-screen notes (not only subtitles).
- Install: **docker-compose + PostgreSQL**, the official SonarSource example
  (github.com/SonarSource/docker-sonarqube, example-compose-files/sq-with-postgres), linked from docs.sonarsource.com.
  Plus 3 memory lines for small laptops, explained.
- File editor: **Antigravity**.
- Browser: a **new, clean Chrome profile** "Ines Cherif" (no private tabs, bookmarks or history).
- Password and token: **blurred**, with a full explanation of what they are and why they are needed. The token is revoked at the end.
  Also blurred: any code line with the JWT key or the admin password (JwtUtil.java, ApiApplication.java).
- Old SonarQube installs deleted (containers, volumes, sonarqube and scanner images). postgres:17 stays because the
  stray elastic_hellman container uses it, so the video shows that it is "already present".
- Workflow: one chapter at a time. I record it, add voice, subtitles and notes, Ines reviews, then the next chapter. At the end, join them.
- Demo project: a clean copy at C:\Users\juba839\dev\demo\DomiAffaire (api, chatapp, web-client). The repo's app/ is never touched.

## Chapters
1. **Get SonarQube.** What SonarQube is (in one sentence, on the real site). Then docs.sonarsource.com: the Community Build,
   install from the Docker image, and the official compose example on GitHub.
2. **Write docker-compose.yml.** Create the folder, open it in Antigravity, paste the example, and explain every block
   (the 2 services, the database login, volumes, the port, healthcheck). Add the memory lines.
3. **Start it.** In PowerShell, run `docker compose up -d`: the download, then the 2 containers in Docker Desktop, the logs, and
   "SonarQube is operational".
4. **First login.** localhost:9000, admin/admin, then the forced password change (blurred, and why). A tour of the empty server.
5. **Project 1: web client (Docker scanner).** Create a local project, choose its key, then the baseline. Generate the token (blurred, what and why).
   Sonar's wizard shows the command for "Other". Run sonar-scanner-cli in Docker and watch the log, then "ANALYSIS SUCCESSFUL".
6. **Project 2: Java API (Maven).** Same wizard, but choose "Maven". Compile first (why Sonar needs the .class files), then the wizard's mvn command.
7. **Read the results.** The Quality Gate, the Overview, and the new/overall code. The 3 software qualities and the severities. The Issues list, its filters,
   and one issue in detail (why + how to fix). Security Hotspots, Measures, Duplications, Code, and Rules.
8. **ISO/IEC 5055 with SonarQube.** The official CISQ page listing the ISO 5055 CWEs. In Sonar, filter by CWE and match
   the issues. Then Sonar's qualities vs ISO's 4 characteristics (Sonar has no Performance), and what Sonar can't prove.
9. **Whole DomiAffaire in one scan.** A third project with everything. Compare it with projects 1+2: what is the same, what differs, and
   errors that were missed or found only in one way.
10. **Clean up.** Revoke the token, `docker compose stop` / `down`, and what happens to the data.

## Before each recording, Ines does
1. Open Docker Desktop herself (the auto-mode check blocks me from starting it).
2. Turn on Windows "Do not disturb" (no pop-ups in the video).
3. Say GO, then do not touch the mouse or keyboard until I say done (each clip is about 2 to 10 min).
