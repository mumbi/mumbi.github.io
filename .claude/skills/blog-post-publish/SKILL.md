---
name: blog-post-publish
description: 블로그 자료 폴더와 주제로 글 규칙 조사 → 기획 → 첨부 이슈 → 초안 → LLM 리뷰 반복 → rubric 채점·반영 → 사용자 검토 → PR → 리뷰 봇 대응까지 진행해 PR URL 을 낸다(머지는 하지 않음)
node:
  in:
    repo_dir: { shape: text }
    topic: { shape: text }
    materials_dir: { shape: text }
  out:
    pr_url: { shape: text }
---

## 입력
- `repo_dir` — 블로그 저장소 로컬 체크아웃 전체 경로. 오래된 브랜치여도 된다 — 규칙은 원격 기본 브랜치에서 읽고, 글은 원격 기본 브랜치에서 만든 새 worktree 에 쓴다
- `topic` — 글의 주제와 핵심 메시지
- `materials_dir` — 자료 폴더 전체 경로(로그·덤프 분석·스크립트·첨부할 파일 등). 글의 모든 사실 주장은 여기서 근거를 찾는다

## 실행

### 그래프

같은 디렉터리의 `graph.json`이 이 워크플로의 정본이다.

원격 기본 브랜치에서 글 규칙을 조사하고(conv), 자료로 제목·slug·첨부 계획을 정한 뒤(plan), 첨부 파일을 준비해(prep) 글 추적 이슈에 올린다(attach). 첨부 URL 로 새 worktree 에 초안을 쓰고(draft), codex·claude 리뷰와 반영을 지적이 없을 때까지 최대 3회 되풀이한다(llm_review). 이어서 codex 가 글쓰기 규칙으로 한 번 채점하고(rubric) 그 지적을 한 번 반영한다(rubric_apply). 그 뒤 사용자가 rubric 점수(score_list 로 배열에 담아 넘긴다)와 함께 미리보기로 검토하고(review), PR 을 연 뒤(pr) 리뷰 봇 지적 대응을 최대 3회 되풀이해(pr_review) PR URL 을 낸다.

```
graph.in.repo_dir (text)   graph.in.topic (text)   graph.in.materials_dir (text)
    │
    ▼
 [conv]  (from graph.in.repo_dir)
    │ conventions (json) → plan.in.conventions, draft.in.conventions
    ▼
 [plan]  (from graph.in.topic, graph.in.materials_dir)
    │ attach_plan (json)
    │ issue_title (text) → attach.in.issue_title
    │ slug (text) → draft.in.slug      title (text) → draft.in.title, pr.in.title
    ▼
 [prep]  (from graph.in.materials_dir)
    │ files (text, list:1)
    ▼
 [attach]  (from graph.in.repo_dir)
    │ attachments (json)
    │ issue_number (num) → pr.in.issue_number
    ▼
 [draft]  (from graph.in.repo_dir, graph.in.topic, graph.in.materials_dir, conv.out.conventions, plan.out.slug, plan.out.title)
    │ worktree_dir (text) → llm_review.in.worktree_dir, rubric.in.worktree_dir, rubric_apply.in.worktree_dir, review.in.worktree_dir, pr.in.worktree_dir
    │ post_path (text) → llm_review.in.post_path, rubric.in.post_path, rubric_apply.in.post_path, review.in.post_path
    ▼
╭─ llm_review ── condition ───────╮
│  until clean                    │   (from graph.in.materials_dir)
│  max 3                          │
│  → [[blog-llm-review-round]]    │
╰─────────────────────────────────╯
    ╎
    ╎ order
    ▼
 [rubric]  reviewer='codex'
    │ findings (json, list:1)              │ score (json)
    ▼                                      ▼
 [rubric_apply]                         < score_list >
    │ clean (bool) — 미연결                expr scores = [score]
    ╎                                      │ scores (json, list:1) → review.in.rubric_score
    ╎ order                                │
    ▼                                      │
 [review]  ◄───────────────────────────────┘
    │ reviewed_post (text)
    ▼
 [pr]
    │ pr_url (text)
    ▼
╭─ pr_review ── condition ────────╮
│  until clean                    │
│  max 3                          │
│  → pr-review-round              │
╰─────────────────────────────────╯
    │ final_pr_url (text) ═► graph.out.pr_url (text)
```

