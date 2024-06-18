---
title: conan 으로 C++ 라이브러리 cmake 프로젝트 만들기
categories: cpp
tags: ["cpp", "conan", "cmake", "cmake_lib"]
---

이 글은 conan new cmake_lib 을 사용하여 C++ 라이브러리 프로젝트를 만드는 방법을 소개합니다.

[c++ 빌드 (feat. conan, cmake)](/cpp/C++-build-with-conan-cmake)

# executable project - hello

먼저 conan new cmake_exe 를 사용하여 라이브러리를 사용할 hello 프로젝트를 만듭니다.

```bash
$ mkdir conan_cmake_lib
$ cd conan_cmake_lib
$ conan new cmake_exe -d name=hello -d version=1.0
File saved: CMakeLists.txt
File saved: conanfile.py 
File saved: src/hello.cpp
File saved: src/hello.h  
File saved: src/main.cpp 
File saved: test_package/conanfile.py
```

conan install 을 실행하여 의존성을 설치합니다. 사실 의존성이 없어서 설치되는 패키지는 없습니다.

```bash
$ conan install .

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
    conanfile.py (hello/1.0): C:\workspace\conan_cmake_lib\conanfile.py

======== Computing necessary packages ========

======== Installing packages ========

======== Finalizing install (deploy, generators) ========
conanfile.py (hello/1.0): Calling generate()
conanfile.py (hello/1.0): Generators folder: C:\workspace\conan_cmake_lib\build\generators
conanfile.py (hello/1.0): CMakeToolchain generated: conan_toolchain.cmake
conanfile.py (hello/1.0): CMakeToolchain: Preset 'conan-default' added to CMakePresets.json.
    (cmake>=3.23) cmake --preset conan-default
    (cmake<3.23) cmake <path> -G "Visual Studio 17 2022" -DCMAKE_TOOLCHAIN_FILE=generators\conan_toolchain.cmake  -DCMAKE_POLICY_DEFAULT_CMP0091=NEW
conanfile.py (hello/1.0): CMakeToolchain generated: C:\workspace\conan_cmake_lib\build\generators\CMakePresets.json
conanfile.py (hello/1.0): CMakeToolchain generated: C:\workspace\conan_cmake_lib\CMakeUserPresets.json
conanfile.py (hello/1.0): Generating aggregated env files
conanfile.py (hello/1.0): Generated aggregated env files: ['conanbuild.bat', 'conanrun.bat']
Install finished successfully
```

conan build 를 실행하여 프로젝트를 빌드합니다.

```bash
$ conan build .

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
    conanfile.py (hello/1.0): C:\workspace\conan_cmake_lib\conanfile.py

======== Computing necessary packages ========

======== Installing packages ========

======== Installing packages ========

======== Finalizing install (deploy, generators) ========
conanfile.py (hello/1.0): Calling generate()
conanfile.py (hello/1.0): Generators folder: C:\workspace\conan_cmake_lib\build\generators
conanfile.py (hello/1.0): CMakeToolchain generated: conan_toolchain.cmake
conanfile.py (hello/1.0): CMakeToolchain: Preset 'conan-default' added to CMakePresets.json.
    (cmake>=3.23) cmake --preset conan-default
    (cmake<3.23) cmake <path> -G "Visual Studio 17 2022" -DCMAKE_TOOLCHAIN_FILE=generators\conan_toolchain.cmake  -DCMAKE_POLICY_DEFAULT_CMP0091=NEW
conanfile.py (hello/1.0): CMakeToolchain generated: C:\workspace\conan_cmake_lib\build\generators\CMakePresets.json
conanfile.py (hello/1.0): CMakeToolchain generated: C:\workspace\conan_cmake_lib\CMakeUserPresets.json
conanfile.py (hello/1.0): Generating aggregated env files
conanfile.py (hello/1.0): Generated aggregated env files: ['conanbuild.bat', 'conanrun.bat']

======== Calling build() ========
conanfile.py (hello/1.0): Calling build()
conanfile.py (hello/1.0): Running CMake.configure()
conanfile.py (hello/1.0): RUN: cmake -G "Visual Studio 17 2022" -DCMAKE_TOOLCHAIN_FILE="generators/conan_toolchain.cmake" -DCMAKE_INSTALL_PREFIX="C:/workspace/conan_cmake_lib" -DCMAKE_POLICY_DEFAULT_CMP0091="NEW" "C:/workspace/conan_cmake_lib"
-- Using Conan toolchain: C:/workspace/conan_cmake_lib/build/generators/conan_toolchain.cmake
-- Conan toolchain: CMAKE_GENERATOR_TOOLSET=v143
-- Conan toolchain: C++ Standard 17 with extensions OFF
-- Selecting Windows SDK version 10.0.22621.0 to target Windows 10.0.19045.
-- The CXX compiler identification is MSVC 19.40.33811.0
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Tools/MSVC/14.40.33807/bin/Hostx64/x64/cl.exe - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Configuring done
-- Generating done
-- Build files have been written to: C:/workspace/conan_cmake_lib/build

conanfile.py (hello/1.0): Running CMake.build()
conanfile.py (hello/1.0): RUN: cmake --build "C:\workspace\conan_cmake_lib\build" --config Debug
msbuild 버전 17.10.4+10fbfbf2e(.NET Framework용)

  Checking Build System
  Building Custom Rule C:/workspace/conan_cmake_lib/CMakeLists.txt
  hello.cpp
  main.cpp
     C:/workspace/conan_cmake_lib/build/Debug/hello.lib 라이브러리 및 C:/workspace/conan_cmake_lib/build/Debug/hello.exp 개체
를 생성하고
  있습니다.
  hello.vcxproj -> C:\workspace\conan_cmake_lib\build\Debug\hello.exe
  Building Custom Rule C:/workspace/conan_cmake_lib/CMakeLists.txt
```

