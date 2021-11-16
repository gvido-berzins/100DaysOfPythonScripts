#!/bin/sh
# Usage: ./extract_links.sh INFILE OUTFILE

INFILE=$1
OUTFILE=$2
IFS=$'\n'

echo "ARGUMENTS supplied."
echo "INFILE: $INFILE"
echo "OUTFILE: $OUTFILE"
echo ""

if [[ -z $INFILE ]] | [[ -z $OUTFILE ]]; then
	echo "Usage: ./extract_links.sh INFILE OUTFILE"
	exit
fi

grep -Eo "(http|https)://[a-zA-Z0-9./?=_%:-]*" "$INFILE" | sort -u -o "$OUTFILE"

echo ""
OUTFILE_CONTENTS=`cat "$OUTFILE"`

if [[ -z $OUTFILE_CONTENTS ]]; then
	echo "No links extracted."
else
	echo "---> Extracted:"
	echo $OUTFILE_CONTENTS
fi
