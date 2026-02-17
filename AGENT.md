# AGENT.md

## 프로젝트 개요

개인 기술 블로그 (mumbi.net). 한국어 콘텐츠 중심.

## 기술 스택

정적 사이트 생성기 기반 블로그. 자세한 기술 스택은 @docs/tech-stack.md 참조.

## 주요 명령어

빌드 및 개발 서버 명령어는 @docs/tech-stack.md 참조.

## 프로젝트 구조

정적 사이트 생성기 표준 구조. 자세한 디렉토리 설명은 @docs/tech-stack.md 참조.

## 포스트 작성

- 로케일: `ko-KR` (한국어 콘텐츠)
- 파일명 및 디렉토리 구조는 @docs/tech-stack.md 참조

### 프론트매터 템플릿

@docs/tech-stack.md 참조.

### SEO 규칙

- SEO 제목 60자 이내, 메타 설명 160자 이내
- 모든 이미지에 alt 텍스트 포함
- Open Graph 태그 배치
- 키워드 배치 및 내부 링크 삽입
- 카테고리·태그 일관성 유지
- 구조화 데이터(Schema.org) 마크업 활용

## 주요 설정

설정 파일 목록 및 용도는 @docs/tech-stack.md 참조.

## Branch Conventions

- Main branch: `master`
- Feature branches: `feature/<description>`

## Git 워크플로우

- 커밋 메시지: `post: 포스트 제목`
- main 브랜치 푸시로 자동 배포


## GitHub Projects 작업 관리

`mumbi.net` 프로젝트(#2)에서 칸반(Todo → In Progress → Done)으로 작업을 관리한다.

- 작업 생성: 이슈 생성 시 `--project "mumbi.net"` 옵션으로 프로젝트에 등록 (워크플로우가 자동으로 Todo 설정)
- 작업 시작: 프로젝트 아이템 상태를 In Progress로 변경
- 작업 완료: 이슈 닫기 (워크플로우가 자동으로 Done 설정)

### 스킬

- `/github-add-task` — 작업 생성
- `/github-check-tasks` — 대기 중인(Todo) 작업 목록 조회
- `/github-start-task <이슈번호|owner/repo#번호>` — 작업 시작 및 완료 처리

## 자동화 파이프라인

이슈 기반 자동화 파이프라인. 세부 지침은 `.github/workflows/` 의 각 워크플로우 파일 참조.

```
이슈 생성 (@claude) → 작업 에이전트 → PR 생성 → 리뷰 에이전트 → approve/changes_requested
```

- **작업 에이전트** (`claude-task-worker.yml`): 이슈 작업 수행 → 커밋 → PR 생성
- **리뷰 에이전트** (`claude-reviewer.yml`): PR 자동 리뷰
- **피드백 에이전트** (`claude-feedback-worker.yml`): 리뷰 피드백 반영 → 커밋

