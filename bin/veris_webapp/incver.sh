#!/bin/bash
bld=`cut -d ':' -f2 veris-app/assets/meta.json` && newbld=`expr "${bld::-1}" + 1` && sed -i "s/$bld/$newbld}/g" veris-app/assets/meta.json