---
title: 원격 MMC(Microsoft Management Console) in WORKGROUP
categories: ops
tags: [원격, MMC, Microsoft Management Console, WORKGROUP]
---

# MMC(Microsoft Management Console)
 - MMC 는 윈도우즈 관리 도구이다.
 - 로컬 컴퓨터 뿐만 아니라 원격 컴퓨터도 관리할 수 있다.
 - 특히, GUI가 없는 서버 윈도우즈를 관리하기 좋다.
 
# WORKGROUP 관리자
 - Active Directory 서비스를 사용하지 않는다면, 같은 네트워크의 WORKGROUP 을 통해서 원격 접속이 가능하다.
 - 클라이언트의 윈도우즈 계정 및 비밀번호가 서버의 윈도우즈 계정 및 비밀번호가 같아야 한다.
 
# 방화벽
 - 관리 용도에 따른 방화벽을 각각 열어야 한다.
 - "네트워크 검색" 규칙을 열어야 한다.
 - 원격 방화벽 관리를 위한 방화벽부터 열면 다른 관리 방화벽은 쉽게 열 수 있다.
 - netsh advfirewall firewall set rule group="네트워크 검색" new enable=yes
 - netsh advfirewall firewall set rule group="Windows 방화벽 원격 관리" new enable=yes
 
# 디스크 관리
 - 디스크 관리는 서버 방화벽 뿐만 아니라 클라이언트 방화벽도 열어야 한다.
 - netsh advfirewall firewall set rule group="원격 볼륨 관리" new enable=yes
