"""Approximate per-method counts for the ISO/IEC 5055 thresholds (Java only).

Applies the standard's default thresholds:
  CWE-1121 cyclomatic complexity > 20          (8.118)
  CWE-1048 outward calls > 5                    (8.128)
  CWE-1073 data-resource accesses > 2           (8.110, Performance)
  CWE-1084 data-resource accesses > 7           (8.119, Maintainability)
  CWE-1064 parameters > 7                       (8.125)
  CWE-1085 commented-out code > 2 % of a method (Table 1; 8.115 says 5 %)
  CWE-1080 file > 1000 lines                    (Table 1)
Heuristic text analysis: a data access = a call on a field whose name ends in 'Repository'.
"""
import re
import sys
from pathlib import Path

ROOTS = [Path(p) for p in sys.argv[1:]]
SIG = re.compile(r"^\s*(?:@\w+(?:\([^)]*\))?\s*)*(?:public|private|protected)?\s*(?:static\s+)?(?:final\s+)?"
                 r"(?:<[^>]+>\s+)?[\w<>\[\], ?]+\s+(\w+)\s*\(([^)]*)\)\s*(?:throws [\w., ]+)?\s*\{")
DECISION = re.compile(r"\b(if|for|while|case|catch)\b|&&|\|\||\?(?!\s*>)")
CALL = re.compile(r"\b([a-zA-Z_]\w*)\s*\.\s*([a-zA-Z_]\w*)\s*\(")
REPO = re.compile(r"\b(\w*Repository)\s*\.\s*(\w+)\s*\(")
CODEY = re.compile(r"^\s*//+.*(;|\{|\}|\)\s*$|=)")

rows = []
for root in ROOTS:
    for f in sorted(root.rglob("*.java")):
        lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        if len(lines) > 1000:
            rows.append((str(f), 0, "<file>", {"loc": len(lines)}))
        i = 0
        while i < len(lines):
            m = SIG.match(lines[i])
            if not m or m.group(1) in {"if", "for", "while", "switch", "catch", "synchronized"}:
                i += 1
                continue
            name, params = m.group(1), m.group(2)
            depth, j, body = 0, i, []
            while j < len(lines):
                depth += lines[j].count("{") - lines[j].count("}")
                body.append(lines[j])
                if depth <= 0 and "{" in "".join(body):
                    break
                j += 1
            code = [b for b in body if not b.strip().startswith("//")]
            text = "\n".join(code)
            cc = 1 + len(DECISION.findall(text))
            calls = {f"{a}.{b}" for a, b in CALL.findall(text) if a not in {"this", "super"}}
            repo = len(REPO.findall(text))
            nparams = 0 if not params.strip() else params.count(",") + 1
            commented = sum(1 for b in body if CODEY.match(b))
            nonempty = sum(1 for b in body if b.strip())
            rows.append((str(f), i + 1, name, {"cc": cc, "fanout": len(calls), "data": repo,
                                                "params": nparams, "commented": commented,
                                                "lines": nonempty}))
            i = j + 1

hits = {"CWE-1121": [], "CWE-1048": [], "CWE-1073": [], "CWE-1084": [], "CWE-1064": [], "CWE-1085": [], "CWE-1080": []}
for f, ln, name, d in rows:
    short = f.split("java" + "\\")[-1].split("java/")[-1]
    if name == "<file>":
        hits["CWE-1080"].append(f"{short} ({d['loc']} lines)")
        continue
    tag = f"{short}:{ln} {name}"
    if d["cc"] > 20: hits["CWE-1121"].append(f"{tag} (CC={d['cc']})")
    if d["fanout"] > 5: hits["CWE-1048"].append(f"{tag} (fan-out={d['fanout']})")
    if d["data"] > 2: hits["CWE-1073"].append(f"{tag} (data={d['data']})")
    if d["data"] > 7: hits["CWE-1084"].append(f"{tag} (data={d['data']})")
    if d["params"] > 7: hits["CWE-1064"].append(f"{tag} (params={d['params']})")
    if d["lines"] and d["commented"] / d["lines"] > 0.02: hits["CWE-1085"].append(f"{tag} ({d['commented']}/{d['lines']} lines)")

print("methods analysed:", sum(1 for r in rows if r[2] != "<file>"))
mx = max((r for r in rows if r[2] != "<file>"), key=lambda r: r[3]["cc"])
print("max CC:", mx[2], mx[3]["cc"], "| max params:", max(r[3].get("params", 0) for r in rows))
for k, v in hits.items():
    print(f"\n{k}: {len(v)}")
    for x in v:
        print("   ", x)
