---
title: c++ 빌드 (feat. conan, cmake)
categories: cpp
tags: ["cpp", "빌드", "conan", "cmake"]
---

이 글은 conan 과 cmake 를 이용하여 C++ 빌드 시스템을 구성하는 방법을 설명합니다.

| cmake | 3.24.0 | 크로스 플랫폼 빌드 시스템 | <https://cmake.org/>{:target="_blank"} |
| conan | 2.3.0 | C++ 패키지 관리 시스템 | <https://conan.io/>{:target="_blank"} |

# cmake

사실, cmake 이 크로스 플랫폼 빌드 시스템이기 때문에 cmake 만으로도 프로젝트 빌드 환경을 구성할 수 있습니다.

아쉬운 점이 있다면 종속성 관리입니다.

오픈소스 라이브러리, 바이너리 라이브러리 등 배포 방법이 다른 라이브러리들을 일일이 관리해야 합니다.

# 패키지 관리 시스템

여러 언어들은 이런 종속성 관리를 위해 패키지 관리 시스템을 제공합니다.

|언어|패키지 관리 시스템|
|:-:|:-:|:-:|
|java|maven, gradle|
|c#|nuget|
|javascript|npm, yarn|
|python|pip|
|rust|cargo|

C++ 도 패키지 관리 시스템이 있습니다. 바로 conan 과 vcpkg 입니다.

# IDE

Visual Studio 와 같은 통합 개발 환경(Integration Development Environment) 에서는 자체적인 프로젝트 환경 구성 및 패키지 관리 시스템을 제공하기도 합니다.

Visual Studio Code(이하 vscode) 는 확장을 통해 IDE 를 구성할 수 있습니다.
여러 조합이 있을 수 있는데 이 글에서는 cmake + conan 을 사용합니다.

CMake Tools 확장을 설치합니다.

