#!/bin/sh

function usage(){
	echo "Usage: ./run.sh script.py smb.txt"
}

PROGRAM="$1"
PATH_FILE="$2"

[[ -z ${PROGRAM} ]] && { echo "No program specified."; usage; exit 1; }
[[ -z ${PATH_FILE} ]] && { echo "No path file specified."; usage; exit 1; }
[[ ! -f ${PROGRAM} ]] && { echo "No program found! Given: $PROGRAM."; usage; exit 1; }
[[ ! -f ${PATH_FILE} ]] && { echo "No path file found! Given: $PATH_FILE"; usage; exit 1; }

PYTHON="python3"
LOG_DIR="run_logs"
PATHS=`cat $PATH_FILE`
LOG_FILE="$LOG_DIR/log.txt"
FAIL_LOG_FILE="$LOG_DIR/fail.txt"
PASS_LOG_FILE="$LOG_DIR/success.txt"

[[ ! -d ${LOG_DIR} ]] && mkdir "$LOG_DIR"


function log() {
	local time=`date -u`
	echo "[$time] \"$1\" \"$2\"" >> $3
}

function handle_execution() {
	local STATUS="FAIL"
	if [ $1 -ne 0 ]; then
		log "$2" $STATUS "$FAIL_LOG_FILE"
	else
		local STATUS="PASS"
		log "$2" $STATUS "$PASS_LOG_FILE"
	fi
	log "$2" $STATUS "$LOG_FILE"
}

function run_porter() {
	local path="$1"
	echo "<<<" >> "$LOG_FILE"
	$PYTHON $PROGRAM a \"$path\" 1>> $LOG_FILE 2>> $FAIL_LOG_FILE
	echo ">>>" >> "$LOG_FILE"
	handle_execution $? $path
}

for path in $PATHS; do
	log "$path" Started "$LOG_FILE"
	run_porter $path
	log "$path" Done "$LOG_FILE"
done
