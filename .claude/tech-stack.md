# 기술 스택

## 프레임워크 & 생성기

- **생성기**: Hugo (Extended, v0.146.0+)
- **테마**: Blowfish (noir 컬러 스킴, git submodule)

## 배포 & 호스팅

- **호스팅**: GitHub Pages + 커스텀 도메인 (mumbi.net)
- **CI/CD**: GitHub Actions (`.github/workflows/hugo.yml`)

## 기능 & 통합

- **댓글**: Disqus
- **검색**: Blowfish 내장 검색 (JSON 인덱스)
- **다크/라이트 모드**: 전환 버튼 지원

## 포스트 파일 규칙

- **위치**: `content/posts/` 디렉토리
- **파일명**: `YYYY-MM-DD-title.md`
- **Permalink 형식**: 프론트매터 `url` 필드로 지정
- **섹션 인덱스**: `content/posts/_index.md`

## 프로젝트 디렉토리

```
config/_default/        # Hugo 분할 설정
  hugo.toml             # 사이트 기본 설정
  params.toml           # Blowfish 테마 파라미터
  languages.ko.toml     # 한국어 언어 설정
  menus.ko.toml         # 메뉴 구성
  markup.toml           # 마크다운 렌더링 설정
content/                # 콘텐츠
  posts/                # 블로그 포스트
  archives/             # 아카이브 페이지
  search/               # 검색 페이지
assets/                 # Hugo 파이프라인 자산 (이미지, CSS)
static/                 # 정적 파일 (CNAME, ads.txt)
themes/blowfish/        # Blowfish 테마 (git submodule)
.github/workflows/      # GitHub Actions 워크플로우
```

## 주요 설정 파일

- `config/_default/hugo.toml`: 사이트 기본 설정 (baseURL, taxonomies, outputs)
- `config/_default/params.toml`: 테마 파라미터 (컬러 스킴, 레이아웃, TOC 등)
- `config/_default/languages.ko.toml`: 한국어 언어 및 작성자 정보
- `config/_default/menus.ko.toml`: 네비게이션 메뉴
- `config/_default/markup.toml`: Goldmark, 코드 하이라이트, TOC 설정

## 빌드 명령어

```bash
# 로컬 개발 서버 (Docker)
docker run --rm -p 1313:1313 -v $(pwd):/src hugomods/hugo:exts server --bind 0.0.0.0

# 정적 사이트 빌드 (Docker)
docker run --rm -v $(pwd):/src hugomods/hugo:exts build

# 테마 서브모듈 초기화
git submodule update --init --recursive

# 테마 업데이트
git submodule update --remote themes/blowfish
```
