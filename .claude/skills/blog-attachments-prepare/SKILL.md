---
name: blog-attachments-prepare
description: 첨부 계획대로 스크린샷을 캡처해 개인 정보를 가리고 배포용 zip 을 만들어, 업로드할 파일의 전체 경로 목록을 낸다
node:
  in:
    materials_dir: { shape: text }
    attach_plan: { shape: json }
  out:
    files: { shape: text, list: 1 }
---

## 입력
- `materials_dir` — 자료 폴더 전체 경로. 결과물은 그 아래 `attach\` 에 만든다
- `attach_plan` — `blog-post-plan` 의 첨부 계획(`files`·`screenshots`·`notes`)

## 실행
결과 폴더 `<materials_dir>\attach` 를 만든다. 경로에 한글이 있으면 파일 대화상자·외부 도구 입력이 깨질 수 있으니, 그런 경우 한글 없는 경로(예: 자료 폴더가 있는 드라이브의 작업 폴더)로 바꾸고 그 사실을 보고한다.

배포 파일(zip):
1. 계획의 `contents` 대로 스테이징 폴더에 모은다. 스크립트가 같은 폴더의 파일을 쓰게 되어 있으면 압축을 푼 구조에서 그대로 동작하도록 기본 경로를 고친 사본을 넣는다
2. PowerShell 5.1 로 실행될 `.ps1` 에 한글이 있으면 UTF-8 **BOM 있음**으로 저장한다(없으면 한글이 깨진다)
3. `Compress-Archive` 로 zip 을 만들고, zip 과 안의 주요 파일 SHA256 을 계산해 `<attach>\SHA256SUMS.txt` 에 적는다

스크린샷:
1. 대상 앱을 띄우고 컴퓨터 유즈(`orca computer get-app-state --app <앱> --restore-window --json`)로 창을 캡처한다. 창이 다른 창에 가려지면 `--restore-window` 로 앞으로 가져온 뒤 다시 찍는다
2. 계획의 `mask` 영역(아바타·계정명 등)을 `System.Drawing` 으로 픽셀화한 PNG 를 저장하고, 결과 이미지를 직접 열어 가림이 됐는지 확인한다
3. 캡처를 위해 앱 상태를 바꿨다면(연결·로그인 등) 끝난 뒤 원래대로 돌린다. 원격 기기를 끄는 선택지(예: "대기 모드 전환")는 켜지 않는다
4. 앱 설치기를 다시 실행해 오류창을 재현하려 하지 않는다 — 설치된 상태에서는 유지 관리(수정/복구/제거) 마법사가 떠서 설치를 망칠 수 있다

## 출력
- `files` — 업로드할 파일의 전체 경로 배열(zip, 가린 스크린샷 순). 계획이 비어 있으면 빈 배열
