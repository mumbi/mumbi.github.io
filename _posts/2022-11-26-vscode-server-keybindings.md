---
title: vscode-server 키 바인딩
categories: dev-tips
tags: ["vscode-server", "키바인딩"]
---

# 개요

`vscode-server` 를 설치하고 사용하다 보니 `ctrl+c`, `ctrl+x`, `ctrl+v` 단축키가 작동하지 않는 것을 발견하고, 키바인딩 방법을 찾아보았습니다.

# `복사하기`, `잘라내기`, `붙여넣기` 키 바인딩 

![image](https://user-images.githubusercontent.com/261637/204093781-f0b43edb-a297-4beb-83d2-13da4e00194a.png)

![image](https://user-images.githubusercontent.com/261637/204093945-e7edd9b8-6ac6-49e8-a1f7-85280d909684.png)

keybindings.json
```json
// 키 바인딩을 이 파일에 넣어서 기본값 재정의
[
    {
        "key": "ctrl+c", "command": "editor.action.clipboardCopyAction"
    },
    {
        "key": "ctrl+x", "command": "editor.action.clipboardCutAction"
    },
    {
        "key": "ctrl+v", "command": "editor.action.clipboardPasteAction"
    }
]
```

# 마무리

아마도 vscode-server 가 브라우저를 통해 접속하다보니 보안상의 이슈로 클립보드 단축키를 제외해 놓은 것 같습니다.

위처럼 설정하면 단축키가 잘 작동합니다.

감사합니다.