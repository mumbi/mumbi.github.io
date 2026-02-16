# AGENT.md

## 프로젝트 개요

개인 기술 블로그 (mumbi.net). 한국어 콘텐츠 중심.

## 기술 스택

정적 사이트 생성기 기반 블로그. 자세한 기술 스택은 `tech-stack.md` 참조.

## 주요 명령어

빌드 및 개발 서버 명령어는 `tech-stack.md` 참조.

## 프로젝트 구조

정적 사이트 생성기 표준 구조. 자세한 디렉토리 설명은 `tech-stack.md` 참조.

## 포스트 작성

- 로케일: `ko-KR` (한국어 콘텐츠)
- 파일명 및 디렉토리 구조는 `tech-stack.md` 참조

### 프론트매터 템플릿

```yaml
---
title: "60자 이내 SEO 제목"
date: YYYY-MM-DDTHH:MM:SS+09:00
categories: [카테고리]
tags: [태그1, 태그2, 태그3]
description: "155자 이내 메타 설명"
image: /assets/img/posts/파일명.webp
author: 작성자
toc: true
---
```

### SEO 규칙

- SEO 제목 60자 이내, 메타 설명 160자 이내
- 모든 이미지에 alt 텍스트 포함
- Open Graph 태그 배치
- 키워드 배치 및 내부 링크 삽입
- 카테고리·태그 일관성 유지
- 구조화 데이터(Schema.org) 마크업 활용

## 주요 설정

설정 파일 목록 및 용도는 `tech-stack.md` 참조.

## Branch Conventions

- Main branch: `master`
- Feature branches: `feature/<description>`

## Git 워크플로우

- 커밋 메시지: `post: 포스트 제목`
- main 브랜치 푸시로 자동 배포

## 블로그 운영 워크플로우

| 단계 | 역할 |
|------|------|
| 기획·조사 | 주제 아이디어 논의, 심층 리서치, 자료 조사 |
| 글 작성 | 템플릿 기반 포스트 생성, 프론트매터 자동 작성 |
| 검수 (SEO·품질) | 기술적 SEO 점검, 스타일 가이드 대비 품질 리뷰 |
| 배포 | `git add/commit/push` 자동 실행, 자동 빌드 트리거 |

## GitHub Projects 작업 관리

`mumbi.net` 프로젝트(#2)에서 칸반(Todo → In Progress → Done)으로 작업을 관리한다.

- 작업 생성: 이슈 생성 시 `--project "mumbi.net"` 옵션으로 프로젝트에 등록 (워크플로우가 자동으로 Todo 설정)
- 작업 시작: 프로젝트 아이템 상태를 In Progress로 변경
- 작업 완료: 이슈 닫기 (워크플로우가 자동으로 Done 설정)

### 스킬

- `/github-add-task` — 작업 생성
- `/github-check-tasks` — 대기 중인(Todo) 작업 목록 조회
- `/github-start-task <이슈번호|owner/repo#번호>` — 작업 시작 및 완료 처리

## 자동화 파이프라인 (CI 에이전트 지침)

### 작업 에이전트 (claude-worker)

리드 에이전트로서 이슈에 기술된 작업을 수행하고 PR을 생성한다.

**핵심 원칙**
- 이슈에 기술된 요청을 **정확히** 수행한다. 임의로 변경하거나 생략하지 않는다.
- PR은 반드시 `gh pr create` 명령으로 **직접 생성**한다. 링크 제공이 아닌 **명령 실행**이다.

**1단계: 분석 및 브랜치 생성**
- 이슈 내용을 꼼꼼히 읽고 요구사항을 파악한다
- feature 또는 fix 브랜치를 생성한다 (feature/<설명> 또는 fix/<설명>)
- `git push -u origin <브랜치>`로 리모트에 브랜치를 생성한다

**2단계: 작업 수행**
- 단일 작업이면 직접 수행한다. 복수 작업이면 커밋 단위로 분해하여 subagent에게 병렬 위임한다.
- subagent 위임 시: 각 task는 서로 다른 파일을 수정하도록 분배한다
- subagent 프롬프트에 포함할 것: 작업 내용, 수정 대상 파일, 커밋 메시지
- 커밋 충돌 시 `git pull --rebase origin <브랜치>` 후 재시도 (최대 3회)

**3단계: PR 생성 (필수)**
- `git push origin <브랜치>`로 푸시한다
- 아래 명령을 **반드시 실행**하여 PR을 생성한다:
  ```
  gh pr create --base master --head <브랜치> --title "<제목>" --body "<본문>\n\n@claude"
  ```
- PR 본문 끝에 반드시 `@claude`를 포함한다 (리뷰 에이전트 트리거용)
- **주의: PR 생성 링크를 제공하는 것이 아니라, `gh pr create` 명령을 직접 실행해야 한다**

**리뷰 피드백 반영 (pull_request_review changes_requested)**
1. 리뷰 피드백을 확인한다
2. 수정이 필요한 항목을 task로 분해하여 subagent에게 병렬 위임한다
3. 모든 수정 완료 후 푸시한다

### 리뷰 에이전트 (claude-reviewer)

PR을 리뷰한다. 전체 요약은 PR 코멘트로, 구체적인 지적사항은 해당 파일/라인에 인라인 리뷰 코멘트로 남긴다. 문제가 없으면 approve, 수정이 필요하면 request changes로 리뷰를 제출한다.

## 수익화 운영 지침

상세 실행 매뉴얼: `monetization-guide.md` 참조

<!-- CI 테스트: 2026-02-16 04:22:07 UTC -->
