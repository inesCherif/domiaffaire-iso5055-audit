# Step 3: Review B, ISO/IEC 5055 review with the standard in hand

**Analyst:** Claude Code. **Date:** 2026-10-15. **Scope:** same as step 2 (`app/api`, `app/chatapp`, Angular web client).

## Method
1. **Read the standard first.** The full text of *ISO/IEC 5055:2021* (248 pages) was read: scope (clause 1),
   conformance (2), the four weakness tables (6.4–6.7), the weakness list (7), the detection patterns used here (8)
   and the calculation (9).
2. **Checked only the publisher's sources.** CISQ (it-cisq.org), which authored the measures, and OMG
   (omg.org/spec/ASCQM), which published the specification adopted by ISO. No other web source was used.
3. **Re-reviewed all the code with the standard as a checklist.**
   - Every one of the 61 findings of review A received a verdict.
   - The code was searched again for the ISO weaknesses review A did not look for.
   - The standard's default thresholds were applied: 1,000 lines per file, cyclomatic complexity 20, 5 outward calls,
     2/7 data accesses, 7 parameters, 90 % similarity, 2–5 % commented-out code.
   - Per-method counts were made with a small script implementing those definitions.

> **Important limit.** ISO/IEC 5055 clause 2 requires measurement to be *automated, objective, transparent and
> verifiable*. The counts below are a careful **expert estimate**, not a conformant ISO measurement. Steps 5 and 6 (CAST,
> SonarQube) provide the automated counts.

## What the standard says (key facts used)
- **The 4 characteristics:**
  - Maintainability: 29 weaknesses;
  - Performance Efficiency: 19 quality measure elements (CWE-1060 appears twice in its list, so 18 distinct CWEs);
  - Reliability: 74;
  - Security: 73 (36 parents + 37 contributing).
- **A weakness may belong to several characteristics.** For example, CWE-772 is in Performance, Reliability and Security.
- **Score = count of occurrences.** For each characteristic: "detection pattern score is the count of occurrences,
  weakness score is its detection pattern score, quality characteristic score is the sum of its weakness scores" (clause 9).
  CISQ adds that counts "may then be transformed into comparative measures such as the density of weaknesses".
- **The measures are "correlated measures rather than absolute measures" (1.2).** They do not measure all possible
  weaknesses, only those experts judged most severe.
- **Access control is outside the list.** The ISO 5055 security list has **no authorization weaknesses** (no CWE-284/285/639/862/863, no CWE-200).
- **CWE-424 / CWE-1057 have an architectural pattern.** Their pattern 8.45 "Ban Unintended Paths" covers, per CISQ, "a path from the user
  interface directly to the database without passing through user authentication routines".
- **Two small inconsistencies in the text itself:**
  - The CWE-1085 threshold is 2 % in Table 1 but 5 % in pattern 8.115.
  - Clause 7 cites patterns as "8.2.x" while clause 8 numbers them "8.x".

## Result 1: how good was the knowledge-only review?

| Verdict on the 61 findings of review A | Count |
|---|---|
| ✅ ISO 5055 weakness, correct CWE | 12 |
| ⚠️ Real issue, counted by ISO under another CWE, or ISO CWE whose detection pattern does not apply here | 16 |
| ❌ Real issue but **not** an ISO 5055 weakness | 33 |

| Characteristic (as labelled in A) | ✅ | ⚠️ | ❌ |
|---|---|---|---|
| Security | 2 | 3 | 16 |
| Reliability | 5 | 6 | 7 |
| Performance Efficiency | 1 | 3 | 4 |
| Maintainability | 4 | 4 | 6 |

- **Of the 5 Critical findings of review A, only 2 are counted by ISO 5055**
  (S04, S14): the hard-coded JWT key (CWE-321) and the unauthenticated chat path (CWE-424/1057).
  The broken access control (S07, S08) is **invisible to the ISO 5055 measure**.
