---
title: 스크립트로 환경 변수 설정하기
categories: dev
tags: sh
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
