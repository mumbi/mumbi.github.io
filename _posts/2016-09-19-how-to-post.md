---
layout: post
title: 어떻게 Jacman  사용하는 방법
tags:
- Jekyll
- Jacman
categories: Jekyll
description: Jacman은, 평면 인 지킬 테마 반응 형 디자인을 보유하고 있습니다. 공식 사이트는 Jacman 테마를 사용합니다. Hexo 테마에서 수정 Jacman 기반 Jacman. 당신은 더 많은 결과이 주제에 사이트 및 데모 미리보기를 방문 할 수 있습니다. 당신은 GitHub의 출판 문제에 오신 것을 환영합니다 질문이나 의견이있는 경우.
---

## 주제 소개
지킬-Jacman은 [지킬] (http://jekyllrb.com)가 신선하고 응답 테마를 설계했다, 풍부한 기능 지원 및 국내 서비스를 많이하고있다. Jacman는 [Jacman (https://github.com/wuchong/jacman)에서 이식하기 시작했다.

<! - 더 ->
## 구성 안내서

Jacman 항목은 구성 등록 정보의 풍부한을 제공합니다, 당신은 주제의 자신의 정의를 얻을 수 있습니다. 테마의 루트 디렉토리에있는`_config.yml` 구성 파일입니다. 당신이 Jacman 전에 사용하는 경우 주요 조정에 대한 구성 파일이 업데이트는 또한 다음과 같은 지침에 따라 수정 될 필요합니다.

```
##### 메뉴
메뉴 :
  홈 /
  아카이브 : / 아카이브
  소개 : / 약

#### 컨트롤
위젯 :
- 카테고리
- 태그
- 링크
- RSS

#### RSS
RSS : /atom.xml

#### 사진
imglogo :
  사용 : 사실 ## 웹 사이트 로고를 표시할지 여부를
  SRC : IMG / logo.png
파비콘 : IMG / favicon.ico의 ## 파비콘
apple_icon : IMG / jacman.jpg ## 기기에서 애플 아이콘이 아닌 투명 배경을
author_img : 아바타 사이트의 블로거의 하단에있는 IMG / author.jpg ##
banner_img : IMG / banner.jpg 이미지는 위에 사진을 블로그 ##

close_aside : 거짓 ## 자동으로 기사 페이지에서 사이드 바의 전원을 꺼 여부

#### 홈 관련
인덱스 :
  확장 : 확장 진정한 ## 홈 기사할지 여부를 지정합니다. 기본값은 확장 디스플레이가 더 읽기된다.
  excerpt_link : 자세히보기

#### 저자 정보
저자 :
  이름 : ## 작성자 이름
  intro_line1 : 사이트의 개인 소개의 하단에 ## ". 안녕하세요, 구글의 래리 페이지 해요"
  intro_line2 : "이것은 내 블로그는 믿거 나 말거나입니다."
  weibo_verifier : ## 마이크로 블로깅 쇼 인증 코드
  tsina : 쇼와 마이크로 블로깅 마이크로 블로깅 공유에 대한 ##
  웨이 보 : ## 사이트의 바닥을 표시하는 소셜 버튼, 아래 같은
  douban :
  zhihu :
  이메일 :
  트위터 :
  GitHub의 :
  페이스 북 :
  링크드 인 :
  GOOGLE_PLUS :
  유래 :


#### 카탈로그
TOC :
  기사 : 사실 ##이 문서 디렉토리에 표시됩니다
  옆으로 : 사실 ## 사이드 바에서 디렉토리를 표시할지 여부를

#### 링크
링크 :
  코드 농업 원 : https://coderq.com, 차세대 커뮤니티의 교환 및 공유를위한 프로그래머
  Jark의 블로그 : http://wuchong.me
  
#### 리뷰
duoshuo_shortname :
disqus_shortname :

#### 공유 버튼
jiathis :
  사용 : 잘못된 ##의 기본 테마 내장 공유
  ID :
  tsina :
  
사이트 통계를 ####
google_analytics :
  사용 : 거짓
  ID : 분석 ID 구글 ##.
  사이트 : ## 웹 사이트 주소.
baidu_tongji :
  사용 : 거짓
  Sitecode를 : ## 바이두 통계 서명 사이트
cnzz_tongji :
  사용 : 거짓
  siteid : ## CNZZ 통계 사이트 ID

#### 기타
ShowCustomFont : 사실
fancybox : 사실
totop : 사실

#### 맞춤 검색
google_cse :
  사용 : 거짓
  CX :
baidu_search :
  사용 : 거짓
  ID :
  사이트 : http://zhannei.baidu.com/cse/search
tinysou_search : ## http://tinysou.com/
  사용 : 거짓
  ID : "4ac092ad8d749fdc6293"
```

### 등록 기능
- 메뉴 메뉴 ** **
당신은`source` 블로그 디렉토리 폴더에 파일을 사용하도록 설정해야하는 경우 기본`/ tags` and` / categories` 페이지에서 사용할 수 없습니다, categories` 각 폴더는 각각 A` 인덱스가 포함 폴더 사용`tags`을 established`되고, .md` 파일입니다. 내용 :

```
레이아웃 : 태그 (또는 카테고리)
제목 : 태그 (또는 카테고리)
---
```


& NBSP; & NBSP; & NBSP; & NBSP; & NBSP; & NBSP; 항목이 두 페이지에 템플릿을 구축하고, 그래서 그들은 제대로 구문 분석 할 수 있기 때문에.

- ** ** 위젯을 제어
가제트의 일곱 종류를 제공. 라벨, 정렬, RSS, 링크, 마이크로 블로깅 쇼를 포함합니다.

 ** ** 링크 : 링크 URL이`links` 속성을 추가합니다.
 
 ** ** 마이크로 블로깅 쇼 : 당신이 마이크로 블로깅 쇼를 사용하려는 경우, 당신은`author` attributes` tsina`와`weibo_verifier`의 값을 입력해야합니다, 그 주, 전 당신을 당신의 트위터 ID입니다 마이크로 블로깅 쇼 코드, 위치에서 다음 그림 http://app.weibo.com/tool​​/weiboshow를 방문, 당신은 같은 당신의 검증을받을 수 있습니다 : 나는 b3593ceb``이었다.
! [] (Http://ww1.sinaimg.cn/large/81b78497jw1emegd6b0ytj209204pweu.jpg)

 당신이 기사를 해제하려면 'TRUE'to` 설정 close_aside`, 자동으로 블로그 페이지의 사이드 바를 꺼집니다.

- 사진 이미지 ** **
이 항목은 사이트 아이콘 (`favicon`), 웹 사이트 로고 (`imglogo`), 저자의 아바타 (`author_img`)와 같은 웹 사이트에 관련 이미지를 설정할 수 있습니다. 우리는`.svg`` .png` 형식의 웹 사이트 로고, 형식이나 제안을 가능하게하는 것이 좋습니다. 동시에 그지지 Apple 디바이스에 파비콘`apple_icon` (투명하지 배경)을 제공하는 것이 제안.

- 디스플레이 모드 지수 ** ** 홈
홈 현재 하나 식의 원래 카드 ([데모] (http://wuchong.me/jacman) 미리보기로 이동)이며, 두 개의 디스플레이 모드를 지원, 다른 하나는 확장 ([사이트 문서의 공식 테마와 유사하다 (http://wuchong.me)이 사용된다). 모두 독자들에게 후자의 문서 내용이 더 매력적으로, 전 집 부하 빠르고, 장점과 단점이있다. FALSE ': 확장은 첫 번째 카드 유형에 대한 개방의 기본 테마를 사용 후,의 속성 index`은`expand`을 설정합니다.

 이 카드는 요약되는 140 단어의 차단 전에 문서의 기사 내용의 요약은`자신의 description`과의 the` 전면 matter`의 시작 부분입니다. 페이지를 확장하여 사용하는 것입니다`<! - 더 -> '차단.

- 저자 정보 저자 ** **
완료에 정보에, 우리는 것이 좋습니다. 어디에서 '사용자 이름이나 트위터 홈페이지 주소에서 다른 사용자의 웨이 보 ID를 tsina`. 이 속성을 사용, 다른 사용자는 동안 자동으로 마이크로 블로깅에 당신의 기사를 공유 할 수 있습니다! 당신을. 동시에 그것은 '블로깅 쇼를 생성하기 위해 함께 작용 weibo_verifier`. `Intro_line1`는 and` intro_line2` 프레젠테이션의 하단에 개인 웹 사이트입니다. `Weibo`는`twitter`는`등 facebook` 사이트의 사회적 버튼의 오른쪽 아래 모서리를 표시하는 데 사용됩니다 아래 그림과 같이.
! [] (Http://ww4.sinaimg.cn/large/81b78497jw1emgscr3575j2078050jrc.jpg)

- ** 목차 목차 **
의 여부를 문서 또는 디렉토리 기능 사이드 바 사용. 모두 TRUE ''로하거나 FALSE 'are` 수 있습니다. 특정 디렉토리를 해제 할 경우에도, 당신이 파일을 수있는 문서의 시작 부분에 기사를 특징으로`전면 matter` TOC in` 줄을 추가 : FALSE '를.

- 댓글 댓글 ** **
채우기`duoshuo_shortname` [말] (http://duoshuo.com/) 사용자 이름, 시스템을 주석 활성화 말한다. 더 나은 코멘트 시스템과 중국 본토에서.

 채우기`disqus_shortname` [Disqus에 (http://disqus.com/) 사용자 이름, Disqus에 코멘트 시스템을 가능하게한다. 주석 달기 시스템의 넓은 국제 사용. `the` disqus_shortname`의 루트 디렉토리에 _config.yml` 블로그 설정 파일은 함수를 열 수있다.

- 공유 jiathis ** ** 심사
[상영] (http://www.jiathis.com/) 공유 시스템. 테마가 기본 공유를 구축하고 있기 때문에, 기본적으로 해제되어 있습니다.

- 사이트 통계 분석 ** **
`Google_analytics` : Google 웹 로그 분석 추적 코드. 참고 : Google 웹 로그 분석이 범용 웹 로그 분석으로 업그레이드되었습니다. 다음 [여기를 클릭]하십시오 자세한 내용은 사용이 가능한 Google 웹 로그 분석 추적 코드 (https://developers.google.com/analytics/devguides/collection/upgrade/?hl=zh_CN) 이해의 버전을 업그레이드로 돌아가주십시오.

 `Baidu_tongji` : 바이두 통계. 사이트에서, 패턴`sitecode`을 작성해야 [공식 웹 사이트 (http://tongji.baidu.com/web/welcome/login) 서명을 얻기 위해 등록하고 사이트를 구성합니다. "사이트 센터"에 서명 ->보기`다음 그림과 같이 e6d1f421bbc9962127a50488f9ed37d1` "코드 받기"는 note`의 3F`의 전면을 제거합니다.
! [] (Http://ww4.sinaimg.cn/large/81b78497jw1emf4v6qf91j20kf07sq8v.jpg)

 `Cnzz_tongji` : 마스터 통계. 사이트 ID`siteid`, [역 집행 네트워크]에 공감을 입력 할 필요가 후 (http://www.cnzz.com)를 등록하고 얻을 수있는 사이트를 구성합니다.

- 수학 공식이 mathjax ** **
테마 지원 LATEX은 수학 공식을 작성합니다. 만에있는 문서 파일`전면 matter`의 시작 부분에서, line`의 mathjax를 추가 : TRUE '는 LATEX은 텍스트의 수식을 작성.

- 사진 브라우저 fancybox ** **
정기적으로 기사 갤러리 유형을 게시하는 경우 기본적으로 꺼짐, 다음 TRUE ''로 설정합니다.

- ** 최고 totop **
``돌아 가기 상단으로 오른쪽 하단 버튼은 기본적으로 활성화되어 있습니다.

- 사용자 정의 검색 검색 ** **
`Baidu_search` 다음 바이두 내에서 사용하도록 설정 한 경우 [바이두 검색 스테이션] 서명 역의 필요를 검색 (http://zn.baidu.com/), 귀하의 사이트를 구성하고 검색 열린 검색 사이트 ID를 얻을, 추가 속성은 site`을 fill` 수 있습니다 또한 CNAME 자신의 두 번째 레벨 도메인을 기입 할 수있는 기본 값이,보다 상세하게 읽을 수 [블로그] (http://gengbiao.me/hexo/hexo%E6%B7%BB%E5%8A%A0% E7 %의 99 % BE %의 E5 %의 BA %의 A6 %의 E7 % AB % 99 % E5의 % 86 % 85 % E6 % 90 % 9C % E7 %의의 B4의 %의 A2 /) 이해.

 `Google_cse` : 사용 Google 맞춤 검색 [구글 CSE (https://www.google.com/cse/)에 서명해야하는 경우, 귀하의 사이트를 구성하고이 사용자 정의 검색 ID를 얻을. 또한 폴더에`search` file` source` 파일 블로그 디렉토리 폴더를 생성해야하고 파일은`index.md`이 포함되어 있습니다. 내용 :
 ```
 레이아웃 : 검색
 제목 : 검색
 ---
 ```

 `Tiny_search`가 : 당신이 설정하려는 경우 [마이크로 검색 (http://tinysou.com/), 당신은 구성 fi​​le` id` 수에서 엔진을, 계정을 등록 구성 키 필의 엔진이 필요합니다.


## 자주 묻는 질문 (FAQ)
- ** Q : 사진을 만들 수있는 센터를 설정하는 방법을 기본 사진이 집에 남아? **
> 사용`<IMG SRC = ""스타일 = "디스플레이 : 블록; 마진 : 자동"는 />`HTML 태그입니다.

- ** Q : 어떻게 이미지 제품 (갤러리 포스트)를 구축하는 방법? **
>은 마크 다운 파일을 다음과 같이 수정 '전면 matter` 만들기를 직접 제공 한 테마 스타일 이미지의 기사를 볼 수 있습니다.
```
---
레이아웃 : 사진
제목 : 갤러리 포스트
사진 :
- Http://i.minus.com/ibobbTlfxZgITW.jpg
- Http://i.minus.com/iedpg90Y0exFS.jpg
---
```

- ** Q :이 항목의 값을 설정하는 구성 파일에,하지만 왜 항상 효과 아를 참조하십시오? **
> '공간을 남겨 두어야 각각의 속성 값 파일의 _config.yml` 전면, 열려있는 모든 공간 모드에서 라임 / 메모장 ++ 표시하는 것이 좋습니다. 각 기사`전면 matter`의 또 다른도이 문제에 관심을 지불합니다.

- ** Q : 어떻게 의견과 제안? **
토론에 참여, 권고를하기> 주제는 여전히 진화, 환영 [공개 문제] (https://github.com/Simpleyyt/jekyll-jacman/issues).

- ** Q : 수정 이유는 무엇 구성 파일이 / 출판 보웬이 그것을 구문 분석하지만 왜곡인가? **
>`UTF-8` 형식으로 구성 파일 / 인하 파일을 저장하십시오.

- ** Q : 열려있는 마이크로 블로깅 쇼 표시가 비어있는 이유는, 내용이없는 노출? **
>이 매개 변수를 수정할 때마다 몇 번을 새로 고치거나 잘 서버에 업로드해야합니다.