![Image](https://github.com/mumbi/mumbi.github.io/assets/261637/37fb114a-f1d8-4295-b67b-6ac47064ee96)

CMakeLists.txt 파일을 생성하기 전에는 왼쪽 사이드바에 아직 보이지 않습니다.


# 시작

## Visual studio 실행

vscode 에서 빈 프로젝트 디렉토리를 엽니다.

```bash
mkdir app
cd app
code .
```

## conan new

conan 은 cmake 로 프로젝트를 구성할 수 있는 명령어를 제공해 줍니다.

```bash
$ conan new cmake_exe -d name=app -d version=1.0
File saved: CMakeLists.txt
File saved: conanfile.py
File saved: src/app.cpp
File saved: src/app.h
File saved: src/main.cpp
File saved: test_package/conanfile.py
```

CMakeLists.txt, conanfile.py 외에 초기 파일들이 생성됩니다.

## conan install

```bash
$ conan install . --build=missing

======== Input profiles ========
Profile host:
[settings]
arch=x86_64
build_type=Debug        
compiler=msvc
compiler.cppstd=17      
compiler.runtime=dynamic
compiler.runtime_type=Debug
compiler.version=193
os=Windows

Profile build:
[settings]
arch=x86_64
build_type=Debug
compiler=msvc
compiler.cppstd=17
compiler.runtime=dynamic
compiler.runtime_type=Debug
compiler.version=193
os=Windows


======== Computing dependency graph ========
Graph root
    conanfile.py (app/1.0): C:\workspace\app\conanfile.py

======== Computing necessary packages ========

======== Installing packages ========

======== Finalizing install (deploy, generators) ========
conanfile.py (app/1.0): Calling generate()
conanfile.py (app/1.0): Generators folder: C:\workspace\app\build\generators
conanfile.py (app/1.0): CMakeToolchain generated: conan_toolchain.cmake
conanfile.py (app/1.0): CMakeToolchain: Preset 'conan-default' added to CMakePresets.json.
    (cmake>=3.23) cmake --preset conan-default
    (cmake<3.23) cmake <path> -G "Visual Studio 17 2022" -DCMAKE_TOOLCHAIN_FILE=generators\conan_toolchain.cmake  -DCMAKE_POLICY_DEFAULT_CMP0091=NEW
conanfile.py (app/1.0): CMakeToolchain generated: C:\workspace\app\build\generators\CMakePresets.json
conanfile.py (app/1.0): CMakeToolchain generated: C:\workspace\app\CMakeUserPresets.json
conanfile.py (app/1.0): Generating aggregated env files
conanfile.py (app/1.0): Generated aggregated env files: ['conanbuild.bat', 'conanrun.bat']
Install finished successfully
```

출력된 내용을 살펴보면 (cmake>=3.23) cmake --preset conan-default 을 발견할 수 있습니다.

## cmake --preset

```bash
$ cmake --preset conan-default
Preset CMake variables:

  CMAKE_POLICY_DEFAULT_CMP0091="NEW"
  CMAKE_TOOLCHAIN_FILE:FILEPATH="generators\conan_toolchain.cmake"

-- Using Conan toolchain: C:/workspace/app/build/generators/conan_toolchain.cmake
-- Conan toolchain: CMAKE_GENERATOR_TOOLSET=v143
-- Conan toolchain: C++ Standard 17 with extensions OFF
-- Selecting Windows SDK version 10.0.22000.0 to target Windows 10.0.19045.
-- The CXX compiler identification is MSVC 19.34.31937.0
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Tools/MSVC/14.34.31933/bin/Hostx64/x64/cl.exe - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Configuring done
-- Generating done
-- Build files have been written to: C:/workspace/app/build
```

여기까지 진행하면 cmake 를 configuration 할 수 있는 상태가 됩니다.

## cmake configuration

configuration 을 cmake cli 로 시작할 수 있지만, CMake Tools 확장을 사용하면 편합니다.

그런데 왼쪽 사이드바에 아직 CMake Tools 아이콘이 안보이는데, CMakeLists.txt 을 인식하지 못했기 때문입니다.

vscode 를 재시작하거나, 

![Image](https://github.com/mumbi/mumbi.github.io/assets/261637/edae50a0-fc48-4432-aa70-9dcec1654c40)

CMakeLists.txt 파일을 우클릭하면 나오는 메뉴에서 [Configure All Projects] 를 선택하면 CMake Tools 아이콘이 생깁니다.

또한 방금 생성된 preset 으로 configuration 을 시작할 수 있습니다.

![Image](https://github.com/mumbi/mumbi.github.io/assets/261637/90788df6-3072-4d18-b6e8-02f81b03dbab)

['conan-default' config] 를 선택하면 configuration 이 시작됩니다.

왼쪽 사이드바에서 CMake Tools 아이콘이 보이고 해당 탭에서는 프로젝트 빌드 환경을 볼 수 있습니다.

![Image](https://github.com/mumbi/mumbi.github.io/assets/261637/fe9d1dfb-f13c-446c-9dbc-02cb131e1d12)

CMake Tools 탭에서 [Configure] - ['conan-default' config] 오른쪽의 연필 모양의 아이콘을 누르면 configuration 할 preset 을 선택할 수 있습니다.

![Image](https://github.com/mumbi/mumbi.github.io/assets/261637/c486bb86-96af-476e-9042-571a2ebe3b0d)

[Configure] 오른쪽의 화살표 아이콘을 누르면 configuration 이 시작됩니다.

![Image](https://github.com/mumbi/mumbi.github.io/assets/261637/f05ca145-8e9e-4795-ace6-86d07b8fa8b5)

## build

CMake Tools 탭에서 [Build] - [conan-debug] 오른쪽의 연필 모양의 아이콘을 누르면 빌드할 preset 을 선택할 수 있습니다.

![Image](https://github.com/mumbi/mumbi.github.io/assets/261637/4ba8b371-9583-4259-9095-988f1b10c0b9)

[Build] 오른쪽의 화살표 모양의 아이콘을 누르면 빌드가 시작됩니다.

![Image](https://github.com/mumbi/mumbi.github.io/assets/261637/9a76e105-6e63-49e6-885b-0ffeede91cd0)

## 실행

[Launch] 오른쪽의 세모 모양의 아이콘을 누르면 빌드한 앱이 실행됩니다.

![Image](https://github.com/mumbi/mumbi.github.io/assets/261637/e859aba9-3915-4a65-91f6-8a38561aab81)

```bash
$ "C:/workspace/app/build/Debug/app.exe"
app/1.0: Hello World Debug!
  app/1.0: _M_X64 defined
  app/1.0: MSVC runtime: MultiThreadedDebugDLL
  app/1.0: _MSC_VER1934
  app/1.0: _MSVC_LANG201703
  app/1.0: __cplusplus199711
app/1.0 test_package
```

## 디버깅

src/main.cpp 파일을 열고, breakpoint 를 설정한 후, 

![Image](https://github.com/mumbi/mumbi.github.io/assets/261637/ec530095-e4f4-4d81-90f1-8d39ee2aac72)

[Debug] 오른쪽의 벌레 세모 모양의 아이콘을 누르면 디버깅이 시작됩니다.

![Image](https://github.com/mumbi/mumbi.github.io/assets/261637/63c30782-4cec-40ca-ae26-ccd21bc49082)

![Image](https://github.com/mumbi/mumbi.github.io/assets/261637/bec03f5f-2d68-45ba-af98-9d344e12d6e8)

## 의존성 설치

### conanfile.py

<https://conan.io/center>{:target="_blank"}

conan center 에서 설치할 라이브러리를 검색합니다.

검색된 라이브러리를 선택하면 conanfile.py 문서를 찾을 수 있습니다.

```python
from conan import ConanFile
from conan.tools.cmake import cmake_layout


class ExampleRecipe(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain"

    def requirements(self):
        self.requires("fmt/10.2.1")

    def layout(self):
        cmake_layout(self)
```

이 문서에서 

```python
def requirements(self):
        self.requires("fmt/10.2.1")
```

부분만 복사하여 프로젝트의 conanfile.py 에 붙여넣고 저장합니다.

```python
from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps


class appRecipe(ConanFile):
    name = "app"
    version = "1.0"
    package_type = "application"

    # Optional metadata
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of app package here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "CMakeLists.txt", "src/*"

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def requirements(self):
        self.requires("fmt/10.2.1")

```

### CMakeLists.txt

conan install 을 실행하면 패키지가 설치됩니다.

```bash
$ conan install . --build=missing

======== Input profiles ========
Profile host:
[settings]
arch=x86_64
build_type=Debug
compiler=msvc
compiler.cppstd=17
compiler.runtime=dynamic
compiler.runtime_type=Debug
compiler.version=193
os=Windows

Profile build:
[settings]
arch=x86_64
build_type=Debug
compiler=msvc
compiler.cppstd=17
compiler.runtime=dynamic
compiler.runtime_type=Debug
compiler.version=193
os=Windows


======== Computing dependency graph ========
Graph root
    conanfile.py (app/1.0): C:\workspace\app\conanfile.py
Requirements
    fmt/10.2.1#9199a7a0611866dea5c8849a77467b25 - Cache

======== Computing necessary packages ========
Requirements
    fmt/10.2.1#9199a7a0611866dea5c8849a77467b25:f134d4c4e8c78a64bfdbe69deb29a8569e822900#328015a59043e2883eed8cd803f0c8b7 - Cache

======== Installing packages ========
fmt/10.2.1: Already installed! (1 of 1)
WARN: deprecated: Usage of deprecated Conan 1.X features that will be removed in Conan 2.X:
WARN: deprecated:     'cpp_info.names' used in: fmt/10.2.1

======== Finalizing install (deploy, generators) ========
conanfile.py (app/1.0): Calling generate()
conanfile.py (app/1.0): Generators folder: C:\workspace\app\build\generators
conanfile.py (app/1.0): CMakeDeps necessary find_package() and targets for your CMakeLists.txt
    find_package(fmt)
    target_link_libraries(... fmt::fmt)
conanfile.py (app/1.0): CMakeToolchain generated: conan_toolchain.cmake
conanfile.py (app/1.0): CMakeToolchain: Preset 'conan-default' added to CMakePresets.json.
    (cmake>=3.23) cmake --preset conan-default
    (cmake<3.23) cmake <path> -G "Visual Studio 17 2022" -DCMAKE_TOOLCHAIN_FILE=generators\conan_toolchain.cmake  -DCMAKE_POLICY_DEFAULT_CMP0091=NEW
conanfile.py (app/1.0): CMakeToolchain generated: C:\workspace\app\build\generators\CMakePresets.json
conanfile.py (app/1.0): CMakeToolchain generated: C:\workspace\app\CMakeUserPresets.json
conanfile.py (app/1.0): Generating aggregated env files
conanfile.py (app/1.0): Generated aggregated env files: ['conanbuild.bat', 'conanrun.bat']
Install finished successfully
```

출력되는 내용에서 

```bash
find_package(fmt)
target_link_libraries(... fmt::fmt)
```

을 찾을 수 있습니다.

프로젝트의 CMakeLists.txt 파일에 add_executable() 밑에 추가합니다.
target_link_libraries() 의 ... 부분을 executable 인 app 으로 수정합니다.

```cmake
cmake_minimum_required(VERSION 3.15)
project(app CXX)

add_executable(app src/app.cpp src/main.cpp)

find_package(fmt)
target_link_libraries(app fmt::fmt)

install(TARGETS app DESTINATION "."
        RUNTIME DESTINATION bin
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib
        )

```

### main.cpp

include<> 추가하고, 함수를 호출을 추가합니다.

```cpp
#include <fmt/core.h>
```

```cpp
fmt::print("Hello world!\n");
```

```cpp
#include "app.h"
#include <vector>
#include <string>

#include <fmt/core.h>

int main() {
    app();

    std::vector<std::string> vec;
    vec.push_back("test_package");

    app_print_vector(vec);

    fmt::print("Hello world!\n");
}
```

빌드하고 실행해보면 잘 호출되는 것을 볼 수 있습니다.

```bash
$ "C:/workspace/app/build/Debug/app.exe"
app/1.0: Hello World Debug!
  app/1.0: _M_X64 defined
  app/1.0: MSVC runtime: MultiThreadedDebugDLL
  app/1.0: _MSC_VER1934
  app/1.0: _MSVC_LANG201703
  app/1.0: __cplusplus199711
app/1.0 test_package
Hello world!
```
# 맺음말

vscode 에서 cmake, conan 을 사용하여 프로젝트 환경 구성을 해보았습니다.
conan 이외에 vcpkg 를 사용할 수도 있습니다. 제공하는 패키지 저장소에 원하는 라이브러리가 있는지 살펴보고 선택하면 좋을 것 같습니다.


 