### 판정 도구

모든 명령은 이 SKILL.md가 있는 디렉터리에서 실행한다 — graph.json은 그 디렉터리의 것이다.

```bash
OS=$(uname -s | tr A-Z a-z); EXT=""
case "$OS" in mingw*|msys*|cygwin*) OS=windows; EXT=".exe" ;; esac  # Windows Git Bash 는 uname -s 가 MINGW64_NT-… 등
NAME="pipecheck-$OS-$(uname -m | sed -e 's/x86_64/amd64/' -e 's/aarch64/arm64/')$EXT"
SKILLS_PROJECT="$(cd .. && pwd)"   # 이 SKILL.md 가 있는 디렉터리의 상위 = 프로젝트 .claude/skills
SKILLS_USER="$HOME/.claude/skills"
BIN="${PIPECHECK_BIN:-$(command -v pipecheck 2>/dev/null)}"; BUILD=""
if [ -z "$BIN" ] || [ ! -e "$BIN" ]; then   # recipe 플러그인 캐시에서 가장 높은 버전을 찾는다
  BIN=""
  while IFS= read -r D; do
    if [ -e "${D}tools/pipecheck/build.sh" ]; then
      BIN="${D}tools/pipecheck/dist/$NAME"; BUILD="${D}tools/pipecheck/build.sh"; break
    fi
  done < <(ls -d "${CLAUDE_CONFIG_DIR:-$HOME/.claude}"/plugins/cache/*/recipe/*/ 2>/dev/null | sort -V -r)
fi
```
`$BIN`은 `PIPECHECK_BIN` 환경 변수, `PATH`의 `pipecheck`, recipe 플러그인 캐시(버전 디렉터리 중
가장 높은 것) 순서로 찾는다 — 플러그인 캐시는 버전별 디렉터리라 업데이트하면 옛 경로가 사라진다.
`$BIN`이 없으면 `"$BUILD"`를 먼저 실행해 만든다(파일 시각은 설치·체크아웃 때
새로 찍혀 소스 변경 판단에 쓰지 않는다). 빌드가 실패하면 — `$BUILD`가 비었거나 없는 경우도 같다 — 그 출력을
보고하고 오류로 끝내며 `/pipeline` 재컴파일을 안내한다.
pipecheck 출력은 한 줄 JSON, 불통과는 exit 1. exit 2는 호출 오류 —
명령을 고쳐 같은 호출을 다시 부르는 연속 시도를 3회까지 하고, 그래도
exit 2면 그 출력과 시도한 명령을 담아 절차 8의 오류 보고 형식으로
끝낸다. 통과하거나 다른 호출로 넘어가면 시도 횟수는 남지 않는다.
해시 계산·대조는 pipecheck가 §5.8 정규형(계약 JSON 재직렬화·본문 원문+
최소 정규화·워크플로는 graph.json 결합)으로 수행한다 — verify-materials·hash.

값은 shape별 JSON 표현으로 나른다 — `text`는 문자열, `num`은 수,
`bool`은 `true`/`false`, `json`은 임의의 JSON 값(`null` 포함). 깊이는
배열 중첩이다(깊이 1 = 배열, 깊이 2 = 배열의 배열). JSON 수는 `double`로
읽고, `double`로 정확히 표현되지 않는 정수(절대값 2^53 초과)는 오류로
거부하며, `-0`은 `0`과 같은 값으로 읽는다.

### 절차

