#!/bin/sh
# Runs every DL program and saves its output to outputs/<name>.txt
cd "$(dirname "$0")"
PY=${PYTHON:-python3}
export TF_CPP_MIN_LOG_LEVEL=3
for p in cnn rnn lstm gan; do
  echo "== $p.py =="
  start=$(date +%s)
  $PY $p.py > outputs/$p.txt 2> outputs/$p.err.log
  echo "exit=$? time=$(( $(date +%s) - start ))s"
done