만약 cmake 로 빌드를 원한다면 configure 를 진행해야 합니다.

```bash
cmake --preset conan-default
cmake build .
```

build 디렉토리에 빌드된 실행파일을 실행해봅니다.

```bash
$ ./build/Debug/hello.exe 
hello/1.0: Hello World Debug!
  hello/1.0: _M_X64 defined
  hello/1.0: MSVC runtime: MultiThreadedDebugDLL
  hello/1.0: _MSC_VER1940
  hello/1.0: _MSVC_LANG201703
  hello/1.0: __cplusplus199711
hello/1.0 test_package
```

# library project - format

이제 conan new cmake_lib 을 사용하여 format 라이브러리를 생성합니다.

```bash
$ mkdir -p libs/format
$ cd libs/format
$ conan new cmake_lib -d name=format -d version=1.0
File saved: CMakeLists.txt
File saved: conanfile.py
File saved: include/format.h
File saved: src/format.cpp
File saved: test_package/CMakeLists.txt
File saved: test_package/conanfile.py
File saved: test_package/src/example.cpp
```

format 라이브러리는 fmt 라이브러리를 의존성으로 사용합니다.
conanfile.py 파일에 requirements 를 추가하여 fmt 라이브러리를 의존성으로 추가합니다.

```python
from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps


class formatRecipe(ConanFile):
    name = "format"
    version = "1.0"
    package_type = "library"

    # Optional metadata
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of format package here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "CMakeLists.txt", "src/*", "include/*"

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

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

    def package_info(self):
        self.cpp_info.libs = ["format"]

    def requirements(self):
        self.requires("fmt/10.2.1")
```

conan install 을 실행하여 추가한 의존성을 설치합니다.

```bash
$ conan install .

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
    conanfile.py (format/1.0): C:\workspace\conan_cmake_lib\libs\format\conanfile.py
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
conanfile.py (format/1.0): Calling generate()
conanfile.py (format/1.0): Generators folder: C:\workspace\conan_cmake_lib\libs\format\build\generators
conanfile.py (format/1.0): CMakeDeps necessary find_package() and targets for your CMakeLists.txt
    find_package(fmt)
    target_link_libraries(... fmt::fmt)
conanfile.py (format/1.0): CMakeToolchain generated: conan_toolchain.cmake
conanfile.py (format/1.0): CMakeToolchain: Preset 'conan-default' added to CMakePresets.json.
    (cmake>=3.23) cmake --preset conan-default
    (cmake<3.23) cmake <path> -G "Visual Studio 17 2022" -DCMAKE_TOOLCHAIN_FILE=generators\conan_toolchain.cmake  -DCMAKE_POLICY_DEFAULT_CMP0091=NEW
conanfile.py (format/1.0): CMakeToolchain generated: C:\workspace\conan_cmake_lib\libs\format\build\generators\CMakePresets.json     
conanfile.py (format/1.0): CMakeToolchain generated: C:\workspace\conan_cmake_lib\libs\format\CMakeUserPresets.json
conanfile.py (format/1.0): Generating aggregated env files
conanfile.py (format/1.0): Generated aggregated env files: ['conanbuild.bat', 'conanrun.bat']
Install finished successfully
```

의존성을 설치한 후에는 CMakeLists.txt 에 find_package() 와 target_link_libraries() 로 의존성을 추가해야 합니다.

```cmake
cmake_minimum_required(VERSION 3.15)
project(format CXX)

add_library(format src/format.cpp)
target_include_directories(format PUBLIC include)

find_package(fmt)
target_link_libraries(format fmt::fmt)

set_target_properties(format PROPERTIES PUBLIC_HEADER "include/format.h")
install(TARGETS format)
```

conan build 를 사용하여 빌드를 합니다.

```bash
$ conan build .

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
    conanfile.py (format/1.0): C:\workspace\conan_cmake_lib\libs\format\conanfile.py
Requirements
    fmt/10.2.1#9199a7a0611866dea5c8849a77467b25 - Cache

======== Computing necessary packages ========
Requirements
    fmt/10.2.1#9199a7a0611866dea5c8849a77467b25:f134d4c4e8c78a64bfdbe69deb29a8569e822900#328015a59043e2883eed8cd803f0c8b7 - Cache

======== Installing packages ========

======== Installing packages ========
fmt/10.2.1: Already installed! (1 of 1)
WARN: deprecated: Usage of deprecated Conan 1.X features that will be removed in Conan 2.X:
WARN: deprecated:     'cpp_info.names' used in: fmt/10.2.1

======== Finalizing install (deploy, generators) ========
conanfile.py (format/1.0): Calling generate()
conanfile.py (format/1.0): Generators folder: C:\workspace\conan_cmake_lib\libs\format\build\generators
conanfile.py (format/1.0): CMakeDeps necessary find_package() and targets for your CMakeLists.txt
    find_package(fmt)
    target_link_libraries(... fmt::fmt)
conanfile.py (format/1.0): CMakeToolchain generated: conan_toolchain.cmake
conanfile.py (format/1.0): CMakeToolchain: Preset 'conan-default' added to CMakePresets.json.
    (cmake>=3.23) cmake --preset conan-default
    (cmake<3.23) cmake <path> -G "Visual Studio 17 2022" -DCMAKE_TOOLCHAIN_FILE=generators\conan_toolchain.cmake  -DCMAKE_POLICY_DEFAULT_CMP0091=NEW
conanfile.py (format/1.0): CMakeToolchain generated: C:\workspace\conan_cmake_lib\libs\format\build\generators\CMakePresets.json     
conanfile.py (format/1.0): CMakeToolchain generated: C:\workspace\conan_cmake_lib\libs\format\CMakeUserPresets.json
conanfile.py (format/1.0): Generating aggregated env files
conanfile.py (format/1.0): Generated aggregated env files: ['conanbuild.bat', 'conanrun.bat']

======== Calling build() ========
conanfile.py (format/1.0): Calling build()
conanfile.py (format/1.0): Running CMake.configure()
conanfile.py (format/1.0): RUN: cmake -G "Visual Studio 17 2022" -DCMAKE_TOOLCHAIN_FILE="generators/conan_toolchain.cmake" -DCMAKE_INSTALL_PREFIX="C:/workspace/conan_cmake_lib/libs/format" -DCMAKE_POLICY_DEFAULT_CMP0091="NEW" "C:/workspace/conan_cmake_lib/libs/format"
-- Using Conan toolchain: C:/workspace/conan_cmake_lib/libs/format/build/generators/conan_toolchain.cmake
-- Conan toolchain: CMAKE_GENERATOR_TOOLSET=v143
-- Conan toolchain: C++ Standard 17 with extensions OFF
-- Conan toolchain: Setting BUILD_SHARED_LIBS = OFF
-- Selecting Windows SDK version 10.0.22621.0 to target Windows 10.0.19045.
-- Conan: Component target declared 'fmt::fmt'
-- Configuring done
-- Generating done
-- Build files have been written to: C:/workspace/conan_cmake_lib/libs/format/build

conanfile.py (format/1.0): Running CMake.build()
conanfile.py (format/1.0): RUN: cmake --build "C:\workspace\conan_cmake_lib\libs\format\build" --config Debug
msbuild 버전 17.10.4+10fbfbf2e(.NET Framework용)

  format.vcxproj -> C:\workspace\conan_cmake_lib\libs\format\build\Debug\format.lib
```