- **Recalled CWE numbers were often outside the standard.** CWE-639, 862, 200, 307, 942, 489, 1104 and 1106 do not
  appear in ISO 5055. Several right ideas carried the wrong CWE (e.g. Optional.get() is CWE-252 in ISO terms, not 754).
- **Thresholds matter.**
  - "Complex methods" (M10) is not an ISO weakness here: the maximum cyclomatic complexity is 11, below 20.
  - "Too many parameters" (M11) is not one either: 7 is not *more than* 7.
- **Reading the standard found 15 weaknesses review A had missed** (N01–N17: 14 counted today, 1 potential;
  N12–N13 do not exist because they were merged into R01 and R16). They are mostly counting rules:
  data accesses per method, fan-out, string concatenation, switch without default, missing security logging,
  unchecked loop input.

## Result 2: the ISO/IEC 5055 measure (expert estimate)

| Characteristic | Occurrences | Density per KLOC* | Main contributors |
|---|---|---|---|
| Maintainability | **182** | 12.6 | CWE-1041 (77), CWE-1048 (68), CWE-561 (14) |
| Performance Efficiency | **86** | 5.9 | CWE-1046 (42), CWE-1073 (29), CWE-1050 (8) |
| Reliability | **48** | 3.3 | CWE-476 (17), CWE-252 (13), CWE-248 (8) |
| Security | **31** | 2.1 | CWE-252 (13), CWE-783 (6), CWE-571 (3) |

\* 14.5 KLOC = 5,747 Java + 8,710 TypeScript non-blank, non-comment lines. A weakness listed in several characteristics
is counted in each, as the standard's tables require. The counts are not added across characteristics.

**Maintainability**: CWE-1041 Redundant code (copy-paste): 77; CWE-1048 Excessive fan-out: 68; CWE-561 Dead code: 14; CWE-783 Operator precedence logic error: 6; CWE-1051 Hard-coded network resource data: 5; CWE-571 Expression always true: 3; CWE-1052 Hard-coded literals in initialization: 3; CWE-478 Missing default case in switch: 2; CWE-1054 Layer-skipping call: 1; CWE-1080 File > 1,000 lines: 1; CWE-1084 Method > 7 data accesses: 1; CWE-1085 Excessive commented-out code: 1

**Performance Efficiency**: CWE-1046 String concatenation: 42; CWE-1073 Method > 2 data accesses: 29; CWE-1050 Resource use inside loops: 8; CWE-1043 Data element > 5 non-primitive members: 3; CWE-1057 Data access outside data manager: 2; CWE-424 Unprotected alternate path: 1; CWE-772 Resource not released: 1

**Reliability**: CWE-476 NULL dereference: 17; CWE-252 Unchecked return value: 13; CWE-248 Uncaught exception: 8; CWE-1051 Hard-coded network resource data: 5; CWE-390 Error detected without action: 2; CWE-392 Missing report of error: 1; CWE-424 Unprotected alternate path: 1; CWE-772 Resource not released: 1

**Security**: CWE-252 Unchecked return value: 13; CWE-783 Operator precedence logic error: 6; CWE-571 Expression always true: 3; CWE-1057 Data access outside data manager: 2; CWE-321/798 Hard-coded cryptographic key: 1; CWE-79 Cross-site scripting: 1; CWE-424 Unprotected alternate path: 1; CWE-477 Obsolete function: 1; CWE-606 Unchecked input for loop condition: 1; CWE-772 Resource not released: 1; CWE-778 Insufficient logging: 1

## Verdict on every finding of review A

