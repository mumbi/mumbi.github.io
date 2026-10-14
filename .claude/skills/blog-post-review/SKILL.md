---
name: blog-post-review
description: 글을 로컬 미리보기로 띄워 빌드를 확인하고, 사용자가 승인할 때까지 사용자의 지적을 반영한다
node:
  in:
    worktree_dir: { shape: text }
    post_path: { shape: text }
  out:
    reviewed_post: { shape: text }
---

## 입력
- `worktree_dir` — 글이 있는 worktree 전체 경로. 미리보기 서버의 작업 폴더
- `post_path` — 검토할 글 파일 전체 경로

## 실행
1. 미리보기 도구를 준비한다. Hugo 면 `hugo` 가 있으면 쓰고, 없으면 GitHub 릴리스(`gohugoio/hugo` latest)의 `hugo_extended_*_windows-amd64.zip` 을 받아 릴리스의 `digest`(sha256)와 대조한 뒤 한글 없는 임시 폴더에 푼다. Docker 데몬이 꺼져 있으면 Docker 를 띄우지 않는다
2. `hugo build -d <임시 출력>` 으로 빌드해 확인한다: 종료 코드 0, 글 페이지 생성, 본문 앵커 링크의 대상 ID 존재, 남은 shortcode 없음, alert·표·이미지 렌더, `og:image`·`twitter:image`, `<title>` 과 메타 설명 길이
3. `hugo server --port 1313` 을 백그라운드로 띄우고 글 URL 을 브라우저로 연다. 새 파일(예: `assets/css/custom.css`)을 추가했으면 서버를 재시작한다 — 실행 중인 서버는 새 자원을 번들에 넣지 않는다
4. 사용자에게 미리보기 URL 을 알리고 지적을 받는다. 지적마다:
   - 글 안의 수정이면 바로 고치고 미리보기에 반영됐는지 확인한다
   - 사이트 전체에 영향을 주는 수정(테마 CSS 등)이면 범위를 묻고, 승인되면 worktree 안에 고친다
   - 화면 확인이 필요하면 컴퓨터 유즈로 해당 위치를 캡처해 확인한다(화면이 가려지면 `--restore-window`)
5. 사용자가 승인할 때까지 4를 반복한다. 승인되면 2의 빌드 확인을 한 번 더 하고 서버를 끄고 임시 도구를 지운다

## 출력
- `reviewed_post` — 사용자가 승인한 글 파일의 전체 경로
