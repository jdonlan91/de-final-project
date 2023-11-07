#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

mkdir -p temp/ingestor-utils/python

cp -R "$SCRIPT_DIR/../src/ingestor/utils" temp/ingestor-utils/python/ 
