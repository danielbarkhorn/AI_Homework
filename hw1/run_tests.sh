#!/bin/bash

MYNAME=`basename "$0"`

if [ "$#" -ne '1' ]
then
  echo "Usage: $MYNAME <test_directory>" 1>&2
  exit 1
fi

TEST_DIR="$1"
RESULTS_DIR="test_results"

die() {
  echo "$1" 1>&2
  exit 1
}

mkdir -p $RESULTS_DIR || die "Failed to create $RESULTS_DIR"

RESULT_PASS=0
RESULT_FAIL_TO_RUN=0
RESULT_FAIL_TO_COMPARE=0

verify_substr() {
  local truncated_name="$1"
  local orig_name="$2"
  local full_filename="$3"

  if [ -z "$truncated_name" ] || [ "$truncated_name" == "$orig_name" ]
  then
    echo "Filename '$full_filename' not in correct format!!!" 1>&2
    echo "  Use <search algo>-<test #>-<uname>.map" 1>&2
    echo "  For example: astar-12-jconner.map" 1>&2
    exit 1
  fi
}

LAST_SEARCH_NAME="NOTASEARCH"

for test_filename in `ls -1 $1 | grep '\.map$' | sort`
do
  str="$test_filename"
  full_filename="$TEST_DIR/$test_filename"

  # Extract algorithm name
  search_algo_name=`echo $str | sed -e 's/\([^-]*\)-.*/\1/'`
  verify_substr "$search_algo_name" "$str" "$test_filename"
  str=`echo $str | sed -e 's/[^-]*-\(.*\)/\1/'`

  # Extract test number
  test_num=`echo $str | sed -e 's/\([^-]*\)-.*/\1/'`
  verify_substr "$test_num" "$str" "$test_filename"
  str=`echo $str | sed -e 's/[^-]*-\(.*\)/\1/'`

  # Extract user-name
  user_name=`echo $str | sed -e 's/\([^.]*\)\.map$/\1/'`
  verify_substr "$user_name" "$str" "$test_filename"

  # Verify that an expected output file exists
  good_out_filename=`echo $test_filename | sed -e 's/\.map$/.out/'`
  if [ "$good_out_filename" == "$test_filename" ] || ! [ -f "$TEST_DIR/$good_out_filename" ]
  then
    die "Cannot find expected output file $good_out_filename for test $test_filename"
  fi
  good_out_filename="$TEST_DIR/$good_out_filename"
  cmd_filename="$TEST_DIR/`echo $test_filename | sed -e 's/.map$/.cmd/'`"
  if [ -f "$cmd_filename" ]
  then
    extra_cmds=`cat $cmd_filename`
  else
    extra_cmds=""
  fi

  # Only run tests for the implemented search algorithms
  if ! [ -f "${search_algo_name}.py" ]
  then
    continue
  fi

  if [ "$LAST_SEARCH_NAME" != "$search_algo_name" ]
  then
    echo
    echo "~~~~~ $search_algo_name ~~~~~"
    LAST_SEARCH_NAME="$search_algo_name"
  fi

  test_out_file="$RESULTS_DIR/${test_filename}.out"
  echo -n "$test_filename..."
  python main.py $extra_cmds "${search_algo_name}.py" "$full_filename" > $test_out_file 2>&1

  if [ "$?" -ne '0' ]
  then
    echo "FAILED TO RUN"
    RESULT_FAIL_TO_RUN=$((RESULT_FAIL_TO_RUN+1))
    continue
  fi

  if ! cmp -s "$test_out_file" "$good_out_filename"
  then
    echo "FAIL"
    RESULT_FAIL_TO_COMPARE=$((RESULT_FAIL_TO_COMPARE+1))
    continue
  fi

  echo "PASS"
  RESULT_PASS=$((RESULT_PASS+1))
done

echo
echo "SUMMARY"
echo "~~~~~~~"
echo "PASSES: $RESULT_PASS"
echo "FAILURES: $RESULT_FAIL_TO_COMPARE"
echo "FAILED TO RUN: $RESULT_FAIL_TO_RUN"
echo

