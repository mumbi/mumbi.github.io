---
title: 갤럭시 탭 S7(안드로이드 태블릿) 에서 Visual Studio Code 사용하기 (feat. vscode-server, vscode.dev)
categories: dev-tips
tags: ['갤럭시 탭 S7', '안드로이드', 'vscode', 'vscode-server']
---

# 개요

`Microsoft` 에서 제공하는 `vscode-server` 를 사용해서 `vscode` 를 사용하는 방법을 설명합니다. 

# `vscode-server` 설치

`vscode-server` 는 리눅스, 맥, 윈도우즈 환경을 지원합니다.

<https://code.visualstudio.com/docs/remote/vscode-server#_quick-start>{:target="_blank"}

안드로이드는 리눅스 위에서 돌아가지만 사용자가 직접 리눅스 쉘에 접근할 수 없기 때문에 에뮬레이터 앱을 설치해야 합니다.

그 중 `Termux` 앱을 사용하는 방법을 설명합니다.

## `Termux` 설치

`Google Play` 스토어에서도 `Termux` 를 설치할 수 있지만, 더 이상 업데이트되지 않고 있어 보안 이슈 등이 업데이트되지 않습니다. 그렇기 때문에 `F-droid` 라는 앱을 통해 `Termux` 를 설치할 것을 권장하고 있습니다.

<https://f-droid.org/ko/packages/com.termux/>{:target="_blank"}

```bash
Welcome to Termux!

Community forum: https://termux.com/community
Gitter chat:     https://gitter.im/termux/termux
IRC channel:     #termux on libera.chat

Working with packages:

 * Search packages:   pkg search <query>
 * Install a package: pkg install <package>
 * Upgrade packages:  pkg upgrade

Subscribing to additional repositories:

 * Root:     pkg install root-repo
 * X11:      pkg install x11-repo

Report issues at https://termux.com/issues

~ $
```

`Termux` 앱이 리눅스 쉘 기능을 제공하지만 리눅스 배포판과는 구조가 다르기 때문에 리눅스 배포판을 설치하여 진행합니다.

### `proot-distro` 설치

패키지들을 최신으로 업그레이드 합니다.

```bash
pkg upgrade
```

`ubuntu` 배포판을 설치하기 위해 `proot-disto` 라는 배포판 관리자를 설치합니다.

```bash
pkg install proot-distro
```

`proot-distro` 를 사용하면 `ubuntu` 뿐만 아니라 다양한 배포판을 설치할 수 있지만, 많이 사용되는 `ubuntu` 로 설명합니다.

```bash
proot-distro install ubuntu
```

설치된 `ubuntu` 에 접속합니다.

```bash
proot-distro login ubuntu
```

#### `vscode-server` 설치

`visual studio` 에서 제공하는 스크립트로 설치를 진행합니다.

혹시 `wget` 이 설치되어 있지 않다면 설치해야 합니다.

```bash
apt update
apt install wget
```

```bash
wget -O- https://aka.ms/install-vscode-server/setup.sh | sh
```

```bash
root@localhost:~# wget -O- https://aka.ms/install-vscode-server/setup.sh | sh
--2022-11-12 22:11:47--  https://aka.ms/install-vscode-server/setup.sh
Resolving aka.ms... 23.49.52.46
Connecting to aka.ms|23.49.52.46|:443... connected.
HTTP request sent, awaiting response... 301 Moved Permanently
Location: https://vscodeserverlauncher.blob.core.windows.net/builds/setup-scripts/setup.sh [following]
--2022-11-12 22:11:49--  https://vscodeserverlauncher.blob.core.windows.net/builds/setup-scripts/setup.sh
Resolving vscodeserverlauncher.blob.core.windows.net... 20.150.78.68
Connecting to vscodeserverlauncher.blob.core.windows.net|20.150.78.68|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 1758 (1.7K) [text/x-sh]
Saving to: ‘STDOUT’

-                                                    100%[======================================================================================================================>]   1.72K  --.-KB/s    in 0s

2022-11-12 22:11:50 (156 MB/s) - written to stdout [1758/1758]

glibc version is 2.35
is min? 1
Installing from https://aka.ms/vscode-server-launcher/aarch64-unknown-linux-gnu
root@localhost:~#
```

#### `vscode-server` 실행 및 설정

```bash
code-server
```

`vscode-server` 를 사용하기 위해서는 라이선스 동의를 해야합니다.

