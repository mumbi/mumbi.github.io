---
title: "스크립트로 환경 변수 설정하기"
date: 2020-09-08T00:00:00+09:00
categories: ["bash"]
tags: ["bash"]
url: "/bash/export-in-script/"
description: "Bash 스크립트에서 환경 변수를 동적으로 추가하거나 업데이트하는 방법을 소개합니다. sed를 활용한 .bashrc 파일 수정 및 자동화 기법을 다룹니다."
author: "mumbi"
draft: false
---

```sh
#!/bin/bash

# https://stackoverflow.com/a/49852337
# call option with parameters: $1=name $2=value $3=file
function option() {
    name=${1//\//\\/}
    value=${2//\//\\/}
    sed -i \
        -e '/^#\?\(\s*'"${name}"'\s*=\s*\).*/{s//\1'"${value}"'/;:a;n;ba;q}' \
        -e '$a'"${name}"'='"${value}" $3
}

option 'export BUILD_UPLOAD_PATH' '/devs/build-upload' ~/.bashrc

source ~/.bashrc
```
