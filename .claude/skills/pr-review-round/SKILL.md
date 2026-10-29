---
name: pr-review-round
description: PR 의 최신 커밋에 대한 리뷰 봇 결과를 기다려 지적을 반영·푸시하고 답글을 단 뒤, 더 반영할 것이 없는지를 낸다
node:
  in:
    pr_url: { shape: text }
  out:
    clean: { shape: bool }
    final_pr_url: { shape: text }
---

## 입력
- `pr_url` — 대상 PR URL

## 실행
필요한 인증: 저장소에 푸시·댓글 권한이 있는 gh 로그인.

리뷰 봇마다 도는 조건이 다르다.
- Claude Reviewer(워크플로 `claude-reviewer.yml`): PR opened·reopened·synchronize(푸시)마다 돌아 판정을 낸다. 자기가 연 스레드가 고쳐졌으면 resolve 하고, 열린 P1·P2 스레드가 남으면 changes_requested 를 낸다. 자기 스레드에 사람이 답글을 달면 `@claude` 없이도 다시 돌아 철회·resolve 하거나 반박 답글을 단다. CI 권한 거부 등으로 실패할 수 있다
- Codex(`chatgpt-codex-connector` 봇): PR 이 열릴 때만 자동으로 리뷰한다. 이후 커밋은 PR 에 `@codex review` 댓글을 달아야 다시 리뷰한다. 지적이 없으면 리뷰 본문에 "Didn't find any major issues" 같은 문구를 남긴다

1. `gh pr view <pr_url> --json number,headRefOid,headRefName,createdAt,commits` 로 최신 커밋을 얻는다. 로컬 worktree 는 `git worktree list` 에서 그 브랜치를 체크아웃한 경로를 찾는다
2. 최신 커밋에 대한 리뷰를 모은다
   - Claude Reviewer: 그 커밋의 실행을 `gh run list --workflow claude-reviewer.yml --event pull_request --json status,conclusion,headSha,databaseId` 로 찾아 완료까지 기다린다(30초 간격, 최대 10분). `conclusion` 이 `failure` 면 `gh run view <id> --log-failed` 의 끝 몇 줄로 원인을 요약해 보고에 넣고, 이 봇은 이번 회차에서 "리뷰 없음"으로 친다. 다시 돌리지 않는다
   - Codex: 최신 커밋이 PR 을 연 커밋이 아니고, 그 커밋 이후 `@codex review` 요청이 없으면 BOM 없는 파일로 `gh pr comment <번호> --body-file <파일>`(본문 `@codex review`)을 단다. 회차마다 커밋당 한 번만 요청한다. 응답은 10분까지 기다린다
   - 봇 리뷰는 워크플로와 별개로 올 수 있으니 `gh pr view --json reviews,comments` 와 `gh api repos/<owner/name>/pulls/<번호>/comments` 를 함께 본다
3. 열려 있고 아직 답하지 않은 지적만 고른다(Claude Reviewer 는 resolve 하지 않은 스레드, Codex 는 최신 커밋에 달린 지적). 지적마다 근거를 확인해 반영·사용자 판단·기각으로 가른다(`blog-post-apply-findings` 와 같은 기준). 사용자 판단이 필요한 것은 묻는다
4. 반영했으면 BOM 없는 메시지 파일로 커밋하고, 이 명령에서만 gh 인증을 쓰는 방식(`-c credential.helper= -c "credential.helper=!gh auth git-credential"`)으로 푸시한다
5. 답글을 단다: `gh api -X POST repos/<owner/name>/pulls/<번호>/comments/<id>/replies --input <BOM 없는 JSON 파일>`. 답글·댓글에 `@claude` 를 쓰지 않는다(멘션으로 Claude Reviewer 가 다시 돈다)
   - Codex 지적: 반영한 것은 반영 커밋과 내용을, 기각한 것은 이유를 단다
   - Claude Reviewer 지적: 기각한 것에만 코드 근거를 들어 이유를 단다. 반영한 것에는 달지 않는다(답글마다 리뷰어가 돌고, 반영 확인은 다음 푸시의 리뷰가 한다)
   - 기각 답글을 달았으면 그 답글로 시작된 실행(`gh run list --workflow claude-reviewer.yml --event pull_request_review_comment`)이 끝날 때까지 기다린다(30초 간격, 최대 10분). 리뷰어가 철회했으면 끝이다. 반박했으면 그 근거를 다시 확인해 반영하거나, 두 번째 기각이면 다시 답하지 않고 사용자에게 묻는다
6. 머지하지 않는다. 승인 상태(`reviewDecision`)와 병합 가능 여부(`mergeStateStatus`), 봇별 결과(지적 수·지적 없음·실패·응답 없음)를 보고한다

## 출력
- `clean` — 이번 회차에 반영할 지적이 없었으면 `true`, 하나라도 반영해 푸시했으면 `false`. 두 봇 모두 실패하거나 응답이 없으면 `true` 로 내되 보고에 "리뷰 없음"을 분명히 적는다
- `final_pr_url` — 대상 PR URL(그대로)
