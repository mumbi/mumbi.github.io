---
name: blog-post-apply-findings
description: 리뷰 지적 목록을 검토해 타당한 것을 글에 반영하고, 더 반영할 것이 없는지를 낸다
node:
  in:
    worktree_dir: { shape: text }
    post_path: { shape: text }
    findings: { shape: json, list: 1, required: false }
  out:
    clean: { shape: bool }
---

## 입력
- `worktree_dir` — 글이 있는 worktree 전체 경로. 사이트 공통 파일(CSS 등) 수정이 필요할 때 이 안에서만 고친다
- `post_path` — 고칠 글 파일 전체 경로
- `findings` — 지적 배열. 여러 리뷰어의 지적이 이어 붙어 온다(중복 가능)

## 실행
1. 같은 위치·같은 내용의 지적을 하나로 합친다
2. 지적마다 근거를 직접 확인한다(글·저장소 규칙·자료 폴더). 확인 결과로 셋 중 하나로 가른다:
   - 반영 — 근거가 맞고 고칠 방법이 하나로 정해진다
   - 사용자 판단 — 고칠 방법이 여럿이거나, 글 범위를 넘는 변경(사이트 공통 CSS·다른 글)이거나, 내용 방향을 바꾼다. 묶어서 AskUserQuestion 으로 묻는다
   - 기각 — 근거가 틀렸거나 이미 반영돼 있다. 이유를 기록한다
3. 반영할 것을 고친다. 커밋하지 않는다
4. 반영 내역(반영·기각·보류와 이유)을 사용자에게 보고한다

## 출력
- `clean` — 이번 회차에 실제로 고친 것이 없으면(지적이 비었거나 전부 기각) `true`, 하나라도 고쳤으면 `false`