빌드가 잘 되었습니다.

conan create 를 실행해야 local 에서 만든 패키지가 패키지 캐시에 설치됩니다.

```bash
$ conan create .

======== Exporting recipe to the cache ========
format/1.0: Exporting package recipe: C:\workspace\conan_cmake_lib\libs\format\conanfile.py
format/1.0: Copied 1 '.py' file: conanfile.py
format/1.0: Copied 1 '.txt' file: CMakeLists.txt
format/1.0: Copied 1 '.h' file: format.h
format/1.0: Copied 1 '.cpp' file: format.cpp
format/1.0: Exported to cache folder: C:\Users\mumbi\.conan2\p\forma4e8ad2fedfb56\e
format/1.0: Exported: format/1.0#4cd5fd8f818aa87b66a18252985ae059 (2024-06-17 13:19:45 UTC)

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
    cli
Requirements
    fmt/10.2.1#9199a7a0611866dea5c8849a77467b25 - Cache
    format/1.0#4cd5fd8f818aa87b66a18252985ae059 - Cache

======== Computing necessary packages ========
format/1.0: Forced build from source
Requirements
    fmt/10.2.1#9199a7a0611866dea5c8849a77467b25:f134d4c4e8c78a64bfdbe69deb29a8569e822900#328015a59043e2883eed8cd803f0c8b7 - Cache
    format/1.0#4cd5fd8f818aa87b66a18252985ae059:6c869b0477a87197a0bfdee7fa3edd261f2e7713 - Build

======== Installing packages ========
fmt/10.2.1: Already installed! (1 of 2)

-------- Installing package format/1.0 (2 of 2) --------
format/1.0: Building from source
format/1.0: Package format/1.0:6c869b0477a87197a0bfdee7fa3edd261f2e7713
format/1.0: Copying sources to build folder
format/1.0: Building your package in C:\Users\mumbi\.conan2\p\b\formaae3cbd588a5d4\b
format/1.0: Calling generate()
format/1.0: Generators folder: C:\Users\mumbi\.conan2\p\b\formaae3cbd588a5d4\b\build\generators
format/1.0: CMakeDeps necessary find_package() and targets for your CMakeLists.txt
    find_package(fmt)
    target_link_libraries(... fmt::fmt)
format/1.0: CMakeToolchain generated: conan_toolchain.cmake
format/1.0: CMakeToolchain generated: C:\Users\mumbi\.conan2\p\b\formaae3cbd588a5d4\b\build\generators\CMakePresets.json
format/1.0: CMakeToolchain generated: C:\Users\mumbi\.conan2\p\b\formaae3cbd588a5d4\b\CMakeUserPresets.json
format/1.0: Generating aggregated env files
format/1.0: Generated aggregated env files: ['conanbuild.bat', 'conanrun.bat']
format/1.0: Calling build()
format/1.0: Running CMake.configure()
format/1.0: RUN: cmake -G "Visual Studio 17 2022" -DCMAKE_TOOLCHAIN_FILE="generators/conan_toolchain.cmake" -DCMAKE_INSTALL_PREFIX="C:/Users/mumbi/.conan2/p/b/formaae3cbd588a5d4/p" -DCMAKE_POLICY_DEFAULT_CMP0091="NEW" "C:/Users/mumbi/.conan2/p/b/formaae3cbd588a5d4/b"
-- Using Conan toolchain: C:/Users/mumbi/.conan2/p/b/formaae3cbd588a5d4/b/build/generators/conan_toolchain.cmake
-- Conan toolchain: CMAKE_GENERATOR_TOOLSET=v143
-- Conan toolchain: C++ Standard 17 with extensions OFF
-- Conan toolchain: Setting BUILD_SHARED_LIBS = OFF
-- Selecting Windows SDK version 10.0.22621.0 to target Windows 10.0.19045.
-- The CXX compiler identification is MSVC 19.40.33811.0
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Tools/MSVC/14.40.33807/bin/Hostx64/x64/cl.exe - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Conan: Component target declared 'fmt::fmt'
-- Configuring done
-- Generating done
-- Build files have been written to: C:/Users/mumbi/.conan2/p/b/formaae3cbd588a5d4/b/build

format/1.0: Running CMake.build()
format/1.0: RUN: cmake --build "C:\Users\mumbi\.conan2\p\b\formaae3cbd588a5d4\b\build" --config Debug
msbuild 버전 17.10.4+10fbfbf2e(.NET Framework용)

  Checking Build System
  Building Custom Rule C:/Users/mumbi/.conan2/p/b/formaae3cbd588a5d4/b/CMakeLists.txt
  format.cpp
  format.vcxproj -> C:\Users\mumbi\.conan2\p\b\formaae3cbd588a5d4\b\build\Debug\format.lib
  Building Custom Rule C:/Users/mumbi/.conan2/p/b/formaae3cbd588a5d4/b/CMakeLists.txt

format/1.0: Package '6c869b0477a87197a0bfdee7fa3edd261f2e7713' built
format/1.0: Build folder C:\Users\mumbi\.conan2\p\b\formaae3cbd588a5d4\b\build
format/1.0: Generating the package
format/1.0: Packaging in folder C:\Users\mumbi\.conan2\p\b\formaae3cbd588a5d4\p
format/1.0: Calling package()
format/1.0: Running CMake.install()
format/1.0: RUN: cmake --install "C:\Users\mumbi\.conan2\p\b\formaae3cbd588a5d4\b\build" --config Debug --prefix "C:/Users/mumbi/.conan2/p/b/formaae3cbd588a5d4/p"
-- Installing: C:/Users/mumbi/.conan2/p/b/formaae3cbd588a5d4/p/lib/format.lib
-- Installing: C:/Users/mumbi/.conan2/p/b/formaae3cbd588a5d4/p/include/format.h

format/1.0: package(): Packaged 1 '.h' file: format.h
format/1.0: package(): Packaged 1 '.lib' file: format.lib
format/1.0: Created package revision 7827af5e9c8fef2c9c1225e678380dc3
format/1.0: Package '6c869b0477a87197a0bfdee7fa3edd261f2e7713' created
format/1.0: Full package reference: format/1.0#4cd5fd8f818aa87b66a18252985ae059:6c869b0477a87197a0bfdee7fa3edd261f2e7713#7827af5e9c8fef2c9c1225e678380dc3
format/1.0: Package folder C:\Users\mumbi\.conan2\p\b\formaae3cbd588a5d4\p
WARN: deprecated: Usage of deprecated Conan 1.X features that will be removed in Conan 2.X:
WARN: deprecated:     'cpp_info.names' used in: fmt/10.2.1

======== Launching test_package ========

======== Computing dependency graph ========
Graph root
    format/1.0 (test package): C:\workspace\conan_cmake_lib\libs\format\test_package\conanfile.py
Requirements
    fmt/10.2.1#9199a7a0611866dea5c8849a77467b25 - Cache
    format/1.0#4cd5fd8f818aa87b66a18252985ae059 - Cache

======== Computing necessary packages ========
Requirements
    fmt/10.2.1#9199a7a0611866dea5c8849a77467b25:f134d4c4e8c78a64bfdbe69deb29a8569e822900#328015a59043e2883eed8cd803f0c8b7 - Cache
    format/1.0#4cd5fd8f818aa87b66a18252985ae059:6c869b0477a87197a0bfdee7fa3edd261f2e7713#7827af5e9c8fef2c9c1225e678380dc3 - Cache

======== Installing packages ========
fmt/10.2.1: Already installed! (1 of 2)
format/1.0: Already installed! (2 of 2)
WARN: deprecated: Usage of deprecated Conan 1.X features that will be removed in Conan 2.X:
WARN: deprecated:     'cpp_info.names' used in: fmt/10.2.1

======== Testing the package ========
Removing previously existing 'test_package' build folder: C:\workspace\conan_cmake_lib\libs\format\test_package\build\msvc-193-x86_64-17-debug
format/1.0 (test package): Test package build: build\msvc-193-x86_64-17-debug
format/1.0 (test package): Test package build folder: C:\workspace\conan_cmake_lib\libs\format\test_package\build\msvc-193-x86_64-17-debug
format/1.0 (test package): Writing generators to C:\workspace\conan_cmake_lib\libs\format\test_package\build\msvc-193-x86_64-17-debug\generators
format/1.0 (test package): Generator 'CMakeDeps' calling 'generate()'
format/1.0 (test package): CMakeDeps necessary find_package() and targets for your CMakeLists.txt
    find_package(format)
    target_link_libraries(... format::format)
format/1.0 (test package): Generator 'CMakeToolchain' calling 'generate()'
format/1.0 (test package): CMakeToolchain generated: conan_toolchain.cmake
format/1.0 (test package): CMakeToolchain generated: C:\workspace\conan_cmake_lib\libs\format\test_package\build\msvc-193-x86_64-17-debug\generators\CMakePresets.json
format/1.0 (test package): CMakeToolchain generated: C:\workspace\conan_cmake_lib\libs\format\test_package\CMakeUserPresets.json     
format/1.0 (test package): Generating aggregated env files
format/1.0 (test package): Generated aggregated env files: ['conanbuild.bat', 'conanrun.bat']

======== Testing the package: Building ========
format/1.0 (test package): Calling build()
format/1.0 (test package): Running CMake.configure()
format/1.0 (test package): RUN: cmake -G "Visual Studio 17 2022" -DCMAKE_TOOLCHAIN_FILE="generators/conan_toolchain.cmake" -DCMAKE_INSTALL_PREFIX="C:/workspace/conan_cmake_lib/libs/format/test_package" -DCMAKE_POLICY_DEFAULT_CMP0091="NEW" "C:/workspace/conan_cmake_lib/libs/format/test_package"
-- Using Conan toolchain: C:/workspace/conan_cmake_lib/libs/format/test_package/build/msvc-193-x86_64-17-debug/generators/conan_toolchain.cmake
-- Conan toolchain: CMAKE_GENERATOR_TOOLSET=v143
-- Conan toolchain: C++ Standard 17 with extensions OFF
-- Selecting Windows SDK version 10.0.22621.0 to target Windows 10.0.19045.
-- The CXX compiler identification is MSVC 19.40.33811.0
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Tools/MSVC/14.40.33807/bin/Hostx64/x64/cl.exe - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Conan: Target declared 'format::format'
-- Conan: Component target declared 'fmt::fmt'
-- Configuring done
-- Generating done
-- Build files have been written to: C:/workspace/conan_cmake_lib/libs/format/test_package/build/msvc-193-x86_64-17-debug

format/1.0 (test package): Running CMake.build()
format/1.0 (test package): RUN: cmake --build "C:\workspace\conan_cmake_lib\libs\format\test_package\build\msvc-193-x86_64-17-debug" 
--config Debug
msbuild 버전 17.10.4+10fbfbf2e(.NET Framework용)

  Checking Build System
  Building Custom Rule C:/workspace/conan_cmake_lib/libs/format/test_package/CMakeLists.txt
  example.cpp
C:\Users\mumbi\.conan2\p\b\formaae3cbd588a5d4\p\include\format.h(6,10): error C1083: 포함 파일을 열 수 없습니다. 'fmt/core.h': No such file or director
y [C:\workspace\conan_cmake_lib\libs\format\test_package\build\msvc-193-x86_64-17-debug\example.vcxproj]

ERROR: format/1.0 (test package): Error in build() method, line 18
        cmake.build()
        ConanException: Error 1 while executing
```

