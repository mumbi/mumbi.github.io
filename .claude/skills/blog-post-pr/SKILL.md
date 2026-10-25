---
name: blog-post-pr
description: 승인된 글과 worktree 의 변경을 블로그 관례대로 커밋·푸시하고, 글 이슈를 닫는 PR 을 만든다
node:
  in:
    worktree_dir: { shape: text }
    reviewed_post: { shape: text }
    issue_number: { shape: num }
    title: { shape: text }
  out:
    pr_url: { shape: text }
---

## 입력
- `worktree_dir` — 글 브랜치 worktree 전체 경로
- `reviewed_post` — 승인된 글 파일 전체 경로. worktree 안에 없으면 오류로 끝낸다
- `issue_number` — 글 추적 이슈 번호. PR 본문에 `Closes #<번호>` 로 넣는다
- `title` — 글 제목. 커밋·PR 제목에 쓴다

## 실행
필요한 인증: 저장소에 푸시·PR 생성 권한이 있는 gh 로그인.

1. `git -C <worktree_dir> status` 로 변경을 확인한다. 글 파일과 리뷰 중 승인된 공통 파일(예: `assets/css/custom.css`) 외의 변경이 있으면 멈추고 사용자에게 묻는다
2. 커밋 메시지를 BOM 없는 UTF-8 파일로 쓴다(`commit_message_pattern`, 예: `post: <title>`, 본문에 `Closes #<issue_number>` 와 공동 작성 줄). 작성자는 저장소 관례(최근 글 커밋의 작성자)를 `-c user.name= -c user.email=` 로 이 커밋에만 지정한다 — 전역 git 설정은 바꾸지 않는다
3. `git -C <worktree_dir> commit -F <파일>` 후 첫 글자가 BOM(U+FEFF)이 아닌지 `git log -1 --format=%s` 로 확인한다
4. 푸시는 이 명령에서만 gh 인증을 쓴다: `git -C <worktree_dir> -c credential.helper= -c "credential.helper=!gh auth git-credential" push -u origin <브랜치>` — 다른 저장소의 저장된 자격 증명을 바꾸지 않는다
5. PR 본문을 BOM 없는 파일로 쓰고(요약·확인한 것·`Closes #<issue_number>`) `gh pr create --base <기본 브랜치> --head <브랜치> --title "<커밋 제목>" --body-file <파일>`
6. 머지하지 않는다. 기본 브랜치 머지가 곧 배포이고 승인 규칙이 있을 수 있다

## 출력
- `pr_url` — 만든 PR 의 URL
