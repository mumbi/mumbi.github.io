"""리뷰 에이전트가 처음 읽을 컨텍스트를 .review-input/ 에 만든다.

작업 폴더는 PR head 를 전체 기록과 함께 체크아웃한 상태여야 한다(origin/<base> 포함).
환경 변수: REPO, PR_NUMBER, MODE(push|reply|mention), GITHUB_EVENT_PATH, OUT_DIR(기본 .review-input)
"""
import json
import os
import re
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

BOT_REST = "claude[bot]"  # REST 는 앱 계정에 [bot] 을 붙이고
BOT_GQL = "claude"  # GraphQL 은 붙이지 않는다

REPO = os.environ["REPO"]
OWNER, NAME = REPO.split("/")
PR = int(os.environ["PR_NUMBER"])
MODE = os.environ["MODE"]
OUT = Path(os.environ.get("OUT_DIR", ".review-input"))

HIGH_EXT = {".py", ".sh", ".ps1", ".js", ".mjs", ".cjs", ".ts", ".go", ".rb"}
MID_EXT = {".json", ".toml", ".yml", ".yaml", ".html"}
CONFIG_PREFIXES = (".claude/", "CLAUDE.md", "CLAUDE.local.md", ".mcp.json", ".claude.json", ".gitmodules", ".ripgreprc", ".husky/")


def run(*args):
    return subprocess.run(args, check=True, capture_output=True, text=True, encoding="utf-8").stdout


def gh_json(*args):
    return json.loads(run("gh", *args))


def graphql(query, **variables):
    args = ["api", "graphql", "-f", f"query={query}"]
    for k, v in variables.items():
        args += ["-F" if isinstance(v, int) else "-f", f"{k}={v}"]
    return gh_json(*args)["data"]


def oneline(text, limit):
    text = re.sub(r"\s+", " ", text or "").strip()
    return text if len(text) <= limit else text[:limit] + " …(생략)"


def write(name, text):
    (OUT / name).write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def severity(body):
    m = re.search(r"\bP([123])\b", (body or "")[:200])
    return f"P{m.group(1)}" if m else "-"


def risk(path):
    lower = path.lower()
    name = lower.rsplit("/", 1)[-1]
    ext = os.path.splitext(name)[1]
    if ext in HIGH_EXT or lower.startswith(".github/"):
        return "높음"
    if name in ("skill.md", "graph.json") or ext in MID_EXT or lower.startswith(("layouts/", "config/")):
        return "중간"
    return "낮음"


# --- PR 과 연결된 이슈 -------------------------------------------------------
pr = graphql(
    """query($owner:String!,$name:String!,$number:Int!){repository(owner:$owner,name:$name){pullRequest(number:$number){
      title body url baseRefName headRefName headRefOid additions deletions changedFiles
      closingIssuesReferences(first:5){nodes{number title body}}
      reviewThreads(first:100){nodes{id isResolved isOutdated path line originalLine
        comments(first:100){nodes{databaseId author{login} body createdAt}}}}}}}""",
    owner=OWNER, name=NAME, number=PR,
)["repository"]["pullRequest"]
base = pr["baseRefName"]
head = run("git", "rev-parse", "HEAD").strip()
base_sha = run("git", "rev-parse", f"origin/{base}").strip()

OUT.mkdir(parents=True, exist_ok=True)

lines = [f"# PR #{PR}: {pr['title']}", "", pr["url"], "",
         f"- 브랜치: `{pr['headRefName']}` → `{base}`",
         f"- 바뀐 파일 {pr['changedFiles']}개, +{pr['additions']} −{pr['deletions']}", "", "## 본문", "", pr["body"] or "(없음)"]
issues = pr["closingIssuesReferences"]["nodes"]
for issue in issues:
    body = issue["body"] or "(없음)"
    if len(body) > 20000:
        body = body[:20000] + "\n…(생략)"
    lines += ["", f"## 연결된 이슈 #{issue['number']}: {issue['title']}", "", body]
if not issues:
    lines += ["", "## 연결된 이슈", "", "(없음)"]
write("pr.md", "\n".join(lines))

# --- 마지막 리뷰와 이후 변경 ----------------------------------------------
pages = gh_json("api", f"repos/{REPO}/pulls/{PR}/reviews?per_page=100", "--paginate", "--slurp")
# 새 커밋이 올라오면 이전 판정은 DISMISSED 로 바뀐다. 그래도 그 커밋까지는 판정한 것이다
reviews = [r for page in pages for r in page
           if r["user"]["login"] == BOT_REST and r["state"] in ("APPROVED", "CHANGES_REQUESTED", "DISMISSED")]
