# kiwano

Kiwano implements an approach for prioritizing epigenomic and transcriptomic characterization in situation that many large consortia have found themselves in where many, but not all, experiments have been performed. This approach relies on submodular optimization, which is the discrete analog of convex optimization, and imputed versions of the experiments. More specifically, a submodular function called facility location is optimized over the similarity matrix derived from imputed experiments. This results in an ordering of experiments based on a notion of how informative performing that experiment is expected to be.

You can read the preprint on bioRxiv here (not yet uploaded).

Download:

[The full similarity matrix calculated on imputed tracks (30,800 by 30,800)](https://noble.gs.washington.edu/~jmschr/2019_experiment_selection/exps/5_15_2019_Similarity/experiment_similarities.npz)

[The biosample and assay for each experiment](https://noble.gs.washington.edu/~jmschr/2019_experiment_selection/exps/5_15_2019_Similarity/experiment_names.tsv)

### Installation

Kiwano can be installed via

```
pip install kiwano
```

or downloaded as a zip file from here.

### Command Line Kiwano

Kiwano can be run on the command line with the following signature:

```
usage: kiwano.py [-h] -s SIMILARITIES -n NAMES [-v] [-o OUTPUT] [-r OUTPUTR]
                 [--include_biosamples INCLUDE_CELLTYPES]
                 [--include_assays INCLUDE_ASSAYS]
                 [--include_experiments INCLUDE_EXPERIMENTS]
                 [--exclude_biosamples EXCLUDE_CELLTYPES]
                 [--exclude_assays EXCLUDE_ASSAYS]
                 [--exclude_experiments EXCLUDE_EXPERIMENTS]

Kiwano is a tool that prioritizes experiments based on minimizing redundancy.

optional arguments:
  -h, --help            show this help message and exit
  -s SIMILARITIES, --similarities SIMILARITIES
                        The filename of the similarity matrix. This matrix
                        should be a non-negative symmetric matrix in either
                        .tsv, .npy, or .npz format, where each row/column is
                        the corresponding value in the names file.
  -n NAMES, --names NAMES
                        The filename of the names file. Each row in this file
                        should be the name of the biosample followed by the
                        name of the assay, separated by tabs. There should be
                        one name for each row in the similarity matrix.
  -v, --verbose         Whether to display a progress bar.
  -o OUTPUT, --output OUTPUT
                        The filename that the ranked experiments should be
                        output to.
  -r OUTPUTR, --output_ranking OUTPUTR
                        The filename that the ranking should be output to.
  --include_biosamples INCLUDE_CELLTYPES
                        The filename of a one column file where each row is
                        the name of a biosample that should be included in the
                        selection. All other biosamples are discarded.
  --include_assays INCLUDE_ASSAYS
                        The filename of a one column file where each row is
                        the name of an assay that should be included in the
                        selection. All other assays are discarded.
  --include_experiments INCLUDE_EXPERIMENTS
                        The filename of a two column file where each row has
                        the name of a specific experiment to include. All
                        other experiments are discarded.
  --exclude_biosamples EXCLUDE_CELLTYPES
                        The filename of a one column file where each row is
                        the name of a biosample that should be excluded from
                        the selection. All other biosamples are included.
  --exclude_assays EXCLUDE_ASSAYS
                        The filename of a one column file where each row is
                        the name of an assay that should be excluded from the
                        selection. All other assays are included.
  --exclude_experiments EXCLUDE_EXPERIMENTS
                        The filename of a two column file where each row has
                        the name of a specific experiment to exclude. All
                        other experiments are included.
```

A subset of the full similarity matrix, `small_similarities.npz`, and the corresponding file of experimental names, `small_experiment_names.tsv`, has been provided. These include every 15th experiment from the full similarity matrix. An example of running Kiwano on this would be

```
python kiwano.py -s small_similarities.npz -n small_experiment_names.tsv -o ranking.tsv
```

The first few lines in `ranking.tsv` should be

```
prostate gland male adult (37 years)	ChIP-seq ETS1
subcutaneous adipose tissue female adult (53 years)	ChIP-seq H3K9ac
Parathyroid adenoma male adult (65 years)	polyA depleted RNA-seq
subcutaneous preadipocyte female adult (62 years) and male adult (65 years)	RAMPAGE
endothelial cell of umbilical vein nuclear fraction male newborn	ChIP-seq SMC3
```

When using the command line tool in conjunction with `head` you may get a `IOError: [Errno 32] Broken pipe` error, which can be safely ignored.

Due to the similarity matrix taking quadratic space with the number of experiments, ranking the full set of experiments can take over 10GB. Make sure that your computer has enough memory before running. 

### Python Kiwano

Kiwano is also implemented as a Python function that serves mostly as a wrapper for the facility locatio function.

```python
from kiwano import kiwano

similarities = numpy.load("small_similarities.npz")['arr_0']
names = numpy.load("small_names.tsv", delimiter='\t', dtype=str)

ranked_names, ranking = kiwano(similarities, names, verbose=True)
print(ranked_names)
```

The first few items printed should be the same as the command line version above.
