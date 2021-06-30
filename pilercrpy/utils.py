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
"""Provides utilities for working with PILER-CR output."""

from collections import Counter
from pathlib import Path
from typing import Dict, Optional, Set

import pandas as pd

from .parser import parse


def read_arraydir(dirpath: Path, filext: Optional[str] = None) -> Dict:
    """Return list of PilerArrays for all output in a directory.

    :param dirpath:  path to directory containing PILER-CR output
    :param filext:  if specified, only files with this extension are
                    processed

    Processes each PILER-CR output file in the passed directory,
    returning a dictionary keyed by filepath, with values that are
    a list of PilerArrays for that file.
    """
    if not dirpath.is_dir():
        raise ValueError("Path must be a directory")

    if filext is None:
        paths = [_ for _ in dirpath.iterdir() if _.is_file()]
    else:
        paths = [_ for _ in dirpath.iterdir() if _.is_file() and _.suffix == filext]

    output = {}
    for path in paths:
        with path.open("r") as ifh:
            output[path] = list(parse(ifh))

    return output


def build_arraydf(arraydict: Dict):
    """Return Pandas dataframe of unique spacer counts.

    :param arraydict:  dictionary of arrays keyed by Path, with values
                       a list of PilerArray objects. We expect this to
                       be output from read_arraydir()

    Constructs a Pandas dataframe where rows are genome files, and
    columns are unique spacer sequences. Each cell contains the count
    for that spacer in the corresponding genome.
    """
    # Build dictionary of all unique spacer sequences, with
    # empty list initial values
    unique_spacers: Set[str] = set()
    for arraylist in arraydict.values():
        for array in arraylist:
            unique_spacers = unique_spacers.union(array.unique_spacer_sequences)
    spacerdict: Dict = {_: [] for _ in unique_spacers}

    # Loop over each input (genome) key, and count occurrences for
    # each unique sequence, updating spacerdict.
    genomes = list(arraydict.keys())  # freeze key order
    for key in genomes:
        spacercounts: Counter = sum(
            [_.spacer_sequence_counts for _ in arraydict[key]], Counter()
        )

        # Add zeroes for all spacers
        for val in spacerdict.values():
            val.append(0)

        # Add counts for spacers we've seen in this genome
        for spacer, count in spacercounts.items():
            spacerdict[spacer][-1] = count

    # Build dataframe from spacerdict and genomes (frozen list)
    spacerdict["filename"] = [str(_.stem) for _ in genomes]
    dfm = pd.DataFrame(data=spacerdict)
    dfm = dfm.set_index("filename")

    return dfm


def read_unique_spacers_to_dfm(
    dirpath: Path, filext: Optional[str] = None
) -> pd.DataFrame:
    """Return Pandas df of unique spacer counts from directory of output.

    :param dirpath:  path to directory containing PILER-CR output
    :param filext:  if specified, only files with this extension are
                    processed

    Processes each PILER-CR output file in the passed directory,
    returning a dataframe with filenames as column labels, unique spacer
    sequences as rows, and cells containing the count of each spacer
    in the corresponding file.
    """
    arraydict = read_arraydir(dirpath, filext)
    dfm = build_arraydf(arraydict).T
    dfm.index = dfm.index.rename("spacer")
    dfm = dfm[sorted(dfm.columns)].sort_values("spacer", ascending=False)

    return dfm