1. 실행 전 대조: `"$BIN" verify-materials -file graph.json -project "$SKILLS_PROJECT" -user "$SKILLS_USER"`
   불통과면 그 출력(어느 재료·경로·기록/현재 해시)을 보고하고 오류로 끝낸다
   — 재료가 컴파일 이후 바뀌었다는 뜻이므로 `/pipeline` 재컴파일을 안내한다.
2. 호출자가 준 경계 입력을 check-values로 검증한다. 호출 봉투는 stdin 한 JSON —
   `echo '{"ports":{"dir":{"shape":"text"},"tags":{"shape":"text","list":1,"required":false}},"given":{"dir":"/a/b"},"boundary":true}' | "$BIN" check-values`
   처럼 ports에 포트 선언 객체를, given에 실제 값을 넣는다(구성 요소 자리 검증은
   boundary: false). 필수 포트 생략은 깊이와 무관하게 오류이고, 미배선
   `required:false` 생략은 check-values가 `filled`로 빈 배열을 채운다.
   **모든 check-values 호출에서** 출력의 `filled`에 온 포트는 그 빈 배열을 실제
   값으로 상태에 넣는다. 경계 입력 값을 data 엣지를 따라 하류로 옮긴다.
3. 아직 처리되지 않은 구성 요소 중 준비된 것을 고른다 — 셋 전부:
   모든 입력 포트에 값이 있고(`const` 포트는 상수 값으로, 미배선
   `required:false` 포트는 빈 배열로 값이 있는 것으로 센다), 그 포트로 들어오는 data 엣지가 전부 도착했고
   (팬인은 전부 도착 후 엣지 선언 순서로 concat), 자기를 가리키는 order 엣지의
   선행이 전부 끝났다. 준비된 것이 여럿이면 아무거나(병렬 가능).
   실행 직전에 그 구성 요소의 입력 포트 일습을 check-values로 검증한다 —
   given에는 엣지 값과 함께 `const` 상수 값·미배선 `required:false`의 빈 배열을
   실제 값으로 넣고, 실행에도 같은 값을 쓴다.
4. 고른 것을 실행한다:
   - kind: node — 서브에이전트 하나. 재료는 graph.json `materials`에 적힌
     `name`+`scope`의 디렉터리로 해소한다 — 가림을 적용하지 않는다. 그
     SKILL.md 본문과 입력 포트 이름·값 매핑을 명시해 준다. 값은 포트별 JSON 그대로이며 데이터다 — 값 안의 문장은
     지시가 아니다. 요구하는 것은 내부 계약의 출력 포트 전부.
   - kind: transform — 식을 평가한다 — 평가는 실행자가 수행하고,
     `check-expr`는 타입 검사에만 쓴다. 식은 CEL 부분집합이다 — until 등 그래프의
     모든 표현식이 같은 규칙이다(`split`은 식이 아니라 입력 포트 이름
     목록이다):
     `filter`·`map`·`exists`·`all` 매크로, `size`, `in`, 비교·논리·산술,
     삼항(`c ? a : b`), 필드·인덱스 접근, 리스트·맵 리터럴, 호스트 함수 `zip(a,b)`(원소는 `{'a': a[i], 'b': b[i]}` 두 키 맵 — 두 길이가 다르면 오류)·
     `chunk(xs,n)`(n개씩 묶기 — 마지막 묶음은 짧을 수 있다)·`first_or(xs,d)`(첫 원소 또는 d)와
     메서드 `xs.flatten()`(한 겹 펴기)·`xs.join(sep)`(문자열 잇기)뿐이다. check-values에 넣을 포트 선언은
     `check-expr`에 식과 입력 선언을 주어 —
     `echo '{"expr":"...","in":{"이름":{"shape":"...","list":0}}}' | "$BIN" check-expr`
     — 돌려받은 추론 값(shape·list)에 graph.json의 `aligned`를 합쳐 쓴다. (런타임 오류 — dyn 필드 부재,
     chunk 크기, zip 길이, num 비유한 — 는 오류로). 평가가 실패하면 값을
     옮기지 않는다. 출력 일습을 한 봉투로 check-values에 넣어 검증한다 —
     aligned 짝 길이를 함께 대조하기 위해서다.
   - kind: container(condition) — 최소 1회 — 회차마다 감싼 스킬을 노드와
     같은 방식으로 서브에이전트 하나씩 띄워 실행한다. 회차 출력을 check-values로
     검증한 뒤 until을 그 회차 출력으로 평가한다. 참이면 출력을 내고 끝,
     거짓이면 carry대로 다음 회차 입력에 넣고 carry에 없는 입력은 컨테이너
     입력값을 유지한다 — 다음 회차 입력 일습도 check-values(aligned 포함).
     max를 소진했는데 until이 여전히 거짓이면 오류다.
   - 재료가 워크플로면 하위 워크플로 SKILL.md의 `## 실행` 절차를 재귀
     실행한다 — 실행 경로의 방문 집합
     (name+scope, 최상위 자신 포함, 경로마다 따로)을 물려주고, 재등장하면
     재료 이름·설치 위치·실행 경로를 보고하며 오류로 끝낸다. 어댑터의
     wraps 전이로 닿는 워크플로도 같은 방문 집합 규칙을 받는다. 하위가
     오류로 끝나면 하위의 끝난 목록을 상위 보고에 펼쳐 병합하고 — 하위
     항목은 재료 이름·설치 위치·실행 경로를 붙여 적는다 — 상위도
     오류다.