```bash
root@localhost:~# code-server

VS Code Server

*
* By using the software, you agree to the
* the Visual Studio Code Server License Terms (https://aka.ms/vscode-server-license) and
* the Microsoft Privacy Statement (https://privacy.microsoft.com/en-US/privacystatement).
*

? Do you accept the terms in the License Agreement (y/n) › yes
```

라이선스 동의를 하게 되면 기기 인증이 필요합니다.

```bash
To grant access to the server, please log into https://github.com/login/device and use code ABCD-1234
```

브라우저로 <https://github.com/login/device>{:target="_blank"} 에 접속한 후, 위에 출력된 `ABCD-1234` 를 입력해줍니다.

> `vscode.dev` 는 `vscode-server` 와 직접 연결하지 않고 `github` 을 통한 `Remote Tunnel` 을 사용하기 때문에 `github` 에 가입하고, 인증해야합니다.

인증을 완료하면 `vscode-server` 에서 기기 이름을 입력하라고 출력됩니다.

```bash
? What would you like to call this machine? (busy-ibis) ›
```

기기 이름을 입력하면 설치된 `vscode-server` 로 접속하는 `vscode.dev` URL 이 출력됩니다.

```bash
✔ What would you like to call this machine? · galaxytab-s7
[2022-11-12 13:49:04] info Creating tunnel with the name: galaxytab-s7

Open this link in your browser https://insiders.vscode.dev/+ms-vscode.remote-server/galaxytab-s7
```

출력된 URL 로 접속하면 초기 설정이 진행되는데 github tunnel 을 사용해서 그런지 시간이 꽤 걸립니다.

![image](https://user-images.githubusercontent.com/261637/201477487-fcb80724-bbaa-4f60-9085-76234864460d.png)

서버와 연결이 완료된 모습입니다.

저 URL 을 꼭 기억해야하는 것은 아닙니다.

<https://vscode.dev>{:target="_blank"} 에 접속한 후 `폴더 열기` 를 누릅니다.

![image](https://user-images.githubusercontent.com/261637/201477732-4cb9c1cf-f6b2-4a3a-9d2b-f8dd47fe28c7.png)

로컬 열기가 지원되지 않는다고 하는데 `원격 열기` 를 누릅니다.

![image](https://user-images.githubusercontent.com/261637/201477821-e38fda93-9098-49b3-a202-bbaf5914f993.png)

`Tunnel에 연결` 을 누릅니다.

`Tunnel에 연결` 이 안나오고 `Visual Studio Code 다운로드` 만 보일 때가 있는데 조금 기다리면 나옵니다.

![image](https://user-images.githubusercontent.com/261637/201477900-8bc2f896-5ead-4ef9-b4a4-5de034397090.png)

GitHub 을 사용하여 로그인하려 한다고 할 때 `허용` 을 누릅니다.

![image](https://user-images.githubusercontent.com/261637/201478087-f54d07f3-e602-419d-bb58-791c0b34264f.png)

로그인이 완료되면 기기 이름으로 입력한 이름을 목록에서 선택합니다.

![image](https://user-images.githubusercontent.com/261637/201478170-81fa2b08-4caf-4b76-b61a-053d89275420.png)

서버에 접속이 완료된 모습입니다.

![image](https://user-images.githubusercontent.com/261637/201478354-22653ca1-0186-42cf-97fb-de5d174719a7.png)

크롬으로 접속했을 때, `점점점` 메뉴를 누르고 `앱 설치` 를 누르면 Code 앱을 설치할 수 있습니다.

![image](https://user-images.githubusercontent.com/261637/201478452-b520580c-8edd-4db7-8815-085f1f96b88a.png)

안드로이드의 sdcard 를 추가할 수도 있는데 sdcard 는 보안 상의 이유인지 실행 권한을 갖을 수 없습니다.

따라서 빌드 후 디버깅을 할 수 없습니다. 빌드가 필요없는 프로젝트들은 sdcard 를 추가해서 사용하셔도 괜찮을 것 같습니다.

# 마무리

`vscode-server` 는 `github` 인증과 Tunnel 을 사용해서 그런지 초기 시간이 오픈소스 `code-server` 에 비해 오래 걸리는 단점이 있습니다.
하지만 `Microsoft` 에서 제공하는 확장을 모두 사용할 수 있다는 장점이 있습니다.

개인적으로는 `Microsoft` 에서 제공하는 기능의 이점이 너무 큰 것 같아서 `vscode-server` 를 사용 중입니다.

오픈소스 `code-server` 를 이용한 `Visual Studio Code` 사용 방법도 있으니 참고해서 설치하시면 좋을 것 같네요.

감사합니다.
