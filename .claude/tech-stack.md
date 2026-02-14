# 기술 스택

## 프레임워크 & 생성기

- **생성기**: Jekyll (Ruby)
- **테마**: Minimal Mistakes v4.24.0 (다크 모드)

## 배포 & 호스팅

- **호스팅**: GitHub Pages + 커스텀 도메인 (mumbi.net)

## 기능 & 통합

- **댓글**: Disqus
- **검색**: Lunr.js

## 포스트 파일 규칙

- **위치**: `_posts/` 디렉토리
- **파일명**: `YYYY-MM-DD-title.md` (Jekyll 규칙)
- **Permalink 형식**: `/:categories/:title/`
- **카테고리 정의**: `_data/navigation.yml`

## 프로젝트 디렉토리

```
_config.yml        # 메인 설정
_posts/            # 블로그 포스트 (마크다운)
_pages/            # 정적 페이지 (아카이브, 태그, 카테고리)
_layouts/          # HTML/Liquid 페이지 템플릿
_includes/         # 재사용 가능한 템플릿 조각
_sass/             # SCSS 스타일시트
_data/             # 네비게이션 및 UI 텍스트 (YAML)
assets/            # CSS, JS, 이미지
```

## 주요 설정 파일

- `_config.yml`: 사이트 설정, 플러그인, 기본값
- `_data/navigation.yml`: 사이드바 및 상단 네비게이션 구조
- `Gemfile`: Ruby 의존성
- `package.json`: JS 빌드 스크립트 (uglify, banner)

## 빌드 명령어

```bash
# 의존성 설치
bundle install

# 로컬 개발 서버 (http://localhost:4000)
bundle exec jekyll serve

# 정적 사이트 빌드
bundle exec jekyll build

# 파일 감시 프리뷰
bundle exec rake preview

# JavaScript 빌드/압축
npm run build:js

# Docker 기반 로컬 개발
./build-and-run.sh
```
- **컨테이너**: Docker (Alpine Linux 3.16)

## 빌드 & 의존성

- **Ruby**: Bundler (gem 관리)
- **JavaScript**: npm (자산 빌드 - uglify, banner)
- **빌드 도구**: Rake (작업 자동화)
