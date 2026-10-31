---
name: blog-post-review
description: 글을 로컬 미리보기로 띄워 빌드를 확인하고, 사용자가 승인할 때까지 사용자의 지적을 반영한다
node:
  in:
    worktree_dir: { shape: text }
    post_path: { shape: text }
    rubric_score: { shape: json, list: 1, required: false }
  out:
    reviewed_post: { shape: text }
---

## 입력
- `worktree_dir` — 글이 있는 worktree 전체 경로. 미리보기 서버의 작업 폴더
- `post_path` — 검토할 글 파일 전체 경로
- `rubric_score` — `blog-post-rubric` 의 `score` 출력을 담은 배열(원소 0~1개). 원소는 `total`·`pass_line`·`passed`·`reviewer`·`type`·`sections`·`items`·`na`·`warnings` 를 갖고, 채점에 실패했으면 `total` 이 `null` 이고 `error` 가 있다. 비어 있으면 점수를 보여 주지 않는다

## 실행
1. 미리보기 도구를 준비한다. Hugo 면 `hugo` 가 있으면 쓰고, 없으면 GitHub 릴리스(`gohugoio/hugo` latest)의 `hugo_extended_*_windows-amd64.zip` 을 받아 릴리스의 `digest`(sha256)와 대조한 뒤 한글 없는 임시 폴더에 푼다. Docker 데몬이 꺼져 있으면 Docker 를 띄우지 않는다
2. `hugo build -d <임시 출력>` 으로 빌드해 확인한다: 종료 코드 0, 글 페이지 생성, 본문 앵커 링크의 대상 ID 존재, 남은 shortcode 없음, alert·표·이미지 렌더, `og:image`·`twitter:image`, `<title>` 과 메타 설명 길이
3. `hugo server --port 1313` 을 백그라운드로 띄우고 글 URL 을 브라우저로 연다. 새 파일(예: `assets/css/custom.css`)을 추가했으면 서버를 재시작한다 — 실행 중인 서버는 새 자원을 번들에 넣지 않는다
4. 사용자에게 미리보기 URL 을 알리고 지적을 받는다. `rubric_score` 에 원소가 있으면 URL 과 함께 보여 준다. 점수는 글쓰기 규칙(`docs/writing-guide.md`)을 얼마나 지켰는지 보는 값이다. 채점한 뒤에 고친 내용은 점수에 들어 있지 않고, 같은 글도 다시 채점하면 10점 안팎 달라질 수 있다고 함께 적는다:
   - `total` 이 수면 첫 줄에 `**총점 <total> / 100** (<reviewer>, type=<type>, 합격선 <pass_line> <통과|미달>)`, 이어서 절별 `score / weight` 표, 그 아래 `items` 중 `score` 가 0·1 인 항목을 점수 낮은 순으로 `항목 | 점수 | 이유` 표로 보여 준다. `warnings` 가 있으면 표 아래에 옮긴다
   - `passed` 가 `false` 면 표 아래에 0점 항목을 먼저 짚어, 승인 전에 고칠지 사용자에게 묻는다. 미달이어도 사용자가 승인하면 진행한다
   - `total` 이 `null` 이면 채점에 실패했다는 사실과 `error` 를 한 줄로 알린다
   지적마다:
   - 글 안의 수정이면 바로 고치고 미리보기에 반영됐는지 확인한다
   - 사이트 전체에 영향을 주는 수정(테마 CSS 등)이면 범위를 묻고, 승인되면 worktree 안에 고친다
   - 화면 확인이 필요하면 컴퓨터 유즈로 해당 위치를 캡처해 확인한다(화면이 가려지면 `--restore-window`)
5. 사용자가 승인할 때까지 4를 반복한다. 승인되면 2의 빌드 확인을 한 번 더 하고 서버를 끄고 임시 도구를 지운다. 오류로 끝나거나 사용자가 그만둘 때도 서버를 끄고 임시 도구를 지운다

## 출력
- `reviewed_post` — 사용자가 승인한 글 파일의 전체 경로
