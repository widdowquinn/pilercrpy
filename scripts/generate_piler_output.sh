#!/usr/bin/env bash
#
# generate_piler_output.sh
#
# This script automates generation of PILER-CR output for
# the genome sequences under tests/fixtures/sequences.
# Output is placed in tests/fixtures/pilercr_output
#
# (c) University of Strathclyde 2021
# Author: Leighton Pritchard

FIXTUREDIR=tests/fixtures
SEQDIR=${FIXTUREDIR}/sequences
OUTDIR=${FIXTUREDIR}/pilercr_output

echo "Generating PILERCR test output."

mkdir -p ${OUTDIR}

for infile in ${SEQDIR}/*
do
  cmd="pilercr -in ${infile} -out ${OUTDIR}/`basename ${infile}`.pilercr"
  echo "Processing ${infile}"
  echo "CMD: ${cmd}"
  ${cmd}
done