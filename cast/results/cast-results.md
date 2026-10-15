# CAST Imaging Express: results for DomiAffaire

**Analysis:** 2026-10-15, about 19:10–19:45 (deep analysis about 30 minutes). Results uploaded to castimaging.io.
**Input:** the clean copy described in [`../setup.md`](../setup.md): 27,998 lines, 444 files.
**Deep analysis coverage:** 154 `.ts`, 146 `.java`, 72 `.html`, 71 `.css`, 1 `.js` analysed; **0 not analysed**.

## Where the results are in the interface

CAST Imaging Express does not open on a list of issues like SonarQube does. It opens on an **architecture map**. The
ISO-5055 results are a layer on top of that map:

1. Left menu **Open View**, then **Architecture overview**.
2. Right panel **Display options**, then **Insights**.
3. Each **ISO-5055 … flaws** line has a switch. Turning it on circles the affected layer in red. Hovering over it shows the count.
4. The **document icon** next to a rule opens its documentation: description, rationale, a vulnerable sample, a
   **remediation sample** and references (CWE, OWASP, CISQ rule).

## ISO/IEC 5055 results

| Characteristic | CAST result |
|---|---|
| **Security** | **1 rule broken: "Avoid cross-site scripting through API requests"** on **2 objects**, in the *Exposed API* layer |
| **Performance efficiency** | **0**: "No Efficiency Structural Flaws were identified." |
| **Reliability** | **0**: "No Reliability Structural Flaws were identified." |
| **Maintainability** | **not available** in CAST Imaging Express (only Security, Performance efficiency and Reliability appear under Insights) |

**The rule broken:**
- **Reference:** CWE-79 (Improper Neutralization of Input During Web Page Generation, "Cross-site Scripting"), **CISQ rule ASCSM-CWE-79**. CWE-79 is one of the Security weaknesses of ISO/IEC 5055.
- **What it detects:** "code paths where data received from API requests is directly reflected back to the user's
  browser without proper sanitization or encoding", found "using static analysis and data-flow tracking".
- **Fix proposed by CAST:** encode the user's data before writing it into HTML (its sample uses `StringEscapeUtils.escapeHtml4`).

**Free-trial limit:** a banner says "Your free trial provides access to only limited numbers of the affected objects."
The counts above are what the trial shows.

## Match with our reviews (first reading)

Review A found the same weakness: **S19**, "Angular sanitizer bypassed on consultation details" (CWE-79, flagged
"in ISO 5055: Yes"). In the code, `bypassSecurityTrustHtml` is called in exactly **2 places**:
- `features/client/consultation/consultation.component.ts`;
- `features/accountant/consultation-validation/in-progress-consultations/in-progress-consultations.component.ts`.

These are very likely the **2 objects** CAST reports. *To confirm in the interface (open the 2 objects).*

## What CAST did not report

None of the ISO-relevant findings from review B appear in the trial view:
- the hard-coded JWT key (S04, CWE-321);
- the unauthenticated chat path (S14, CWE-424/1057);
- the 0 performance and 0 reliability results, compared with our estimate of 86 and 48 occurrences.

Possible reasons, to discuss in report 05:
1. The trial shows only part of the rules or objects.
2. CAST's rules are **data-flow paths across layers**, not line patterns, so they report far fewer, more certain issues.
3. Our count of 86 + 48 is an **expert estimate** with heuristics (see review B). It is not an automated, ISO-conformant count.