| ID | A said | Verdict | ISO CWE / clause | Why |
|---|---|---|---|---|
| S01 | Public endpoint returns every user with password hash (CWE-200 / CWE-862) | ❌ not in ISO 5055 | - | CWE-200 and CWE-862 are not in any ISO 5055 list (Tables 1-4). Real, critical issue, but outside the measure. |
| S02 | Public lookup of any user by e-mail (enumeration + data exposure) (CWE-200 / CWE-204) | ❌ not in ISO 5055 | - | CWE-200/204 are not ISO 5055 weaknesses. |
| S03 | Password hashes leak through DTOs that embed User entities (CWE-200) | ❌ not in ISO 5055 | - | CWE-200 is not an ISO 5055 weakness. |
| S04 | Hard-coded JWT signing key (CWE-798 (CWE-321)) | ✅ in ISO 5055 | CWE-321 (child of CWE-798), 7.4.17 / 7.4.56, pattern 8.44 | The literal key is passed to the signing primitive: exactly 'Ban Hard-Coded Literals used to Connect to Resource' ('covers ... encryption keys, tokens'). |
| S05 | Hard-coded accountant registration code "abcd" (CWE-798) | ⚠️ partly / other CWE | CWE-798 (7.4.56) - not counted | Same weakness family, but pattern 8.44 needs the literal to reach a resource-access call; here "abcd" is only compared. |
| S06 | Admin credentials left in comments (CWE-615 / CWE-798) | ❌ not in ISO 5055 | - | Credentials inside comments are not code; the block is counted instead as commented-out code (CWE-1085, see N07). |
| S07 | Any client or accountant can delete any account (CWE-639 / CWE-862) | ❌ not in ISO 5055 | - | CWE-639/862 (missing authorization) are not in ISO 5055. |
| S08 | Profile update by path id: overwrite other users and their role (CWE-639) | ❌ not in ISO 5055 | - | CWE-639 is not in ISO 5055. |
| S09 | Clients can read other clients' domiciliation files (CWE-639) | ❌ not in ISO 5055 | - | CWE-639 is not in ISO 5055. |
| S10 | Clients can cancel other clients' requests (CWE-639) | ❌ not in ISO 5055 | - | CWE-639 is not in ISO 5055. |
| S11 | Clients can accept/protest contracts of other clients (CWE-639) | ❌ not in ISO 5055 | - | CWE-639 is not in ISO 5055. |
| S12 | Any client/accountant can read any chat (CWE-639) | ❌ not in ISO 5055 | - | CWE-639 is not in ISO 5055. |
| S13 | Accountants can modify or delete anyone's blog posts (CWE-639 / CWE-862) | ❌ not in ISO 5055 | - | CWE-639/862 are not in ISO 5055. |
| S14 | Chat service has no authentication; sender id is trusted from the client (CWE-306 / CWE-290) | ⚠️ partly / other CWE | CWE-424 + CWE-1057, 7.4.23 / 7.4.71, pattern 8.45 'Ban Unintended Paths' | Re-classified. CISQ describes this pattern as 'a path from the user interface directly to the database without passing through user authentication routines': the chat service is exactly that. Counted once in Performance, Reliability (424) and Security. |
| S15 | CORS allows any origin and any header (CWE-942) | ❌ not in ISO 5055 | - | CWE-942 is not in ISO 5055. |
| S16 | No protection against password guessing on login (CWE-307) | ❌ not in ISO 5055 | - | CWE-307 is not in ISO 5055. |
| S17 | Upload checks trust the client Content-Type (CWE-434) | ⚠️ partly / other CWE | CWE-434 (7.4.24) - not counted | CWE-434 is listed, but its only pattern (8.86) needs the upload to reach a file-path operation; files go to MongoDB, so 0 occurrences. |
| S18 | JSON built by string concatenation with untrusted text (CWE-116) | ❌ not in ISO 5055 | - | CWE-116 is not in ISO 5055. |
| S19 | Angular sanitizer bypassed on consultation details (CWE-79) | ✅ in ISO 5055 | CWE-79, 7.4.55, pattern 8.91 | Stored user input reaches the page after the vetted sanitizer is bypassed (bypassSecurityTrustHtml). |
| S20 | OAuth client secret was in the properties file (now a placeholder) (CWE-798) | ❌ not in ISO 5055 | - | The public code uses a placeholder; a properties value is configuration, not a code literal: 0 occurrences. |
| S21 | Chat content and data written to the browser console (CWE-532) | ❌ not in ISO 5055 | - | CWE-532 is not in ISO 5055. |
| R01 | Optional.get() without check: unknown ids crash with HTTP 500 (CWE-754 (CWE-476)) | ⚠️ partly / other CWE | CWE-252 Unchecked Return Value, 7.3.13 / 7.4.15 | Re-classified: the Optional returned by findById is used without checking it. Counted in Reliability and Security (13 occurrences). |
| R02 | String fields compared without null check (CWE-476) | ✅ in ISO 5055 | CWE-476, 7.3.27, pattern 8.11 | Dereference without a NULL check (15 occurrences). |
| R03 | Operator-precedence bug in every file-type check (CWE-783) | ✅ in ISO 5055 | CWE-783, 7.1.8 / 7.4.50 | Operator-precedence logic error (6 occurrences); ISO counts it in Maintainability and Security. |
| R04 | Contract acceptance can crash and poison the scheduler (CWE-476) | ✅ in ISO 5055 | CWE-476, 7.3.27 | 2 occurrences. |
| R05 | Reminder/overdue flag logic is inconsistent (CWE-670) | ❌ not in ISO 5055 | - | CWE-670 is not in ISO 5055. |
| R06 | Room double-booking: overlap check only matches identical slots (CWE-697) | ❌ not in ISO 5055 | - | CWE-697 is not in ISO 5055. |
| R07 | Money computed with float (CWE-681 / CWE-1339) | ⚠️ partly / other CWE | CWE-681 / CWE-682 listed - not counted | Patterns 8.20/8.48 target incompatible conversions without a cast; float to double is a legal widening, so it is not flagged although the money values are imprecise. |
| R08 | Hard-coded absolute Windows paths of the author's PC (none certain) | ❌ not in ISO 5055 | - | A file path is not a network resource (CWE-1051) and is a call argument, not an initialization (CWE-1052). |
| R09 | Exceptions swallowed with printStackTrace (CWE-390) | ✅ in ISO 5055 | CWE-390, 7.3.16, pattern 8.23 | Catch block that neither re-throws nor returns the error (2 occurrences). |
| R10 | Lombok @Builder drops field defaults (CWE-665) | ⚠️ partly / other CWE | CWE-665 (7.3.73) - not counted | The faulty code is generated by Lombok, not present in the source that ISO 5055 analyses. |
| R11 | Seed data parsed wrongly and re-written at every start (CWE-20) | ⚠️ partly / other CWE | CWE-1052, 7.1.21, pattern 8.130 | The parsing bug is not an ISO weakness, but the hard-coded data literal is (see N09). |
| R12 | Bad-word filter rejects normal business words (CWE-697) | ❌ not in ISO 5055 | - | CWE-697 is not in ISO 5055. |
| R13 | Uncaught JWT and login exceptions return 500 (CWE-248 / CWE-755) | ⚠️ partly / other CWE | CWE-248 (7.3.12) - not counted here | Pattern 8.66 needs a method that declares the exception; JwtException is unchecked. Declared IOExceptions that are not caught are counted in N11. |
| R14 | Possible infinite recursion in toString/hashCode (CWE-674) | ❌ not in ISO 5055 | - | CWE-674 is not in ISO 5055. |
| R15 | Front end never releases subscriptions or the WebSocket (CWE-772 / CWE-401) | ✅ in ISO 5055 | CWE-772, 7.2.4 / 7.3.44 / 7.4.46 | The STOMP connection is never released (1 occurrence, counted in Performance, Reliability and Security). |
| R16 | Silent failures and broken features (CWE-754) | ⚠️ partly / other CWE | CWE-392, 7.3.18 | Re-classified: changePassword encounters an error (unknown id) and reports nothing (1 occurrence). |
| R17 | Generic RuntimeException wrapping and malformed error bodies (CWE-397) | ❌ not in ISO 5055 | - | CWE-397 is not in ISO 5055. |
| R18 | Phone-number regex has a broken character class (CWE-185) | ❌ not in ISO 5055 | - | CWE-185 is not in ISO 5055. |
| P01 | Scheduler reloads all deadlines every second (CWE-1050) | ⚠️ partly / other CWE | CWE-1050, 7.2.18, pattern 8.107 | Running every second is not itself an ISO weakness; the database writes inside its loop are (counted in P04). |
| P02 | File contents stored inside documents and sent in every list (CWE-1049 (approx.)) | ❌ not in ISO 5055 | - | CWE-1049 needs SQL joins/sub-queries on 1,000,000-row tables; not applicable. Related CWE-1043 is counted in N04. |
| P03 | N+1 queries on deadlines (CWE-1060 (approx.)) | ⚠️ partly / other CWE | CWE-1050, 7.2.18 | Re-classified: one query per loop turn = resource use inside a loop (CWE-1060 is about stored procedures). |
| P04 | Database calls inside loops (CWE-1050) | ✅ in ISO 5055 | CWE-1050, 7.2.18, pattern 8.107 | 8 database calls inside loops in total (with P01 and P03). |
| P05 | Full collection scans and in-memory filtering (CWE-1049 (approx.)) | ❌ not in ISO 5055 | - | CWE-1049 is not applicable (no SQL, small tables); the many queries per method are counted as CWE-1073 (N01). |
| P06 | Pack embeds full User documents (unbounded growth) (none certain) | ❌ not in ISO 5055 | - | Embedding users in Pack is a design issue; Pack has only one non-primitive field, below the CWE-1043 threshold of 5. |
| P07 | Chat history list grows forever and is rewritten on each message (CWE-1050 (approx.)) | ⚠️ partly / other CWE | CWE-1073, 7.2.6 | Re-classified: sendMessage makes 4 data accesses (threshold 2). |
| P08 | No pagination on any list endpoint (CWE-1049 (approx.)) | ❌ not in ISO 5055 | - | Missing pagination is not an ISO 5055 weakness. |
| M01 | God class: DomiAffaireServiceImpl (CWE-1080 / CWE-1048) | ✅ in ISO 5055 | CWE-1080 (7.1.26) + CWE-1048 (7.1.22) | 1,585 lines > 1,000; most of its methods exceed 5 outward calls (N03). |
| M02 | Heavy code duplication (CWE-1041) | ✅ in ISO 5055 | CWE-1041, 7.1.18, pattern 8.117 | 47 Java method pairs are more than 90 % similar (63 of 258 methods), plus 31 copies of the same error handler in Angular. |
| M03 | Dead and commented-out code (CWE-561 / CWE-563) | ✅ in ISO 5055 | CWE-561 (7.1.5) + CWE-1085 (7.1.24) | 11 never-called methods + 3 unreachable 'return null' (after always-true tests); CWE-563 (unused variables) is not in ISO 5055. |
| M04 | Conditions that are always true (CWE-571) | ✅ in ISO 5055 | CWE-571, 7.1.7 / 7.4.34 | 3 occurrences; counted in Maintainability and Security. |
| M05 | Layering bypassed: controllers use repositories and concrete classes (CWE-1057) | ⚠️ partly / other CWE | CWE-1054 (7.1.11) / CWE-1057 (7.2.7, 7.4.71) | Re-classified: controller -> repository skips the service layer. ISO puts CWE-1057 in Performance and Security, not Maintainability. |
| M06 | Magic numbers and hard-coded literals (CWE-1106) | ⚠️ partly / other CWE | CWE-1051 (7.1.14) + CWE-1052 (7.1.21) | CWE-1106 is not in ISO 5055; the hard-coded URLs and literals are counted as 1051/1052 (N08, N09). |
| M07 | Same domain model duplicated in two services (CWE-1041) | ⚠️ partly / other CWE | CWE-1041 | Duplicated classes are not counted as such; their duplicated methods are (in M02). |
| M08 | Outdated, conflicting or incompatible dependencies (CWE-1104) | ⚠️ partly / other CWE | CWE-477, 7.4.27, pattern 8.94 | CWE-1104 is not in ISO 5055; the deprecated BigDecimal.ROUND_HALF_UP call is (N16). 'Deprecated libraries' requires a list as input. |
| M09 | Debug output left in code (CWE-489) | ❌ not in ISO 5055 | - | CWE-489 is not in ISO 5055. |
| M10 | Long, deeply nested methods (CWE-1121) | ❌ not in ISO 5055 | CWE-1121 threshold not reached | Highest cyclomatic complexity found is 11 (checkDeadlines); the ISO threshold is 20. |
| M11 | Too many parameters (CWE-1064) | ❌ not in ISO 5055 | CWE-1064 threshold not reached | 7 parameters; the ISO threshold is 'more than 7'. |
| M12 | Unclear or misleading text in code (none) | ❌ not in ISO 5055 | - | Not an ISO 5055 weakness. |
| M13 | State changes through HTTP GET (none) | ❌ not in ISO 5055 | - | Not an ISO 5055 weakness. |
| M14 | Almost no automated tests (none) | ❌ not in ISO 5055 | - | Test coverage is not measured by ISO 5055. |

