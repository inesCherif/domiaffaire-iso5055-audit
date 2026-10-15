# Step 2: Review A, ISO/IEC 5055 review from knowledge only

**Analyst:** Claude Code (AI coding assistant), reading the source code. **Date:** 2026-10-15.
**Scope:** `app/api` and `app/chatapp` (all Java, about 6,800 lines), plus the Angular services, guards and
risky templates of `app/web-client-07-06-2024`.

## Method and rules
- **Allowed:** reading the code (file read and text search), and the analyst's own prior knowledge of ISO/IEC 5055 and of the CWE list.
- **Not allowed:** static-analysis tools, the internet, the text of the ISO/IEC 5055 standard, and the team's earlier material.
- **Honesty labels:**
  - `seen during planning`: noticed before the review started (CORS, OAuth secret).
  - `seen during step 1`: noticed while making the app run (dependency problems, hard-coded API URL).
- **CWE numbers are written from memory.** The column *In ISO 5055? (guess)* is the analyst's belief, not a check.
  Step 3 verifies both against the standard.
- **Not dynamically tested.** Every finding comes from reading the code. Severity is the analyst's judgement.

## Summary

| Characteristic | Findings | Critical | High | Medium | Low/Info |
|---|---|---|---|---|---|
| Security | 21 | 5 | 6 | 6 | 4 |
| Reliability | 18 | 0 | 3 | 11 | 4 |
| Performance Efficiency | 8 | 0 | 2 | 6 | 0 |
| Maintainability | 14 | 0 | 2 | 7 | 5 |
| **Total** | **61** | **5** | **13** | **30** | **13** |

### The five most important problems
1. **Broken access control everywhere (S07–S13).** The API checks the *role* but never the *owner*.
   - Any client can delete any account, edit any profile and even demote the admin.
   - Any client can read other clients' ID-card files and anyone's chats.
2. **Secrets in the code (S04, S05).**
   - The JWT signing key is in the public repository, so admin tokens can be forged.
   - Accountant sign-up is protected only by the code `abcd`.
3. **Password hashes are published (S01–S03).** A public endpoint lists every user with their bcrypt hash, and many
   responses embed full `User` objects.
4. **Chat service without authentication (S14).** Anyone can read any conversation or write in someone else's name.
5. **Performance design (P01, P02).**
   - A job reloads every deadline, with all attached files, **every second**.
   - Uploaded files are stored inside documents and sent back in every list.

## Security