그런데 마지막 단계에서 

C:\Users\mumbi\.conan2\p\b\formaae3cbd588a5d4\p\include\format.h(6,10): error C1083: 포함 파일을 열 수 없습니다. 'fmt/core.h': No such file or director

와 같은 에러가 발생합니다.

마지막 단계는 패키지를 사용하여 테스트하는 단계입니다.

에러가 발생한 이유는 라이브러리 헤더는 잘 설치되었지만 의존성 헤더는 설치가 되지 않았기 때문입니다.

의존성의 헤더까지 설치되게하려면 transitive_headers=True 를 추가해줍니다.

```python
from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps


class formatRecipe(ConanFile):
    name = "format"
    version = "1.0"
    package_type = "library"

    # Optional metadata
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of format package here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "CMakeLists.txt", "src/*", "include/*"

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

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

    def package_info(self):
        self.cpp_info.libs = ["format"]

    def requirements(self):
        self.requires("fmt/10.2.1", transitive_headers=True)
```

다시 conan create 를 실행하면 설치가 잘 됩니다.

```bash
$ conan install .
$ conan create .

======== Exporting recipe to the cache ========
format/1.0: Exporting package recipe: C:\workspace\conan_cmake_lib\libs\format\conanfile.py
format/1.0: Copied 1 '.py' file: conanfile.py
format/1.0: Copied 1 '.txt' file: CMakeLists.txt
format/1.0: Copied 1 '.h' file: format.h
format/1.0: Copied 1 '.cpp' file: format.cpp
format/1.0: Exported to cache folder: C:\Users\mumbi\.conan2\p\formadff6f1afcc1a4\e
format/1.0: Exported: format/1.0#27d771f6df9d5c41066282fd010d306a (2024-06-17 13:26:48 UTC)

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
    cli
Requirements
    fmt/10.2.1#9199a7a0611866dea5c8849a77467b25 - Cache
    format/1.0#27d771f6df9d5c41066282fd010d306a - Cache

======== Computing necessary packages ========
format/1.0: Forced build from source
Requirements
    fmt/10.2.1#9199a7a0611866dea5c8849a77467b25:f134d4c4e8c78a64bfdbe69deb29a8569e822900#328015a59043e2883eed8cd803f0c8b7 - Cache
    format/1.0#27d771f6df9d5c41066282fd010d306a:6c869b0477a87197a0bfdee7fa3edd261f2e7713 - Build

======== Installing packages ========
fmt/10.2.1: Already installed! (1 of 2)

-------- Installing package format/1.0 (2 of 2) --------
format/1.0: Building from source
format/1.0: Package format/1.0:6c869b0477a87197a0bfdee7fa3edd261f2e7713
format/1.0: Copying sources to build folder
format/1.0: Building your package in C:\Users\mumbi\.conan2\p\b\forma6d9cfed072012\b
format/1.0: Calling generate()
format/1.0: Generators folder: C:\Users\mumbi\.conan2\p\b\forma6d9cfed072012\b\build\generators
format/1.0: CMakeDeps necessary find_package() and targets for your CMakeLists.txt
    find_package(fmt)
    target_link_libraries(... fmt::fmt)
format/1.0: CMakeToolchain generated: conan_toolchain.cmake
format/1.0: CMakeToolchain generated: C:\Users\mumbi\.conan2\p\b\forma6d9cfed072012\b\build\generators\CMakePresets.json
format/1.0: CMakeToolchain generated: C:\Users\mumbi\.conan2\p\b\forma6d9cfed072012\b\CMakeUserPresets.json
format/1.0: Generating aggregated env files
format/1.0: Generated aggregated env files: ['conanbuild.bat', 'conanrun.bat']
format/1.0: Calling build()
format/1.0: Running CMake.configure()
format/1.0: RUN: cmake -G "Visual Studio 17 2022" -DCMAKE_TOOLCHAIN_FILE="generators/conan_toolchain.cmake" -DCMAKE_INSTALL_PREFIX="C:/Users/mumbi/.conan2/p/b/forma6d9cfed072012/p" -DCMAKE_POLICY_DEFAULT_CMP0091="NEW" "C:/Users/mumbi/.conan2/p/b/forma6d9cfed072012/b"
-- Using Conan toolchain: C:/Users/mumbi/.conan2/p/b/forma6d9cfed072012/b/build/generators/conan_toolchain.cmake
-- Conan toolchain: CMAKE_GENERATOR_TOOLSET=v143
-- Conan toolchain: C++ Standard 17 with extensions OFF
-- Conan toolchain: Setting BUILD_SHARED_LIBS = OFF
-- Selecting Windows SDK version 10.0.22621.0 to target Windows 10.0.19045.
-- The CXX compiler identification is MSVC 19.40.33811.0
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Tools/MSVC/14.40.33807/bin/Hostx64/x64/cl.exe - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Conan: Component target declared 'fmt::fmt'
-- Configuring done
-- Generating done
-- Build files have been written to: C:/Users/mumbi/.conan2/p/b/forma6d9cfed072012/b/build

format/1.0: Running CMake.build()
format/1.0: RUN: cmake --build "C:\Users\mumbi\.conan2\p\b\forma6d9cfed072012\b\build" --config Debug
msbuild 버전 17.10.4+10fbfbf2e(.NET Framework용)

  Checking Build System
  Building Custom Rule C:/Users/mumbi/.conan2/p/b/forma6d9cfed072012/b/CMakeLists.txt
  format.cpp
  format.vcxproj -> C:\Users\mumbi\.conan2\p\b\forma6d9cfed072012\b\build\Debug\format.lib
  Building Custom Rule C:/Users/mumbi/.conan2/p/b/forma6d9cfed072012/b/CMakeLists.txt

format/1.0: Package '6c869b0477a87197a0bfdee7fa3edd261f2e7713' built
format/1.0: Build folder C:\Users\mumbi\.conan2\p\b\forma6d9cfed072012\b\build
format/1.0: Generating the package
format/1.0: Packaging in folder C:\Users\mumbi\.conan2\p\b\forma6d9cfed072012\p
format/1.0: Calling package()
format/1.0: Running CMake.install()
format/1.0: RUN: cmake --install "C:\Users\mumbi\.conan2\p\b\forma6d9cfed072012\b\build" --config Debug --prefix "C:/Users/mumbi/.conan2/p/b/forma6d9cfed072012/p"
-- Installing: C:/Users/mumbi/.conan2/p/b/forma6d9cfed072012/p/lib/format.lib
-- Installing: C:/Users/mumbi/.conan2/p/b/forma6d9cfed072012/p/include/format.h

format/1.0: package(): Packaged 1 '.h' file: format.h
format/1.0: package(): Packaged 1 '.lib' file: format.lib
format/1.0: Created package revision 921a86ed551b88597e5339bbf3502d05
format/1.0: Package '6c869b0477a87197a0bfdee7fa3edd261f2e7713' created
format/1.0: Full package reference: format/1.0#27d771f6df9d5c41066282fd010d306a:6c869b0477a87197a0bfdee7fa3edd261f2e7713#921a86ed551b88597e5339bbf3502d05
format/1.0: Package folder C:\Users\mumbi\.conan2\p\b\forma6d9cfed072012\p
WARN: deprecated: Usage of deprecated Conan 1.X features that will be removed in Conan 2.X:
WARN: deprecated:     'cpp_info.names' used in: fmt/10.2.1

======== Launching test_package ========

======== Computing dependency graph ========
Graph root
    format/1.0 (test package): C:\workspace\conan_cmake_lib\libs\format\test_package\conanfile.py
Requirements
    fmt/10.2.1#9199a7a0611866dea5c8849a77467b25 - Cache
    format/1.0#27d771f6df9d5c41066282fd010d306a - Cache

======== Computing necessary packages ========
Requirements
    fmt/10.2.1#9199a7a0611866dea5c8849a77467b25:f134d4c4e8c78a64bfdbe69deb29a8569e822900#328015a59043e2883eed8cd803f0c8b7 - Cache
    format/1.0#27d771f6df9d5c41066282fd010d306a:6c869b0477a87197a0bfdee7fa3edd261f2e7713#921a86ed551b88597e5339bbf3502d05 - Cache

======== Installing packages ========
fmt/10.2.1: Already installed! (1 of 2)
format/1.0: Already installed! (2 of 2)
WARN: deprecated: Usage of deprecated Conan 1.X features that will be removed in Conan 2.X:
WARN: deprecated:     'cpp_info.names' used in: fmt/10.2.1

======== Testing the package ========
Removing previously existing 'test_package' build folder: C:\workspace\conan_cmake_lib\libs\format\test_package\build\msvc-193-x86_64-17-debug
format/1.0 (test package): Test package build: build\msvc-193-x86_64-17-debug
format/1.0 (test package): Test package build folder: C:\workspace\conan_cmake_lib\libs\format\test_package\build\msvc-193-x86_64-17-debug
format/1.0 (test package): Writing generators to C:\workspace\conan_cmake_lib\libs\format\test_package\build\msvc-193-x86_64-17-debug\generators
format/1.0 (test package): Generator 'CMakeDeps' calling 'generate()'
format/1.0 (test package): CMakeDeps necessary find_package() and targets for your CMakeLists.txt
    find_package(format)
    target_link_libraries(... format::format)
format/1.0 (test package): Generator 'CMakeToolchain' calling 'generate()'
format/1.0 (test package): CMakeToolchain generated: conan_toolchain.cmake
format/1.0 (test package): CMakeToolchain generated: C:\workspace\conan_cmake_lib\libs\format\test_package\build\msvc-193-x86_64-17-debug\generators\CMakePresets.json
format/1.0 (test package): CMakeToolchain generated: C:\workspace\conan_cmake_lib\libs\format\test_package\CMakeUserPresets.json     
format/1.0 (test package): Generating aggregated env files
format/1.0 (test package): Generated aggregated env files: ['conanbuild.bat', 'conanrun.bat']

======== Testing the package: Building ========
format/1.0 (test package): Calling build()
format/1.0 (test package): Running CMake.configure()
format/1.0 (test package): RUN: cmake -G "Visual Studio 17 2022" -DCMAKE_TOOLCHAIN_FILE="generators/conan_toolchain.cmake" -DCMAKE_INSTALL_PREFIX="C:/workspace/conan_cmake_lib/libs/format/test_package" -DCMAKE_POLICY_DEFAULT_CMP0091="NEW" "C:/workspace/conan_cmake_lib/libs/format/test_package"
-- Using Conan toolchain: C:/workspace/conan_cmake_lib/libs/format/test_package/build/msvc-193-x86_64-17-debug/generators/conan_toolchain.cmake
-- Conan toolchain: CMAKE_GENERATOR_TOOLSET=v143
-- Conan toolchain: C++ Standard 17 with extensions OFF
-- Selecting Windows SDK version 10.0.22621.0 to target Windows 10.0.19045.
-- The CXX compiler identification is MSVC 19.40.33811.0
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Tools/MSVC/14.40.33807/bin/Hostx64/x64/cl.exe - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Conan: Target declared 'format::format'
-- Conan: Component target declared 'fmt::fmt'
-- Configuring done
-- Generating done
-- Build files have been written to: C:/workspace/conan_cmake_lib/libs/format/test_package/build/msvc-193-x86_64-17-debug

format/1.0 (test package): Running CMake.build()
format/1.0 (test package): RUN: cmake --build "C:\workspace\conan_cmake_lib\libs\format\test_package\build\msvc-193-x86_64-17-debug" 
--config Debug
msbuild 버전 17.10.4+10fbfbf2e(.NET Framework용)

  Checking Build System
  Building Custom Rule C:/workspace/conan_cmake_lib/libs/format/test_package/CMakeLists.txt
  example.cpp
     C:/workspace/conan_cmake_lib/libs/format/test_package/build/msvc-193-x86_64-17-debug/Debug/example.lib 라이브러리 및 C:/workspace/conan_cmake_lib/libs/format/test_package/build/msvc-193-x86_64-17-debug/Debug/example.exp 개체를 생성하고 있습니다.
  example.vcxproj -> C:\workspace\conan_cmake_lib\libs\format\test_package\build\msvc-193-x86_64-17-debug\Debug\example.exe
  Building Custom Rule C:/workspace/conan_cmake_lib/libs/format/test_package/CMakeLists.txt


======== Testing the package: Executing test ========
format/1.0 (test package): Running test()
format/1.0 (test package): RUN: Debug\example
format/1.0: Hello World Debug!
  format/1.0: _M_X64 defined
  format/1.0: MSVC runtime: MultiThreadedDebugDLL
  format/1.0: _MSC_VER1940
  format/1.0: _MSVC_LANG201703
  format/1.0: __cplusplus199711
format/1.0 test_package
```

