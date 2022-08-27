FROM ruby:alpine3.16

WORKDIR /blog
EXPOSE 80

RUN apk add --update \
  build-base \
  libxml2-dev \
  libxslt-dev && \
  rm -rf /var/cache/apk/* && \
  gem install bundler

COPY . /blog

ENTRYPOINT ["/blog/entrypoint.sh"]