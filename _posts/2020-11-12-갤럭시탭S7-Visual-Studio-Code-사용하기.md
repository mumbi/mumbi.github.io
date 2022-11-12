---
title: 갤럭시 탭 S7(안드로이드 태블릿) 에서 Visual Studio Code 사용하기
categories: dev-tips
tags: ['갤럭시 탭 S7', '안드로이드', 'vscode']
---

# 개요
Visual Studio Code 가 안드로이드 앱으로는 제공되지 않지만 code-server 라는 오픈소스를 사용해서 안드로이드에서 Visual Studio Code 를 사용할 수 있습니다.

# code-server 설치
code-server 를 설치하는 방법은 여러가지를 제공되지만 이 문서에서는 Termux + ubuntu 를 사용하는 방법을 설명합니다.

## Termux 설치
Google Play 스토어에서도 Termux 를 설치할 수 있지만, 더 이상 업데이트되지 않고 있어 보안 이슈 등이 업데이트되지 않습니다. 그렇기 때문에 F-droid 라는 앱을 통해 Termux 를 설치할 것을 권장하고 있습니다.

[https://f-droid.org/ko/packages/com.termux/](https://f-droid.org/ko/packages/com.termux/)

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

### proot-distro 설치
패키지들을 최신으로 업그레이드 합니다.
```bash
pkg upgrade
```

우분투 배포판을 설치하기 위해 proot-disto 라는 배포판 관리자를 설치합니다.
```bash
pkg install proot-distro
```

proot-distro 를 사용하면 우분투 뿐만 아니라 다양한 배포판을 설치할 수 있지만, 많이 사용되는 우분투로 설명합니다.
```bash
proot-distro install ubuntu
```

설치된 우분투에 접속합니다.
```bash
proot-distro login ubuntu
```

code-server 는 다양한 방법의 설치 방법을 지원하는데 가장 쉬운 install.sh 로 설치로 설명합니다.

install.sh 는 실행 환경에 맞춰서 자동으로 설치됩니다.

우분투는 deb 패키지 관리자를 사용해서 설치됩니다.

```bash
root@localhost:~# curl -fsSL https://code-server.dev/install.sh | sh
Ubuntu 22.04 LTS
Installing v4.8.2 of the arm64 deb package from GitHub.

+ mkdir -p ~/.cache/code-server
+ curl -#fL -o ~/.cache/code-server/code-server_4.8.2_arm64.deb.incomplete -C - https://github.com/coder/code-server/releases/download/v4.8.2/code-server_4.8.2_arm64.deb
######################################################################## 100.0%
+ mv ~/.cache/code-server/code-server_4.8.2_arm64.deb.incomplete ~/.cache/code-server/code-server_4.8.2_arm64.deb
+ dpkg -i ~/.cache/code-server/code-server_4.8.2_arm64.deb
Selecting previously unselected package code-server.
(Reading database ... 5620 files and directories currently installed.)
Preparing to unpack .../code-server_4.8.2_arm64.deb ...
Unpacking code-server (4.8.2) ...
Setting up code-server (4.8.2) ...

deb package has been installed.

To have systemd start code-server now and restart on boot:
  sudo systemctl enable --now code-server@$USER
Or, if you don't want/need a background service you can run:
  code-server
```

apt 패키지 관리자를 통해 설치 된 것을 확인할 수 있고 systemctl 을 사용할 수 있다는 안내가 출력됩니다.

하지만 안드로이드 리눅스 환경에서는 PID 1 을 사용할 수 없기 때문에 systemctl 을 사용할 수 없습니다.
```bash
root@localhost:~# code-server
[2022-11-07T06:02:00.079Z] info  Wrote default config file to ~/.config/code-server/config.yaml
[2022-11-07T06:02:02.198Z] info  code-server 4.8.2 ef82b1a565709cc91a53dc7b609aeee435404c0e
[2022-11-07T06:02:02.200Z] info  Using user-data-dir ~/.local/share/code-server
[2022-11-07T06:02:02.233Z] info  Using config file ~/.config/code-server/config.yaml
[2022-11-07T06:02:02.233Z] info  HTTP server listening on http://127.0.0.1:8080/
[2022-11-07T06:02:02.233Z] info    - Authentication is enabled
[2022-11-07T06:02:02.233Z] info      - Using password from ~/.config/code-server/config.yaml
[2022-11-07T06:02:02.233Z] info    - Not serving HTTPS
```

code-server 를 실행하면 config.yaml 이 생성되는데 이 설정 파일에서 비밀번호를 설정해야 합니다.

설정 파일을 수정하기 위해 vim 과 repository 파일들을 가져오기 위해 git을 설치합니다.

```bash
apt update
apt install vim git
```

vi 로 config.yaml 의 비밀버호를 변경하고 다시 code-server 를 실행 시킨 후, 브라우저로 [localhost:8080](http://localhost:8080) 에 접속하여 설정 파일에 입력한 비밀번호를 입력하면 설치가 완료됩니다.
![image](https://user-images.githubusercontent.com/261637/201463178-56493def-324b-4957-98a0-84d4e26552d6.png)

code-server 의 장점 중 하나는 터미널 창(Ctrl + `) 에서 ubuntu 쉘을 사용할 수 있는 것입니다.

# 마무리
이 포스트를 작성하기 위해 몇가지 방법으로 시도해보았는데 code-server 의 install.sh 을 사용하지 않고 직접 release 중 arm 버전(대부분의 모바일 기기는 arm 아키텍처를 사용합니다.)을 설치하면 code-server 앱을 설치할 수 있었습니다. arm 아키텍처를 모바일에서 많이 사용하기 때문에 앱을 제공해주는 것 같기도 합니다.
브라우저가 아닌 앱으로 실헹하기 때문에 Visual Studio Code 앱을 설치한 느낌을 받을 수 있었습니다. 

이것으로 갤럭시 탭 S7 에서 Visual Studio Code 를 사용하는 방법을 포스팅을 마무리합니다.

감사합니다.