# executable project using library project

이제 hello 프로젝트에서 format 프로젝트를 사용하기 위해 conanfile.py 에 라이브러리 의존성을 추가합니다.

```python
from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps


class helloRecipe(ConanFile):
    name = "hello"
    version = "1.0"
    package_type = "application"

    # Optional metadata
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of hello package here>"
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
        self.requires("format/1.0")
```

conan install 을 실행하여 의존성을 설치합니다. 사실 라이브러리 빌드시 conan create 를 실행하여 이미 설치되어 있습니다.

```bash
$ conan install .

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
    conanfile.py (hello/1.0): C:\workspace\conan_cmake_lib\conanfile.py
Requirements
    fmt/10.2.1#9199a7a0611866dea5c8849a77467b25 - Cache
    format/1.0#27d771f6df9d5c41066282fd010d306a - Cache

======== Computing necessary packages ========
Requirements
    fmt/10.2.1#9199a7a0611866dea5c8849a77467b25:f134d4c4e8c78a64bfdbe69deb29a8569e822900#328015a59043e2883eed8cd803f0c8b7 - Cache
    format/1.0#27d771f6df9d5c41066282fd010d306a:6c869b0477a87197a0bfdee7fa3edd261f2e7713#194304abbc0f3650cead5f6b7f228240 - Cache

======== Installing packages ========
fmt/10.2.1: Already installed! (1 of 2)
format/1.0: Already installed! (2 of 2)
WARN: deprecated: Usage of deprecated Conan 1.X features that will be removed in Conan 2.X:
WARN: deprecated:     'cpp_info.names' used in: fmt/10.2.1

======== Finalizing install (deploy, generators) ========
conanfile.py (hello/1.0): Calling generate()
conanfile.py (hello/1.0): Generators folder: C:\workspace\conan_cmake_lib\build\generators
conanfile.py (hello/1.0): CMakeDeps necessary find_package() and targets for your CMakeLists.txt
    find_package(format)
    target_link_libraries(... format::format)
conanfile.py (hello/1.0): CMakeToolchain generated: conan_toolchain.cmake
conanfile.py (hello/1.0): CMakeToolchain: Preset 'conan-default' added to CMakePresets.json.
    (cmake>=3.23) cmake --preset conan-default
    (cmake<3.23) cmake <path> -G "Visual Studio 17 2022" -DCMAKE_TOOLCHAIN_FILE=generators\conan_toolchain.cmake  -DCMAKE_POLICY_DEFAULT_CMP0091=NEW
conanfile.py (hello/1.0): CMakeToolchain generated: C:\workspace\conan_cmake_lib\build\generators\CMakePresets.json
conanfile.py (hello/1.0): CMakeToolchain generated: C:\workspace\conan_cmake_lib\CMakeUserPresets.json
conanfile.py (hello/1.0): Generating aggregated env files
conanfile.py (hello/1.0): Generated aggregated env files: ['conanbuild.bat', 'conanrun.bat']
Install finished successfully
```

