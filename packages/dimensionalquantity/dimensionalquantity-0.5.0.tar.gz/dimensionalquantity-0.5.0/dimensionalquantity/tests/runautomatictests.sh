#!/bin/bash
ls -d ../*.py *.py | entr -d ./runcovtests.sh
