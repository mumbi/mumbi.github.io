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

## 수익화 운영 지침

상세 실행 매뉴얼: `monetization-guide.md` 참조
