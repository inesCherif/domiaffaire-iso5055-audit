# Step 1: Running DomiAffaire locally

The goal was to prove the audited application is real and working before measuring it.

![DomiAffaire home page running locally](img/01-home.png)

## Result
| Part | Technology | URL | Status |
|---|---|---|---|
| Database | MongoDB 7 (Docker) | `127.0.0.1:27017`, database `domi_db` | ✅ running |
| API | Spring Boot 3.1.10, run on JDK 21 | http://localhost:8081 | ✅ started in about 4 s; public endpoints answer `200` |
| Chat service | Spring Boot 3.1.11 (WebSocket / STOMP) | http://localhost:8084 | ✅ started |
| Web client | Angular 15 (Node 22) | http://localhost:4200 | ✅ compiled successfully |

The database starts empty, because the project has no seed data. Accounts are created through **Sign up**.

## Where it runs and why
- **The app runs from a copy outside OneDrive:** `C:\Users\juba839\dev\domiaffaire-run`.
  - `node_modules` alone is about 1,600 packages. Building inside OneDrive would make it sync hundreds of MB.
  - The audit repository itself stays clean.
- **Long paths:** some Angular file paths exceed Windows' 260-character limit. Git needs `core.longpaths=true`, and Windows long-path support is already enabled.

## Configuration
The public code uses placeholders in `api/src/main/resources/application.properties`:
`${LINK}`, `${GOOGLE_CLIENT_ID}`, `${GOOGLE_CLIENT_SECRET}`.

- **Local values:** they are given in `app/api/config/application.properties`. Spring Boot automatically loads `./config/application.properties` from the working directory.
- **Git:** that file is in `.gitignore` and never committed.
- **Placeholders:** the values used locally are placeholders. Every feature works except Google sign-in, which needs the real Google OAuth values from the project author.

## Problems met and how they were solved
| Problem | Cause | Fix |
|---|---|---|
| `git clone` failed: "Filename too long" | Deep Angular folder paths, over 260 chars | `git -c core.longpaths=true clone ...` |
| API crashed: "insufficient memory … paging file is too small" | Docker's VM (about 4.4 GB) plus other apps left about 0.5 GB free; the JVM reserves a large heap by default | Give each JVM a fixed budget: `-Xms128m -Xmx384m`. Stop the unused SonarQube containers until step 6. |
| API: "Port 8080 was already in use" | A local Apache `httpd` (XAMPP/WAMP) already uses port 8080 | Run the API on **8081**, and point the web client there in `src/environments/environment.ts` (local copy only) |
| `npm install`: ERESOLVE peer-dependency conflict | `@tinymce/tinymce-angular@8` expects a newer Angular than 15.2 | `npm install --legacy-peer-deps` |
| `ng serve` stopped after compiling | It was launched through a PowerShell wrapper that exited | Start it with `node node_modules/@angular/cli/bin/ng.js serve` |

## Observations for the audit (no analysis yet)
These were noticed only by **running** the app, not by reviewing its code:
- **Outdated dependencies:** the npm peer-dependency conflict, and many deprecated packages reported by npm.
- **Swagger doesn't work:** the project uses **springfox**, which does not support Spring Boot 3, and `/swagger-ui` returns `403`.
- **API port 8080 is hard-coded** in the web client's environment file.

## How to start everything again
Order: Docker → MongoDB → chat → API → web. Run each block in its own terminal (Git Bash).

```bash
# 0. Start Docker Desktop from the Start menu and wait for "Engine running"

# 1. MongoDB (the container already exists; this just starts it)
docker start domi-mongo

# 2. Chat service (port 8084)
cd ~/dev/domiaffaire-run/app/chatapp
export JAVA_HOME="/c/Program Files/Eclipse Adoptium/jdk-21.0.12.101-hotspot"; export PATH="$JAVA_HOME/bin:$PATH"
./mvnw -o -DskipTests spring-boot:run -Dspring-boot.run.jvmArguments="-Xmx384m"

# 3. API (port 8081)
cd ~/dev/domiaffaire-run/app/api
export JAVA_HOME="/c/Program Files/Eclipse Adoptium/jdk-21.0.12.101-hotspot"; export PATH="$JAVA_HOME/bin:$PATH"
./mvnw -o -DskipTests spring-boot:run -Dspring-boot.run.jvmArguments="-Xmx384m" -Dspring-boot.run.arguments="--server.port=8081"

# 4. Web client (port 4200), then open http://localhost:4200
cd ~/dev/domiaffaire-run/app/web-client-07-06-2024
node node_modules/@angular/cli/bin/ng.js serve --port 4200
```

**To stop:**
- press `Ctrl+C` in each terminal;
- then run `docker stop domi-mongo`.