## New findings from review B

| ID | Characteristic | Finding | ISO CWE / clause / pattern | Occurrences | Location |
|---|---|---|---|---|---|
| N01 | Performance Efficiency | Methods with more than 2 data accesses: 29 methods send 3 to 9 repository calls each instead of one efficient query. | CWE-1073, 7.2.6, pattern 8.110 (threshold 2) | 29 | `api/…/services/DomiAffaireServiceImpl.java (25 methods), DeadlineServiceImpl.java:45, ReservationServiceImpl.java:44,77; chatapp/…/services/WebSocketService.java:25` |
| N02 | Maintainability | Method with more than 7 data accesses: sendDomiciliationRequestPMTransfert: 1 user lookup + 6 file saves + 1 pack lookup + 1 save = 9. | CWE-1084, 7.1.13, pattern 8.119 (threshold 7) | 1 | `api/…/services/DomiAffaireServiceImpl.java:501` |
| N03 | Maintainability | Methods with more than 5 outward calls (fan-out): Heuristic count of distinct calls on other objects; includes getters, so it is an upper estimate. | CWE-1048, 7.1.22, pattern 8.128 (threshold 5) | 68 | `api/…/services/*, controllers, chatapp/…/services` |
| N04 | Performance Efficiency | Data elements aggregating more than 5 non-primitive elements: Up to 14 File/User/Pack/Deadline/Response references in one document (enums and dates not counted). | CWE-1043, 7.2.8, pattern 8.108 (threshold 5) | 3 | `api/…/entities/DomiciliationRequest.java; dto/DomiciliationRequestDTO.java; dto/DomiciliationDTO.java` |
| N05 | Performance Efficiency | Text built by incremental concatenation: Immutable strings rebuilt in loops instead of using join/builder. | CWE-1046, 7.2.12, pattern 8.111 | 42 | `web/… (41 'errorMessage +=' in 31 files); api/…/services/DomiAffaireServiceImpl.java:1533` |
| N06 | Maintainability | Switch statements without default case: Unknown actions are silently ignored. | CWE-478, 7.1.2, pattern 8.136 | 2 | `web/…/features/admin/clients-documents/add-files/add-files.component.ts:38,65` |
| N07 | Maintainability | Method with excessive commented-out code: Table 1 sets 2 % (3 methods exceed it), pattern 8.115 sets 5 % (1 method); the stricter-consistent count 1 is used. | CWE-1085, 7.1.24, pattern 8.115 | 1 | `api/…/ApiApplication.java:34 (87 of 134 lines)` |
| N08 | Maintainability; Reliability | Hard-coded network resource identifiers: Origins and backend URLs written as literals (localhost:4200/8080/8084). | CWE-1051, 7.1.14 / 7.3.65, pattern 8.44 | 5 | `api/…/config/WebSocketConfiguration.java:25; controllers/ClientController.java:28; chatapp/…/config/WebSocketConfiguration.java:29; web-client environment.ts:3-4` |
| N09 | Maintainability | Hard-coded literals used to initialise data: Seed data and word lists initialised from literals instead of configuration. | CWE-1052, 7.1.21, pattern 8.130 | 3 | `api/…/ApiApplication.java:143; api/…/validators/NoBadWordsValidator.java; chatapp/…/validators/NoBadWordsValidator.java` |
| N10 | Maintainability | Layer-skipping call: controller uses repository: Controller -> repository bypasses the service layer (also CWE-1057 in Performance/Security, counted with S14). | CWE-1054, 7.1.11, pattern 8.45 | 1 | `api/…/controllers/AuthController.java:39,84,107` |
| N11 | Reliability | Declared exceptions not caught by the caller: Service methods declared 'throws IOException' are called without catching it; the framework returns a raw 500. | CWE-248, 7.3.12, pattern 8.66 | 8 | `api/…/controllers/AdminController.java:108,383,415; AccountantController.java:136,168; ClientController.java:120,131,158` |
| N14 | Security | User input controls a loop bound: addReservation loops over a client-supplied list of slots with no size limit (one DB write per slot). | CWE-606, 7.4.35, pattern 8.98 | 1 | `api/…/services/ReservationServiceImpl.java:53` |
| N15 | Security | Caught security exception not logged: BadCredentialsException is caught and answered with 401 but never logged, so failed logins leave no trace. | CWE-778, 7.4.48, pattern 8.100 | 1 | `api/…/controllers/AuthController.java:98` |
| N16 | Security | Use of an obsolete function: BigDecimal.ROUND_HALF_UP is deprecated (use RoundingMode.HALF_UP). | CWE-477, 7.4.27, pattern 8.94 | 1 | `api/…/services/DomiAffaireServiceImpl.java:864` |
| N17 | Performance Efficiency | Query on a field without index (potential): No @Indexed on email; counts only once the collection exceeds 500 rows (threshold), so 0 today. | CWE-1067, 7.2.15, pattern 8.104 | 0 | `api/…/repositories/UserRepository.java (findFirstByEmail); entities/User.java (email)` |

## Conclusions for the talk
1. **ISO 5055 is a structural-quality measure, not a full security audit.** The most dangerous problems of this
   application (anyone can delete or edit other users, read their ID cards) are authorization flaws, which the
   standard does not list. That matches its own scope: "correlated measures rather than absolute measures".
2. **The standard is precise where knowledge is vague.** Exact CWE IDs, exact thresholds and an exact counting rule
   turned 'feels complex' into 'not a weakness (11 < 20)' and 'many queries' into '29 occurrences of CWE-1073'.
3. **Counting by hand is not ISO-conformant (clause 2).** It is slow and approximate. Specialized tools are needed;
   steps 5 (CAST) and 6 (SonarQube) test that.

## Sources
- ISO/IEC 5055:2021(E), *Information technology — Software measurement — Software quality measurement — Automated source code quality measures*, first edition 2021-03 (local copy, not redistributed).
- CISQ, *Software Quality Standards – ISO 5055*: https://www.it-cisq.org/standards/code-quality-standards/
- OMG, *Automated Source Code Quality Measures (ASCQM) 1.0*, formal/20-01-02: https://www.omg.org/spec/ASCQM/1.0/About-ASCQM