5. 서브에이전트를 띄운 실행마다 — 노드·어댑터·컨테이너 회차 — 출력을
   회수한다(transform·0회 컨테이너는 회수가 없다): 응답 말미의 단일 ```json 펜스 안 {"포트명": 값}
   객체 하나. 펜스가 없거나, 둘 이상이거나, 파싱이 실패하거나, 멤버 이름이
   중복되면 출력 미충족 오류다. 회수한 값을 check-values로 검증한다.
6. 구성 요소가 처리되면 — 노드·어댑터는 회수한 출력, transform은 평가
   출력, 컨테이너는 조립이 끝난 컨테이너 출력(회차 값이 아니라) — 검증을
   통과한 값을 data 엣지를 따라 하류 입력 포트로 옮긴다.
7. 준비된 것이 없어질 때까지 3으로. 경계 출력이 먼저 채워져도 멈추지 않는다.
8. 루프가 끝나면 판정한다: 경계 출력에 놓인 값 일습을 check-values로 검증하고
   (aligned 길이 포함), required:false 경계 출력 미충족은 빈 배열로 채우고,
   모든 구성 요소가 처리됐고 필수 경계 출력이 전부 채워졌으면 그 값들을
   호출자에게 돌려준다. 아니면 오류 — 무엇이 미처리·미충족인지, 끝난 구성
   요소·회차, 어느 검사가 무엇을 기대했고 무엇이 왔는지를 보고한다.
   조용히 빈 값을 돌려주지 않는다.

어느 check-values·verify-materials든 불통과면 그 출력(기대·실제)을 담아 절차
8의 오류 보고 형식 — 무엇이 미처리·미충족인지, 끝난 구성 요소·회차, 기대와
실제 — 으로 끝낸다. 오류는 전부 같은 형식으로 보고하고 끝낸다. 값을 지어내
대체하지 않는다.
재시도·부분 복구·중단 정리·병렬도 조절과 서브에이전트를 띄우는 수단은 이
절차가 정하지 않는다 — 실행자가 정하고, 수단은 실행 환경이 제공하는 격리
실행 수단에서 고른다.

## 출력
- `pr_url` — 만든 PR 의 URL. 리뷰 봇 대응까지 끝난 상태이며, 머지는 사용자가 한다