| ID | Severity | Finding | Location | CWE (recalled) | In ISO 5055? (guess) | Origin |
|---|---|---|---|---|---|---|
| S01 | Critical | Public endpoint returns every user with password hash | `api/…/controllers/AuthController.java:105-109; api/…/config/WebSecurityConfiguration.java:36` | CWE-200 / CWE-862 | Unsure | review |
| S02 | High | Public lookup of any user by e-mail (enumeration + data exposure) | `api/…/controllers/AuthController.java:43-51` | CWE-200 / CWE-204 | Unsure | review |
| S03 | High | Password hashes leak through DTOs that embed User entities | `api/…/entities/User.java:27; api/…/dto/UserDTO.java:16; api/…/dto/BlogDTO.java:16 (also ChatDTO, ConsultationRequestDTO, DeadlineDTO, ReservationDTO, DomiciliationRequestDTO, ResponseDomiAdminDTO)` | CWE-200 | Unsure | review |
| S04 | Critical | Hard-coded JWT signing key | `api/…/utils/JwtUtil.java:65` | CWE-798 (CWE-321) | Yes | review |
| S05 | High | Hard-coded accountant registration code "abcd" | `api/…/services/AuthServiceImpl.java:46` | CWE-798 | Yes | review |
| S06 | Medium | Admin credentials left in comments | `api/…/ApiApplication.java:36-42` | CWE-615 / CWE-798 | Unsure | review |
| S07 | Critical | Any client or accountant can delete any account | `api/…/controllers/UserController.java:109-117; api/…/services/DomiAffaireServiceImpl.java:1314-1321` | CWE-639 / CWE-862 | Unsure | review |
| S08 | Critical | Profile update by path id: overwrite other users and their role | `api/…/controllers/ClientController.java:44-60; api/…/controllers/AccountantController.java:37-53; api/…/services/DomiAffaireServiceImpl.java:1466-1499` | CWE-639 | Unsure | review |
| S09 | High | Clients can read other clients' domiciliation files | `api/…/controllers/ClientController.java:172-179; api/…/services/DomiAffaireServiceImpl.java:642-649` | CWE-639 | Unsure | review |
| S10 | High | Clients can cancel other clients' requests | `api/…/controllers/ClientController.java:81-99; api/…/services/DomiAffaireServiceImpl.java:232-249` | CWE-639 | Unsure | review |
| S11 | Medium | Clients can accept/protest contracts of other clients | `api/…/controllers/ClientController.java:200-218; api/…/services/DomiAffaireServiceImpl.java:787-853` | CWE-639 | Unsure | review |
| S12 | High | Any client/accountant can read any chat | `api/…/controllers/UserController.java:28-50; api/…/controllers/ClientController.java:193-196; api/…/services/DomiAffaireServiceImpl.java:365-376` | CWE-639 | Unsure | review |
| S13 | Medium | Accountants can modify or delete anyone's blog posts | `api/…/controllers/AccountantController.java:167-203,268-290; api/…/services/DomiAffaireServiceImpl.java:1063-1106,1189-1234` | CWE-639 / CWE-862 | Unsure | review |
| S14 | Critical | Chat service has no authentication; sender id is trusted from the client | `chatapp/…/controllers/WebSocketController.java:15-18; app/chatapp/pom.xml (no spring-security); web/…/core/services/chat.service.ts:47` | CWE-306 / CWE-290 | Unsure | review |
| S15 | Medium | CORS allows any origin and any header | `api/…/config/SimpleCorsFilter.java:29-32` | CWE-942 | Unsure | seen during planning |
| S16 | Medium | No protection against password guessing on login | `api/…/controllers/AuthController.java:79-101` | CWE-307 | Unsure | review |
| S17 | Medium | Upload checks trust the client Content-Type | `api/…/controllers/AdminController.java:109-111 (same pattern 131,244,267,287,307; blogs 386-388)` | CWE-434 | Yes | review |
| S18 | Low | JSON built by string concatenation with untrusted text | `api/…/controllers/*.java (e.g. AdminController.java:52; AuthController.java:49)` | CWE-116 | Unsure | review |
| S19 | Low | Angular sanitizer bypassed on consultation details | `web/…/features/client/consultation/consultation.component.ts:95` | CWE-79 | Yes | review |
| S20 | Info | OAuth client secret was in the properties file (now a placeholder) | `app/api/src/main/resources/application.properties:13` | CWE-798 | Yes | seen during planning |
| S21 | Low | Chat content and data written to the browser console | `web/…/core/services/chat.service.ts:49-55 (182 console.log in total)` | CWE-532 | Unsure | review |

