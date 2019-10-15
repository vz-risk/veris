#!/bin/bash
bld=`cut -d ':' -f2 assets/meta.json` && newbld=`expr "${bld::-1}" + 1` && sed -i "s/$bld/$newbld}/g" assets/meta.json