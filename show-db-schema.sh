#!/bin/sh

echo ".schema" | sqlite3 -noheader -batch bhot.db
