# DomiAffaire: ISO/IEC 5055 source-code quality audit

This repository contains **DomiAffaire**, a business-domiciliation platform written by **Wassim Ouertani**. It also
contains an **ISO/IEC 5055:2021** source-code quality audit of that application, made for the course *Qualité du
logiciel* (Dr. Sana Ben Abdallah).

---

## 1. The application

DomiAffaire helps entrepreneurs in Tunisia **domicile their company** (get an official business address) and
**create their company**. It connects three kinds of users:

| Role | What they can do |
|---|---|
| **Visitor** | Browse the site, packs, FAQ and company-creation documents; sign up and sign in (including Google sign-in) |
| **Client** | Request a domiciliation and follow its status, request a consultation with an accountant, save favorite blog posts, chat, manage their profile. On mobile, the client can also reserve meeting rooms and get room recommendations |
| **Accountant** | Validate or reject consultation requests, write blog posts, chat with clients, manage their profile |
| **Admin** | Dashboard; manage clients (including archived ones), their documents, accountants, domiciliation requests, packs, rooms, reservations, blog categories, blog posts and FAQs |

### Architecture

```
 Angular web client (4200) ──REST──▶ Spring Boot API (8080) ──▶ MongoDB (27017, db "domi_db")
          │                                                        ▲
          └────WebSocket/STOMP──▶ Spring Boot chat service (8084) ──┘
 Flutter mobile client ──REST──▶ API (8080)  and  ──▶ Flask room-recommendation API (5000)
```

| Folder | Part | Technology |
|---|---|---|
| `app/api` | Main REST API: authentication (JWT + Google OAuth), domiciliation, consultations, reservations, blogs, files | Java 17, Spring Boot 3.1.10, Spring Security, Spring Data MongoDB |
| `app/chatapp` | Real-time chat service | Java 17, Spring Boot 3.1.11, WebSocket/STOMP, MongoDB |
| `app/web-client-07-06-2024` | Web front end | Angular 15, Tailwind CSS |
| `app/mobile-client-v1.0.4` | Mobile front end | Flutter (Dart ≥ 3.3) |
| `app/room-recommendation-system` | Room recommendation service (nearest-neighbours on past reservations), plus the notebooks used to build it | Python, Flask, pandas, scikit-learn |

---

## 2. Running the whole application

### Prerequisites
| Tool | Version | Used by |
|---|---|---|
| JDK | 17 or newer (tested with 21) | API, chat |
| Node.js + npm | 16/18 recommended for Angular 15 (works with 22) | web client |
| Docker Desktop | any recent | MongoDB (or install MongoDB 7 natively) |
| Python | 3.9+ | recommendation service (optional) |
| Flutter SDK | 3.19+ (Dart ≥ 3.3) | mobile client (optional) |
| Git | with `core.longpaths=true` on Windows | clone (some Angular paths exceed 260 characters) |

### Clone
```bash
git -c core.longpaths=true clone https://github.com/inesCherif/domiaffaire-iso5055-audit.git
cd domiaffaire-iso5055-audit/app
```

### Configuration
The API reads three values that are **not** stored in the repository: `LINK`, `GOOGLE_CLIENT_ID` and
`GOOGLE_CLIENT_SECRET` (Google OAuth). Provide them in one of two ways:
- as environment variables;
- in a file `app/api/config/application.properties`. Spring Boot loads it automatically when started from
  `app/api`, and `.gitignore` excludes it.

```properties
LINK=https://www.googleapis.com
GOOGLE_CLIENT_ID=<your Google OAuth client id>
GOOGLE_CLIENT_SECRET=<your Google OAuth client secret>
```
Placeholder values are enough to start the API. Only Google sign-in needs real ones.

### Start everything
Start the parts in this order, each in its own terminal.

