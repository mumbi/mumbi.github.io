---
name: blog-llm-review
description: 글 초안을 외부 LLM 에이전트 CLI(codex 또는 claude) 하나로 독립 리뷰해, 저장소 규칙·독자 절차 재현성·자료 대비 사실 관점의 지적 목록을 낸다
node:
  in:
    worktree_dir: { shape: text }
    post_path: { shape: text }
    materials_dir: { shape: text }
    reviewer: { shape: text, values: [codex, claude] }
  out:
    findings: { shape: json, list: 1, required: false }
---

## 입력
- `worktree_dir` — 글이 있는 worktree 전체 경로. 리뷰어가 저장소 규칙 문서(AGENTS.md 등)를 여기서 읽는다
- `post_path` — 리뷰할 글 파일 전체 경로. 없으면 오류로 끝낸다
- `materials_dir` — 자료 폴더 전체 경로. 사실 대조와 첨부 내용 확인의 근거
- `reviewer` — 쓸 CLI. `codex` 또는 `claude`

## 실행
`recipe:oneshot` 스킬의 래퍼로 한 번 실행한다. 리뷰어는 글을 쓴 세션과 컨텍스트를 공유하지 않는다.

1. 실행마다 새 임시 디렉터리(`mktemp -d`)를 만들어 프롬프트·stdout·stderr 파일을 그 안에 둔다. codex 와 claude 리뷰가 병렬로 돌므로 고정 파일 이름을 공유하면 서로 덮어쓴다. 프롬프트 파일은 BOM 없는 UTF-8 로 쓴다. 담을 내용:
   - 역할: 블로그 PR 리뷰어. 수정하지 말고 지적만
   - 읽을 것: `post_path`, `worktree_dir` 의 `AGENTS.md`·참조 문서·최근 글 2개, `materials_dir`(zip 은 내용 목록만)
   - 관점 넷: (1) 저장소 규칙 위반 — 프론트매터 필수 항목(대표 이미지 포함), 길이, 카테고리/태그 관례(최근 글들의 `categories` 와 `tags` 를 비교해 카테고리 값을 태그에 다시 넣는지 확인하고, 리뷰할 글의 태그를 그 관례와 대조) (2) 독자 절차 재현성 — 명령을 쓰인 그대로 실행하면 되는지(폴더 이동, 상대 경로, 압축 구조), 앞 명령의 산출물이 뒤 명령·스크립트가 읽는 위치에 놓이는지(스크립트 소스에서 확인) (3) 자료 대비 사실 — 자료에 근거가 없거나 범위를 넘는 단정(한 버전·한 환경에서 확인한 것을 전체로 일반화), 해시·크기·날짜·개수 같은 값은 자료 파일에서 직접 계산해 대조 (4) 링크·앵커·이미지 alt — 문서 안 앵커는 대상 제목에서 생성기 규칙(Hugo: 소문자, 공백→하이픈, 마침표 등 문장부호 제거)으로 만든 ID 와 대조
   - 출력 형식: JSON 배열만. 항목은 `{"severity": "P1"|"P2"|"P3", "category": "rules"|"repro"|"fact"|"link", "location": "줄 번호나 소제목", "issue": "...", "suggestion": "..."}`. 지적이 없으면 `[]`
2. 실행: `bash <oneshot 스킬 디렉터리>/references/oneshot.sh --mode read --prompt-file <프롬프트 파일> <reviewer>` 를 `worktree_dir` 에서 실행한다. `<oneshot 스킬 디렉터리>` 는 설치된 recipe 플러그인의 실제 경로로 바꾼다
3. 종료 코드 0 또는 3(강등 — stdout 에 결과 있음)이면 stdout 에서 JSON 배열을 뽑는다. 그 밖이거나 JSON 이 아니면 한 번 다시 실행하고, 그래도 실패하면 `{"severity": "P1", "category": "rules", "location": "-", "issue": "<reviewer> 리뷰 실패: <요약>", "suggestion": "수동 리뷰"}` 하나를 낸다
4. 각 항목에 `"reviewer": <reviewer>` 를 붙인다

## 출력
- `findings` — 지적 객체 배열(`severity`·`category`·`location`·`issue`·`suggestion`·`reviewer`). 지적이 없으면 빈 배열
