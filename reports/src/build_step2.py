"""Step 2 (review A, knowledge only): generate findings.csv, the full Markdown report and the short PDF source (HTML).

Usage: python build_step2.py <repo_root>
"""
import csv
import html
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(sys.argv[1])
API = "app/api/src/main/java/com/domiaffaire/api"
CHAT = "app/chatapp/src/main/java/com/wassim/chatapp"
WEB = "app/web-client-07-06-2024/src/app"

SEC, REL, PERF, MAIN = "Security", "Reliability", "Performance Efficiency", "Maintainability"
REVIEW, PLAN, STEP1 = "review", "seen during planning", "seen during step 1"

# id, characteristic, severity, confidence, title, location(s), CWE as recalled, in ISO 5055 (my guess), origin, explanation, fix
F = [
 # ---------------- SECURITY ----------------
 ("S01", SEC, "Critical", "High", "Public endpoint returns every user with password hash",
  f"{API}/controllers/AuthController.java:105-109; {API}/config/WebSecurityConfiguration.java:36",
  "CWE-200 / CWE-862", "Unsure", REVIEW,
  "GET /api/auth/clients is under the permitAll rule for /api/auth/** and returns userRepository.findAll(): every User entity, including pwd (bcrypt hash), role, phone, birth date and the accountant code.",
  "Remove the endpoint or move it under /api/admin; never return entities, only DTOs without secrets."),
 ("S02", SEC, "High", "High", "Public lookup of any user by e-mail (enumeration + data exposure)",
  f"{API}/controllers/AuthController.java:43-51",
  "CWE-200 / CWE-204", "Unsure", REVIEW,
  "GET /api/auth/{email} is public and returns the full User entity (password hash, image, code). Its 404 message also confirms whether an e-mail exists.",
  "Delete it or restrict it to the authenticated user; return a minimal DTO."),
 ("S03", SEC, "High", "High", "Password hashes leak through DTOs that embed User entities",
  f"{API}/entities/User.java:27; {API}/dto/UserDTO.java:16; {API}/dto/BlogDTO.java:16 (also ChatDTO, ConsultationRequestDTO, DeadlineDTO, ReservationDTO, DomiciliationRequestDTO, ResponseDomiAdminDTO)",
  "CWE-200", "Unsure", REVIEW,
  "pwd has no @JsonIgnore and getPassword() is serialised. DTOs hold whole User objects, so for example any client listing blogs receives the author's bcrypt hash; update-profile returns UserDTO with pwd.",
  "Add @JsonIgnore on pwd/getPassword/code; replace User fields in DTOs with small summary DTOs (id, name)."),
 ("S04", SEC, "Critical", "High", "Hard-coded JWT signing key",
  f"{API}/utils/JwtUtil.java:65",
  "CWE-798 (CWE-321)", "Yes", REVIEW,
  "The HMAC key is a literal in source code. The repository is public, so anyone can forge a valid token for any e-mail, including the admin.",
  "Load the key from configuration/secret store; rotate it."),
 ("S05", SEC, "High", "High", "Hard-coded accountant registration code \"abcd\"",
  f"{API}/services/AuthServiceImpl.java:46",
  "CWE-798", "Yes", REVIEW,
  "Anyone can self-register with role ACCOUNTANT by sending code=abcd, then read all consultation requests and chat with clients.",
  "Create accountants from the admin console only (invitation), never by a shared static code."),
 ("S06", SEC, "Medium", "High", "Admin credentials left in comments",
  f"{API}/ApiApplication.java:36-42",
  "CWE-615 / CWE-798", "Unsure", REVIEW,
  "Commented seeding code contains an admin e-mail and clear-text password. If that account was created this way, the password is public.",
  "Remove the block; change that password if it was ever used."),
 ("S07", SEC, "Critical", "High", "Any client or accountant can delete any account",
  f"{API}/controllers/UserController.java:109-117; {API}/services/DomiAffaireServiceImpl.java:1314-1321",
  "CWE-639 / CWE-862", "Unsure", REVIEW,
  "DELETE /api/users/delete/{email} deletes whatever e-mail is given; no check that it is the caller's own account (admins can be deleted too).",
  "Delete only the authenticated user's account (or admin-only); compare with SecurityContext."),
 ("S08", SEC, "Critical", "High", "Profile update by path id: overwrite other users and their role",
  f"{API}/controllers/ClientController.java:44-60; {API}/controllers/AccountantController.java:37-53; {API}/services/DomiAffaireServiceImpl.java:1466-1499",
  "CWE-639", "Unsure", REVIEW,
  "updateUser(…, id) loads the user from the URL id and forces userRole=CLIENT/ACCOUNTANT. A client can change another user's name, phone and photo, and demote an ADMIN to CLIENT.",
  "Ignore the path id; update the authenticated user; never set the role from this endpoint."),
 ("S09", SEC, "High", "High", "Clients can read other clients' domiciliation files",
  f"{API}/controllers/ClientController.java:172-179; {API}/services/DomiAffaireServiceImpl.java:642-649",
  "CWE-639", "Unsure", REVIEW,
  "GET /api/clients/domiciliation-requests/{id} has no ownership check and returns ID-card (CIN) files, contracts and business licences (with file bytes).",
  "Check request.client == authenticated user (or admin)."),
 ("S10", SEC, "High", "High", "Clients can cancel other clients' requests",
  f"{API}/controllers/ClientController.java:81-99; {API}/services/DomiAffaireServiceImpl.java:232-249",
  "CWE-639", "Unsure", REVIEW,
  "Consultation and domiciliation requests are deleted by id without checking who owns them.",
  "Add an ownership check before delete."),
 ("S11", SEC, "Medium", "High", "Clients can accept/protest contracts of other clients",
  f"{API}/controllers/ClientController.java:200-218; {API}/services/DomiAffaireServiceImpl.java:787-853",
  "CWE-639", "Unsure", REVIEW,
  "acceptContractTermsClient/protestContractTermsClient act on any request id.",
  "Check ownership and the current status before changing it."),
 ("S12", SEC, "High", "High", "Any client/accountant can read any chat",
  f"{API}/controllers/UserController.java:28-50; {API}/controllers/ClientController.java:193-196; {API}/services/DomiAffaireServiceImpl.java:365-376",
  "CWE-639", "Unsure", REVIEW,
  "/chat/messages/{id} and /all-chats/{id} return messages of any chat id; messages include the sender User entity (see S03).",
  "Allow only the chat's client and accountant."),
 ("S13", SEC, "Medium", "High", "Accountants can modify or delete anyone's blog posts",
  f"{API}/controllers/AccountantController.java:167-203,268-290; {API}/services/DomiAffaireServiceImpl.java:1063-1106,1189-1234",
  "CWE-639 / CWE-862", "Unsure", REVIEW,
  "updateBlog/deleteBlog/archiveBlog never check blog.createdBy, so an accountant can edit or delete the admin's posts.",
  "Check authorship (or admin role)."),
 ("S14", SEC, "Critical", "High", "Chat service has no authentication; sender id is trusted from the client",
  f"{CHAT}/controllers/WebSocketController.java:15-18; app/chatapp/pom.xml (no spring-security); {WEB}/core/services/chat.service.ts:47",
  "CWE-306 / CWE-290", "Unsure", REVIEW,
  "The STOMP endpoint accepts anyone. The userId header decides who 'sent' the message, and anyone can subscribe to /topic/{roomId} to read a conversation.",
  "Authenticate the WebSocket handshake with the JWT; take the sender from the authenticated principal; authorise subscriptions."),
 ("S15", SEC, "Medium", "High", "CORS allows any origin and any header",
  f"{API}/config/SimpleCorsFilter.java:29-32",
  "CWE-942", "Unsure", PLAN,
  "Access-Control-Allow-Origin: * on the whole API. Impact is limited because the token is a bearer header, not a cookie.",
  "Use Spring's CorsConfiguration with the real front-end origin(s)."),
 ("S16", SEC, "Medium", "Medium", "No protection against password guessing on login",
  f"{API}/controllers/AuthController.java:79-101",
  "CWE-307", "Unsure", REVIEW,
  "No rate limit, lockout or delay on /api/auth/login.",
  "Add rate limiting / progressive delay per account and IP."),
 ("S17", SEC, "Medium", "Medium", "Upload checks trust the client Content-Type",
  f"{API}/controllers/AdminController.java:109-111 (same pattern 131,244,267,287,307; blogs 386-388)",
  "CWE-434", "Yes", REVIEW,
  "Only the declared MIME type is checked; the bytes are never inspected. Files are stored in MongoDB and served back to users.",
  "Check magic bytes / size; store outside the DB; serve with Content-Disposition: attachment."),
 ("S18", SEC, "Low", "High", "JSON built by string concatenation with untrusted text",
  f"{API}/controllers/*.java (e.g. AdminController.java:52; AuthController.java:49)",
  "CWE-116", "Unsure", REVIEW,
  "Bodies like \"{\\\"message\\\":\\\"\" + e.getMessage() + \"\\\"}\" break or can be altered when the message contains quotes (it can contain the user's e-mail).",
  "Return a Map/record and let Jackson serialise it."),
 ("S19", SEC, "Low", "Medium", "Angular sanitizer bypassed on consultation details",
  f"{WEB}/features/client/consultation/consultation.component.ts:95",
  "CWE-79", "Yes", REVIEW,
  "bypassSecurityTrustHtml(item.details) renders raw HTML typed by the client (self-XSS today; stored XSS if the view is ever reused for other users).",
  "Remove the bypass; Angular's default [innerHTML] sanitising is enough."),
 ("S20", SEC, "Info", "High", "OAuth client secret was in the properties file (now a placeholder)",
  "app/api/src/main/resources/application.properties:13",
  "CWE-798", "Yes", PLAN,
  "The copy shared privately held a real Google client secret; the public repo uses ${GOOGLE_CLIENT_SECRET}. The property is not even used by the code (no oauth2ResourceServer() in the security chain).",
  "Revoke the secret that was shared; remove the unused OAuth properties or wire them properly."),
 ("S21", SEC, "Low", "High", "Chat content and data written to the browser console",
  f"{WEB}/core/services/chat.service.ts:49-55 (182 console.log in total)",
  "CWE-532", "Unsure", REVIEW,
  "Messages and API responses are logged in the console of every user.",
  "Remove debug logging from production builds."),
 # ---------------- RELIABILITY ----------------
 ("R01", REL, "High", "High", "Optional.get() without check: unknown ids crash with HTTP 500",
  f"{API}/services/DomiAffaireServiceImpl.java:366,422,481,574,975,1000,1079,1468,1483,1503; {API}/services/ReservationServiceImpl.java:56; {CHAT}/services/WebSocketService.java:26,28",
  "CWE-754 (CWE-476)", "Unsure", REVIEW,
  "findById(...).get() throws NoSuchElementException when the id (or the 'Default' blog category) does not exist; the request fails with 500.",
  "Use orElseThrow(NotFoundException) and map it to 404."),
 ("R02", REL, "Medium", "High", "String fields compared without null check",
  f"{API}/services/AuthServiceImpl.java:20,35; {API}/services/DomiAffaireServiceImpl.java:402,425,515,1525",
  "CWE-476", "Yes", REVIEW,
  "signupRequest.getRole(), getCompanyStatus(), getPaymentMode(), getOldLegalForm(), file.getType() are dereferenced directly; a missing field gives a NullPointerException.",
  "Use enums with @NotNull validation, or \"literal\".equals(value)."),
 ("R03", REL, "Medium", "High", "Operator-precedence bug in every file-type check",
  f"{API}/controllers/AdminController.java:109-111,131-133,244-246,267-269,287-289,307-309",
  "CWE-783", "Unsure", REVIEW,
  "file != null && (A || B) || C: when file is null the third test still runs and throws NullPointerException; getContentType() may also be null.",
  "Write one helper: file != null && ALLOWED.contains(file.getContentType())."),
 ("R04", REL, "High", "High", "Contract acceptance can crash and poison the scheduler",
  f"{API}/services/DomiAffaireServiceImpl.java:787-824; {API}/services/DeadlineServiceImpl.java:52-56",
  "CWE-476", "Yes", REVIEW,
  "If a client accepts before the admin answered, getResponseDomiAdmin() is null (NPE). If paymentMode is null, limitedDate stays null and checkDeadlines() throws NPE every second.",
  "Check the request status before accepting; make paymentMode mandatory."),
 ("R05", REL, "Medium", "Medium", "Reminder/overdue flag logic is inconsistent",
  f"{API}/services/DeadlineServiceImpl.java:56-83",
  "CWE-670", "Unsure", REVIEW,
  "emailSent is set true, saved, then set false only in memory (lines 58-60, 67-68, 80, 83). Once 'true' is persisted the overdue branch never runs again for that request; no e-mail is actually sent.",
  "Model reminder state explicitly (lastReminderAt, lastOverdueAt) and send real notifications."),
 ("R06", REL, "Medium", "High", "Room double-booking: overlap check only matches identical slots",
  f"{API}/services/ReservationServiceImpl.java:79-86; {API}/entities/Reservation.java (equals)",
  "CWE-697", "Unsure", REVIEW,
  "acceptReservation compares with equals() (same start, same end, same room). 10:00-12:00 and 11:00-13:00 can both be accepted.",
  "Query for overlapping ACCEPTED reservations (start < otherEnd && end > otherStart)."),
 ("R07", REL, "Medium", "High", "Money computed with float",
  f"{API}/entities/Pack.java:23; {API}/entities/Deadline.java (packPrice); {API}/services/DomiAffaireServiceImpl.java:858-865",
  "CWE-681 / CWE-1339", "Unsure", REVIEW,
  "Prices are float; BigDecimal.valueOf(float) widens to double, so 70.1 becomes 70.0999984741211 before tax and rounding. Also uses the deprecated ROUND_HALF_UP.",
  "Store prices as BigDecimal (or millimes as long); use RoundingMode.HALF_UP."),
 ("R08", REL, "Medium", "High", "Hard-coded absolute Windows paths of the author's PC",
  f"{API}/controllers/AdminController.java:554,562,621,632; {API}/controllers/ClientController.java:305-306; {API}/controllers/UserController.java:132-133",
  "none certain", "No", REVIEW,
  "CSV exports for the recommendation service are written to C:/Users/ouert/Desktop/...; on any other machine the write fails (silently, see R09).",
  "Make the path a configuration property; better, let the Python service read MongoDB directly."),
 ("R09", REL, "Medium", "High", "Exceptions swallowed with printStackTrace",
  f"{API}/services/ReservationServiceImpl.java:129-131,153-155",
  "CWE-390", "Yes", REVIEW,
  "Export failures are printed and ignored; the caller reports success.",
  "Log with the logger and propagate or report the failure."),
 ("R10", REL, "Medium", "High", "Lombok @Builder drops field defaults",
  f"{API}/entities/*.java (e.g. Room.java createdAt; used at {API}/ApiApplication.java:160)",
  "CWE-665", "Unsure", REVIEW,
  "Fields initialised inline (createdAt = now(), lists = new ArrayList<>()) are null when objects are built with the builder, unless @Builder.Default is used. Seeded rooms get createdAt = null.",
  "Add @Builder.Default or initialise in a constructor."),
 ("R11", REL, "Medium", "High", "Seed data parsed wrongly and re-written at every start",
  f"{API}/ApiApplication.java:143-168",
  "CWE-20", "Unsure", REVIEW,
  "line.split(\",\") splits inside the quoted equipment list, so each seeded room keeps only its first equipment. The 6 rooms are overwritten each time the API starts.",
  "Use a CSV parser (OpenCSV is already a dependency) and seed only if empty."),
 ("R12", REL, "High", "High", "Bad-word filter rejects normal business words",
  f"{CHAT}/validators/NoBadWordsValidator.java:21",
  "CWE-697", "No", REVIEW,
  "Substring matching on short words (\"con\", \"cul\", \"pd\", \"tg\") blocks words like contrat, consultation, compte, calcul: exactly the vocabulary of this business.",
  "Match whole words (regex \\b...\\b) and keep the list in configuration."),
 ("R13", REL, "Medium", "Medium", "Uncaught JWT and login exceptions return 500",
  f"{API}/config/JwtAuthenticationFilter.java:40; {API}/controllers/AuthController.java:98",
  "CWE-248 / CWE-755", "Unsure", REVIEW,
  "An expired or malformed token throws inside the filter (500, not 401). Login only catches BadCredentialsException, not DisabledException/LockedException (archived users).",
  "Catch JwtException in the filter; handle AuthenticationException globally."),
 ("R14", REL, "Low", "Medium", "Possible infinite recursion in toString/hashCode",
  f"{API}/entities/Chat.java:31 and Message.java (sender/chat); same in chatapp",
  "CWE-674", "Unsure", REVIEW,
  "@Data/@ToString on the bidirectional Chat <-> Message relation: calling toString() or hashCode() on either recurses until StackOverflowError.",
  "Exclude the back-reference (@ToString.Exclude, @EqualsAndHashCode.Exclude)."),
 ("R15", REL, "Medium", "High", "Front end never releases subscriptions or the WebSocket",
  f"{WEB} (128 .subscribe(), 1 ngOnDestroy); {WEB}/core/services/chat.service.ts:47",
  "CWE-772 / CWE-401", "Yes", REVIEW,
  "Each visit to the chat opens a new STOMP connection and subscription that is never closed; other components keep subscriptions alive after navigation.",
  "Unsubscribe in ngOnDestroy (takeUntil) and disconnect the STOMP client."),
 ("R16", REL, "Low", "High", "Silent failures and broken features",
  f"{API}/services/DomiAffaireServiceImpl.java:1563-1581; {WEB}/core/services/auth.service.ts:36-39,71-76,95-96",
  "CWE-754", "Unsure", REVIEW,
  "changePassword returns success when the id does not exist. The front end calls /api/auth/verifyEmail and /password-reset-request, which the API does not implement; resetPassword posts to a URL read from a cookie.",
  "Throw when the user is missing; implement or remove the reset flow."),
 ("R17", REL, "Low", "High", "Generic RuntimeException wrapping and malformed error bodies",
  f"{API}/controllers/AdminController.java:141,565,394,396,427,429; {API}/controllers/ClientController.java:126,138,168",
  "CWE-397", "Unsure", REVIEW,
  "Checked exceptions are re-thrown as RuntimeException (500); several error bodies miss their braces and are not valid JSON.",
  "Use a @ControllerAdvice with typed exceptions and a standard error body."),
 ("R18", REL, "Low", "High", "Phone-number regex has a broken character class",
  f"{API}/dto/SignupRequest.java:32",
  "CWE-185", "Unsure", REVIEW,
  "[2-5-4-7|9] also accepts '-' and '|' as the first character.",
  "Use ^[2-9]\\d{7}$ (or the exact list of Tunisian prefixes)."),
 # ---------------- PERFORMANCE EFFICIENCY ----------------
 ("P01", PERF, "High", "High", "Scheduler reloads all deadlines every second",
  f"{API}/services/DeadlineServiceImpl.java:44-46",
  "CWE-1050", "Yes", REVIEW,
  "@Scheduled(fixedRate = 1000) loads every domiciliation request with a deadline, each with about 10 eager @DBRef objects (files with their bytes, users with photos): 86,400 times a day.",
  "Run daily (cron), query only deadlines in the next 5 days, project only the needed fields."),
 ("P02", PERF, "High", "High", "File contents stored inside documents and sent in every list",
  f"{API}/entities/File.java:21; {API}/entities/User.java (image); {API}/dto/DomiciliationRequestDTO.java; {API}/mappers/Mapper.java",
  "CWE-1049 (approx.)", "Unsure", REVIEW,
  "byte[] fileData / image are loaded through @DBRef whenever a request, blog, chat or user is read, and serialised as base64 in list responses (e.g. all domiciliation requests with up to 9 files each).",
  "Store files in GridFS/object storage; return metadata + a download URL; exclude bytes from lists."),
 ("P03", PERF, "Medium", "High", "N+1 queries on deadlines",
  f"{API}/services/DeadlineServiceImpl.java:93-98,106-111",
  "CWE-1060 (approx.)", "Unsure", REVIEW,
  "One findByDeadline() query per deadline in the loop.",
  "Fetch the requests for all deadlines in one query (deadline in [...])."),
 ("P04", PERF, "Medium", "High", "Database calls inside loops",
  f"{API}/services/ReservationServiceImpl.java:56; {API}/services/DomiAffaireServiceImpl.java:976-978,1199-1206",
  "CWE-1050", "Yes", REVIEW,
  "addReservation reloads the same room for every slot; deleteBlogCategory saves blogs one by one; archiveBlog loads all users and rewrites all of them with saveAll.",
  "Load once outside the loop; use saveAll on the changed items only; use an update query ($pull) for archiveBlog."),
 ("P05", PERF, "Medium", "High", "Full collection scans and in-memory filtering",
  f"{API}/services/DomiAffaireServiceImpl.java:266-274,82-88,120-131,1354-1358",
  "CWE-1049 (approx.)", "Unsure", REVIEW,
  "validateConsultationRequest loads all chats to find one; clients are filtered in Java; getPackCounts loads every pack with its full user list just to count.",
  "Use derived queries (findByClientAndAccountant, findByUserRoleAndEnabled...) and count queries."),
 ("P06", PERF, "Medium", "High", "Pack embeds full User documents (unbounded growth)",
  f"{API}/entities/Pack.java:26; {API}/services/DomiAffaireServiceImpl.java:807-809",
  "none certain", "Unsure", REVIEW,
  "users is a Set<User> without @DBRef, so whole user documents (photo bytes, password hash) are copied into each pack; the document grows with every subscriber toward MongoDB's 16 MB limit.",
  "Keep only user ids (or a counter) in Pack."),
 ("P07", PERF, "Medium", "High", "Chat history list grows forever and is rewritten on each message",
  f"{CHAT}/services/WebSocketService.java:26-35; {API}/services/DomiAffaireServiceImpl.java:300-317; Chat.java messages",
  "CWE-1050 (approx.)", "Unsure", REVIEW,
  "Sending one message loads the chat with all previous messages (eager @DBRef) and saves the whole array: cost grows with history length.",
  "Do not keep messages inside Chat; query messages by chatId with paging."),
 ("P08", PERF, "Medium", "High", "No pagination on any list endpoint",
  f"{API}/controllers/*.java (findAll* everywhere)",
  "CWE-1049 (approx.)", "Unsure", REVIEW,
  "All lists (users, requests, blogs, reservations, deadlines) are returned in full.",
  "Use Pageable / Page<T> in repositories and endpoints."),
 # ---------------- MAINTAINABILITY ----------------
 ("M01", MAIN, "High", "High", "God class: DomiAffaireServiceImpl",
  f"{API}/services/DomiAffaireServiceImpl.java (1,585 lines, about 70 methods, 15 repositories)",
  "CWE-1080 / CWE-1048", "Yes", REVIEW,
  "Users, files, chats, consultations, domiciliation, packs, blogs, FAQs and reporting all live in one class.",
  "Split by domain (UserService, DomiciliationService, BlogService, ChatService...)."),
 ("M02", MAIN, "High", "High", "Heavy code duplication",
  f"{API}/services/DomiAffaireServiceImpl.java:390-595 (3 near-identical methods), File.builder block x12, auth-user lookup x~35; controllers repeat the same endpoints",
  "CWE-1041", "Yes", REVIEW,
  "The same code is copied many times: three sendDomiciliationRequest variants, the 'find authenticated user' block, the upload type check (x6), identical blog/chat endpoints in Client/Accountant/User controllers, two branches of updateUser.",
  "Extract helpers (currentUser(), saveFile(), allowedType()), merge controllers."),
 ("M03", MAIN, "Medium", "High", "Dead and commented-out code",
  f"{API}/ApiApplication.java:36-141; {API}/controllers/AuthController.java:40; {API}/utils/JwtUtil.java:45-49; {API}/config/SimpleCorsFilter.java:27-28; {API}/config/RestTemplateConfig.java; {API}/services/DeadlineServiceImpl.java:3",
  "CWE-561 / CWE-563", "Yes", REVIEW,
  "100+ commented lines, unused methods (findAllUsers, uploadFile, findAllFiles, resetUserPassword, generateRefreshToken), unused field tokenBlacklist, unused locals, unused import, unused RestTemplate bean and WebSocket config in the API.",
  "Delete; version control keeps the history."),
 ("M04", MAIN, "Low", "High", "Conditions that are always true",
  f"{API}/services/DomiAffaireServiceImpl.java:1422,1436,1504",
  "CWE-571", "Unsure", REVIEW,
  "newFile != null right after new File(); admin != null right after .get(). The 'return null' branches are unreachable.",
  "Remove the dead conditions."),
 ("M05", MAIN, "Medium", "High", "Layering bypassed: controllers use repositories and concrete classes",
  f"{API}/controllers/AuthController.java:39,107; all controllers inject *ServiceImpl",
  "CWE-1057", "Yes", REVIEW,
  "AuthController calls UserRepository directly; controllers depend on implementations instead of the service interfaces that exist.",
  "Inject the interfaces; keep data access in services."),
 ("M06", MAIN, "Medium", "High", "Magic numbers and hard-coded literals",
  f"{API}/utils/JwtUtil.java:41; {API}/services/DomiAffaireServiceImpl.java:860-863,975; app/web-client-07-06-2024/src/environments/environment.ts:3",
  "CWE-1106", "Yes", REVIEW,
  "Token lifetime 10000*60*24 = 4 h (probably meant 24 h); tax rates 0.19 and 0.1; category name 'Default'; status strings 'In Process', 'Quarter'; API URL in environment.ts (seen in step 1).",
  "Named constants, enums and configuration properties."),
 ("M07", MAIN, "Medium", "High", "Same domain model duplicated in two services",
  f"{CHAT}/entities/User.java, Chat.java, Message.java vs {API}/entities/",
  "CWE-1041", "Yes", REVIEW,
  "User/Chat/Message are defined twice and already differ; a change in one service silently breaks the other.",
  "Share a module, or let only one service own the chat data."),
 ("M08", MAIN, "Medium", "High", "Outdated, conflicting or incompatible dependencies",
  "app/api/pom.xml:53-76,100-115; web-client package.json (tinymce-angular 8 vs Angular 15)",
  "CWE-1104", "Yes", STEP1,
  "jjwt 0.9.1 together with jjwt 0.11.5; springfox (does not support Spring Boot 3, plus @EnableWebMvc disables Boot's MVC auto-configuration); android-json in a server; unused webflux/google-api-client; npm peer conflict.",
  "Remove unused libraries, keep one jjwt, replace springfox with springdoc-openapi."),
 ("M09", MAIN, "Low", "High", "Debug output left in code",
  f"{API}/controllers/ClientController.java:184; AccountantController.java:114; UserController.java:40; ReservationServiceImpl.java:127,151; front end: 182 console.log",
  "CWE-489", "Unsure", REVIEW,
  "System.out.println and console.log used for debugging; the controller lines even call the service twice just to print a size.",
  "Use the logger at debug level; strip console.log in production."),
 ("M10", MAIN, "Medium", "Medium", "Long, deeply nested methods",
  f"{API}/services/DomiAffaireServiceImpl.java:787-824,827-853; {API}/services/DeadlineServiceImpl.java:45-87",
  "CWE-1121", "Yes", REVIEW,
  "Several branches, nested ifs and side effects mixed in one method (status, pack, deadline, notification, document code).",
  "Split into small steps; replace if/else chains on PaymentMode with an enum method (months())."),
 ("M11", MAIN, "Low", "High", "Too many parameters",
  f"{API}/services/DomiAffaireServiceImpl.java:501-507",
  "CWE-1064", "Yes", REVIEW,
  "sendDomiciliationRequestPMTransfert takes 7 parameters (6 files).",
  "Group the files into one request object."),
 ("M12", MAIN, "Low", "High", "Unclear or misleading text in code",
  f"{API}/services/DomiAffaireServiceImpl.java:835; {API}/controllers/AdminController.java:106; {CHAT}/services/WebSocketService.java:53",
  "none", "No", REVIEW,
  "User-facing message in Tunisian dialect slang; comments in mixed languages; a comment says 'convert nanoseconds to milliseconds' but nothing is converted.",
  "Use clear, consistent messages (i18n) and accurate comments."),
 ("M13", MAIN, "Low", "High", "State changes through HTTP GET",
  f"{API}/controllers/AdminController.java:433-455,617-637; ClientController.java:239-263",
  "none", "No", REVIEW,
  "archive/unarchive, accept/reject reservation and save/unsave blog are GET requests; they can be triggered by prefetching or a simple link.",
  "Use POST/PUT/DELETE for state changes."),
 ("M14", MAIN, "Medium", "High", "Almost no automated tests",
  "app/api/src/test (2 test classes, about 300 lines for about 6,800 lines of Java)",
  "none", "No", REVIEW,
  "None of the bugs above (null handling, ownership, money, scheduling) is covered by a test.",
  "Add service tests for each rule and security tests for each role."),
]

