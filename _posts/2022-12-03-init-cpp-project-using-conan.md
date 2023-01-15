---
title: vscode 로 으로 linux c++ 프로젝트 구성하기 (feat. conan)
categories: cpp
tags: ["cpp", "conan", "cmake", "clang", "linux"]
---

# 개요

`Windows` 에서 `c++` 프로젝트는 `Visual Studio` 를 설치하면 쉽게 구성할 수 있습니다.

`Linux` 프로젝트를 구성하는 방법에는 여러가지가 있는데 그 중 `vscode`, `conan`, `cmake` 를 활용한 방법을 알아보고자 합니다.

# 개발환경

`Linux` 프로젝트를 구성한다고 해서 반드시 `Linux` 에서 개발할 필요는 없습니다.

`vscode` 는 `vscode-server` 를 `Linux` 에 설치하여 `Windows` 에서 개발 할 수 있습니다.

`vscode-server` 의 설치는 아래 링크를 참고해 주시기 바랍니다.

[갤럭시 탭 S7(안드로이드 태블릿) 에서 vscode 사용하기 (feat. vscode-server, vscode.dev)](https://mumbi.net/dev-tips/%EA%B0%A4%EB%9F%AD%EC%8B%9C%ED%83%ADS7-vscode-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0-vscode-server){:target="_blank"}

## `conan` 설치

`conan` 은 `c++` 패키지 매니저 입니다. 

`python` 으로 개발되어서 `pip3` 로 설치할 수 있습니다.

```bash
sudo yum install python3-pip
sudo pip3 install conan
```

## `cmake` 설치

`cmake` 는 빌드 구성 도구입니다.

```bash
sudo yum install cmake
```

## `clang`

`clang` 은 `c++` 컴파일러 입니다. 

`gcc` 를 사용하셔도 됩니다.

```bash
sudo yum install clang
```

## `vscode` 확장 설치

`C/C++ Extension Pack`
`CMake`

# 소스 코드 작성

소스 코드를 `src/` 에 생성합니다.

```cpp
#include <iostream>

int main()
{
    std::cout << "hello world!" << std::endl;
}
```

# `conan` 빌드

## `conanfile.txt` 파일 생성

종속성과 빌드 구성 툴을 설정합니다.

```conf
[generators]
cmake
```

## install

`conanfile.txt` 가 준비되면 `build` 디렉토리를 생성하고 이동하여 `conan` 으로 종속성들을 설치합니다.

```bash
mkdir build
cd build
conan install ..
```

`conan install` 를 실행하면 `conanfile.txt` 에 명시된 종속성들이 설치되고, `generators` 와 연동하기 위한 파일들이 생성됩니다.

# `CMake` 구성

## `CMakeLists.txt` 파일 생성

프로젝트의 빌드 구성 파일입니다.

프로젝트의 루트 디렉토리로 이동하여 파일을 생성합니다.

```bash
cd ..
```

```cmake
cmake_minimum_required(VERSION 2.8.12)
project(main)

add_definitions("-std=c++2a")

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(main src/main.cpp)
target_link_libraries(main ${CONAN_LIBS})
```

빌드에 필요한 종속성들을 `conan` 이 생성한 `cmake` 파일에서 참조합니다.

## 빌드 구성

`build` 디렉토리로 이동하여 `CMake` 를 실행합니다.

```bash
cd build
cmake ..
```

여기까지 진행하면 아래와 같은 디렉토리 구조가 생성됩니다.

+ build/
+ src/
+ conanfile.txt

# 빌드

`build/` 로 이동하여 빌드를 진행합니다.

```bash
cd build
make
```

에러없이 빌드가 되면 `build/bin/` 에 실행 파일이 생성됩니다.

# 실행

```bash
./bin/main
```

# 마무리

`Linux` 개발 환경을 구성하는 여러 방법이 있지만 빌드 구성을 용이하게 도와주는 `Cmake` 와 종속성을 관리해주는 `conan` 을 이용하는 방법을 알아보았습니다.

종속성을 관리해주는 솔루션은 여러가지가 있으니 프로젝트에 적합한 솔루션을 선택하시면 좋을 것 같습니다.

감사합니다.