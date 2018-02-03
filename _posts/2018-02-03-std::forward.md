---
layout: post
title: std::forward
categories: dev
tags: [c++, std, forward]
---

# std::forward
 - std::forward는 모든 것을 전달하지는 않는다.
 - std::forward는 인수가 특정 조건을 만족할 때에 rvalue로 캐스팅한다.
 - 특정 조건은 rvalue 로 호출했을 때 다시 rvalue로 캐스팅한다. (rvalue로 호출했더라도 매개변수는 lvalue이다.)
 - 특정 조건인지 아닌지 여부는 참조 축약에 의해 이루어진다.
