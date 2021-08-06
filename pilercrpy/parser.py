# -*- coding: utf-8 -*-
# (c) University of Strathclyde 2021
# Author: Leighton Pritchard
#
# Contact: leighton.pritchard@strath.ac.uk
#
# Leighton Pritchard,
# Strathclyde Institute for Pharmacy and Biomedical Sciences,
# Cathedral Street,
# Glasgow,
# G4 0RE
# Scotland,
# UK
#
# The MIT License
#
# Copyright (c) 2021 University of Strathclyde
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""Describes a parser for PILER-CR array output data."""

import re

from enum import Enum
from typing import TextIO

from .piler import PilerArray

__version__ = "v0.1a"

HEADER_PATTERN = re.compile("Array [0-9]*$")


class ParserState(Enum):

    """Current parser state."""

    HEADER = 1
    SPACERS = 2
    CONSENSUS = 3
    NORECORD = 0


def parse(handle: TextIO):
    """Iterate over handle and return PilerArray objects.

    :param handle:  input file handle
    """
    # Zip forward in file to the DETAIL REPORT, skipping header info
    while True:
        line = handle.readline()
        if line.strip() == "DETAIL REPORT":
            break

    # Start with no array
    array = None  # current CRISPR array
    state = ParserState.NORECORD  # parser state

    # Read each array
    while True:
        # Instantiate next array
        # Each array report starts with the line "Array <N>" where
        # <N> is the number of the array in the file.
        # print(line)
        # print(state)
        if re.match(HEADER_PATTERN, line):  # New CRISPR array
            state = ParserState.HEADER
            if array is not None:  # Report the last array
                yield array
            arraynum = int(line.strip().split()[-1])
            array = PilerArray(arraynum)  # instantiate array
            # print(line, state, len(array))
        elif line.startswith(">"):  # sequence header
            array.seqname = line.strip()[1:]  # type:ignore
        elif line.strip().startswith("="):  # section divider
            if state == ParserState.HEADER:
                state = ParserState.SPACERS
            elif state == ParserState.SPACERS:
                state = ParserState.CONSENSUS
            # print(state)
        elif state == ParserState.SPACERS:
            data = line.strip().split()
            if len(data) == 7:
                array.add_spacer(  # type: ignore
                    int(data[0]),
                    int(data[1]),
                    float(data[2]),
                    int(data[3]),
                    data[4],
                    data[5],
                    data[6],
                )
            else:  # last spacer
                if len(data) < 6:
                    data.append("")
                array.add_spacer(  # type: ignore
                    int(data[0]),
                    int(data[1]),
                    float(data[2]),
                    0,
                    data[3],
                    data[4],
                    data[5],
                )
        elif state == ParserState.CONSENSUS and line.strip():
            data = line.strip().split()
            array.repeat_len = int(data[1])  # type: ignore
            array.spacer_len = int(data[2])  # type: ignore
            array.consensus = data[-1]  # type: ignore
            state = ParserState.NORECORD

        try:
            line = next(handle)
        except StopIteration:
            break

    if array:
        yield array


def read(handle):
    """Parse PILER-CR output into a single PilerArray object.

    :param handle:  filehandle with PILER-CR output

    This is for when there is one and only one target array. We
    usually don't know if this is the case ahead of time, and it
    is provided for completeness only. We expect that parse()
    will be the usual way a user interacts with the file.

    PILER-CR output with more than one array should raise an error.
    """
    iterator = parse(handle)
    try:
        array = next(iterator)
    except StopIteration:
        raise ValueError("No array found in handle") from None
    try:
        next(iterator)
        raise ValueError("More than one array found in handle")
    except StopIteration:
        pass
    return array