last = reviews[-1] if reviews else None

diff = run("git", "-c", "core.quotepath=false", "diff", "--no-color", "-M", f"origin/{base}...HEAD")
write("diff.patch", diff or "(변경 없음)")

if not last:
    since_note = "첫 리뷰입니다. 비교할 이전 리뷰가 없습니다"
    write("since-last.patch", "(첫 리뷰)")
elif last["commit_id"] == head:
    since_note = "마지막 리뷰 뒤로 새 커밋이 없습니다"
    write("since-last.patch", "(새 커밋 없음)")
elif subprocess.run(["git", "cat-file", "-e", f"{last['commit_id']}^{{commit}}"], capture_output=True).returncode:
    since_note = "마지막 리뷰 커밋을 찾을 수 없습니다(force push 로 보임). 전체 diff 로 판단합니다"
    write("since-last.patch", "(마지막 리뷰 커밋 없음)")
else:
    since = run("git", "-c", "core.quotepath=false", "diff", "--no-color", "-M", last["commit_id"], "HEAD")
    since_note = f"`{last['commit_id'][:7]}..{head[:7]}` 의 변경입니다. 그 사이 base 를 병합했다면 base 의 변경도 섞여 있습니다"
    write("since-last.patch", since or "(변경 없음)")

# --- 바뀐 파일 목차 ----------------------------------------------------------
status = run("git", "-c", "core.quotepath=false", "diff", "--name-status", "-z", "-M", f"origin/{base}...HEAD").split("\0")
entries = []
i = 0
while i < len(status) and status[i]:
    code = status[i]
    if code[0] in "RC":
        entries.append((code[0], status[i + 1], status[i + 2]))
        i += 3
    else:
        entries.append((code[0], None, status[i + 1]))
        i += 2

blocks = []  # diff.patch 에서 파일마다 (시작 줄, 끝 줄, 줄들)
diff_lines = diff.split("\n")
for n, line in enumerate(diff_lines, 1):
    if line.startswith("diff --git "):
        if blocks:
            blocks[-1][1] = n - 1
        blocks.append([n, len(diff_lines), []])
    elif blocks:
        blocks[-1][2].append(line)

KIND = {"A": "추가", "M": "수정", "D": "삭제", "R": "이름 변경", "C": "복사", "T": "종류 변경"}
rows = []
for idx, (code, old, path) in enumerate(entries):
    start, end, body = blocks[idx] if len(blocks) == len(entries) else (None, None, [])
    added = sum(1 for b in body if b.startswith("+") and not b.startswith("+++"))
    removed = sum(1 for b in body if b.startswith("-") and not b.startswith("---"))
    binary = any(b.startswith("Binary files ") for b in body)
    hunks = []
    for b in body:
        m = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", b)
        if m:
            s, c = int(m.group(1)), int(m.group(2) or 1)
            hunks.append(f"{s}(삭제만)" if c == 0 else f"{s}-{s + c - 1}")
    name = f"{old} → {path}" if old else path
    notes = []
    if binary:
        notes.append("바이너리: diff 에 내용이 없으니 이미지는 Read 로 엽니다")
    if path.startswith(CONFIG_PREFIXES):
        notes.append(f"PR 버전은 `.claude-pr/{path}`")
    rows.append(
        f"| `{name}` | {KIND.get(code, code)} | {risk(path)} | +{added} −{removed} | "
        f"{', '.join(hunks) if hunks else '-'} | {f'{start}-{end}' if start else '-'} | {'; '.join(notes)} |"
    )
files_md = ["# 바뀐 파일", "",
            f"`origin/{base}...HEAD` 기준입니다. hunk 범위는 head 파일의 줄 번호이고, diff 범위는 `diff.patch` 안의 줄 번호입니다(Read 의 offset·limit 에 씁니다).", "",
            "| 파일 | 종류 | 위험도 | 줄 | hunk (head 줄) | diff.patch 줄 | 참고 |", "|---|---|---|---|---|---|---|", *rows]
if len(blocks) != len(entries):
    files_md += ["", "diff.patch 줄 범위를 맞추지 못했습니다. 파일 diff 는 `git diff origin/<base>...HEAD -- <파일>` 로 봅니다"]
write("files.md", "\n".join(files_md))

