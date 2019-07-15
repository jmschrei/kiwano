# kiwano

Kiwano implements an approach for prioritizing epigenomic and transcriptomic characterization in situation that many large consortia have found themselves in where many, but not all, experiments have been performed. This approach relies on submodular optimization, which is the discrete analog of convex optimization, and imputed versions of the experiments. More specifically, a submodular function called facility location is optimized over the similarity matrix derived from imputed experiments. This results in an ordering of experiments based on a notion of how informative performing that experiment is expected to be.

You can read the preprint on bioRxiv here (not yet uploaded).

### Installation

Kiwano can be installed via

```
pip install kiwano
```

### Command Line Kiwano

Kiwano can be run on the command line with the following signature:

```
stuff
```

This takes in a precalculated similarity matrix, the corresponding biosample and assays involved in each experiment, and optional lists of biosamples, assays, or experiments to explicitly include or exclude. Running this on the full similarity matrix can take over 10 GB, so make sure that your computer has enough before running.

### Python Kiwano

Kiwano is also implemented as a Python function that serves mostly as a wrapper for the facility locatio function.

```python
from kiwano import kiwano

similarities = numpy.load("small_similarities.npz")['arr_0']
names = numpy.load("small_names.tsv", delimiter='\t', dtype=str)

ranked_names, ranking = kiwano(similarities, names, verbose=True)
print(ranked_names)
```

The first few items printed should be

```
suprapubic skin female adult (51 year)	ChIP-seq HDAC2
cingulate gyrus male adult (81 year)	ChIP-seq GTF2F1
omental fat pad female adult (51 year)	ChIP-seq H3K79me1
subcutaneous preadipocyte female adult (62 years) and male adult (65 years)	RAMPAGE
omental fat pad male adult (37 years)	polyA RNA-seq
```
