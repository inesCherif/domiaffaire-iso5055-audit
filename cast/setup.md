# CAST Imaging: how the project was prepared, and why

This file records **what was done before the CAST analysis, and why**, so the analysis can be repeated and checked.
The click-by-click guide is in [`guide.md`](guide.md). The French video script is in [`video-script.md`](video-script.md).

## 1. Why CAST Imaging Express

- CAST is the only tool vendor that documents native **ISO/IEC 5055** support ("critical violations based on ISO-5055
  standards", listed by quality factor). It is analyst **C** in this audit.
- The free trial is enough for a student project: **30 days, 1 application, less than 250k lines of code**.
- **Constraint:** one application, and in practice **one shot**. Everything below aims to make that shot count.
- **Privacy:** the Analyzer runs on our PC. Only the structural analysis results are uploaded; the source code never leaves
  the machine (official docs, and shown on the Analyzer's first screen: "Your source code will never be uploaded").

Source: CAST Imaging Express documentation, doc.castsoftware.com/imagingexpress.

## 2. What we give CAST: a clean copy of the code

**Location:** `C:\Users\juba839\dev\cast\DomiAffaire\` (outside OneDrive and outside this repo).

**Why a separate copy, not `app/`?**
- `app/` stays exactly as Wassim wrote it. We never modify it.
- OneDrive syncs files while they are read, and Angular paths exceed 260 characters. A short local path avoids both problems.
- CAST should measure **the team's code**, not third-party code. Vendor files would add thousands of lines of violations
  that Wassim did not write, and would make the comparison with reviews A and B unfair.

**How it was made:**
1. `git archive` of the three in-scope folders: `app/api`, `app/chatapp`, `app/web-client-07-06-2024`.
   `git archive` exports only tracked files, so `node_modules/`, `target/` and local secrets are left out automatically.
2. Removed by hand, with the reason:

| Removed | Why |
|---|---|
| Unit tests (`src/test`, `*.spec.ts`), Cypress | ISO 5055 measures production code; reviews A and B did not review tests either |
| `web-client/src/assets` | Purchased "Midone" admin template plus jQuery/Bootstrap vendor files: third-party code |
| `.mvn/` and wrapper jars | Build tooling, binary |
| `package-lock.json` | Generated file, thousands of lines, no code |
| `postcss.config.js`, `webpack.mix.js` | Template build configuration, not application code |

3. **Out of scope:** `mobile-client-v1.0.4` (Flutter) and `room-recommendation-system` (Python), the same scope as reviews A and B.

**Result (checked 2026-10-15):**

| Measure | Value |
|---|---|
| Files | 466 (1.9 MB) |
| Java | 146 files, 5,876 non-blank lines |
| TypeScript | 154 files, 8,922 non-blank lines |
| HTML | 72 files, 10,356 non-blank lines |
| CSS | 72 files, 2,835 non-blank lines |
| **Total** | **about 28.5k non-blank lines**, far below the 250k trial limit |

**Secrets:** `application.properties` contains only placeholders such as `${GOOGLE_CLIENT_SECRET}`. The values that are
hard-coded in the Java source (the JWT key, finding S04) are left in on purpose: they are part of the code under audit,
and we want to see whether CAST detects them.

## 3. Why these settings in the Analyzer

| Setting | Value | Why |
|---|---|---|
| Source folder | `C:\Users\juba839\dev\cast\DomiAffaire` | The clean copy above, with the three folders at its root |
| Application name | `DomiAffaire` | CAST says the name **cannot be changed later**, so we use the application name, not a version |
| Profiling first | yes, then **stop and check** | Profiling is free and changes nothing. We check size and technologies before the one-shot deep analysis |
| Expected technologies | Java, Spring Boot/MVC/Data/Security, MongoDB, TypeScript/Angular, HTML/CSS | All listed as covered in CAST's docs (Angular 2–17, TypeScript extension 1.13) |

## 4. Machine preparation

- Windows 11, 15.4 GB RAM, Ryzen 5 5500H. CAST asks for 8 GB minimum.
- Before the deep analysis we close heavy apps (DomiAffaire's servers, `domi-mongo`, Docker Desktop, Discord, extra
  Chrome tabs), because the PC had only about 0.5 GB of free RAM during step 1.

## 5. What comes next

1. Profiling, then a screenshot check (guide, Part C).
2. Deep analysis and upload (guide, Part D).
3. Explore the results and record (guide, Parts E and F).
4. Fill the `found_CAST` column of `findings.csv` and write `reports/05-cast-vs-claude.md`.
