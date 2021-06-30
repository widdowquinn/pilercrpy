# `piler-crpy`

This repository contains a Python package for working with the `PILER-CR` CRISPR repeat finding software package.

- [`PILER-CR`](http://www.drive5.com/pilercr/)

It provides a parser to aid processing `PILER-CR` output files. We plan to add helper functions for running the prediction tool and processing its output.

---------------------------

## Installation

Download from this repository and install using the code below:

```bash
git clone
cd piler-crpy
python setup.py install
```

## Usage

### Read contents of a `PILER-CR` output file

- Read arrays into a list with `pilercrpy.parse()`

```python
>>> import pilercrpy
>>> with open("tests/fixtures/pilercr_output/2168.fasta.pilercr", "r") as ifh:
...     arrays = list(pilercrpy.parse(ifh))
... 
>>> arrays
[<pilercrpy.piler.PilerArray object at 0x7f8859362af0>, <pilercrpy.piler.PilerArray object at 0x7f885922bbb0>]
```

- Operate on all arrays in a file

```python
>>> import pilercrpy
>>> with open("tests/fixtures/pilercr_output/2168.fasta.pilercr", "r") as ifh:
...     for array in pilercrpy.parse(ifh):
...         # Do something with array
... 
```

### Explore a `PILER-CR` `PilerArray` object

The `PilerArray` object contains a list of `PilerSpacer` objects.

```python
>>> array
<pilercrpy.piler.PilerArray object at 0x7f8859362af0>
>>> array.seqname  # array parent sequence
'NODE_2_length_236594_cov_5.82525'
>>> array.start_position  # position of array on parent sequence
16684
>>> len(array)  # length of array in bases
2128
>>> array.spacers
[<pilercrpy.piler.PilerSpacer object at 0x7f8859362b50>, ..., <pilercrpy.piler.PilerSpacer object at 0x7f885922b970>]
>>> array.spacer_sequences  # spacer sequences in array (list)
['TTGAAATTAGTGACGTGAGCAGAATCGTAAAC', ..., 'TGTAGCCCGA']
>>> array.unique_spacer_sequences  # unique spacer sequences in array (set)
{'AGCTTGCGTTGCTCGTCTGTCAAATTGCGGGT', ..., 'TTGAAATTAGTGACGTGAGCAGAATCGTAAAC'}
>>> array.num_spacers  # number of spacers in array
32
>>> len(array.unique_spacer_sequences)
32
>>> array.spacer_sequence_counts  # count of spacer sequence occurrences (Counter)
Counter({'AACCGTCGCTCGCTGGCCACTGTACGATTCGC': 3, ..., 'TGTAGCCCGA': 1})
>>> array.spacer_len  # length of spacer sequence in array
32
>>> array.consensus  # repeat sequence consensus
'TTTCTAAGCTGCCTGTACGGCAGTGAAC'
>>> array.repeats  # repeat sequence representation
['..........A.................', ..., '............................']
```
