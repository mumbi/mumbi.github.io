---
title: alpine 리눅스에서 jekyll 실행 시 sass-embedded-1.57.1 에러
categories: jekyll
tags: ["alpine", "jekyll", "sass-embedded"]
---

# 개요

블로그 오타를 수정하기 위해 한 달여 만에 로컬에서 `jekyll` 을 실행해 보았습니다.

실행을 위해 종속성들을 설치하는 과정에서 에러가 발생하였는데 이 에러에 대해 살펴보겠습니다.

# 원인

에러 메시지를 보니 아래와 같았습니다.

```bash
Gem::Ext::BuildError: ERROR: Failed to build gem native extension.

    current directory: /usr/local/bundle/gems/sass-embedded-1.57.1/ext/sass
/usr/local/bin/ruby -I/usr/local/lib/ruby/3.1.0 -rrubygems
/usr/local/lib/ruby/gems/3.1.0/gems/rake-13.0.6/exe/rake
RUBYARCHDIR\=/usr/local/bundle/extensions/x86_64-linux-musl/3.1.0/sass-embedded-1.57.1
RUBYLIBDIR\=/usr/local/bundle/extensions/x86_64-linux-musl/3.1.0/sass-embedded-1.57.1
rake aborted!
NotImplementedError: sass_embedded for x86_64-linux-musl not available at
https://github.com/sass/dart-sass-embedded/releases/tag/1.57.1
/usr/local/bundle/gems/sass-embedded-1.57.1/ext/sass/Rakefile:226:in
`default_sass_embedded'
/usr/local/bundle/gems/sass-embedded-1.57.1/ext/sass/Rakefile:21:in `block (2
levels) in <top (required)>'
/usr/local/bundle/gems/sass-embedded-1.57.1/ext/sass/Rakefile:21:in `fetch'
/usr/local/bundle/gems/sass-embedded-1.57.1/ext/sass/Rakefile:21:in `block in
<top (required)>'
Tasks: TOP => default => install => embedded.rb => sass_embedded
(See full trace by running task with --trace)

rake failed, exit code 1

Gem files will remain installed in /usr/local/bundle/gems/sass-embedded-1.57.1
for inspection.
Results logged to
/usr/local/bundle/extensions/x86_64-linux-musl/3.1.0/sass-embedded-1.57.1/gem_make.out

  /usr/local/lib/ruby/3.1.0/rubygems/ext/builder.rb:95:in `run'
  /usr/local/lib/ruby/3.1.0/rubygems/ext/rake_builder.rb:28:in `build'
  /usr/local/lib/ruby/3.1.0/rubygems/ext/builder.rb:161:in `build_extension'
/usr/local/lib/ruby/3.1.0/rubygems/ext/builder.rb:195:in `block in
build_extensions'
  /usr/local/lib/ruby/3.1.0/rubygems/ext/builder.rb:192:in `each'
  /usr/local/lib/ruby/3.1.0/rubygems/ext/builder.rb:192:in `build_extensions'
  /usr/local/lib/ruby/3.1.0/rubygems/installer.rb:853:in `build_extensions'
/usr/local/bundle/gems/bundler-2.3.25/lib/bundler/rubygems_gem_installer.rb:72:in
`build_extensions'
/usr/local/bundle/gems/bundler-2.3.25/lib/bundler/rubygems_gem_installer.rb:28:in
`install'
/usr/local/bundle/gems/bundler-2.3.25/lib/bundler/source/rubygems.rb:207:in
`install'
/usr/local/bundle/gems/bundler-2.3.25/lib/bundler/installer/gem_installer.rb:54:in
`install'
/usr/local/bundle/gems/bundler-2.3.25/lib/bundler/installer/gem_installer.rb:16:in
`install_from_spec'
/usr/local/bundle/gems/bundler-2.3.25/lib/bundler/installer/parallel_installer.rb:186:in
`do_install'
/usr/local/bundle/gems/bundler-2.3.25/lib/bundler/installer/parallel_installer.rb:177:in
`block in worker_pool'
  /usr/local/bundle/gems/bundler-2.3.25/lib/bundler/worker.rb:62:in `apply_func'
/usr/local/bundle/gems/bundler-2.3.25/lib/bundler/worker.rb:57:in `block in
process_queue'
  /usr/local/bundle/gems/bundler-2.3.25/lib/bundler/worker.rb:54:in `loop'
/usr/local/bundle/gems/bundler-2.3.25/lib/bundler/worker.rb:54:in
`process_queue'
/usr/local/bundle/gems/bundler-2.3.25/lib/bundler/worker.rb:91:in `block (2
levels) in create_threads'

An error occurred while installing sass-embedded (1.57.1), and Bundler cannot
continue.

In Gemfile:
  minimal-mistakes-jekyll was resolved to 4.24.0, which depends on
    jekyll-feed was resolved to 0.17.0, which depends on
      jekyll was resolved to 4.3.1, which depends on
        jekyll-sass-converter was resolved to 3.0.0, which depends on
          sass-embedded
```

```bash
NotImplementedError: sass_embedded for x86_64-linux-musl not available at
https://github.com/sass/dart-sass-embedded/releases/tag/1.57.1
```

이 메시지를 보니 뭔가 구현이 되지 않아서 사용할 수 없다는 내용인 것 같습니다.

응? 바꾼게 없는데 왜 갑자기 안되는 걸까요? 

저는 `jekyll` 빌드를 `docker build` 로 구성해 놓았는데 중간 이미지(jekyll 빌드에 필요한 종속성들을 설치한 이미지) 만들지 않고, `ruby:alpine3.16` 로부터 매번 새로 빌드하고 있었습니다.

그런데 `ruby` 종속성 라이브러리들 명시해 놓은 `Gemfile` 을 보니 구체적인 버전이 명시되어 있지 않네요.

```ruby
gem "jekyll"
```

그러니까 jekyll 에서 사용하는 모든 종속성들을 설치할텐데 최신 버전으로 설치가 되고 있었습니다. 

그 최신 버전 라이브러리 중 `sass-embedded (1.57.1)` 이 호환이 안되었던 것으로 보입니다.

# 해결 방안

호환되는 버전을 구글링해서 찾아보니 `jekyll-sass-converter` 의 최신 버전에서 위 라이브러리를 사용하고 있는 것으로 보입니다. 

그래서 `Gemfile` 에 `jekyll-sass-converter` 의 버전을 이전 버전으로 명시해주어 위 라이브러리를 사용하지 않게 하여 해결할 수 있습니다.

```ruby
gem "jekyll-sass-converter", "~> 2.0"
```

# 마무리

`jekyll`, `ruby` 뿐만 아니라 종속성을 관리해주는 솔루션(package manager)을 사용할 때는 종속성 버전 관리에 유의해야 할 것 같습니다.

감사합니다.
