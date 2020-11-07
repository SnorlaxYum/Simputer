#!/bin/bash

for FILE in $(find dist -type f -iname '*.css' -o -iname '*.js' -o -iname '*.svg' -o -iname '*.json' -o -iname '*.html' -o -iname '*.xml'); do
    echo -n "Compressing ${FILE}..."
    brotli -f ${FILE} -o ${FILE}.br;
    echo "done."
done