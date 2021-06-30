# `piler-crpy`

This repository contains a Python package for working with the `PILER-CR` CRISPR repeat finding software package.

- [`PILER-CR`](http://www.drive5.com/pilercr/)

> Edgar, R.C. PILER-CR: Fast and accurate identification of CRISPR repeats. BMC Bioinformatics 8, 18 (2007). [https://doi.org/10.1186/1471-2105-8-18](https://doi.org/10.1186/1471-2105-8-18)

It provides a parser to aid processing `PILER-CR` output files. We plan to add helper functions for running the prediction tool and processing its output.

---------------------------

## Installation

Download from this repository and install using the code below:

```bash
git clone git@github.com:widdowquinn/pilercrpy.git
cd pilercrpy
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

### Read a directory of `PILER-CR` output files

The `pilercrpy.read_arraydir()` function will read a directory of `PILER-CR` output files and return a dictionary, keyed by file path, containing a list of `PilerArray` objects for the corresponding file.

```python
>>> arrays = pilercrpy.read_arraydir(Path("tests/fixtures/pilercr_output/"))
>>> arrays
{PosixPath('tests/fixtures/pilercr_output/22873wG6_SCRI1113.fasta.pilercr'): [<pilercrpy.piler.PilerArray object at 0x7fc0103a1820>], ..., PosixPath('tests/fixtures/pilercr_output/22873wB2_SCRI1030.fasta.pilercr'): [<pilercrpy.piler.PilerArray object at 0x7fc011fc4d90>, <pilercrpy.piler.PilerArray object at 0x7fc011fc87f0>]}
```

### Count unique spacer sequences in a directory of `PILER-CR` output by filename

The `pilercrpy.read_unique_spacers_to_dfm()` function will read a directory of `PILER-CR` output files and return a `Pandas` dataframe with counts of each unique spacer sequence.

```python
>>> dfm = pilercrpy.read_unique_spacers_to_dfm(Path("tests/fixtures/pilercr_output/"))
>>> dfm
filename                          14205wC5_DM9_07.fasta  2168.fasta  22873wB2_SCRI1030.fasta  ...  6146.fasta  7383.fasta  DM48-09.fasta
spacer                                                                                        ...                                       
TTTGTCCTTGAGCCTGACCGCTTCCGCCATCG                      0           0                        0  ...           0           0              1
TTTATCGTACCAACACGATCCTGAGTACTGGA                      0           0                        0  ...           1           0              1
TTGCTTTAACAACCACCGTCTGAACTCACTGT                      1           1                        0  ...           0           0              0
TTGCGATTGGCACCGTTAACCGCTCAGTGACC                      0           0                        1  ...           0           0              0
TTGAAATTAGTGACGTGAGCAGAATCGTAAAC                      1           1                        0  ...           0           0              1
...                                                 ...         ...                      ...  ...         ...         ...            ...
AACTGAATAAACTCGACTCAACGCAAGATGCA                      0           0                        1  ...           1           0              0
AACCGTCGCTCGCTGGCCACTGTACGATTCGC                      3           3                        0  ...           0           0              1
AACACGCCGCGCGATTTTGTCCACAATGCGCA                      1           1                        0  ...           0           0              1
AAATCAGCCAGCAACTCATCAGGGTTTACCTC                      0           0                        1  ...           1           0              0
AAAATCCGCACGGATGCACTGAAAAAGGAAAT                      1           1                        0  ...           0           0              0

[118 rows x 8 columns]
```
