#!/usr/bin/env bash

${BOOKS_PATH:-./build/books}

for bookPath in $BOOKS_PATH/*; do
  book=$(basename $bookPath);
  for pagePath in $BOOKS_PATH/$book/pages/*; do
    page=$(basename $pagePath);
    echo "$pagePath";
    errors=$(html-validator  --validator='http://localhost:8888' --verbose --file=$pagePath  | grep 'Unclosed element' | sort | uniq);
    if [ ! -z "$errors" ]; then
      echo "$book / $page" >> errors.txt;
      echo "$errors" >> errors.txt;
    fi;
  done;
done