# --- 리뷰 스레드 -------------------------------------------------------------
threads = []
for t in pr["reviewThreads"]["nodes"]:
    comments = t["comments"]["nodes"]
    if not comments:
        continue
    root = comments[0]
    threads.append({**t, "comments": comments, "root": root,
                    "ours": (root["author"] or {}).get("login") == BOT_GQL, "sev": severity(root["body"])})
SEV_ORDER = {"P1": 0, "P2": 1, "P3": 2}
threads.sort(key=lambda t: (not t["ours"], t["isResolved"], SEV_ORDER.get(t["sev"], 3), t["root"]["createdAt"]))


def render_thread(t, limit=1500):
    state = "resolve됨" if t["isResolved"] else "열림"
    if t["isOutdated"]:
        state += " · outdated"
    owner = "claude (처리 대상)" if t["ours"] else f"{(t['root']['author'] or {}).get('login', '?')} (읽기 전용)"
    where = f"{t['path']}:{t['line'] or t['originalLine'] or '-'}"
    out = [f"## 스레드 {t['root']['databaseId']} — {where} [{t['sev']}] {state}",
           f"- node ID: `{t['id']}`", f"- 연 쪽: {owner}"]
    for c in t["comments"]:
        out.append(f"- {(c['author'] or {}).get('login', '?')} ({c['createdAt'][:10]}): {oneline(c['body'], limit)}")
    return out + [""]


ours_open = [t for t in threads if t["ours"] and not t["isResolved"]]
count = {s: sum(1 for t in ours_open if t["sev"] == s) for s in ("P1", "P2", "P3", "-")}
open_summary = f"P1 {count['P1']}, P2 {count['P2']}, P3 {count['P3']}" + (f", 심각도 없음 {count['-']}" if count["-"] else "")
thread_md = ["# 리뷰 스레드", "",
             f"claude 가 연 스레드 중 열린 것: {open_summary}. 다른 봇·사람이 연 스레드는 읽기만 합니다", ""]
for t in threads:
    thread_md += render_thread(t)
if not threads:
    thread_md.append("(없음)")
write("threads.md", "\n".join(thread_md))

# --- 이번 실행을 부른 코멘트 --------------------------------------------------
event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8")) if os.environ.get("GITHUB_EVENT_PATH") else {}
comment = event.get("comment")
if MODE == "push" or not comment:
    write("trigger.md", "(새 커밋으로 시작된 리뷰입니다. 부른 코멘트가 없습니다)")
else:
    trig = ["# 이번 실행을 부른 코멘트", "",
            f"- 작성자: {comment['user']['login']}", f"- 코멘트 번호: {comment['id']}", "", comment["body"], ""]
    root_id = comment.get("in_reply_to_id") or comment["id"]
    thread = next((t for t in threads if t["root"]["databaseId"] == root_id), None)
    if "pull_request_review_id" in comment:
        trig += [f"인라인 스레드 {root_id} 에 달린 코멘트입니다. 답글은 이 스레드에 남깁니다", ""]
        trig += render_thread(thread, limit=6000) if thread else ["(스레드를 찾지 못했습니다)"]
    else:
        trig += ["PR 대화에 달린 코멘트입니다. 답은 PR 코멘트로 남깁니다", "", "## 최근 PR 대화", ""]
        recent = gh_json("api", f"repos/{REPO}/issues/{PR}/comments?per_page=100")[-10:]
        trig += [f"- {c['user']['login']} ({c['created_at'][:10]}): {oneline(c['body'], 1500)}" for c in recent]
    write("trigger.md", "\n".join(trig))

# --- 실행 상황 ---------------------------------------------------------------
today = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d")
last_state = "DISMISSED(새 커밋으로 무효가 됨)" if last and last["state"] == "DISMISSED" else (last or {}).get("state")
last_line = (f"`{last['commit_id'][:7]}` 에서 {last_state} ({last['submitted_at'][:10]})" if last else "없음")
write("context.md", "\n".join([
    "# 실행 상황", "",
    f"- 오늘 날짜(KST): {today}. 이보다 앞선 날짜를 미래라고 판단하지 않습니다",
    f"- 모드: {MODE}",
    f"- PR: #{PR} {pr['title']}",
    f"- base: `origin/{base}` ({base_sha[:7]}), head: `{head}`",
    f"- 인라인 코멘트의 commit_id: `{head}`",
    f"- claude 의 마지막 판정: {last_line}",
    f"- since-last.patch: {since_note}",
    f"- claude 가 연 열린 스레드: {open_summary}",
]))

for f in sorted(OUT.iterdir()):
    print(f"{f.name}\t{f.stat().st_size}")
