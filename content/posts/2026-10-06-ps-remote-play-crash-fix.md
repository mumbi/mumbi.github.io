---
title: "Windows 용 PS Remote Play 강제 종료(0xc0000005) 원인과 해결"
date: 2026-10-06T23:00:00+09:00
categories: ["windows"]
tags: ["ps-remote-play", "0xc0000005", "UnifiedTelemetry", "windbg", "dll"]
url: "/windows/ps-remote-play-crash-fix/"
description: "Windows 용 PS Remote Play 가 PS 연결 직후 강제 종료되던 문제를 덤프로 분석해 텔레메트리 DLL 에서 원인을 찾고, 대체 DLL 로 해결한 과정과 9.5 에서는 안 되는 이유를 정리합니다."
image: "https://github.com/user-attachments/assets/8b7c06e6-5037-42be-9031-39b69f75a1d2"
images: ["https://github.com/user-attachments/assets/8b7c06e6-5037-42be-9031-39b69f75a1d2"]
author: "mumbi"
draft: false
toc: true
---

Windows 용 PS Remote Play 가 로그인 후 PS 에 연결하려는 순간 아무 메시지 없이 꺼지는 문제가 있습니다.

인터넷에 알려진 해결책은 "8.5 로 다운그레이드 + 버전 패처" 입니다. 그런데 제 PC 에서는 8.5 도 똑같이 꺼졌고, 지금은 8.5 설치 파일조차 Sony 서버에서 내려가 그 방법을 그대로 따라 할 수도 없습니다.

결국 크래시 덤프를 분석해 원인을 찾았고, **텔레메트리(사용 통계 전송) DLL 을 아무 일도 하지 않는 대체 DLL 로 바꿔서** 해결했습니다.

| 항목 | 내용 |
|:--|:--|
| 증상 | PS 연결 직후 앱 강제 종료, `0xc0000005`, 모듈 `UnifiedTelemetry.Service.dll` |
| 원인 (제 환경) | 텔레메트리 초기화 중 숫자를 문자열 주소로 읽음 |
| 해결 | 8.5 + 버전 패처 + 대체 텔레메트리 DLL |
| 확인 환경 | Windows 11 (26200), PS Remote Play 8.5.0.08070, 2026년 10월 |

{{< alert >}}
비공식 방법입니다. 앱 파일을 바꾸므로 본인 책임 하에 사용하세요. 텔레메트리가 꺼지므로 Sony 로 사용 통계가 전송되지 않습니다.
{{< /alert >}}

## 증상 확인

이벤트 뷰어 → Windows 로그 → 응용 프로그램에서 아래 오류가 보이면 이 글과 같은 문제입니다.

```text
오류 있는 응용 프로그램 이름: RemotePlay.exe, 버전: 9.5.0.8040
오류 있는 모듈 이름: UnifiedTelemetry.Service.dll, 버전: 0.0.0.0, 타임스탬프: 0x65573955
예외 코드: 0xc0000005
오류 오프셋: 0x00000000000f2e53
```

`.NET Runtime` 1026 이벤트(`처리되지 않은 예외로 인해 프로세스가 종료되었습니다`)도 함께 남습니다.

## 해결 방법

