# chicago-lead

how much lead is pouring out of chicago's fixtures?

## requirements

* postgres ([instructions](http://exponential.io/blog/2015/02/21/install-postgresql-on-mac-os-x-via-brew/))
* ogr2ogr (`brew install gdal`) 
* csvkit (`pip install csvkit`)
* pandas (`pip install pandas`)

## to reproduce

clone this repo and from a terminal window, run:

`make all`

the files should land in `output/`.

## data docs

* [parks](documentation/parks-README.md)
* [schools](documentation/schools-README.md)
* water projects