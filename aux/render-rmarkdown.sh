#!/bin/sh

die()
{
    b=$(basename "$0")
    echo "$b: error: $*" >&2
    exit 1
}

if test "$#" -lt 2 ; then
    echo "usage: $0 TEMPLATE.Rmd  DATA.RCC  [DISPLAY_FILENAME]" >&2
    exit 1
fi

RMD_FILE="$1"
FILENAME="$2"
DISPLAY_FILENAME="$3"

set -u

test -n "$RMD_FILE" || die "missing RMD template filename"
test -e "$RMD_FILE" || die "Rmarkdown template '$RMD_FILE' not found"
test -n "$FILENAME" || die "missing RCC data file to process"
test -e "$FILENAME" || die "file '$FILENAME' not found"

expr "$FILENAME" : '^[-_a-zA-Z0-9/.]*$' > /dev/null \
     || die "file name '$FILENAME' contains forbidden characters"

if test -z "$DISPLAY_FILENAME" ; then
    DISPLAY_FILENAME=$(basename "$FILENAME")
fi

OUTPUT="$FILENAME.html"

unset DISPLAY
RSCRIPT="
rmarkdown::render('$RMD_FILE',
                  output_file='$OUTPUT',
                  params=list(
                     filename='$FILENAME',
                     display_filename='$DISPLAY_FILENAME'))
"
echo "$RSCRIPT" | R --vanilla