9.5 에서는 대체 DLL 이 통하지 않아서(이유는 아래 [9.5 에서는 왜 안 되나](#95-에서는-왜-안-되나)) 8.5 로 내린 뒤에 적용합니다. 다른 분들은 8.5 다운그레이드만으로 해결됐다는 보고도 있으니, **다운그레이드를 먼저 해 보고 그래도 같은 크래시가 날 때만** DLL 을 교체하세요.

1. 현재 버전(9.x)에서 PSN 로그인을 한 번 해 둡니다. 8.5 는 저장된 로그인 정보를 그대로 씁니다. (기존 다운그레이드 가이드의 방법이며, 저도 9.x 에서 로그인해 둔 상태로 진행했습니다.)
2. 9.x 를 제거합니다.
3. 8.5 MSI 를 설치하고, **실행하지 않습니다.**
4. 버전 패처를 실행합니다.
5. Remote Play 를 실행해 PS 에 연결해 봅니다. 꺼지지 않으면 여기서 끝입니다.
6. 그래도 꺼지고 이벤트 로그에 위와 같은 `UnifiedTelemetry.Service.dll` 오류가 남으면, 텔레메트리 DLL 3개를 대체 DLL 로 바꿉니다.

### 8.5 설치 파일 받기

Uptodown 등에 올라온 8.5 설치 파일(`ps-remote-play-8-5-0-08070.exe`)은 3 MB 짜리 **웹 설치기**입니다. 실행하면 Sony 서버에서 MSI 를 받아 오는데, Sony 가 구버전 MSI 를 내려서 1 바이트짜리 응답만 돌아옵니다. 그래서 "설치 패키지를 열지 못했습니다" 오류로 실패합니다.

```text
DownloadFiles: downloading https://remoteplay.dl.playstation.net/remoteplay/module/win/RemotePlayInstaller_8.5.0.08070_x64.msi
Error opening MSI database: 110
Launch result 1, exit code 1620
```

대신 Internet Archive(Wayback Machine)가 2026-03-20 에 보관한 Sony 원본 MSI 를 받을 수 있습니다.

- [RemotePlayInstaller_8.5.0.08070_x64.msi 받기 (Wayback Machine)](https://web.archive.org/web/20260320131233id_/https://remoteplay.dl.playstation.net/remoteplay/module/win/RemotePlayInstaller_8.5.0.08070_x64.msi)

```text
https://web.archive.org/web/20260320131233id_/https://remoteplay.dl.playstation.net/remoteplay/module/win/RemotePlayInstaller_8.5.0.08070_x64.msi
```

받은 뒤 반드시 확인하세요. 파일 속성 → 디지털 서명이 **Sony Interactive Entertainment Inc.** 이고 유효해야 합니다.

| 항목 | 값 |
|:--|:--|
| 크기 | 19,881,984 바이트 |
| SHA256 | `4363a6ef5548ad682e69153b30397f32620a7b532f2f7592b79b8deed9abffc1` |

PowerShell 에서 파일을 받은 폴더로 이동한 뒤 확인합니다.

```powershell
cd $HOME\Downloads   # MSI 를 받은 폴더
Get-FileHash .\RemotePlayInstaller_8.5.0.08070_x64.msi
Get-AuthenticodeSignature .\RemotePlayInstaller_8.5.0.08070_x64.msi
```

더블클릭으로 설치하고, 마지막 화면에 실행 체크박스가 있으면 끕니다. 패처 없이 8.5 를 실행하면 최신 버전으로 강제 업데이트될 수 있습니다.

### 버전 패처

[xeropresence/remoteplay-version-patcher](https://github.com/xeropresence/remoteplay-version-patcher) 를 관리자 권한으로 실행합니다. Sony 서버에서 현재 버전 번호를 받아와 `RemotePlay.exe` 의 버전 정보만 바꿔 주는 도구라, 8.5 를 쓰면서도 업데이트 요구를 피할 수 있습니다.

### 대체 DLL 교체

[ps-remote-play-telemetry-stub.zip](https://github.com/user-attachments/files/33250570/ps-remote-play-telemetry-stub.zip) 을 받아 압축을 풉니다. 안에는 이렇게 들어 있습니다.

```text
ps-remote-play-telemetry-stub\
├─ install-stub.ps1               ← 교체·복원 스크립트
├─ UnifiedTelemetry.Service.dll   ← 대체 DLL 3개
├─ UnifiedTelemetry.Client.dll
├─ UnifiedTelemetry.Model.dll
└─ src\                           ← 대체 DLL 의 C 소스
   ├─ ut_service.c
   ├─ ut_client.c
   └─ ut_model.c
```

| 파일 | SHA256 |
|:--|:--|
| ps-remote-play-telemetry-stub.zip | `0731b5f052e634f844e53a7a6a753f9a0b01c13df0287aafadcda7594593148e` |
| UnifiedTelemetry.Service.dll | `3f8c6276179d64975ec92efec4cb1cb459ccaa6a1d3e0860992f5bfe91d077e6` |
| UnifiedTelemetry.Client.dll | `f219235532aff21795a4071388f7149640bdc1c25037e7792bd4c457aa1c01b4` |
| UnifiedTelemetry.Model.dll | `825e3d777cf16589cf9d6588f3419607444ada3c5bf3e77416dea790d7703a90` |

C 소스(`src\`)도 함께 들어 있으니 직접 빌드하셔도 됩니다(MinGW-w64 gcc 필요).

```bash
cd src
gcc -shared -O2 -s -static-libgcc -o ../UnifiedTelemetry.Service.dll ut_service.c
gcc -shared -O2 -s -static-libgcc -o ../UnifiedTelemetry.Client.dll  ut_client.c
gcc -shared -O2 -s -static-libgcc -o ../UnifiedTelemetry.Model.dll   ut_model.c
```

빌드 결과는 `install-stub.ps1` 이 있는 상위 폴더에 덮어씁니다.

Remote Play 를 종료한 상태에서, **관리자 PowerShell** 을 열어 압축을 푼 폴더(`install-stub.ps1` 이 있는 곳)로 이동한 뒤 실행합니다. 스크립트는 같은 폴더의 DLL 3개를 `C:\Program Files (x86)\Sony\PS Remote Play` 에 복사합니다.

```powershell
cd $HOME\Downloads\ps-remote-play-telemetry-stub   # 압축을 푼 폴더
powershell -ExecutionPolicy Bypass -File .\install-stub.ps1
```

원본은 설치 폴더에 `*.dll.old` 로 남습니다. 스크립트를 여러 번 실행해도 이미 교체된 파일은 건너뛰므로 원본 백업은 지켜집니다. 되돌릴 때는 `-Restore` 를 붙입니다.

```powershell
powershell -ExecutionPolicy Bypass -File .\install-stub.ps1 -Restore
```

이제 Remote Play 를 실행해 연결하면 됩니다.

![대체 DLL 적용 후 PS Remote Play 시작 화면](https://github.com/user-attachments/assets/366bd3e3-3ad4-4546-b543-ac90044e3275)

![대체 DLL 적용 후 PS5 에 정상 연결된 PS Remote Play](https://github.com/user-attachments/assets/8b7c06e6-5037-42be-9031-39b69f75a1d2)

{{< alert "circle-info" >}}
Remote Play 가 업데이트되면 다시 꺼질 수 있습니다. 9.x 로 올라갔다면 대체 DLL 이 통하지 않으니 8.5 를 다시 설치하고 버전 패처를 실행한 뒤 `install-stub.ps1` 을 다시 실행하세요. 8.5 를 재설치만 했다면 버전 패처와 스크립트를 다시 실행하면 됩니다.
{{< /alert >}}

## 원인 분석

여기부터는 제 PC 에서 원인을 찾은 과정입니다.

### 버전 문제가 아니었다

처음에는 다들 말하는 대로 9.x 버전의 버그라고 보고 8.5 로 내렸습니다. 그런데 제 PC 에서는 8.5 도 **같은 모듈, 같은 오프셋(`0xf2e53`)** 에서 죽었습니다.

확인해 보니 크래시가 나는 `UnifiedTelemetry.Service.dll` 은 8.5 와 9.5 모두 PE 타임스탬프가 같은(`0x65573955`, 2023-11) DLL 이었습니다. 앱 버전을 바꿔도 이 DLL 은 그대로라 소용이 없었던 것으로 보입니다.

매번 정확히 같은 주소에서 죽어서, 무작위로 나는 메모리 오류 같은 하드웨어 문제일 가능성은 낮다고 판단했습니다.

### 크래시 지점 잡기

WinDbg 의 콘솔 버전인 `cdb` 로 Remote Play 를 실행하고, 텔레메트리 DLL 안에서 접근 위반이 나는 순간에 멈추도록 했습니다.

```text
.if ( (@rip >= UnifiedTelemetry_Service) & (@rip < (UnifiedTelemetry_Service + 0x400000)) ) { ... .dump /ma ... } .else { gn }
```

PS 에 연결하자마자 걸렸습니다. 덤프를 남기는 명령 파일은 경로 문제로 실패해서, 멈춰 있는 프로세스에 두 번째 `cdb` 를 비침습 모드(`-pv`)로 붙여 레지스터·스택·덤프를 떴습니다.

```text
UnifiedTelemetry_Service!UnifiedTelemetry::TelemetrySender::sendEvent+0x30f3:
00007ffa`c08e2e53 43803c0600      cmp     byte ptr [r14+r8],0 ds:00000000`00000dac=??

 # Call Site
00 UnifiedTelemetry_Service!UnifiedTelemetry::TelemetrySender::sendEvent+0x30f3
01 UnifiedTelemetry_Service!utQueue::SqlQueue::configureEventLimits+0x62d
02 UnifiedTelemetry_Service!utQueue::SqlQueueRecordLimitRow::operator=+0xc75
03 UnifiedTelemetry_Service!utServiceInit+0x9
04 RpCtrlWrapper!Function168+0x6c816
```

심볼이 없어서 함수 이름은 가장 가까운 export 이름일 뿐이지만, 흐름은 분명합니다.

- Remote Play 본체(`RpCtrlWrapper.dll`)가 텔레메트리 서비스를 초기화합니다(`utServiceInit`).
- 그 안에서 문자열 길이를 세는 루프(`cmp byte ptr [r14+r8],0` / `inc r8`)가 돕니다.
- 그런데 문자열 주소여야 할 `r14` 가 `0xdac`(3500) 입니다.

바로 앞 코드를 보면 NULL 검사는 합니다.

```text
mov     r14,qword ptr [rbp+77h]
test    r14,r14
je      ...
```

3500 은 NULL 이 아니니 통과하고, 3500 번지를 읽다가 죽습니다. `RpCtrlWrapper` 가 채워 넘긴 설정 구조체와 2023년 빌드 DLL 이 기대하는 구조체가 맞지 않는 것으로 보입니다. (3500 이 어떤 필드인지까지는 확인하지 못했습니다.)

### 대체 DLL

같은 텔레메트리 DLL 로 **PlayStation Accessories** 앱이 죽던 사례에서, DLL 을 아무것도 하지 않는 것으로 바꿔 해결한 저장소가 있습니다.

- [Epokhe/playstation-accessories-fix](https://github.com/Epokhe/playstation-accessories-fix)

Remote Play 에 맞추기 위해 두 가지를 확인했습니다.

**1. Remote Play 가 쓰는 함수**

`RpCtrlWrapper.dll` 이 세 DLL 에서 가져다 쓰는 함수는 26 개였고, 모두 C 이름(`utCreateService`, `utServiceInit`, `utCreateStaticServiceTransport` …)입니다. 대체 DLL 에는 원본의 C 함수 전부(23 / 11 / 25 개)를 넣었습니다.

**2. 원본이 쓰는 메모리 크기**

대체 함수가 호출한 쪽 버퍼에 원본보다 많이 쓰면 메모리를 덮어씁니다. Remote Play 가 쓰는 함수 중 출력이 있는 것은 원본을 디스어셈블해서 크기를 맞췄습니다.

```text
UnifiedTelemetry_Service!utGetServiceConfig:
  mov     r8d,816h        ; 0x816 바이트 복사
```

| 함수 | Accessories 판 | 이 글 |
|:--|:--|:--|
| `utGetServiceConfig` | 2048 바이트를 0 으로 | 원본과 같은 0x816(2070) 바이트 |
| `utServiceGetCommonPropertiesObject` | 4 바이트(int) | 원본과 같은 8 바이트(포인터) |
| `utCreateService` 등 생성 함수 | 8 바이트 핸들 | 원본과 같은 8 바이트 핸들 |

Remote Play 가 쓰지 않아 크기를 확인하지 못한 함수의 출력은 건드리지 않고, 모든 함수가 성공(0)을 돌려줍니다.

```c
#define UT_SERVICE_CONFIG_SIZE 0x816

EXPORT int utServiceInit(intptr_t service) { return 0; }

EXPORT int utGetServiceConfig(intptr_t service, void *config) {
    if (config) memset(config, 0, UT_SERVICE_CONFIG_SIZE);
    return 0;
}
```

### 9.5 에서는 왜 안 되나

9.5 에 같은 대체 DLL 을 넣으면 연결은커녕 **실행하자마자** 꺼집니다.

```text
오류 있는 모듈 이름: unknown
예외 코드: 0xc0000005
오류 오프셋: 0x00007ffc8e400000
```

9.5 는 구조가 8.5 와 다릅니다. 본체가 보호된 `preloader.dll` + `runtime.dll`(62 MB) 로 바뀌었고, 디버거를 붙이면 의도적인 것으로 보이는 예외(레지스터가 모두 0 인 접근 위반, 싱글 스텝 예외)가 연달아 나서 디버거로 따라가기 어려웠습니다. 그래서 디버거 대신 Windows 오류 보고(WER LocalDumps)로 덤프를 받았습니다.

```text
(덤프 분석 출력 발췌·요약)
rip=00007ffc`8e400000                ; = runtime 모듈 시작 주소 (MZ 헤더)
call    runtime (00007ffc`8e400000)   ; runtime+0x2b489e 에서 자기 시작 주소를 호출
lmn m UnifiedTelemetry*              ; → 결과 없음 (텔레메트리 DLL 은 로드조차 안 됨)
```

- 텔레메트리 DLL 이 **로드되기도 전에** 죽습니다.
- 보호 모듈이 자기 시작 주소를 호출합니다. 정상이라면 미리 실제 코드로 바꿔 놓았을 자리로 보입니다.
- 원본 DLL 로 되돌리면 켜지기는 합니다(PS 에 연결하면 처음의 텔레메트리 크래시가 그대로 납니다).

그래서 9.5 의 보호 모듈이 설치 폴더의 서명된 파일이 바뀐 것을 감지하고 진행을 막는 것으로 추정합니다. 보호 코드 자체는 분석하지 않았고, 보호 장치를 우회하는 것도 이 글의 범위가 아닙니다. 8.5 에는 이 보호 모듈(`preloader.dll`·`runtime.dll`)이 없고, 대체 DLL 로 정상 동작하는 것을 확인했습니다.

## 마무리

정리하면 이렇습니다.

- 제 PC 에서 꺼진 원인은 앱 버전이 아니라 8.5 와 9.5 가 함께 쓰는 **2023년 텔레메트리 DLL** 이었습니다.
- 8.5 는 텔레메트리 DLL 을 대체 DLL 로 바꾸면 정상 동작합니다.
- 9.5 는 보호 모듈 때문에 DLL 교체가 통하지 않습니다.
- 8.5 설치 파일은 Sony 서버에서 내려갔으니 Wayback 사본을 서명 확인 후 사용합니다.

Sony 가 정식으로 고쳐 주기 전까지의 임시 방편입니다. 감사합니다.

## 참고

- [Epokhe/playstation-accessories-fix](https://github.com/Epokhe/playstation-accessories-fix) — 같은 DLL 로 인한 PlayStation Accessories 크래시 해결
- [xeropresence/remoteplay-version-patcher](https://github.com/xeropresence/remoteplay-version-patcher) — 버전 패처
- [ResetEra 스레드](https://www.resetera.com/threads/playstation-remote-play-windows-desktop-has-been-consistently-crashing-since-its-9-0-update.1491382/) — Remote Play 9.0 이후 크래시
