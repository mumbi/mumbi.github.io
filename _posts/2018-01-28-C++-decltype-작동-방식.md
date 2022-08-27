---
title: C++ decltype 작동 방식
categories: dev
tags: [c++, decltype, auto]
---

# decltype 작동 방식
 - decltype 은 주어진 이름이나 표현식의 구체적인 타입을 알려준다.

```c++
widget w;
const widget& cw = w;

auto my_widget1 = cw;		// my_widget1의 타입은 widget
decltype(auto) my_widget2 = cw;	// my_widget2의 타입은 const widget&
```

 - decltype을 이름에 적용하면 그 이름에 대해 선언된 타입은 대체로 lvalue 타입이다. 그런데 이름보다 복잡한 lvalue 표현식은 항상 lvalue 타입의 참조로 추론한다. 
 
```c++
decltype(auto) f1()
{
 	int x = 0;
	return x;	// decltype(x) 는 int 이므로 f1은 int 를 반환
}
 
decltype(auto) f2()
{
 	int x - 0;
	return (x);	// decltype((x)) 는 int& 이므로 f2는 int& 를 반환
}
```

 - 지역변수의 참조를 반환하는 것은 아주 위험한 일이므로 decltype(auto)를 아주 조심해서 사용해야 한다.
