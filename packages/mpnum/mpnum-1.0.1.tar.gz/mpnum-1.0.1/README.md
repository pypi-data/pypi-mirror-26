![mpnum](docs/mpnum_logo_144.png)
=====


## A matrix product representation library for Python

[![Travis](https://travis-ci.org/dseuss/mpnum.svg?branch=master)](https://travis-ci.org/dseuss/mpnum)
[![Documentation Status](https://readthedocs.org/projects/mpnum/badge/?version=latest)](http://mpnum.readthedocs.org/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/dseuss/mpnum/badge.svg?branch=master)](https://coveralls.io/github/dseuss/mpnum?branch=master)
[![Code Climate](https://codeclimate.com/github/dseuss/mpnum/badges/gpa.svg)](https://codeclimate.com/github/dseuss/mpnum)
[![PyPI](https://img.shields.io/pypi/v/mpnum.svg)](https://pypi.python.org/pypi/mpnum/)

mpnum is a flexible, user-friendly, and expandable toolbox for the matrix product state/tensor train tensor format. mpnum provides:

* support for well-known matrix product representations, such as:
  * matrix product states ([MPS](http://mpnum.readthedocs.org/en/latest/intro.html#matrix-product-states-mps)), also known as tensor trains (TT)
  * matrix product operators ([MPO](http://mpnum.readthedocs.org/en/latest/intro.html#matrix-product-operators-mpo))
  * local purification matrix product states ([PMPS](http://mpnum.readthedocs.org/en/latest/intro.html#local-purification-form-mps-pmps))
  * arbitrary matrix product arrays ([MPA](http://mpnum.readthedocs.org/en/latest/intro.html#matrix-product-arrays))
* arithmetic operations: addition, multiplication, contraction etc.
* [compression](http://mpnum.readthedocs.org/en/latest/mpnum.html#mpnum.mparray.MPArray.compress), [canonical forms](http://mpnum.readthedocs.org/en/latest/mpnum.html#mpnum.mparray.MPArray.canonicalize), etc.
* finding [extremal eigenvalues](http://mpnum.readthedocs.org/en/latest/mpnum.html#mpnum.linalg.eig) and eigenvectors of MPOs (DMRG)
* flexible tools for new matrix product algorithms



For more information, see:

* [Introduction to mpnum](http://mpnum.readthedocs.org/en/latest/intro.html)
* [Notebook with code examples](examples/mpnum_intro.ipynb)
* [Library reference](http://mpnum.readthedocs.org/en/latest/)

Required packages:

* six, numpy, scipy

Supported Python versions:

* 2.7, 3.4, 3.5, 3.6


## Contributors

* Daniel Suess, <daniel@dsuess.me>, [University of Cologne](http://www.thp.uni-koeln.de/gross/)
* Milan Holzaepfel, <mail@mholzaepfel.de>, [Ulm University](http://qubit-ulm.com/)


## License

Distributed under the terms of the BSD 3-Clause License (see [LICENSE](LICENSE)).


## Citations

mpnum has been used and cited in the following publications:

* I. Dhand et al. (2017), [arXiv 1710.06103](https://arxiv.org/abs/1710.06103)
* I. Schwartz, J. Scheuer et al. (2017), [arXiv 1710.01508](https://arxiv.org/abs/1710.01508)
* J. Scheuer et al. (2017), [arXiv 1706.01315](https://arxiv.org/abs/1706.01315)
* B. P. Lanyon, Ch. Maier et al, [Nat. Phys. (2017)](https://doi.org/10.1038/nphys4244), [arXiv 1612.08000](https://arxiv.org/abs/1612.08000)
