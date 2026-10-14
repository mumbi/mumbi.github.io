---
name: blog-post-draft
description: 원격 기본 브랜치에서 글 전용 worktree 를 만들고, 블로그 규칙과 자료·첨부 URL 로 글 초안 파일을 쓴다
node:
  in:
    repo_dir: { shape: text }
    slug: { shape: text }
    title: { shape: text }
    topic: { shape: text }
    materials_dir: { shape: text }
    conventions: { shape: json }
    attachments: { shape: json }
  out:
    worktree_dir: { shape: text }
    post_path: { shape: text }
---

## 입력
- `repo_dir` — 블로그 저장소 로컬 경로. 이 체크아웃의 작업 트리와 미추적 파일은 건드리지 않는다
- `slug` — 파일명·URL·브랜치 이름에 쓰는 slug
- `title` — 확정된 제목
- `topic` — 글의 주제와 핵심 메시지
- `materials_dir` — 자료 폴더 전체 경로. 글의 모든 사실 주장은 여기서 근거를 찾는다
- `conventions` — `blog-conventions` 의 규칙 객체
- `attachments` — `github-issue-attach` 의 파일별 첨부 URL 배열. 글의 이미지·다운로드 링크는 이 URL 만 쓴다

## 실행
1. `git -C <repo_dir> fetch origin` 후 `git -C <repo_dir> worktree add -b <branch_pattern 대로, 예: feature/post-<slug>> <repo_dir>-<slug> origin/<기본 브랜치>`, 테마가 서브모듈이면 `git -C <worktree> submodule update --init --recursive`
2. `<worktree>/<post_dir>/<YYYY-MM-DD>-<slug>.md` 를 쓴다. 프론트매터는 `conventions.frontmatter_template` 과 최근 글을 따른다 — Hugo 면 `url`(`url_pattern`), `author`, `draft: false`, `toc: true`. 대표 이미지는 템플릿의 `image` 와 테마/Hugo OG 템플릿이 읽는 `images`(목록)를 함께 첨부 URL 로 넣는다
3. 본문 구성: 해결 방법을 먼저(독자가 바로 따라 할 절차), 원인 분석은 뒤에. 제목 다음 절은 `##` 부터
4. 쓰는 규칙:
   - 사실 주장마다 자료의 근거가 있어야 한다. 근거가 없거나 한 환경에서만 확인한 것은 "제 환경에서", "~로 보입니다"로 범위를 밝힌다
   - 독자가 따라 할 명령은 압축을 푼 실제 구조에서 그대로 동작해야 한다(작업 폴더 이동, 하위 폴더 경로 포함). 첨부 zip 의 내용물 구성도를 넣는다
   - 첨부(zip 등)에 소스가 들어 있으면 직접 빌드하는 절차를 반드시 넣는다: 실행할 폴더(`cd`), 빌드 명령, 산출물이 놓이는 위치. 빌드 도구·버전은 자료에서 확인한 것만 적는다
   - 명령끼리 경로가 이어져야 한다. 앞 명령이 만든 파일(빌드 산출물 등)은 뒤 명령·스크립트가 읽는 위치에 놓여야 한다. 스크립트가 파일을 찾는 위치는 스크립트 소스(예: `$PSScriptRoot`, 기본 인자)에서 확인하고, 산출 위치를 본문에 한 줄로 밝힌다
   - 다운로드는 클릭할 수 있는 링크로 두고, 확인용 전체 URL·해시는 코드 블록이나 표로 둔다
   - 경고·안내 상자는 테마 shortcode(Blowfish: `{{< alert >}}`)를 쓴다. Jekyll 식 `{: .notice }`·`{:target}` 를 쓰지 않는다
   - 다른 장으로 가는 앵커 링크는 실제 생성 ID(빌드 결과)로 확인할 수 있게 둔다
   - 외부 출처는 참고 절에 "링크 — 설명" 형식으로 모은다
5. 커밋하지 않는다

## 출력
- `worktree_dir` — 만든 worktree 의 전체 경로
- `post_path` — 쓴 글 파일의 전체 경로
