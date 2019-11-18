#!/bin/bash

a=(bare-cache-amsterdam.webp bare-cache-bangalore.webp bare-cache-dallas.webp bare-cache-frankfurt.webp bare-cache-london.webp bare-cache-miami.webp bare-cache-newyork.webp bare-cache-paris.webp bare-cache-san-francisco.webp bare-cache-seattle.webp bare-cache-singapore.webp bare-cache-sydney.webp bare-cache-tokyo.webp bare-cache-toronto.webp bare-dev-amsterdam.webp bare-dev-bangalore.webp bare-dev-dallas.webp bare-dev-frankfurt.webp bare-dev-london.webp bare-dev-miami.webp bare-dev-newyork.webp bare-dev-paris.webp bare-dev-san-francisco.webp bare-dev-seattle.webp bare-dev-singapore.webp bare-dev-sydney.webp bare-dev-tokyo.webp bare-dev-toronto.webp cf-cache-amsterdam.webp cf-cache-bangalore.webp cf-cache-dallas.webp cf-cache-frankfurt.webp cf-cache-london.webp cf-cache-miami.webp cf-cache-newyork.webp cf-cache-paris.webp cf-cache-san-francisco.webp cf-cache-seattle.webp cf-cache-singapore.webp cf-cache-sydney.webp cf-cache-tokyo.webp cf-cache-toronto.webp cf-dev-amsterdam.webp cf-dev-bangalore.webp cf-dev-dallas.webp cf-dev-frankfurt.webp cf-dev-london.webp cf-dev-miami.webp cf-dev-newyork.webp cf-dev-paris.webp cf-dev-san-francisco.webp cf-dev-seattle.webp cf-dev-singapore.webp cf-dev-sydney.webp cf-dev-tokyo.webp cf-dev-toronto.webp)

for t in ${a[@]}
do 
	curl https://snorl.ax/img/20190610-cf-vs-bare/${t}
done
