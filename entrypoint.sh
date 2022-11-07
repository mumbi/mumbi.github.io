#!/bin/sh
bundle add webrick
bundle install
bundle exec jekyll serve --host 0.0.0.0