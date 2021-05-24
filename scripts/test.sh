#!/usr/bin/env bash

cd $(dirname $0) && cd ..

TEST_RESOURCES_DIR="tests/resources/"
for DIC_TYPE in {system,user,user2}; do
  IN="${TEST_RESOURCES_DIR}${DIC_TYPE}.csv"
  OUT="${TEST_RESOURCES_DIR}${DIC_TYPE}.dic"
  DES="the ${DIC_TYPE} dictionary for the unit tests"
  python -c "import sys; from chikkarpy.command_line import build_dictionary; build_dictionary(sys.argv[1], sys.argv[2], sys.argv[3]);" "${IN}" "${OUT}" "${DES}"
done

python -m unittest discover tests -p '*test*.py'
