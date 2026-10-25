---
name: blog-conventions
description: 블로그 저장소의 원격 기본 브랜치에서 글 작성 규칙(프론트매터·파일 위치·카테고리/태그 관례·브랜치/커밋 규칙·자동화 트리거)을 조사해 구조화된 값으로 낸다
node:
  in:
    repo_dir: { shape: text }
  out:
    conventions: { shape: json }
---

## 입력
- `repo_dir` — 블로그 저장소 로컬 체크아웃의 전체 경로. 원격 이름·기본 브랜치를 읽는 데만 쓰고, 작업 트리 내용은 근거로 쓰지 않는다

## 실행
로컬 체크아웃은 오래된 브랜치일 수 있다(예: 원격은 Hugo 로 바뀌었는데 로컬은 Jekyll). 규칙은 반드시 원격 기본 브랜치 기준으로 읽는다.

1. `repo_dir` 가 git 저장소가 아니면 오류로 끝낸다. 소유자 불일치("dubious ownership")로 git 이 거부하면 `git config --global --add safe.directory <repo_dir 의 슬래시 경로>` 를 사용자 승인 후 추가한다
2. `git -C <repo_dir> fetch origin` 후 `git -C <repo_dir> remote show origin` 으로 기본 브랜치(`HEAD branch`)를, `remote get-url origin` 으로 `owner/name` 을 얻는다
3. 원격 기본 브랜치의 파일을 `git show origin/<기본>:<경로>` 로 읽는다(체크아웃하지 않는다):
   - 에이전트 지침: `AGENTS.md`, `CLAUDE.md`, `.claude/CLAUDE.md` 와 거기서 `@` 로 참조하는 문서(예: `docs/tech-stack.md`)
   - 정적 사이트 생성기 판별: `config/`·`hugo.toml`(Hugo) 또는 `_config.yml`(Jekyll), 테마 서브모듈(`.gitmodules`)
   - 글 디렉터리(`content/posts` 또는 `_posts`)의 최근 글 5개 프론트매터 — `git ls-tree -r --name-only` 로 찾고 파일명 날짜순
   - `.github/workflows/*.yml` 의 `on:` 과 `if:` — 이슈·댓글·PR 이벤트로 도는 자동화와 그 트리거 문자열(예: 본문에 `@claude` 가 있으면 작업 에이전트 실행)
4. 저장소 규칙 API 로 병합 조건을 읽는다: `gh api repos/<owner/name>/rules/branches/<기본>` (gh 미인증이면 이 항목은 `null` 로 두고 `notes` 에 적는다)
5. 최근 글의 커밋 작성자를 `git log origin/<기본> --format='%an <%ae>' -- <글 디렉터리>` 로 확인한다
6. 최근 글들이 카테고리를 태그에도 넣는지 본다. 섞여 있으면 가장 최근 글의 방식을 `tag_style` 로 정하고 그 사실을 `notes` 에 적는다
7. 같은 규칙을 문서마다 다르게 적었으면(예: 메타 설명 최대 길이를 AGENTS.md 는 160자, `docs/tech-stack.md` 는 155자) 더 엄격한 값을 쓰고, 두 값과 출처를 `notes` 에 적는다. 문서와 실제 이력(최근 글·커밋)이 다르면 실제 이력을 따르고(예: 문서의 작성자와 실제 커밋 작성자가 다르면 실제 커밋 작성자, 문서의 이미지 경로와 최근 글의 첨부 URL 이 다르면 첨부 URL) 차이를 `notes` 에 적는다

## 출력
- `conventions` — 다음 키를 가진 객체. 원격에서 확인하지 못한 값은 `null` 로 두고 이유를 `notes` 에 적는다
  - `repo`(owner/name), `default_branch`, `generator`(hugo|jekyll), `theme`
  - `post_dir`(저장소 상대 경로), `filename_pattern`(예: `YYYY-MM-DD-slug.md`)
  - `frontmatter_template`(문자열), `required_fields`(배열), `title_max`·`description_max`(수)
  - `url_pattern`(예: `/<category>/<slug>/`), `categories`(기존 값 배열), `tag_style`(`exclude_category`|`include_category`)
  - `branch_pattern`(예: `feature/<desc>`), `commit_message_pattern`(예: `post: <제목>`), `commit_author`(이름·메일)
  - `deploy_trigger`(예: 기본 브랜치 push), `merge_rule`(필요 승인 수 등), `automation_triggers`(배열: 이벤트·조건·주의)
  - `attachment_practice`(예: 글마다 이슈를 만들고 이슈 첨부 URL 을 글에서 링크)
  - `notes`(배열)
