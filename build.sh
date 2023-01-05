#!/bin/bash

CFILE=wapp_links_database_flask

# cd ..
# rm -f ./$CFILE.database.db
# pyinstaller $CFILE/__main__.spec
# $CFILE/dist/__main__  --bind 0.0.0.0:5021

# rm -f ./$CFILE.database.db
# pyinstaller __main__.spec
# dist/__main__  --bind 0.0.0.0:5021

if [ "$1" == "" ]; then
    pyinstaller -F --path "." --add-data "templates:templates" --add-data "static:static" --hidden-import "main" --hidden-import "baselib" --hidden-import "database" --hidden-import "request_vars" __main__.py
    cp dist/__main__ ../$CFILE
    cd ..
    $CFILE  --bind 0.0.0.0:5021
elif [ "$1" == "zipapp" ]; then
    cd ..
    python3 -m zipapp $CFILE -p "/usr/bin/env python3"
    rm ./$CFILE.database.db
    echo $PWD/$CFILE.pyz
    ./$CFILE.pyz --bind 0.0.0.0:5021
fi

# python3 -m zipapp $CFILE -p "/usr/bin/env python3"
# echo $PWD/$CFILE.pyz

#./$CFILE.pyz --bind 0.0.0.0:5021