의존성을 추가했으니 라이브러리와 마찬가지로 CMakeLists.txt 에 find_package() 와 target_link_libraries() 를 사용하여 의존성을 추가합니다.

```cmake
cmake_minimum_required(VERSION 3.15)
project(hello CXX)

add_executable(hello src/hello.cpp src/main.cpp)

find_package(format)
target_link_libraries(hello format::format)

install(TARGETS hello DESTINATION "."
        RUNTIME DESTINATION bin
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib
        )
```

main.cpp 에서 라이브러리 함수인 format() 을 사용해봅니다.

```cpp
#include "hello.h"
#include <vector>
#include <string>

#include <format.h>

int main() {
    hello();

    format();

    std::vector<std::string> vec;
    vec.push_back("test_package");

    hello_print_vector(vec);
}
```

conan build 를 사용하여 빌드합니다.

```bash
$ conan build .

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
    conanfile.py (hello/1.0): C:\workspace\conan_cmake_lib\conanfile.py
Requirements
    fmt/10.2.1#9199a7a0611866dea5c8849a77467b25 - Cache
    format/1.0#27d771f6df9d5c41066282fd010d306a - Cache

======== Computing necessary packages ========
Requirements
    fmt/10.2.1#9199a7a0611866dea5c8849a77467b25:f134d4c4e8c78a64bfdbe69deb29a8569e822900#328015a59043e2883eed8cd803f0c8b7 - Cache
    format/1.0#27d771f6df9d5c41066282fd010d306a:6c869b0477a87197a0bfdee7fa3edd261f2e7713#194304abbc0f3650cead5f6b7f228240 - Cache

======== Installing packages ========

======== Installing packages ========
fmt/10.2.1: Already installed! (1 of 2)
format/1.0: Already installed! (2 of 2)
WARN: deprecated: Usage of deprecated Conan 1.X features that will be removed in Conan 2.X:
WARN: deprecated:     'cpp_info.names' used in: fmt/10.2.1

======== Finalizing install (deploy, generators) ========
conanfile.py (hello/1.0): Calling generate()
conanfile.py (hello/1.0): Generators folder: C:\workspace\conan_cmake_lib\build\generators
conanfile.py (hello/1.0): CMakeDeps necessary find_package() and targets for your CMakeLists.txt
    find_package(format)
    target_link_libraries(... format::format)
conanfile.py (hello/1.0): CMakeToolchain generated: conan_toolchain.cmake
conanfile.py (hello/1.0): CMakeToolchain: Preset 'conan-default' added to CMakePresets.json.
    (cmake>=3.23) cmake --preset conan-default
    (cmake<3.23) cmake <path> -G "Visual Studio 17 2022" -DCMAKE_TOOLCHAIN_FILE=generators\conan_toolchain.cmake  -DCMAKE_POLICY_DEFAULT_CMP0091=NEW
conanfile.py (hello/1.0): CMakeToolchain generated: C:\workspace\conan_cmake_lib\build\generators\CMakePresets.json
conanfile.py (hello/1.0): CMakeToolchain generated: C:\workspace\conan_cmake_lib\CMakeUserPresets.json
conanfile.py (hello/1.0): Generating aggregated env files
conanfile.py (hello/1.0): Generated aggregated env files: ['conanbuild.bat', 'conanrun.bat']

======== Calling build() ========
conanfile.py (hello/1.0): Calling build()
conanfile.py (hello/1.0): Running CMake.configure()
conanfile.py (hello/1.0): RUN: cmake -G "Visual Studio 17 2022" -DCMAKE_TOOLCHAIN_FILE="generators/conan_toolchain.cmake" -DCMAKE_INSTALL_PREFIX="C:/workspace/conan_cmake_lib" -DCMAKE_POLICY_DEFAULT_CMP0091="NEW" "C:/workspace/conan_cmake_lib"
-- Using Conan toolchain: C:/workspace/conan_cmake_lib/build/generators/conan_toolchain.cmake
-- Conan toolchain: CMAKE_GENERATOR_TOOLSET=v143
-- Conan toolchain: C++ Standard 17 with extensions OFF
-- Selecting Windows SDK version 10.0.22621.0 to target Windows 10.0.19045.
-- Conan: Target declared 'format::format'
-- Conan: Component target declared 'fmt::fmt'
-- Configuring done
-- Generating done
-- Build files have been written to: C:/workspace/conan_cmake_lib/build

conanfile.py (hello/1.0): Running CMake.build()
conanfile.py (hello/1.0): RUN: cmake --build "C:\workspace\conan_cmake_lib\build" --config Debug
msbuild 버전 17.10.4+10fbfbf2e(.NET Framework용)

  hello.vcxproj -> C:\workspace\conan_cmake_lib\build\Debug\hello.exe
```

빌드된 executable 을 실행합니다.

```bash
$ ./build/Debug/hello.exe 
hello/1.0: Hello World Debug!
  hello/1.0: _M_X64 defined
  hello/1.0: MSVC runtime: MultiThreadedDebugDLL
  hello/1.0: _MSC_VER1940
  hello/1.0: _MSVC_LANG201703
  hello/1.0: __cplusplus199711
format/1.0: Hello World Debug!
  format/1.0: _M_X64 defined
  format/1.0: MSVC runtime: MultiThreadedDebugDLL
  format/1.0: _MSC_VER1940
  format/1.0: _MSVC_LANG201703
  format/1.0: __cplusplus199711
hello/1.0 test_package
```

# transitive_headers

transitive_headers 는 라이브러리의 의존성 헤더를 같이 포함하는 기능입니다.
라이브러리의 헤더에서 의존성 헤더를 include 할 때 유용합니다.

감사합니다.