**S01: Public endpoint returns every user with password hash** (Critical, confidence high)
- *Why it matters:* GET /api/auth/clients is under the permitAll rule for /api/auth/** and returns userRepository.findAll(): every User entity, including pwd (bcrypt hash), role, phone, birth date and the accountant code.
- *Fix:* Remove the endpoint or move it under /api/admin; never return entities, only DTOs without secrets.

**S02: Public lookup of any user by e-mail (enumeration + data exposure)** (High, confidence high)
- *Why it matters:* GET /api/auth/{email} is public and returns the full User entity (password hash, image, code). Its 404 message also confirms whether an e-mail exists.
- *Fix:* Delete it or restrict it to the authenticated user; return a minimal DTO.

**S03: Password hashes leak through DTOs that embed User entities** (High, confidence high)
- *Why it matters:* pwd has no @JsonIgnore and getPassword() is serialised. DTOs hold whole User objects, so for example any client listing blogs receives the author's bcrypt hash; update-profile returns UserDTO with pwd.
- *Fix:* Add @JsonIgnore on pwd/getPassword/code; replace User fields in DTOs with small summary DTOs (id, name).

**S04: Hard-coded JWT signing key** (Critical, confidence high)
- *Why it matters:* The HMAC key is a literal in source code. The repository is public, so anyone can forge a valid token for any e-mail, including the admin.
- *Fix:* Load the key from configuration/secret store; rotate it.

**S05: Hard-coded accountant registration code "abcd"** (High, confidence high)
- *Why it matters:* Anyone can self-register with role ACCOUNTANT by sending code=abcd, then read all consultation requests and chat with clients.
- *Fix:* Create accountants from the admin console only (invitation), never by a shared static code.

**S06: Admin credentials left in comments** (Medium, confidence high)
- *Why it matters:* Commented seeding code contains an admin e-mail and clear-text password. If that account was created this way, the password is public.
- *Fix:* Remove the block; change that password if it was ever used.

**S07: Any client or accountant can delete any account** (Critical, confidence high)
- *Why it matters:* DELETE /api/users/delete/{email} deletes whatever e-mail is given; no check that it is the caller's own account (admins can be deleted too).
- *Fix:* Delete only the authenticated user's account (or admin-only); compare with SecurityContext.

**S08: Profile update by path id: overwrite other users and their role** (Critical, confidence high)
- *Why it matters:* updateUser(…, id) loads the user from the URL id and forces userRole=CLIENT/ACCOUNTANT. A client can change another user's name, phone and photo, and demote an ADMIN to CLIENT.
- *Fix:* Ignore the path id; update the authenticated user; never set the role from this endpoint.

**S09: Clients can read other clients' domiciliation files** (High, confidence high)
- *Why it matters:* GET /api/clients/domiciliation-requests/{id} has no ownership check and returns ID-card (CIN) files, contracts and business licences (with file bytes).
- *Fix:* Check request.client == authenticated user (or admin).

**S10: Clients can cancel other clients' requests** (High, confidence high)
- *Why it matters:* Consultation and domiciliation requests are deleted by id without checking who owns them.
- *Fix:* Add an ownership check before delete.

**S11: Clients can accept/protest contracts of other clients** (Medium, confidence high)
- *Why it matters:* acceptContractTermsClient/protestContractTermsClient act on any request id.
- *Fix:* Check ownership and the current status before changing it.

**S12: Any client/accountant can read any chat** (High, confidence high)
- *Why it matters:* /chat/messages/{id} and /all-chats/{id} return messages of any chat id; messages include the sender User entity (see S03).
- *Fix:* Allow only the chat's client and accountant.

**S13: Accountants can modify or delete anyone's blog posts** (Medium, confidence high)
- *Why it matters:* updateBlog/deleteBlog/archiveBlog never check blog.createdBy, so an accountant can edit or delete the admin's posts.
- *Fix:* Check authorship (or admin role).

**S14: Chat service has no authentication; sender id is trusted from the client** (Critical, confidence high)
- *Why it matters:* The STOMP endpoint accepts anyone. The userId header decides who 'sent' the message, and anyone can subscribe to /topic/{roomId} to read a conversation.
- *Fix:* Authenticate the WebSocket handshake with the JWT; take the sender from the authenticated principal; authorise subscriptions.

**S15: CORS allows any origin and any header** (Medium, confidence high)
- *Why it matters:* Access-Control-Allow-Origin: * on the whole API. Impact is limited because the token is a bearer header, not a cookie.
- *Fix:* Use Spring's CorsConfiguration with the real front-end origin(s).

**S16: No protection against password guessing on login** (Medium, confidence medium)
- *Why it matters:* No rate limit, lockout or delay on /api/auth/login.
- *Fix:* Add rate limiting / progressive delay per account and IP.

**S17: Upload checks trust the client Content-Type** (Medium, confidence medium)
- *Why it matters:* Only the declared MIME type is checked; the bytes are never inspected. Files are stored in MongoDB and served back to users.
- *Fix:* Check magic bytes / size; store outside the DB; serve with Content-Disposition: attachment.

**S18: JSON built by string concatenation with untrusted text** (Low, confidence high)
- *Why it matters:* Bodies like "{\"message\":\"" + e.getMessage() + "\"}" break or can be altered when the message contains quotes (it can contain the user's e-mail).
- *Fix:* Return a Map/record and let Jackson serialise it.

**S19: Angular sanitizer bypassed on consultation details** (Low, confidence medium)
- *Why it matters:* bypassSecurityTrustHtml(item.details) renders raw HTML typed by the client (self-XSS today; stored XSS if the view is ever reused for other users).
- *Fix:* Remove the bypass; Angular's default [innerHTML] sanitising is enough.

**S20: OAuth client secret was in the properties file (now a placeholder)** (Info, confidence high)
- *Why it matters:* The copy shared privately held a real Google client secret; the public repo uses ${GOOGLE_CLIENT_SECRET}. The property is not even used by the code (no oauth2ResourceServer() in the security chain).
- *Fix:* Revoke the secret that was shared; remove the unused OAuth properties or wire them properly.

**S21: Chat content and data written to the browser console** (Low, confidence high)
- *Why it matters:* Messages and API responses are logged in the console of every user.
- *Fix:* Remove debug logging from production builds.

## Reliability

| ID | Severity | Finding | Location | CWE (recalled) | In ISO 5055? (guess) | Origin |
|---|---|---|---|---|---|---|
| R01 | High | Optional.get() without check: unknown ids crash with HTTP 500 | `api/…/services/DomiAffaireServiceImpl.java:366,422,481,574,975,1000,1079,1468,1483,1503; api/…/services/ReservationServiceImpl.java:56; chatapp/…/services/WebSocketService.java:26,28` | CWE-754 (CWE-476) | Unsure | review |
| R02 | Medium | String fields compared without null check | `api/…/services/AuthServiceImpl.java:20,35; api/…/services/DomiAffaireServiceImpl.java:402,425,515,1525` | CWE-476 | Yes | review |
| R03 | Medium | Operator-precedence bug in every file-type check | `api/…/controllers/AdminController.java:109-111,131-133,244-246,267-269,287-289,307-309` | CWE-783 | Unsure | review |
| R04 | High | Contract acceptance can crash and poison the scheduler | `api/…/services/DomiAffaireServiceImpl.java:787-824; api/…/services/DeadlineServiceImpl.java:52-56` | CWE-476 | Yes | review |
| R05 | Medium | Reminder/overdue flag logic is inconsistent | `api/…/services/DeadlineServiceImpl.java:56-83` | CWE-670 | Unsure | review |
| R06 | Medium | Room double-booking: overlap check only matches identical slots | `api/…/services/ReservationServiceImpl.java:79-86; api/…/entities/Reservation.java (equals)` | CWE-697 | Unsure | review |
| R07 | Medium | Money computed with float | `api/…/entities/Pack.java:23; api/…/entities/Deadline.java (packPrice); api/…/services/DomiAffaireServiceImpl.java:858-865` | CWE-681 / CWE-1339 | Unsure | review |
| R08 | Medium | Hard-coded absolute Windows paths of the author's PC | `api/…/controllers/AdminController.java:554,562,621,632; api/…/controllers/ClientController.java:305-306; api/…/controllers/UserController.java:132-133` | none certain | No | review |
| R09 | Medium | Exceptions swallowed with printStackTrace | `api/…/services/ReservationServiceImpl.java:129-131,153-155` | CWE-390 | Yes | review |
| R10 | Medium | Lombok @Builder drops field defaults | `api/…/entities/*.java (e.g. Room.java createdAt; used at api/…/ApiApplication.java:160)` | CWE-665 | Unsure | review |
| R11 | Medium | Seed data parsed wrongly and re-written at every start | `api/…/ApiApplication.java:143-168` | CWE-20 | Unsure | review |
| R12 | High | Bad-word filter rejects normal business words | `chatapp/…/validators/NoBadWordsValidator.java:21` | CWE-697 | No | review |
| R13 | Medium | Uncaught JWT and login exceptions return 500 | `api/…/config/JwtAuthenticationFilter.java:40; api/…/controllers/AuthController.java:98` | CWE-248 / CWE-755 | Unsure | review |
| R14 | Low | Possible infinite recursion in toString/hashCode | `api/…/entities/Chat.java:31 and Message.java (sender/chat); same in chatapp` | CWE-674 | Unsure | review |
| R15 | Medium | Front end never releases subscriptions or the WebSocket | `web/… (128 .subscribe(), 1 ngOnDestroy); web/…/core/services/chat.service.ts:47` | CWE-772 / CWE-401 | Yes | review |
| R16 | Low | Silent failures and broken features | `api/…/services/DomiAffaireServiceImpl.java:1563-1581; web/…/core/services/auth.service.ts:36-39,71-76,95-96` | CWE-754 | Unsure | review |
| R17 | Low | Generic RuntimeException wrapping and malformed error bodies | `api/…/controllers/AdminController.java:141,565,394,396,427,429; api/…/controllers/ClientController.java:126,138,168` | CWE-397 | Unsure | review |
| R18 | Low | Phone-number regex has a broken character class | `api/…/dto/SignupRequest.java:32` | CWE-185 | Unsure | review |

**R01: Optional.get() without check: unknown ids crash with HTTP 500** (High, confidence high)
- *Why it matters:* findById(...).get() throws NoSuchElementException when the id (or the 'Default' blog category) does not exist; the request fails with 500.
- *Fix:* Use orElseThrow(NotFoundException) and map it to 404.

**R02: String fields compared without null check** (Medium, confidence high)
- *Why it matters:* signupRequest.getRole(), getCompanyStatus(), getPaymentMode(), getOldLegalForm(), file.getType() are dereferenced directly; a missing field gives a NullPointerException.
- *Fix:* Use enums with @NotNull validation, or "literal".equals(value).

**R03: Operator-precedence bug in every file-type check** (Medium, confidence high)
- *Why it matters:* file != null && (A || B) || C: when file is null the third test still runs and throws NullPointerException; getContentType() may also be null.
- *Fix:* Write one helper: file != null && ALLOWED.contains(file.getContentType()).

**R04: Contract acceptance can crash and poison the scheduler** (High, confidence high)
- *Why it matters:* If a client accepts before the admin answered, getResponseDomiAdmin() is null (NPE). If paymentMode is null, limitedDate stays null and checkDeadlines() throws NPE every second.
- *Fix:* Check the request status before accepting; make paymentMode mandatory.

**R05: Reminder/overdue flag logic is inconsistent** (Medium, confidence medium)
- *Why it matters:* emailSent is set true, saved, then set false only in memory (lines 58-60, 67-68, 80, 83). Once 'true' is persisted the overdue branch never runs again for that request; no e-mail is actually sent.
- *Fix:* Model reminder state explicitly (lastReminderAt, lastOverdueAt) and send real notifications.

**R06: Room double-booking: overlap check only matches identical slots** (Medium, confidence high)
- *Why it matters:* acceptReservation compares with equals() (same start, same end, same room). 10:00-12:00 and 11:00-13:00 can both be accepted.
- *Fix:* Query for overlapping ACCEPTED reservations (start < otherEnd && end > otherStart).

**R07: Money computed with float** (Medium, confidence high)
- *Why it matters:* Prices are float; BigDecimal.valueOf(float) widens to double, so 70.1 becomes 70.0999984741211 before tax and rounding. Also uses the deprecated ROUND_HALF_UP.
- *Fix:* Store prices as BigDecimal (or millimes as long); use RoundingMode.HALF_UP.

**R08: Hard-coded absolute Windows paths of the author's PC** (Medium, confidence high)
- *Why it matters:* CSV exports for the recommendation service are written to C:/Users/ouert/Desktop/...; on any other machine the write fails (silently, see R09).
- *Fix:* Make the path a configuration property; better, let the Python service read MongoDB directly.

**R09: Exceptions swallowed with printStackTrace** (Medium, confidence high)
- *Why it matters:* Export failures are printed and ignored; the caller reports success.
- *Fix:* Log with the logger and propagate or report the failure.

**R10: Lombok @Builder drops field defaults** (Medium, confidence high)
- *Why it matters:* Fields initialised inline (createdAt = now(), lists = new ArrayList<>()) are null when objects are built with the builder, unless @Builder.Default is used. Seeded rooms get createdAt = null.
- *Fix:* Add @Builder.Default or initialise in a constructor.

**R11: Seed data parsed wrongly and re-written at every start** (Medium, confidence high)
- *Why it matters:* line.split(",") splits inside the quoted equipment list, so each seeded room keeps only its first equipment. The 6 rooms are overwritten each time the API starts.
- *Fix:* Use a CSV parser (OpenCSV is already a dependency) and seed only if empty.

**R12: Bad-word filter rejects normal business words** (High, confidence high)
- *Why it matters:* Substring matching on short words ("con", "cul", "pd", "tg") blocks words like contrat, consultation, compte, calcul: exactly the vocabulary of this business.
- *Fix:* Match whole words (regex \b...\b) and keep the list in configuration.

**R13: Uncaught JWT and login exceptions return 500** (Medium, confidence medium)
- *Why it matters:* An expired or malformed token throws inside the filter (500, not 401). Login only catches BadCredentialsException, not DisabledException/LockedException (archived users).
- *Fix:* Catch JwtException in the filter; handle AuthenticationException globally.

**R14: Possible infinite recursion in toString/hashCode** (Low, confidence medium)
- *Why it matters:* @Data/@ToString on the bidirectional Chat <-> Message relation: calling toString() or hashCode() on either recurses until StackOverflowError.
- *Fix:* Exclude the back-reference (@ToString.Exclude, @EqualsAndHashCode.Exclude).

**R15: Front end never releases subscriptions or the WebSocket** (Medium, confidence high)
- *Why it matters:* Each visit to the chat opens a new STOMP connection and subscription that is never closed; other components keep subscriptions alive after navigation.
- *Fix:* Unsubscribe in ngOnDestroy (takeUntil) and disconnect the STOMP client.

**R16: Silent failures and broken features** (Low, confidence high)
- *Why it matters:* changePassword returns success when the id does not exist. The front end calls /api/auth/verifyEmail and /password-reset-request, which the API does not implement; resetPassword posts to a URL read from a cookie.
- *Fix:* Throw when the user is missing; implement or remove the reset flow.

**R17: Generic RuntimeException wrapping and malformed error bodies** (Low, confidence high)
- *Why it matters:* Checked exceptions are re-thrown as RuntimeException (500); several error bodies miss their braces and are not valid JSON.
- *Fix:* Use a @ControllerAdvice with typed exceptions and a standard error body.

**R18: Phone-number regex has a broken character class** (Low, confidence high)
- *Why it matters:* [2-5-4-7|9] also accepts '-' and '|' as the first character.
- *Fix:* Use ^[2-9]\d{7}$ (or the exact list of Tunisian prefixes).

## Performance Efficiency

| ID | Severity | Finding | Location | CWE (recalled) | In ISO 5055? (guess) | Origin |
|---|---|---|---|---|---|---|
| P01 | High | Scheduler reloads all deadlines every second | `api/…/services/DeadlineServiceImpl.java:44-46` | CWE-1050 | Yes | review |
| P02 | High | File contents stored inside documents and sent in every list | `api/…/entities/File.java:21; api/…/entities/User.java (image); api/…/dto/DomiciliationRequestDTO.java; api/…/mappers/Mapper.java` | CWE-1049 (approx.) | Unsure | review |
| P03 | Medium | N+1 queries on deadlines | `api/…/services/DeadlineServiceImpl.java:93-98,106-111` | CWE-1060 (approx.) | Unsure | review |
| P04 | Medium | Database calls inside loops | `api/…/services/ReservationServiceImpl.java:56; api/…/services/DomiAffaireServiceImpl.java:976-978,1199-1206` | CWE-1050 | Yes | review |
| P05 | Medium | Full collection scans and in-memory filtering | `api/…/services/DomiAffaireServiceImpl.java:266-274,82-88,120-131,1354-1358` | CWE-1049 (approx.) | Unsure | review |
| P06 | Medium | Pack embeds full User documents (unbounded growth) | `api/…/entities/Pack.java:26; api/…/services/DomiAffaireServiceImpl.java:807-809` | none certain | Unsure | review |
| P07 | Medium | Chat history list grows forever and is rewritten on each message | `chatapp/…/services/WebSocketService.java:26-35; api/…/services/DomiAffaireServiceImpl.java:300-317; Chat.java messages` | CWE-1050 (approx.) | Unsure | review |
| P08 | Medium | No pagination on any list endpoint | `api/…/controllers/*.java (findAll* everywhere)` | CWE-1049 (approx.) | Unsure | review |

**P01: Scheduler reloads all deadlines every second** (High, confidence high)
- *Why it matters:* @Scheduled(fixedRate = 1000) loads every domiciliation request with a deadline, each with about 10 eager @DBRef objects (files with their bytes, users with photos): 86,400 times a day.
- *Fix:* Run daily (cron), query only deadlines in the next 5 days, project only the needed fields.

**P02: File contents stored inside documents and sent in every list** (High, confidence high)
- *Why it matters:* byte[] fileData / image are loaded through @DBRef whenever a request, blog, chat or user is read, and serialised as base64 in list responses (e.g. all domiciliation requests with up to 9 files each).
- *Fix:* Store files in GridFS/object storage; return metadata + a download URL; exclude bytes from lists.

**P03: N+1 queries on deadlines** (Medium, confidence high)
- *Why it matters:* One findByDeadline() query per deadline in the loop.
- *Fix:* Fetch the requests for all deadlines in one query (deadline in [...]).

**P04: Database calls inside loops** (Medium, confidence high)
- *Why it matters:* addReservation reloads the same room for every slot; deleteBlogCategory saves blogs one by one; archiveBlog loads all users and rewrites all of them with saveAll.
- *Fix:* Load once outside the loop; use saveAll on the changed items only; use an update query ($pull) for archiveBlog.

**P05: Full collection scans and in-memory filtering** (Medium, confidence high)
- *Why it matters:* validateConsultationRequest loads all chats to find one; clients are filtered in Java; getPackCounts loads every pack with its full user list just to count.
- *Fix:* Use derived queries (findByClientAndAccountant, findByUserRoleAndEnabled...) and count queries.

**P06: Pack embeds full User documents (unbounded growth)** (Medium, confidence high)
- *Why it matters:* users is a Set<User> without @DBRef, so whole user documents (photo bytes, password hash) are copied into each pack; the document grows with every subscriber toward MongoDB's 16 MB limit.
- *Fix:* Keep only user ids (or a counter) in Pack.

**P07: Chat history list grows forever and is rewritten on each message** (Medium, confidence high)
- *Why it matters:* Sending one message loads the chat with all previous messages (eager @DBRef) and saves the whole array: cost grows with history length.
- *Fix:* Do not keep messages inside Chat; query messages by chatId with paging.

**P08: No pagination on any list endpoint** (Medium, confidence high)
- *Why it matters:* All lists (users, requests, blogs, reservations, deadlines) are returned in full.
- *Fix:* Use Pageable / Page<T> in repositories and endpoints.

## Maintainability

| ID | Severity | Finding | Location | CWE (recalled) | In ISO 5055? (guess) | Origin |
|---|---|---|---|---|---|---|
| M01 | High | God class: DomiAffaireServiceImpl | `api/…/services/DomiAffaireServiceImpl.java (1,585 lines, about 70 methods, 15 repositories)` | CWE-1080 / CWE-1048 | Yes | review |
| M02 | High | Heavy code duplication | `api/…/services/DomiAffaireServiceImpl.java:390-595 (3 near-identical methods), File.builder block x12, auth-user lookup x~35; controllers repeat the same endpoints` | CWE-1041 | Yes | review |
| M03 | Medium | Dead and commented-out code | `api/…/ApiApplication.java:36-141; api/…/controllers/AuthController.java:40; api/…/utils/JwtUtil.java:45-49; api/…/config/SimpleCorsFilter.java:27-28; api/…/config/RestTemplateConfig.java; api/…/services/DeadlineServiceImpl.java:3` | CWE-561 / CWE-563 | Yes | review |
| M04 | Low | Conditions that are always true | `api/…/services/DomiAffaireServiceImpl.java:1422,1436,1504` | CWE-571 | Unsure | review |
| M05 | Medium | Layering bypassed: controllers use repositories and concrete classes | `api/…/controllers/AuthController.java:39,107; all controllers inject *ServiceImpl` | CWE-1057 | Yes | review |
| M06 | Medium | Magic numbers and hard-coded literals | `api/…/utils/JwtUtil.java:41; api/…/services/DomiAffaireServiceImpl.java:860-863,975; app/web-client-07-06-2024/src/environments/environment.ts:3` | CWE-1106 | Yes | review |
| M07 | Medium | Same domain model duplicated in two services | `chatapp/…/entities/User.java, Chat.java, Message.java vs api/…/entities/` | CWE-1041 | Yes | review |
| M08 | Medium | Outdated, conflicting or incompatible dependencies | `app/api/pom.xml:53-76,100-115; web-client package.json (tinymce-angular 8 vs Angular 15)` | CWE-1104 | Yes | seen during step 1 |
| M09 | Low | Debug output left in code | `api/…/controllers/ClientController.java:184; AccountantController.java:114; UserController.java:40; ReservationServiceImpl.java:127,151; front end: 182 console.log` | CWE-489 | Unsure | review |
| M10 | Medium | Long, deeply nested methods | `api/…/services/DomiAffaireServiceImpl.java:787-824,827-853; api/…/services/DeadlineServiceImpl.java:45-87` | CWE-1121 | Yes | review |
| M11 | Low | Too many parameters | `api/…/services/DomiAffaireServiceImpl.java:501-507` | CWE-1064 | Yes | review |
| M12 | Low | Unclear or misleading text in code | `api/…/services/DomiAffaireServiceImpl.java:835; api/…/controllers/AdminController.java:106; chatapp/…/services/WebSocketService.java:53` | none | No | review |
| M13 | Low | State changes through HTTP GET | `api/…/controllers/AdminController.java:433-455,617-637; ClientController.java:239-263` | none | No | review |
| M14 | Medium | Almost no automated tests | `app/api/src/test (2 test classes, about 300 lines for about 6,800 lines of Java)` | none | No | review |

**M01: God class: DomiAffaireServiceImpl** (High, confidence high)
- *Why it matters:* Users, files, chats, consultations, domiciliation, packs, blogs, FAQs and reporting all live in one class.
- *Fix:* Split by domain (UserService, DomiciliationService, BlogService, ChatService...).

**M02: Heavy code duplication** (High, confidence high)
- *Why it matters:* The same code is copied many times: three sendDomiciliationRequest variants, the 'find authenticated user' block, the upload type check (x6), identical blog/chat endpoints in Client/Accountant/User controllers, two branches of updateUser.
- *Fix:* Extract helpers (currentUser(), saveFile(), allowedType()), merge controllers.

**M03: Dead and commented-out code** (Medium, confidence high)
- *Why it matters:* 100+ commented lines, unused methods (findAllUsers, uploadFile, findAllFiles, resetUserPassword, generateRefreshToken), unused field tokenBlacklist, unused locals, unused import, unused RestTemplate bean and WebSocket config in the API.
- *Fix:* Delete; version control keeps the history.

**M04: Conditions that are always true** (Low, confidence high)
- *Why it matters:* newFile != null right after new File(); admin != null right after .get(). The 'return null' branches are unreachable.
- *Fix:* Remove the dead conditions.

**M05: Layering bypassed: controllers use repositories and concrete classes** (Medium, confidence high)
- *Why it matters:* AuthController calls UserRepository directly; controllers depend on implementations instead of the service interfaces that exist.
- *Fix:* Inject the interfaces; keep data access in services.

**M06: Magic numbers and hard-coded literals** (Medium, confidence high)
- *Why it matters:* Token lifetime 10000*60*24 = 4 h (probably meant 24 h); tax rates 0.19 and 0.1; category name 'Default'; status strings 'In Process', 'Quarter'; API URL in environment.ts (seen in step 1).
- *Fix:* Named constants, enums and configuration properties.

**M07: Same domain model duplicated in two services** (Medium, confidence high)
- *Why it matters:* User/Chat/Message are defined twice and already differ; a change in one service silently breaks the other.
- *Fix:* Share a module, or let only one service own the chat data.

**M08: Outdated, conflicting or incompatible dependencies** (Medium, confidence high)
- *Why it matters:* jjwt 0.9.1 together with jjwt 0.11.5; springfox (does not support Spring Boot 3, plus @EnableWebMvc disables Boot's MVC auto-configuration); android-json in a server; unused webflux/google-api-client; npm peer conflict.
- *Fix:* Remove unused libraries, keep one jjwt, replace springfox with springdoc-openapi.

**M09: Debug output left in code** (Low, confidence high)
- *Why it matters:* System.out.println and console.log used for debugging; the controller lines even call the service twice just to print a size.
- *Fix:* Use the logger at debug level; strip console.log in production.

**M10: Long, deeply nested methods** (Medium, confidence medium)
- *Why it matters:* Several branches, nested ifs and side effects mixed in one method (status, pack, deadline, notification, document code).
- *Fix:* Split into small steps; replace if/else chains on PaymentMode with an enum method (months()).

**M11: Too many parameters** (Low, confidence high)
- *Why it matters:* sendDomiciliationRequestPMTransfert takes 7 parameters (6 files).
- *Fix:* Group the files into one request object.

**M12: Unclear or misleading text in code** (Low, confidence high)
- *Why it matters:* User-facing message in Tunisian dialect slang; comments in mixed languages; a comment says 'convert nanoseconds to milliseconds' but nothing is converted.
- *Fix:* Use clear, consistent messages (i18n) and accurate comments.

**M13: State changes through HTTP GET** (Low, confidence high)
- *Why it matters:* archive/unarchive, accept/reject reservation and save/unsave blog are GET requests; they can be triggered by prefetching or a simple link.
- *Fix:* Use POST/PUT/DELETE for state changes.

**M14: Almost no automated tests** (Medium, confidence high)
- *Why it matters:* None of the bugs above (null handling, ownership, money, scheduling) is covered by a test.
- *Fix:* Add service tests for each rule and security tests for each role.

## What this review could not see
- Runtime behaviour: nothing was executed for this review.
- Library vulnerabilities (CVEs) in the dependency versions.
- The Flutter mobile client and the Python recommendation service, which are out of scope.
- Cross-file data flows longer than a few calls; specialized tools (steps 5 and 6) should do better here.

The machine-readable list is in [`findings.csv`](../findings.csv): one row per finding, with empty columns for steps 3, 5 and 6.
