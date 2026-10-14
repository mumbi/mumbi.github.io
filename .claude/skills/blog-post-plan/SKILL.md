---
name: blog-post-plan
description: 글 주제와 자료 폴더, 블로그 규칙을 받아 제목·slug·이슈 제목과 첨부할 파일 계획을 세운다
node:
  in:
    topic: { shape: text }
    materials_dir: { shape: text }
    conventions: { shape: json }
  out:
    slug: { shape: text }
    title: { shape: text }
    issue_title: { shape: text }
    attach_plan: { shape: json }
---

## 입력
- `topic` — 글의 주제와 핵심 메시지
- `materials_dir` — 자료 폴더 전체 경로. 없거나 비어 있으면 오류로 끝낸다
- `conventions` — `blog-conventions` 가 낸 규칙 객체. 제목 길이·카테고리·태그 방식·파일명 패턴을 여기서 따른다

## 실행
1. `materials_dir` 를 훑어 자료 목록을 만든다(로그·스크립트·소스·이미지·설치 파일 등). 큰 바이너리(덤프 등)는 이름과 크기만 본다
2. 제목을 정한다 — `conventions.title_max` 이내, 검색어를 앞쪽에. 증상을 과장하거나 다른 뜻으로 읽히는 표현을 쓰지 않는다(예: 앱이 종료되는 문제를 "PC 꺼짐"이라 쓰지 않는다)
3. slug 를 영문 소문자·숫자·하이픈으로 정한다. 기존 글 URL 과 겹치지 않는지 `git -C <저장소> ls-tree` 결과로 확인한다
4. 카테고리는 `conventions.categories` 중에서 고르고, 태그는 `tag_style` 을 따른다(`exclude_category` 면 카테고리를 태그에 넣지 않는다)
5. 첨부 계획을 세운다 — 독자가 받을 파일(zip 등)과 글에 넣을 스크린샷. 스크린샷마다 무엇을 보여 주는지, 어떤 개인 정보(계정 아바타·ID·이메일 등)를 가려야 하는지 적는다. 재현이 불가능한 장면(이미 설치 상태가 바뀌어 다시 띄울 수 없는 오류창 등)은 계획에 넣지 않고 로그 텍스트로 대신한다는 메모를 남긴다
6. 이슈 제목은 `<YYYY-MM-DD>-<slug>` 로 한다. `@claude` 처럼 `conventions.automation_triggers` 에 걸리는 문자열을 넣지 않는다
7. 제목·slug·첨부 계획을 사용자에게 보여 주고 확정받는다

## 출력
- `slug` — 확정된 slug
- `title` — 확정된 제목
- `issue_title` — `<YYYY-MM-DD>-<slug>` 형식의 이슈 제목
- `attach_plan` — `{ "files": [...], "screenshots": [...], "notes": [...] }`. `files` 항목은 `{source, archive_name, contents}`, `screenshots` 항목은 `{name, how_to_capture, mask}`
