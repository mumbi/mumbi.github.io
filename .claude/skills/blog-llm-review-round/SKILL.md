---
name: blog-llm-review-round
description: 글 초안을 codex 와 claude 로 병렬 리뷰하고 지적을 반영하는 한 회차를 돌려, 더 반영할 것이 없는지를 낸다
node:
  in:
    worktree_dir: { shape: text }
    post_path: { shape: text }
    materials_dir: { shape: text }
  out:
    clean: { shape: bool }
---

## 입력
- `worktree_dir` — 글이 있는 worktree 전체 경로. 리뷰어가 저장소 규칙 문서(AGENTS.md 등)를 여기서 읽고, 반영도 여기서 한다
- `post_path` — 리뷰·반영할 글 파일 전체 경로
- `materials_dir` — 자료 폴더 전체 경로. 사실 대조와 첨부 내용 확인의 근거

## 실행

### 그래프

같은 디렉터리의 `graph.json`이 이 워크플로의 정본이다.

codex 와 claude 가 같은 글을 서로 독립으로 리뷰하고(`blog-llm-review` 두 번, 병렬 가능), 두 지적 목록을 선언 순서(codex → claude)로 이어 `blog-post-apply-findings` 가 근거를 확인해 반영한다. 상위 워크플로가 조건 컨테이너로 이 회차를 `clean` 이 될 때까지 되풀이한다.

```
graph.in.worktree_dir (text)   graph.in.post_path (text)   graph.in.materials_dir (text)
    ├────────────────────────────────────┐
    ▼                                    ▼
 [review_codex]  reviewer='codex'     [review_claude]  reviewer='claude'
    │ findings (json, list:1)            │ findings (json, list:1)
    │ → apply.in.findings 1              │ → apply.in.findings 2
    ▼                                    │
 [apply]  ◄──────────────────────────────┘   (from graph.in.worktree_dir, graph.in.post_path)
    │ clean (bool) ═► graph.out.clean (bool)
```

### 판정 도구

모든 명령은 이 SKILL.md가 있는 디렉터리에서 실행한다 — graph.json은 그 디렉터리의 것이다.

```bash
BIN="/c/Users/예의상/Desktop/workspaces/claude-plugins/plugins/recipe/tools/pipecheck/dist/pipecheck-windows-amd64.exe"
SKILLS_PROJECT="$(cd .. && pwd)"   # 이 SKILL.md 가 있는 디렉터리의 상위 = 프로젝트 .claude/skills
SKILLS_USER="$HOME/.claude/skills"
BUILD="/c/Users/예의상/Desktop/workspaces/claude-plugins/plugins/recipe/tools/pipecheck/build.sh"
if [ ! -e "$BIN" ]; then   # 플러그인 업데이트로 버전 디렉터리가 바뀐 경우
  BASE="${BIN%/tools/pipecheck/dist/*}"; NAME="${BIN##*/}"
  while IFS= read -r D; do
    if [ -e "${D}tools/pipecheck/build.sh" ]; then
      BIN="${D}tools/pipecheck/dist/$NAME"; BUILD="${D}tools/pipecheck/build.sh"; break
    fi
  done < <(ls -d "${BASE%/*}"/*/ 2>/dev/null | sort -V -r)
fi
```
기록한 `$BIN`이 없으면 위 블록이 기록 경로의 버전 디렉터리를 형제 중 가장 높은 버전으로
바꿔 다시 찾는다 — 플러그인 캐시는 버전별 디렉터리라 업데이트하면 옛 경로가 사라진다.
그래도 `$BIN`이 없으면 `"$BUILD"`를 먼저 실행해 만든다(파일 시각은 설치·체크아웃 때
새로 찍혀 소스 변경 판단에 쓰지 않는다). 빌드가 실패하면 — `$BUILD`가 없는 경우도 같다 — 그 출력을
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
- `clean` — 이번 회차에 반영할 지적이 없었으면 `true`, 하나라도 반영했으면 `false`