HEAD = ["id", "characteristic", "severity", "confidence", "title", "location", "cwe_A", "in_iso5055_guess_A",
        "origin", "explanation", "fix", "found_A", "verdict_B", "iso_cwe_B", "found_CAST", "found_Sonar"]


def write_csv():
    with open(ROOT / "findings.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(HEAD)
        for r in F:
            w.writerow(list(r) + ["yes", "", "", "", ""])


ORDER = [SEC, REL, PERF, MAIN]
SEV = ["Critical", "High", "Medium", "Low", "Info"]


def counts():
    c = Counter((r[1], r[2]) for r in F)
    return c


def md_report():
    c = counts()
    lines = []
    a = lines.append
    a("# Step 2: Review A, ISO/IEC 5055 review from knowledge only")
    a("")
    a("**Analyst:** Claude Code (AI coding assistant), reading the source code. **Date:** 2026-10-15.")
    a("**Scope:** `app/api` and `app/chatapp` (all Java, about 6,800 lines), plus the Angular services, guards and")
    a("risky templates of `app/web-client-07-06-2024`.")
    a("")
    a("## Method and rules")
    a("- **Allowed:** reading the code (file read and text search), and the analyst's own prior knowledge of ISO/IEC 5055 and of the CWE list.")
    a("- **Not allowed:** static-analysis tools, the internet, the text of the ISO/IEC 5055 standard, and the team's earlier material.")
    a("- **Honesty labels:**")
    a("  - `seen during planning`: noticed before the review started (CORS, OAuth secret).")
    a("  - `seen during step 1`: noticed while making the app run (dependency problems, hard-coded API URL).")
    a("- **CWE numbers are written from memory.** The column *In ISO 5055? (guess)* is the analyst's belief, not a check.")
    a("  Step 3 verifies both against the standard.")
    a("- **Not dynamically tested.** Every finding comes from reading the code. Severity is the analyst's judgement.")
    a("")
    a("## Summary")
    a("")
    a("| Characteristic | Findings | Critical | High | Medium | Low/Info |")
    a("|---|---|---|---|---|---|")
    tot = Counter()
    for ch in ORDER:
        n = sum(1 for r in F if r[1] == ch)
        row = [c[(ch, s)] for s in SEV]
        tot.update({"n": n, "c": row[0], "h": row[1], "m": row[2], "l": row[3] + row[4]})
        a(f"| {ch} | {n} | {row[0]} | {row[1]} | {row[2]} | {row[3] + row[4]} |")
    a(f"| **Total** | **{tot['n']}** | **{tot['c']}** | **{tot['h']}** | **{tot['m']}** | **{tot['l']}** |")
    a("")
    a("### The five most important problems")
    a("1. **Broken access control everywhere (S07–S13).** The API checks the *role* but never the *owner*.")
    a("   - Any client can delete any account, edit any profile and even demote the admin.")
    a("   - Any client can read other clients' ID-card files and anyone's chats.")
    a("2. **Secrets in the code (S04, S05).**")
    a("   - The JWT signing key is in the public repository, so admin tokens can be forged.")
    a("   - Accountant sign-up is protected only by the code `abcd`.")
    a("3. **Password hashes are published (S01–S03).** A public endpoint lists every user with their bcrypt hash, and many")
    a("   responses embed full `User` objects.")
    a("4. **Chat service without authentication (S14).** Anyone can read any conversation or write in someone else's name.")
    a("5. **Performance design (P01, P02).**")
    a("   - A job reloads every deadline, with all attached files, **every second**.")
    a("   - Uploaded files are stored inside documents and sent back in every list.")
    a("")
    for ch in ORDER:
        a(f"## {ch}")
        a("")
        a("| ID | Severity | Finding | Location | CWE (recalled) | In ISO 5055? (guess) | Origin |")
        a("|---|---|---|---|---|---|---|")
        for r in F:
            if r[1] != ch:
                continue
            loc = r[5].replace("app/api/src/main/java/com/domiaffaire/api/", "api/…/").replace(
                "app/chatapp/src/main/java/com/wassim/chatapp/", "chatapp/…/").replace(
                "app/web-client-07-06-2024/src/app", "web/…")
            a(f"| {r[0]} | {r[2]} | {r[4]} | `{loc}` | {r[6]} | {r[7]} | {r[8]} |")
        a("")
        for r in F:
            if r[1] != ch:
                continue
            a(f"**{r[0]}: {r[4]}** ({r[2]}, confidence {r[3].lower()})")
            a(f"- *Why it matters:* {r[9]}")
            a(f"- *Fix:* {r[10]}")
            a("")
    a("## What this review could not see")
    a("- Runtime behaviour: nothing was executed for this review.")
    a("- Library vulnerabilities (CVEs) in the dependency versions.")
    a("- The Flutter mobile client and the Python recommendation service, which are out of scope.")
    a("- Cross-file data flows longer than a few calls; specialized tools (steps 5 and 6) should do better here.")
    a("")
    a("The machine-readable list is in [`findings.csv`](../findings.csv): one row per finding, with empty columns for steps 3, 5 and 6.")
    return "\n".join(lines) + "\n"


CSS = """
@page { size: A4; margin: 16mm 14mm; }
body { font-family: 'Segoe UI', Arial, sans-serif; font-size: 10pt; color: #1d2433; line-height: 1.4; }
h1 { font-size: 20pt; margin: 0 0 4px; color: #0b3d91; }
h2 { font-size: 13pt; color: #0b3d91; border-bottom: 2px solid #0b3d91; padding-bottom: 2px; margin-top: 16px; }
.sub { color: #555; margin-bottom: 10px; }
table { border-collapse: collapse; width: 100%; margin: 6px 0 10px; font-size: 8.6pt; }
th, td { border: 1px solid #c9d1e0; padding: 3px 5px; vertical-align: top; text-align: left; }
th { background: #e9eef8; }
.num { text-align: center; }
.k { display: inline-block; padding: 1px 6px; border-radius: 8px; font-size: 8pt; color: #fff; }
.Critical { background: #b00020; } .High { background: #d9480f; } .Medium { background: #e6a700; color:#222 }
.Low { background: #5c7cfa; } .Info { background: #868e96; }
.box { background: #f4f6fb; border-left: 4px solid #0b3d91; padding: 6px 10px; margin: 8px 0; }
.small { font-size: 8.5pt; color: #444; }
ol li { margin-bottom: 3px; }
.pb { page-break-before: always; }
"""


def pdf_html():
    c = counts()
    e = html.escape
    out = [f"<!doctype html><html><head><meta charset='utf-8'><title>Review A: ISO 5055 (knowledge only)</title><style>{CSS}</style></head><body>"]
    out.append("<h1>DomiAffaire: ISO/IEC 5055 review A</h1>")
    out.append("<div class='sub'>Knowledge-only code review by Claude Code &middot; 2026-10-15 &middot; Step 2 of the audit "
               "(github.com/inesCherif/domiaffaire-iso5055-audit)</div>")
    out.append("<div class='box'><b>Method.</b> The analyst read the code only (about 6,800 lines of Java in <code>api</code> and <code>chatapp</code>, plus the "
               "key Angular files). It used no scanner, no internet and <b>not the ISO 5055 text</b>; CWE numbers are from memory. "
               "Step 3 checks them against the standard.</div>")
    out.append("<h2>Results per ISO 5055 characteristic</h2><table><tr><th>Characteristic</th><th class='num'>Findings</th>"
               "<th class='num'>Critical</th><th class='num'>High</th><th class='num'>Medium</th><th class='num'>Low / Info</th></tr>")
    tot = [0, 0, 0, 0, 0]
    for ch in ORDER:
        row = [sum(1 for r in F if r[1] == ch), c[(ch, 'Critical')], c[(ch, 'High')], c[(ch, 'Medium')], c[(ch, 'Low')] + c[(ch, 'Info')]]
        tot = [a + b for a, b in zip(tot, row)]
        out.append(f"<tr><td>{ch}</td>" + "".join(f"<td class='num'>{v}</td>" for v in row) + "</tr>")
    out.append("<tr><th>Total</th>" + "".join(f"<th class='num'>{v}</th>" for v in tot) + "</tr></table>")
    out.append("<h2>The five most important problems</h2><ol>"
               "<li><b>Broken access control (S07&ndash;S13).</b> The API checks the role, never the owner. Any client can delete any account, "
               "edit any profile (even demote the admin), and read other clients' ID-card files and chats.</li>"
               "<li><b>Secrets in code (S04, S05).</b> The JWT signing key is in the public repo, so tokens can be forged. "
               "Accountant sign-up is protected only by the code <code>abcd</code>.</li>"
               "<li><b>Password hashes exposed (S01&ndash;S03).</b> A <i>public</i> endpoint lists all users with their bcrypt hash, "
               "and many responses embed full <code>User</code> objects.</li>"
               "<li><b>Chat service without authentication (S14).</b> Anyone can read any room or write as anyone.</li>"
               "<li><b>Performance design (P01, P02).</b> A scheduler reloads every deadline, with attached files, every second. "
               "Files are stored inside documents and returned in every list.</li></ol>")
    top = ["S07", "S08", "S04", "S14", "S01", "S09", "R04", "R12", "P01", "P02", "M01", "M02"]
    out.append("<h2>Top findings with evidence</h2><table><tr><th>ID</th><th>Sev.</th><th>Finding</th><th style='width:24%'>Where</th><th style='width:11%'>CWE (recalled)</th></tr>")
    for r in F:
        if r[0] in top:
            loc = r[5].split(";")[0].replace("app/api/src/main/java/com/domiaffaire/api/", "api/").replace(
                "app/chatapp/src/main/java/com/wassim/chatapp/", "chatapp/")
            out.append(f"<tr><td>{r[0]}</td><td><span class='k {r[2]}'>{r[2]}</span></td><td><b>{e(r[4])}</b><br><span class='small'>{e(r[9])}</span></td>"
                       f"<td style='word-break:break-all'><code>{e(loc)}</code></td><td>{e(r[6])}</td></tr>")
    out.append("</table>")
    out.append("<h2>All findings</h2><table><tr><th>ID</th><th>Characteristic</th><th>Sev.</th><th>Finding</th><th>CWE (recalled)</th><th>In ISO 5055? (guess)</th></tr>")
    for r in F:
        out.append(f"<tr><td>{r[0]}</td><td>{r[1]}</td><td><span class='k {r[2]}'>{r[2]}</span></td><td>{e(r[4])}</td><td>{e(r[6])}</td><td>{r[7]}</td></tr>")
    out.append("</table>")
    out.append("<h2>Limits</h2><ul class='small'><li>Nothing was executed for this review, and library CVEs were not checked.</li>"
               "<li>The mobile client and the Python recommendation service are out of scope.</li>"
               "<li>CWE labels and ISO 5055 membership are recalled, not verified. That is the purpose of step 3.</li>"
               "<li>Origins: 2 findings were seen during planning (S15, S20) and 1 during step 1 (M08); the permitAll rule behind S01 was also seen in step 1. All others come from the review.</li></ul>")
    out.append("<p class='small'>Full report: <code>reports/02-review-knowledge.md</code> &middot; data: <code>findings.csv</code></p></body></html>")
    return "".join(out)


if __name__ == "__main__":
    write_csv()
    (ROOT / "reports" / "02-review-knowledge.md").write_text(md_report(), encoding="utf-8")
    (ROOT / "reports" / "src").mkdir(exist_ok=True)
    (ROOT / "reports" / "src" / "02-review-knowledge.html").write_text(pdf_html(), encoding="utf-8")
    c = Counter(r[1] for r in F)
    print(len(F), dict(c), dict(Counter(r[2] for r in F)))
