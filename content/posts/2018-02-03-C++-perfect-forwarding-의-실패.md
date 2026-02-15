---
title: "C++ perfect forwarding 의 실패"
date: 2018-02-03T00:00:00+09:00
categories: ["cpp"]
tags: [cpp, perfect forwarding, 중괄호 초기치, null, static const, constexpr, overloading, 비트필드]
url: "/cpp/C++-perfect-forwarding-의-실패/"
description: "C++ perfect forwarding이 실패하는 5가지 경우를 정리합니다. 중괄호 초기치, null 포인터 0, 정수 static const/constexpr, 오버로딩된 함수, 비트필드 상황을 다룹니다."
author: "mumbi"
draft: false
---

# perfect forwarding 의 실패
 - 중괄호 초기치
 - null 포인터를 뜻하는 0
 - 정의가 없이 선언만 된 정수 static const 및 constexpr 멤버 변수
 - 오버로딩된 함수 이름과 템플릿 함수 이름
 - 비트필드
