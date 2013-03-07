#!/usr/bin/python

from numpy import array


def stddev(numbers):
	np_array = array(numbers)
	return np_array.std()

def mean(numbers):
	np_array = array(numbers)
	return np_array.mean()
