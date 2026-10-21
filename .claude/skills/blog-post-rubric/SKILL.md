---
name: blog-post-rubric
description: 글 초안을 외부 LLM 에이전트 CLI(codex 또는 claude) 하나로 독립 채점해, 글쓰기 규칙(docs/writing-guide.md) 기준 20개 항목 점수와 100점 총점, 2점 미만 항목의 지적 목록을 낸다
node:
  in:
    worktree_dir: { shape: text }
    post_path: { shape: text }
    reviewer: { shape: text, values: [codex, claude] }
  out:
    score: { shape: json }
    findings: { shape: json, list: 1, required: false }
---

## 입력
- `worktree_dir` — 글이 있는 worktree 전체 경로. 채점자가 `docs/writing-guide.md` 와 `AGENTS.md` 를 여기서 읽는다
- `post_path` — 채점할 글 파일 전체 경로. 없으면 오류로 끝낸다
- `reviewer` — 쓸 CLI. `codex` 또는 `claude`

## 실행
`recipe:oneshot` 스킬의 래퍼로 실행한다. 채점자는 글을 쓴 세션과 컨텍스트를 공유하지 않는다. 글을 쓴 세션이 직접 채점하면 자기 글에 후해지기 때문이다. 이 스킬을 부른 세션은 점수를 고치지 않는다.

1. **준비.** 실행마다 새 임시 디렉터리를 만든다(`tmp=$(mktemp -d)`). codex 와 claude 채점이 병렬로 돌 수 있어 고정 파일 이름을 공유하면 서로 덮어쓴다. 이 디렉터리에 `prompt.txt`, `stdout.txt`, `stderr.txt`, `result.json` 을 둔다.
2. **프롬프트.** `prompt.txt` 를 BOM 없는 UTF-8 로 쓴다. 아래 틀을 그대로 쓰고 `<...>` 만 바꾼다. 채점 기준은 경로가 아니라 `references/rubric.md` 본문 전체를 붙인다. 글이 있는 worktree 에는 이 스킬이 없을 수 있기 때문이다.

   ````text
   너는 블로그 글 채점자다. 글을 고치지 말고 아래 기준으로 채점만 한다.

   읽을 파일(모두 UTF-8 이다. PowerShell 기본 인코딩으로 읽으면 한글이 깨지므로 UTF-8 을 지정해 읽는다):
   - 채점할 글: <post_path>
   - 블로그 규칙: <worktree_dir>/AGENTS.md
   - 글쓰기 규칙: <worktree_dir>/docs/writing-guide.md (없으면 아래 기준만으로 채점한다)

   출력은 아래 기준의 "출력 형식"에 맞는 JSON 객체 하나뿐이다.

   <references/rubric.md 본문 전체>
   ````
3. **실행.** `worktree_dir` 에서 `bash "$oneshot/references/oneshot.sh" --mode read --prompt-file "$tmp/prompt.txt" <reviewer> > "$tmp/stdout.txt" 2> "$tmp/stderr.txt"` 를 실행한다. `$oneshot` 은 설치된 recipe 플러그인의 oneshot 스킬 디렉터리다. 여러 버전이 있으면 가장 높은 버전을 쓴다(`ls -d ~/.claude/plugins/cache/*/recipe/*/skills/oneshot | sort -V | tail -1`). 모델과 effort 는 지정하지 않고 CLI 기본값을 쓴다. 종료 코드 0 또는 3(강등 — stdout 에 결과 있음)이면 다음 단계로 간다. stderr 는 codex 세션 로그가 항상 섞이므로 성공 판정에 쓰지 않고, 실패했을 때 원인을 찾는 데만 본다
4. **검증·계산.** `python <이 스킬 디렉터리>/scripts/score.py --rubric <이 스킬 디렉터리>/references/rubric.json --post <post_path> --review "$tmp/stdout.txt" --reviewer <reviewer> --out "$tmp/result.json"` (`python` 이 없으면 `python3`). 스크립트가 항목 누락, 점수 범위, 글 유형별 N/A 허용 여부, 인용이 글에 실제로 있는지를 검사하고 총점을 계산한다. 총점은 채점자에게 맡기지 않는다
5. **다시 시키기(한 번만).** 3단계 종료 코드가 0·3 이 아니거나 4단계가 종료 코드 1(`ok: false`)이면, `prompt.txt` 끝에 아래 문단을 붙여 3·4단계를 한 번 더 실행한다. 3단계가 실패했으면 `<문제>` 에는 stderr 마지막 몇 줄의 요약을, 4단계가 실패했으면 `errors` 를 한 줄에 하나씩 넣는다. 처음부터 다시 채점하게 하는 것이므로 직전 출력은 붙이지 않는다

   ```text
   직전 출력의 문제(이것을 고쳐 C1~C20 전체를 다시 출력한다):
   - <문제>
   ```
6. **실패로 끝내기.** 두 번째도 실패하면 `score` 는 `{"total": null, "reviewer": <reviewer>, "error": "<요약>"}`, `findings` 는 `{"severity": "P1", "category": "writing", "location": "-", "issue": "<reviewer> 채점 실패: <요약>", "suggestion": "수동 채점", "reviewer": <reviewer>}` 하나로 낸다. 이때는 임시 디렉터리를 지우지 않고 경로를 보고해, 사람이 stdout·stderr 를 볼 수 있게 한다
7. **정리.** 성공했으면 `result.json` 에서 `score` 와 `findings` 를 꺼낸 뒤 임시 디렉터리를 지운다

## 출력
- `score` — `result.json` 의 `score`. `total`(0~100 정수), `type`, `sections`(절별 환산 가중치와 점수), `items`(항목별 `score`·`evidence`·`location`·`reason`·`fix`), `na`(N/A 항목 id), `not_scored`(원문으로 채점하지 않는 규칙·관점과 사유), `warnings`
- `findings` — `result.json` 의 `findings`. 2점 미만 항목을 `blog-post-apply-findings` 가 읽는 지적 형식(`severity` 0점→P2·1점→P3, `category: "writing"`)으로 바꾼 배열. 모두 2점이거나 N/A 면 빈 배열
- 사용자에게는 아래 형식으로 보고한다. 2점 미만 항목 표는 점수가 낮은 순서로 쓰고, `warnings` 가 있으면 표 아래에 그대로 옮긴다. `not_scored` 는 매번 반복하지 않는다

  ```markdown
  **총점 <total> / 100** (<reviewer>, type=<type>, N/A <na 개수>개)

  | 절 | 점수 / 가중치 |
  |---|---|
  | 시작 | 11.2 / 15 |

  | 항목 | 점수 | 위치 | 이유 | 고칠 점 |
  |---|---|---|---|---|
  | C14 공식 문서 이상의 선택·이유·실패 | 0 | 전체 | ... | ... |
  ```
