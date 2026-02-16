# mumbi.github.io

`mumbi.net` 개인 블로그 저장소입니다.  
Hugo와 Blowfish 테마를 사용하며, GitHub Pages로 배포합니다.

## 프로젝트 개요

- URL: <https://mumbi.net/>
- 엔진: Hugo (Extended)
- 테마: Blowfish (`themes/blowfish`, git submodule)
- 기본 언어: 한국어
- 정적 출력 디렉터리: `dist`

## 빠른 시작

### 1) 저장소 클론 및 서브모듈 초기화

```bash
git clone https://github.com/mumbi/mumbi.github.io.git
cd mumbi.github.io
git submodule update --init --recursive
```

### 2) 로컬 개발 서버 실행

```bash
hugo server
```

- 기본 접속 주소: <http://localhost:1313>
- 변경 사항 저장 시 자동 리빌드

### 3) 정적 빌드

```bash
hugo --gc --minify
```

- 빌드 결과물은 `dist/`에 생성됩니다.

## 디렉터리 구조

```text
.
├── content/
│   ├── posts/             # 블로그 포스트
│   ├── archives/          # 아카이브 페이지
│   └── search/            # 검색 페이지
├── config/_default/       # Hugo 설정 (hugo/params/languages/menus/markup)
├── static/                # 정적 파일 (CNAME, ads.txt 등)
├── themes/blowfish/       # Blowfish 테마 서브모듈
└── .github/workflows/     # 배포/자동화 워크플로
```

## 글 작성 가이드

### 새 포스트 파일 생성

- 위치: `content/posts/`
- 권장 파일명: `YYYY-MM-DD-slug.md`

예시:

```text
content/posts/2026-02-16-example-post.md
```

### front matter 기본 예시

```yaml
---
title: "포스트 제목"
date: 2026-02-16T00:00:00+09:00
categories: ["devops"]
tags: ["hugo", "github-actions"]
url: "/devops/example-post/"
description: "포스트 요약"
author: "mumbi"
draft: true
---
```

### 게시 전 체크

- `draft: false`로 변경했는지 확인
- `url`, `categories`, `tags` 누락 여부 확인
- 로컬에서 `hugo --gc --minify` 빌드 성공 확인

## 배포 및 자동화

### GitHub Pages 배포 (`.github/workflows/hugo.yml`)

- 트리거: `master` 브랜치 push, 수동 실행(`workflow_dispatch`)
- 빌드:
  - Hugo Extended `0.146.0` 설치
  - `hugo --gc --minify --baseURL ...` 실행
  - `dist/build-info.json` 생성
- 배포: `dist/`를 GitHub Pages 아티팩트로 업로드 후 배포

### 보조 자동화 워크플로

- `claude-worker.yml`: 이슈/리뷰 이벤트 기반 작업 자동화
- `claude-reviewer.yml`: PR 리뷰 자동화

위 2개는 블로그 렌더링/Pages 배포 자체와는 분리된 보조 자동화입니다.

## 운영 팁 (트러블슈팅)

### 테마가 깨지거나 없는 경우

증상:

- 템플릿/레이아웃 관련 오류
- Blowfish 관련 리소스 로드 실패

해결:

```bash
git submodule update --init --recursive
```

### Hugo가 설치되지 않은 경우

증상:

- `hugo: command not found`

해결:

- Hugo Extended를 설치한 뒤 다시 실행합니다.
- CI는 워크플로에서 Hugo를 별도 설치하므로 로컬 환경과 분리됩니다.

### 로컬/배포 결과가 다른 경우

- `baseURL` 차이:
  - 로컬: `http://localhost:1313`
  - 배포: GitHub Pages 워크플로에서 `--baseURL` 주입
- 출력 경로 차이:
  - 이 저장소는 `_site`가 아니라 `dist`를 사용

## 라이선스

이 저장소의 라이선스는 `LICENSE` 파일을 따릅니다.
