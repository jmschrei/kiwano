# kiwano.py
# Author: Jacob Schreiber <jmschreiber91@gmail.com>

import sys
import argparse
import numpy

from apricot import FacilityLocationSelection

def kiwano(similarities, names, **kwargs):
	"""Kiwano will take in a similarity matrix and output an ordering.

	Kiwano is the implementation of a procedure that can determine the
	order that experiments should be performed based on a submodular
	optimization procedure applied to imputed versions of those
	experiments. Thus, the input to this procedure is a calculated
	similarity matrix, and the output is an ordering over those
	experiments. The similarity matrix must be symmetric and
	non-negative, with higher values indicating higher similarity.
	We anticipate that these similarities are squared correlation
	valus, but they can be any similarity metric that follows
	those properties. The ranking procedure involves optimizing a
	facility location function.

	This is an implementation of the code for the paper

	blah bah blah
	Jacob Schreiber, Jeffrey Bilmes, William Noble
	"""

	if not isinstance(similarities, numpy.ndarray):
		raise ValueError("Similarities must be a 2D symmetric numpy array.")
	if numpy.any(similarities.T != similarities):
		raise ValueError("Similarities must be a 2D symmetric numpy array.")
	if similarities.ndim != 2:
		raise ValueError("Similarities must be a 2D symmetric numpy array")

	if len(similarities) != len(names):
		raise ValueError("The length of similarities must be the same as the length of names")


	selector = FacilityLocationSelection(len(names), pairwise_func='precomputed', **kwargs)
	selector.fit(similarities)
	print('')
	return names[selector.ranking], selector.ranking

if __name__ == '__main__':
	#parser = argparse.ArgumentParser()
	#parser.add_argument()

	similarities_file, names_file = sys.argv[1:]

	include_celltypes_file = False
	include_assays_file = False
	include_experiments_file = False
	exclude_celltypes_file = False
	exclude_assays_file = False 
	exclude_experiments_file = False
	verbose = False

	include_experiments_file = 'test_file.tsv'

	similarities = numpy.loadtxt(similarities_file, delimiter='\t', dtype='float64')
	names = numpy.loadtxt(names_file, delimiter='\t', dtype=str)

	idx = numpy.ones(similarities.shape[0], dtype=bool)

	if include_celltypes_file:
		include_celltypes = numpy.loadtxt(include_celltypes_file, delimiter='\t', dtype=str)
		idx = idx & numpy.isin(names[:,0], include_celltypes)

	if include_assays_file:
		include_assays = numpy.loadtxt(include_assays_file, delimiter='\t', dtype=str)
		idx = idx & numpy.isin(names[:,1], include_assays)

	if include_experiments_file:
		include_experiments = numpy.loadtxt(include_experiments_file, delimiter='\t', dtype=str)
		idx = idx & numpy.isin(names[:,0], include_experiments[:,0]) & numpy.isin(names[:,1], include_experiments[:,1])

	if exclude_celltypes_file:
		exclude_celltypes = numpy.loadtxt(exclude_celltypes_file, delimiter='\t', dtype=str)
		idx = idx & ~numpy.isin(names[:,0], exclude_celltypes)

	if exclude_assays_file:
		exclude_assays = numpy.loadtxt(exclude_assays_file, delimiter='\t', dtype=str)
		idx = idx & ~numpy.isin(names[:,1], exclude_assays)

	if exclude_experiments_file:
		exclude_experiments = numpy.loadtxt(exclude_experiments_file, delimiter='\t', dtype=str)
		idx = idx & ~(numpy.isin(names[:,0], exclude_experiments[:,0]) & numpy.isin(names[:,1], exclude_experiments[:,1]))

	similarities = similarities[idx][:, idx]
	names = names[idx]

	ranked_names, ranking = kiwano(similarities, names, verbose=verbose)
	
	print(ranked_names)
	print(ranking)

	#numpy.savetxt(output_file, ranked_names)
	