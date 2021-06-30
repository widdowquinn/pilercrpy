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
"""Describes a class representing PILER-CR array output data."""

from collections import Counter
from typing import List


class PilerSpacer:

    """Represents a CRISPR spacer predicted by PILER-CR."""

    def __init__(
        self,
        position: int,
        repeat_len: int,
        identity: float,
        spacer_len: int,
        left_flank: str,
        repeat: str,
        spacer: str,
    ):
        """Instantiate a spacer representaiton."""
        self.position = position
        self.repeat_len = repeat_len
        self.identity = identity
        self.spacer_len = spacer_len
        self.left_flank = left_flank
        self.repeat = repeat
        self.spacer = spacer

    def __len__(self):
        """Return combined length of repeat sequence and spacer."""
        return len(self.repeat) + len(self.spacer)

    def __str__(self):
        """Return string representation of PILER-CR predicted spacer."""
        outstr = [
            f"{self.position}",
            f"{self.repeat_len}",
            f"{self.identity}",
            f"{self.spacer_len}",
            f"{self.left_flank}",
            f"{self.repeat}",
            f"{self.spacer}",
        ]
        return "\t".join(outstr)


class PilerArray:

    """Represents a single Array result given by PilerCR."""

    def __init__(self, arraynum: int, seqname: str = "") -> None:
        """Instantiate array.

        :param arraynum:  ID number of array assigned by PILER-CR
        """
        self.arraynum = arraynum
        self.seqname = seqname
        self.spacers: List[PilerSpacer] = []
        self.consensus: str = ""
        self.comments: str = ""
        self.repeat_len: int = 0
        self.spacer_len: int = 0

    def add_spacer(
        self,
        position: int,
        repeat_len: int,
        identity: float,
        spacer_len: int,
        left_flank: str,
        repeat: str,
        spacer: str,
    ):
        """Add PilerSpacer to current array."""
        self.spacers.append(
            PilerSpacer(
                position, repeat_len, identity, spacer_len, left_flank, repeat, spacer
            )
        )

    def __len__(self):
        """Return sequence length of array."""
        return sum([len(_) for _ in self.spacers]) - len(self.spacers[-1].spacer)

    def __str__(self):
        """Return tring representation of PILER-CR array."""
        outstr = [f"PILER-CR Array {self.arraynum}"]
        outstr.append(f">{self.seqname}")
        outstr.extend([f"\t{str(_)}" for _ in self.spacers])
        outstr.append(
            (
                f"{len(self.spacers)} spacers: repeat length={self.num_repeats}"
                f", spacer length = {self.num_spacers}"
            )
        )
        return "\n".join(outstr)

    @property
    def seqname(self) -> str:
        """Return name of sequence to which array refers."""
        return self._seqname

    @seqname.setter
    def seqname(self, val: str) -> None:
        """Set sequence name for array.

        :param seqname: sequence to which array refers
        """
        if val:
            self._seqname = val
        else:
            self._seqname = f"Sequence for array {self.arraynum}"

    @property
    def copies(self):
        """Return number of spacers in array."""
        return len(self.spacers)

    @property
    def flank_sequences(self):
        """Return list of left flank sequences for spacers in the array."""
        return [_.left_flank for _ in self.spacers]

    @property
    def num_repeats(self):
        """Return number of spacers in array."""
        return len(self.repeats)

    @property
    def num_spacers(self):
        """Return number of spacers in array."""
        return len(self.spacers)

    @property
    def repeats(self):
        """Return repeats from each spacer."""
        return [_.repeat for _ in self.spacers]

    @property
    def spacer_sequences(self):
        """Return list of spacer sequences for the array."""
        return [_.spacer for _ in self.spacers]

    @property
    def spacer_sequence_counts(self):
        """Return counts of spacer sequences for the array."""
        return Counter(self.spacer_sequences)

    @property
    def start_position(self):
        """Return start position of array on source sequence."""
        return min([_.position for _ in self.spacers])

    @property
    def unique_spacer_sequences(self):
        """Return set of unique spacer sequences in array."""
        return set(self.spacer_sequences)
