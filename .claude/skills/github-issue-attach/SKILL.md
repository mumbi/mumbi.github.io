---
name: github-issue-attach
description: 블로그 저장소에 글 추적 이슈를 만들고 파일들을 GitHub 이슈 첨부로 올려, 이슈 번호와 파일별 첨부 URL 을 낸다
node:
  in:
    repo_dir: { shape: text }
    issue_title: { shape: text }
    files: { shape: text, list: 1 }
  out:
    issue_number: { shape: num }
    attachments: { shape: json }
---

## 입력
- `repo_dir` — 블로그 저장소 로컬 경로. `git remote get-url origin` 으로 `owner/name` 을 얻는다
- `issue_title` — 만들 이슈 제목. 자동화 트리거 문자열(`@claude` 등)이 들어 있으면 오류로 끝낸다
- `files` — 첨부할 파일 전체 경로 배열. 하나라도 없으면 오류로 끝낸다

## 실행
필요한 인증: 저장소에 push 권한이 있는 gh 로그인. 이미지·영상이 아닌 파일(zip 등)이 있으면 같은 계정으로 GitHub 에 로그인된 브라우저도 필요하다.

REST API 에는 첨부 업로드 엔드포인트가 없다. 이미지·영상은 gh 2.99.0 이상의 `--attach` 로 올리고, 그 밖의 파일은 브라우저로 올린다.

1. 준비
   - `gh auth status` 로 로그인 계정을 확인한다. 미인증이면 `gh auth login -h github.com -p https -w -s repo,read:org,project` 를 백그라운드로 띄워 일회용 코드를 받고, 브라우저의 `https://github.com/login/device` 에서 저장소 소유 계정으로 로그인돼 있는지 사용자에게 확인받는다. 다른 계정이면 사용자가 직접 로그인하게 한다(비밀번호는 입력하지 않는다)
   - 이슈는 `mumbi.net` 프로젝트(칸반)에 등록해야 한다(AGENTS.md 의 GitHub Projects 작업 관리). `gh auth status` 의 Token scopes 에 `project` 가 없으면 `gh auth refresh -h github.com -s project` 로 권한을 더하고, 브라우저 확인은 로그인과 같은 방법으로 받는다
   - 토큰이 `ghu_`(GitHub App 사용자 토큰)면 `--attach` 가 거부된다(cli/cli#14495). 이때는 이미지도 브라우저로 올린다
   - `gh --version` 이 2.99.0 미만이면 업그레이드할지 사용자에게 묻는다(winget 은 UAC 확인이 필요하므로 포그라운드로 실행한다). 거절하면 이미지도 브라우저로 올린다
   - `files` 를 확장자로 나눈다: 이미지·영상(`png jpg jpeg gif webp svg mp4 mov webm`)은 `media`, 나머지는 `other`
2. 본문을 BOM 없는 UTF-8 파일로 쓰고 `gh issue create -R <owner/name> --title <issue_title> --body-file <파일> --project "mumbi.net"` 로 이슈를 만든다. 프로젝트 워크플로가 상태를 Todo 로 둔다(PowerShell `Set-Content -Encoding utf8` 은 BOM 을 붙이므로 `[IO.File]::WriteAllText(..., New-Object Text.UTF8Encoding($false))` 를 쓴다)
3. `media` 업로드(gh)
   - 본문 파일에 파일마다 `![<alt>](./<파일 이름>)` 줄을 쓰고 `gh issue comment <번호> -R <owner/name> --body-file <파일> --attach '<전체 경로>#<alt>' ...` 로 올린다. gh 가 본문의 참조를 업로드 URL 로 바꾼다
   - 올린 댓글 본문을 `gh api repos/<owner/name>/issues/comments/<id> --jq .body` 로 읽어 파일마다 URL 을 뽑는다
   - 뽑은 URL 이 `https://github.com/user-attachments/` 로 시작하지 않거나 URL 이 없는 파일은 `other` 로 옮겨 4의 브라우저 업로드로 다시 올린다
4. `other` 업로드(브라우저, 컴퓨터 유즈). 다른 세션이나 사용자가 같은 브라우저·화면을 쓰고 있을 수 있다
   - 이슈 URL 은 `Start-Process <이슈 URL>` 로 OS 가 기본 브라우저의 새 탭에 열게 한다. 앱 단축키(Ctrl+T)나 기존 탭 주소창 바꾸기는 다른 세션의 탭을 덮을 수 있으므로 쓰지 않는다
   - 클릭·키 입력 전에 `get-app-state` 의 스크린샷과 창 제목으로 브라우저가 맨 앞이고 이슈 탭이 활성인지 확인한다. 아니면 조작하지 말고, 브라우저를 앞에 두고 조작하는 동안 입력을 멈춰 달라고 사용자에게 요청한 뒤 "준비됨"을 기다린다
   - 댓글 영역의 "Paste, drop, or click to add files" 를 접근성 요소 번호로 클릭한다(`click --element-index`). 파일 선택 창이 열리지 않으면 최신 스크린샷 기준 화면 좌표로 클릭한다
   - 열린 "열기"/"Open" 대화상자는 키 입력이 들어가지 않는다. Win32 로 조작한다: `FindWindow('#32770', <제목>)` → 컨트롤 ID 1148(ComboBoxEx32) 안의 `Edit` 에 `WM_SETTEXT` 로 폴더 경로를 넣고 ID 1 버튼에 `BM_CLICK` → 같은 방법으로 `"a.zip" "b.zip"` 처럼 따옴표로 묶은 파일 이름들을 넣고 `BM_CLICK`
   - 업로드가 끝나면 댓글 입력칸 값(`get-app-state` 트리)에서 `https://github.com/user-attachments/...` URL 을 읽는다. 요소 번호는 페이지가 바뀔 때마다 달라지므로 매번 트리를 다시 읽는다
   - 키 입력이 브라우저 페이지로 새면 GitHub 단축키가 동작할 수 있다. 끝난 뒤 이슈의 레이블·담당자·마일스톤이 바뀌지 않았는지 `gh issue view --json` 으로 확인한다
   - 댓글은 브라우저로 제출하지 않는다. 첨부 URL 로 깨끗한 댓글 본문을 만들어 BOM 없는 파일로 `gh issue comment --body-file` 로 올린다. 브라우저 입력칸에 남은 초안은 지워지지 않을 수 있는데, 게시되지 않으므로 그대로 두고 사용자에게 알린다
5. 첨부 URL 마다 내려받아 200 과 원본 SHA256 일치를 확인한다. 올린 직후에는 404 가 날 수 있으므로 15초 간격으로 최대 4번 다시 시도한다
6. 화면을 조작했으면 끝났다고 사용자에게 알려, 브라우저와 다른 창을 다시 쓸 수 있게 한다

## 출력
- `issue_number` — 만든 이슈 번호
- `attachments` — 파일별 객체 배열 `[{ "file": 전체 경로, "name": 파일 이름, "url": 첨부 URL, "sha256": 해시, "kind": "image"|"file" }]`
