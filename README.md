# DomiAffaire: ISO/IEC 5055 source-code quality audit

This study audits one real application with four "analysts", against the
**ISO/IEC 5055:2021** standard (*Automated source code quality measures*). It was made for the course
*Qualité du logiciel* (Dr. Sana Ben Abdallah).

| # | Analyst | Method |
|---|---|---|
| A | Claude Code, knowledge only | Manual code review from prior knowledge of ISO 5055 and CWE. No scanner, no web, no standard text. |
| B | Claude Code + ISO 5055 text | Full new review using the standard's weakness lists as the checklist. |
| C | CAST Imaging | Specialized tool with native ISO 5055 support (free trial). |
| D | SonarQube Community | Widespread free static analyzer. |

ISO/IEC 5055 measures **4 characteristics**: Security, Reliability, Performance Efficiency and Maintainability. It
does so by counting occurrences of CWE-based weaknesses in the source code.

## The audited application
`app/` is **DomiAffaire**, written by **Wassim Ouertani**, with its original commit history kept. It is a business
domiciliation platform made of:
- `app/api`: Spring Boot 3.1 REST API (Java 17, MongoDB, JWT);
- `app/chatapp`: Spring Boot WebSocket chat service;
- `app/web-client-07-06-2024`: Angular 15 front end.

Out of scope: `mobile-client-v1.0.4` (Flutter) and `room-recommendation-system` (Python notebooks).

## Progress
| Step | Content | Output |
|---|---|---|
| 0 | Repository setup | this repo |
| 1 | Run the application locally | `reports/01-run-app.md` |
| 2 | Review A: knowledge only | `reports/02-review-knowledge.*` |
| 3 | Review B: knowledge + ISO 5055 text | `reports/03-review-iso.*` |
| 4 | CAST preparation | `cast/` |
| 5 | CAST results vs Claude | `reports/05-cast-vs-claude.*` |
| 6 | SonarQube + final comparison | `sonar/`, `reports/06-final-comparison.*` |

`findings.csv` holds one row per weakness, with one column per analyst.

## Note on the standard
The ISO/IEC 5055 text is copyrighted by ISO and is **not** included in this repository.