```bash
# 1. MongoDB 7 (first time: creates the container; afterwards: docker start domi-mongo)
docker run -d --name domi-mongo -p 127.0.0.1:27017:27017 -v domi_mongo_data:/data/db mongo:7

# 2. Chat service → http://localhost:8084
cd app/chatapp
./mvnw spring-boot:run          # Windows cmd/PowerShell: mvnw.cmd spring-boot:run

# 3. REST API → http://localhost:8080
cd app/api
./mvnw spring-boot:run

# 4. Web client → http://localhost:4200
cd app/web-client-07-06-2024
npm install --legacy-peer-deps  # first time only (tinymce-angular 8 vs Angular 15 peer conflict)
npm start                       # = ng serve

# 5. (optional) Room-recommendation API → http://localhost:5000/recommend
cd app/room-recommendation-system
pip install flask flask-cors pandas numpy scipy scikit-learn
python FLASK_API.py

# 6. (optional) Mobile client, with an emulator or device connected
cd app/mobile-client-v1.0.4
flutter pub get
flutter run
```

Open **http://localhost:4200** and create an account with **Sign up**. The database starts empty.

### Stop
- Press `Ctrl+C` in each terminal.
- Then run `docker stop domi-mongo`. The data stays in the `domi_mongo_data` volume.

### Troubleshooting
| Symptom | Fix |
|---|---|
| `Filename too long` when cloning | `git config --global core.longpaths true` (Windows long paths must also be enabled) |
| `Port 8080 was already in use` | Start the API on another port: `./mvnw spring-boot:run -Dspring-boot.run.arguments="--server.port=8081"`. Then set `urlBackend` to that port in `web-client-07-06-2024/src/environments/environment.ts` |
| JVM: `insufficient memory` / `paging file is too small` | Limit the heap: `-Dspring-boot.run.jvmArguments="-Xmx384m"` (and `MAVEN_OPTS=-Xmx384m`) |
| `npm install` fails with `ERESOLVE` | Add `--legacy-peer-deps` |
| Mobile app can't reach the API from an Android emulator | The app uses `localhost`. On the emulator the host PC is `10.0.2.2` |

A detailed log of the first local run is in [`reports/01-run-app.md`](reports/01-run-app.md).

---

## 3. The ISO/IEC 5055 audit

ISO/IEC 5055 measures **4 characteristics** of source code: Security, Reliability, Performance Efficiency and
Maintainability. It does so by counting occurrences of CWE-based weaknesses. The same application is analysed by four
"analysts", and their results are compared:

| # | Analyst | Method |
|---|---|---|
| A | Claude Code, knowledge only | Manual code review from prior knowledge of ISO 5055 and CWE. No scanner, no web, no standard text. |
| B | Claude Code + ISO 5055 text | Full new review using the standard's weakness lists as the checklist |
| C | CAST Imaging | Specialized tool with native ISO 5055 support (free trial) |
| D | SonarQube Community | Widespread free static analyzer |

**Scope:** `app/api`, `app/chatapp` and `app/web-client-07-06-2024`. The mobile client and the recommendation service are
out of scope.

### Progress
| Step | Content | Output |
|---|---|---|
| 0 | Repository setup | this repository |
| 1 | Run the application locally | [`reports/01-run-app.md`](reports/01-run-app.md) |
| 2 | Review A: knowledge only | `reports/02-review-knowledge.*` |
| 3 | Review B: knowledge + ISO 5055 text | `reports/03-review-iso.*` |
| 4 | CAST preparation | `cast/` |
| 5 | CAST results vs Claude | `reports/05-cast-vs-claude.*` |
| 6 | SonarQube + final comparison | `sonar/`, `reports/06-final-comparison.*` |

`findings.csv` holds one row per weakness, with one column per analyst.

### Note on the standard
The ISO/IEC 5055 text is copyrighted by ISO and is **not** included in this repository.

---

## Credits
- **Application:** Wassim Ouertani. His original commit history is kept under `app/`.
- **Audit:** Ines Cherif, with the ISAMM team (Firas Chabouh, Rihab Gharbi, Wassim Ouertani).
