---
layout: post
title: C++ constexpr
categories: dev
tags: c++ constexpr
---

# constexpr
 - 어떠한 값이 단지 상수일 뿐만 아니라 컴파일 시점에서 알려진다.
 - 배열 크기, 정수 템플릿 인수, 열거자 값, alignment 지정자를 지정하는 등의 여러 문맥에 쓸 수 있다.
 - 모든 constexpr 객체는 const 이지만 모든 const 객체가 constexpr 인 것은 아니다. 
 - 어떤 변수의 값을 반디스 컴파일 시점 상수를 요구하는 문맥에서 사용할 수 있어야 한다면 선택할 도구는 const 가 아니라 constexpr 이다.
 - constexpr 함수에 넘겨주는 인수가 컴파일 시점에 알려진다면 함수의 결과는 컴파일 도중에 계산된다.
 - 컴파일 시점에서 알려지지 않는 값들로 constexpr 함수를 호출하면 함수는 보통의 함수처럼 작동한다. 
 
```c++
// C++11 의 constexpr 함수의 제약 조건은 
// 실행 가능 문장의 개수가 0 ~ 1 개이다. 
// 요령 1. 삼항 연산자를 if - else 문 대신 사용한다.
// 요령 2. loop 대신 재귀를 사용한다.

constexpr int pow(int base, int exp) noexcept
{
	return (exp == 0 ? 1 : base * pow(base, exp - 1));
}
```

 - constexpr 함수는 반드시 리터럴 타입(void를 제외한 내장 타입)을을 받고 돌려주어야 한다.
 - 생성자와 멤버 함수들이 constexpr인 사용자 타입도 리터럴 타입이 될 수 있다.
 
```c++
class point
{
public:
	constexpr point(double x_value = 0, double y_value = 0) noexcept
		: x(x_value), y(y_value)
	{ }
	
	constexpr double x_value() const noexcept { return x; }
	constexpr double y_value() const noexcept { return y; }
	
	void set_x(double new_x) noexcept { x = new_x; }
	void set_y(double new_y) noexcept { y = new_y; }
private:
	double x, y;
};
```

 - class 의 생성자를 constexpr로 선언할 수 있는 이유는 주어진 인수들이 컴파일 시점에서 알려진다면 생성된 객체의 자료 멤버들의 값 역시 컴파일 시점에서 알려질 수 있기 때문이다. 
 
```c++
constexpr point p1(9.4, 27.7);	// ok, constexpr 생성자가 컴파일 시점에서 실행됨.

constexpr point p2(28.8, 5.3);	// ok. 
```

 - 컴파일 도중에 알려진 값으로 초기화된 constexpr 객체의 constexp 멤버 함수도 역시 constexpr 이다.
 - constexpr 멤버 함수들을 호출한 결과들고 또 다른 constexpr 객체를 초기화하는 constexpr 함수를 작성하는 것이 가능하다.
 
```c++
constexpr point midpoint(const point& p1, const point& p2) noexcept
{
	return { (p1.x_value() + p2.x_value()) / 2,
		(p1.y_value() + p2.y_value()) / 2 };
}

constexpr auto mid = midpoint(p1, p2);	// constexpr 함수의 결과를 이용해서 constexpr 객체를 초기화한다.
```

 - constexpr 이 객체나 함수의 인터페이스의 일부라는 점을 명심해야 한다. 
