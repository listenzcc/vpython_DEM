#! /bin/sh

eio clip -o Rome-30m-DEM.tif --bounds 12.35 41.8 12.65 42

eio --product SRTM3 clip -o Rome-90m-DEM.tif --bounds 12.35 41.8 12.65 42

eio --product SRTM3 clip -o Shanghai-90m-DEM.tif --bounds 120.52 30.40 122.12 31.53
