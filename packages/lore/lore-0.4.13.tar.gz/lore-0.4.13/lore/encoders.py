from __future__ import unicode_literals
from abc import ABCMeta, abstractmethod
import math
import os
import re
import sys
import logging
from datetime import timedelta

import inflection
import numpy
import pandas
from smart_open import smart_open

import lore
import lore.transformers
from lore.util import timer


logger = logging.getLogger(__name__)


class Base(object):
    """
    Encoders reduces a data set to a more efficient representation suitable
    for learning. Encoders may be lossy, and should first be `fit` after
    initialization before `transform`ing data.
    """
    __metaclass__ = ABCMeta

    def __init__(self, column, name=None):
        """
        :param column: the index name of a column in a dataframe, or a Transformer
        :param name: an optional debugging hint, otherwise a default will be supplied
        """
        super(Base, self).__init__()
        self.infinite_warning = True
        self.column = column
        if name:
            self.name = name
        else:
            if isinstance(self.column, lore.transformers.Base):
                self.name = self.column.name
            else:
                self.name = self.column
            self.name = inflection.underscore(self.__class__.__name__) + '_' + self.name
        
    def fit(self, data):
        """
        Establishes the encoding for a data set

        :param data: representative samples
        """
        pass
    
    @abstractmethod
    def transform(self, data):
        """
        :param data: DataFrame with column to encode
        :return: encoded Series
        """
        pass

    @abstractmethod
    def reverse_transform(self, series):
        """
        Decodes data

        :param data: encoded set to be decoded
        :return: decoded series
        """
        pass

    @abstractmethod
    def cardinality(self):
        """
        The required array size for a 1-hot encoding of all possible values,
        including missing_value for encoders that distinguish missing data.

        :return: the unique number of values this encoding can transform
        """
        pass

    def fit_transform(self, data):
        """
        Conveniently combine fit + transform on a data set

        :param data: representative samples
        :return: transformed data
        """
        self.fit(data)
        return self.transform(data)

    def fillna(self, data, addition=0):
        """
        Fills with encoder specific default values.

        :param data: examined to determine defaults
        :param addition: uniquely identify this set of fillnas if necessary
        :return: filled data
        """
        if self.series(data).dtype == numpy.object:
            return self.series(data)
        
        return self.series(data).fillna(self.missing_value + addition)
    
    def source_column(self):
        column = self.column
        while isinstance(column, lore.transformers.Base):
            column = column.column
        return column
    
    def series(self, data):
        if isinstance(self.column, lore.transformers.Base):
            series = self.column.transform(data)
        else:
            series = data[self.column]

        if self.infinite_warning and series.dtype in ['float32', 'float64'] and numpy.isinf(series).any():
            logger.warn('Infinite values are present for %s' % self.name)

        return series
    

class Boolean(Base):
    """
    Transforms a series of booleans into floating points suitable for
    training.
    """
    
    def transform(self, data):
        with timer('transform %s:' % (self.name), logging.DEBUG):
            series = self.series(data).astype(float)
            null = series.isnull()
            series[series != 0] = 1
            series[null] = 2
            return series
    
    def reverse_transform(self, series):
        return series.round().astype(bool)

    def cardinality(self):
        return 3
    
    
class Equals(Base):
    """
    Provides element-wise comparison of left and right "column" and "other"
    
    see also: numpy.equal
    """
    def __init__(self, column, other, name=None):
        """
        :param column: the index name of a column in a DataFrame, or a Transformer
        :param other: the index name of a column in a DataFrame, or a Transformer
        :param name: an optional debugging hint, otherwise a default will be supplied
        """
        if not name:
            column_name = column.name if isinstance(column, lore.transformers.Base) else column
            other_name = other.name if isinstance(other, lore.transformers.Base) else other
            name = 'match_' + column_name + '_and_' + other_name
        super(Equals, self).__init__(column=column, name=name)
        self.other = other

    def transform(self, data):
        with timer('transform %s:' % self.name, logging.DEBUG):
            return numpy.equal(self.series(data), self.other_series(data)).astype(float)
    
    def reverse_transform(self, data):
        return numpy.full((len(data),), 'LOSSY')

    def cardinality(self):
        return 2

    def other_series(self, data):
        if isinstance(self.other, lore.transformers.Base):
            return self.other.transform(data)
    
        return data[self.other]


class Continuous(Base):
    """Abstract Base Class for encoders that return continuous values"""
    
    def __init__(self, column, name=None):
        super(Continuous, self).__init__(column, name)

    def cardinality(self):
        raise ValueError('Continous values have infinite cardinality')


class Pass(Base):
    """This encoder performs a noop on the input series. It's only useful
    to efficiently pass a pre-encoded value directly as an input to the
    model.
    """
    def transform(self, data):
        """ :return: the series exactly as it is"""
        return self.series(data)
    
    def reverse_transform(self, series):
        return series
    
    def cardinality(self):
        return float('nan')
    

class Norm(Continuous):
    """
    Encodes data between 0 and 1. Missing values are encoded to 0, and cannot be
    distinguished from the minimum value observed. New data that exceeds the fit
    range will be capped from 0 to 1.
    """

    def __init__(self, column, name=None):
        super(Norm, self).__init__(column, name)
        self.__min = float('nan')
        self.__range = float('nan')
        self.missing_value = 0

    def fit(self, data):
        with timer(('fit %s:' % self.name), logging.DEBUG):
            series = self.series(data)
            self.__min = float(series.min())
            self.__range = series.max() - self.__min

    def transform(self, data):
        with timer('transform %s:' % self.name, logging.DEBUG):
            if self.__range > 0:
                series = self.series(data)
                difference = numpy.maximum(0, series - self.__min)
                result = numpy.minimum(self.__range, difference) / self.__range
                result[series.isnull()] = self.missing_value
            else:
                result = numpy.zeros(len(data))
            return pandas.Series(result)

    def reverse_transform(self, series):
        with timer('reverse_transform %s:' % self.name, logging.DEBUG):
            return series * self.__range + self.__min

    
class Discrete(Base):
    """
    Discretizes continuous values into a fixed number of bins from [0,bins).
    Values outside of the fit range are capped between observed min and max.
    Missing values are encoded distinctly from all others, so cardinality is
    bins + 1.
    """
    
    def __init__(self, column, name=None, bins=10):
        super(Discrete, self).__init__(column, name)
        self.__norm = bins - 1
        self.__min = float('nan')
        self.__range = float('nan')
        self.missing_value = self.__norm + 1
        self.zero = 0.0
    
    def fit(self, data):
        with timer(('fit %s:' % self.name), logging.DEBUG):
            series = self.series(data)
            self.__min = series.min()
            self.__range = series.max() - self.__min
            if isinstance(self.__range, timedelta):
                logger.warn('Discrete timedelta requires (slower) 64bit float math. '
                            'Could you use the epoch instead for %s?' % self.name)
                self.__range = self.__range.total_seconds() * 1000000000

    def transform(self, data):
        with timer('transform %s:' % self.name, logging.DEBUG):
            if self.__range > self.zero:
                series = self.series(data)
                difference = series - self.__min
                if (difference.dtype == 'timedelta64[ns]'):
                    difference = pandas.to_numeric(difference)
                difference[difference < self.zero] = self.zero
                difference[difference > self.__range] = self.__range
                result = difference * self.__norm // self.__range
                result[result.isnull()] = self.missing_value
            else:
                result = pandas.Series(numpy.zeros(len(data)), copy=False)
            return result
        
    def reverse_transform(self, series):
        with timer('reverse_transform %s:' % self.name, logging.DEBUG):
            series[series >= self.missing_value] = float('nan')
            return (series / self.__norm * self.__range) + self.__min
            
    def cardinality(self):
        return self.__norm + 2


class Enum(Base):
    """
    Encodes a number of values from 0 to the max observed. New values that
    exceed previously fit max are given a unique value. Missing values are
    also distinctly encoded.
    """
    def __init__(self, column, name=None):
        super(Enum, self).__init__(column, name)
        self.__max = None
        self.unfit_value = None
        self.missing_value = None

    def fit(self, data):
        with timer(('fit %s:' % self.name), logging.DEBUG):
            self.__max = self.series(data).max()
            self.unfit_value = self.__max + 1
            self.missing_value = self.__max + 2

    def transform(self, data):
        with timer('transform %s:' % self.name, logging.DEBUG):
            series = self.series(data)
            result = pandas.Series(series, copy=True)
            result[(series > self.__max) | (series < 0)] = self.unfit_value
            result[series.isnull()] = self.missing_value
            result.astype(int, copy=False)
            return result
            
    def reverse_transform(self, series):
        with timer('reverse_transform %s:' % self.name, logging.DEBUG):
            series[series >= self.missing_value] = float('nan')
            return series

    def cardinality(self):
        return self.__max + 3


class Quantile(Base):
    """Encodes values uniformly across bins. If the encoder is fit data is not
    uniformly distributed enough to have a point in each quantile, duplicate
    quantiles will be dropped.
    
    Values the excede the upper and lower bound fit, will be placed into
    distinct bins, as well nans.
    """
    def __init__(self, column, name=None, quantiles=10):
        """
        :param quantiles: the number of bins
        """
        super(Quantile, self).__init__(column, name)
        self.quantiles = quantiles
        self.missing_value = self.quantiles + 2
        self.upper_bound = None
        self.lower_bound = None
        self.bins = None
    
    def fit(self, data):
        with timer(('fit %s:' % self.name), logging.DEBUG):
            series = self.series(data)
            series_cut, self.bins = pandas.qcut(series, self.quantiles, retbins=True, labels=False, duplicates='drop')
            self.quantiles = len(self.bins) - 1
            self.missing_value = self.quantiles + 2
            self.lower_bound = series.min()
            self.upper_bound = series.max()
    
    def transform(self, data):
        with timer('transform %s:' % (self.name), logging.DEBUG):
            series = self.series(data)
            cut = pandas.cut(series, bins=self.bins, labels=False, include_lowest=True)
            cut[series < self.lower_bound] = self.quantiles
            cut[series > self.upper_bound] = self.quantiles + 1
            cut[series.isnull()] = self.missing_value
            return cut
    
    def reverse_transform(self, series):
        result = series.apply(lambda i: self.bins[int(i)] if i < self.quantiles else None)
        result[series == self.quantiles] = '<' + str(self.lower_bound)
        result[series == self.quantiles + 1] = '>' + str(self.upper_bound)
        result[series == self.missing_value] = None
        return result
    
    def cardinality(self):
        return self.missing_value + 1


class MissingValueMap(dict):
    def __missing__(self, key):
        return 0


class Unique(Base):
    """Encodes distinct values. Values that appear fewer than
    minimum_occurrences are mapped to a unique shared encoding to compress the
    long tail. New values that were not seen during fit will be
    distinctly encoded from the long tail values.
    """
    
    def __init__(self, column, name=None, minimum_occurrences=1):
        """
        :param minimum_occurrences: ignore ids with less than this many occurrences
        """
        super(Unique, self).__init__(column, name)
        self.minimum_occurrences = minimum_occurrences
        self.map = None
        self.inverse = None
        self.missing_value = 1
    
    def fit(self, data):
        with timer(('fit unique %s:' % self.name), logging.DEBUG):
            ids = pandas.DataFrame({'id': self.series(data)})
            counts = pandas.DataFrame({'n': ids.groupby('id').size()})
            qualified = counts[counts.n >= self.minimum_occurrences].copy()
            qualified['encoded_id'] = numpy.arange(len(qualified)) + 1
            
            self.map = MissingValueMap(qualified.to_dict()['encoded_id'])
            self.inverse = {v: k for k, v in self.map.items()}
            self.inverse[0] = 'LONG_TAIL'
            self.missing_value = len(self.map) + 1
    
    def transform(self, data):
        with timer('transform uniqe %s:' % self.name, logging.DEBUG):
            result = self.series(data).map(self.map, na_action='ignore')
            result[result.isnull()] = self.missing_value
            return result.astype(int)
    
    def reverse_transform(self, series):
        with timer('reverse_transform unique %s:' % self.name, logging.DEBUG):
            result = series.map(self.inverse, na_action=None)
            result[result.isnull()] = 'MISSING_VALUE'
            return result
        
    def cardinality(self):
        return len(self.map) + 2


class Token(Unique):
    """
    Breaks sentences into individual words, and encodes each word individually,
    with the same properties as the ID encoder.
    """
    PUNCTUATION_FILTER = re.compile(r'\W+\s\W+|\W+(\s|$)|(\s|^)\W+', re.UNICODE)
    
    def __init__(self, column, name=None, sequence_length=10, minimum_occurrences=1):
        """
        :param sequence_length: truncates tokens after sequence_length
        :param minimum_occurrences: ignore tokens with less than this many occurrences
        """
        super(Token, self).__init__(column, name, minimum_occurrences)
        self.sequence_length = sequence_length
    
    def fit(self, data):
        with timer(('fit token %s:' % self.name), logging.DEBUG):
            tokens = pandas.DataFrame({self.column: self.tokenize(data).values.flatten()}, copy=False)
            super(Token, self).fit(tokens)
    
    def transform(self, data):
        """
        :param data: DataFrame with column to encode
        :return: encoded Series
        """
        with timer('transform token %s:' % self.name, logging.DEBUG):
            tokens = self.tokenize(data)
            for column in tokens:
                tokens[column] = super(Token, self).transform(pandas.DataFrame({self.column: tokens[column]}, copy=False))
            return pandas.Series(tokens.values.tolist())
        
    def reverse_transform(self, series):
        with timer('reverse_transform token %s:' % self.name, logging.DEBUG):
            data = pandas.DataFrame(series.tolist())
            for column in data:
                data[column] = super(Token, self).reverse_transform(data[column])
            return data.T.apply(' '.join)
        
    def get_token(self, tokens, i):
        if isinstance(tokens, float) or i >= len(tokens):
            return self.missing_value
        return tokens[i]
    
    def tokenize(self, data):
        cleaned = self.series(data).str.replace(Token.PUNCTUATION_FILTER, ' ')
        lowered = cleaned.str.lower()
        dataframe = lowered.str.split(expand=True)
        return dataframe.loc[:,0:self.sequence_length]
    

class Glove(Token):
    """
    Encodes tokens using the GloVe embeddings.
    https://nlp.stanford.edu/projects/glove/
    https://blog.keras.io/using-pre-trained-word-embeddings-in-a-keras-model.html
    """
    map = None
    inverse = None
    
    def __getstate__(self):
        # only pickle the bare necessities, pickling the GloVe encodings is
        # prohibitively inefficient
        return {
            'sequence_length': self.sequence_length,
            'dimensions': self.dimensions,
        }

    def __setstate__(self, newstate):
        # re-load the GloVe encodings after unpickling
        self.__dict__.update(newstate)
        self.fit(None)

    def fit(self, data):
        with timer('fit %s:' % self.name, logging.DEBUG):
            self.missing_value = numpy.asarray([0.0] * self.dimensions, dtype='float32')

            if not Glove.map:
                Glove.map = {}
                Glove.inverse = {}
    
                path = os.path.join(lore.env.models_dir, 'encoders', 'glove.6B.%dd.txt.gz' % self.dimensions)
                local = lore.io.download(path)
                for line in smart_open(local):
                    values = line.split()
                    word = values[0]
                    parameters = numpy.asarray(values[1:], dtype='float32')
                    Glove.map[word] = parameters
                    Glove.inverse[tuple(parameters.tolist())] = word

            self.map = Glove.map
            self.inverse = Glove.inverse


class MiddleOut(Base):
    """Creates an encoding out of a picking sequence

    Tracks the first d (depth) positions and the last d
    positions, and encodes all positions in-between to
    a middle value. Sequences shorter than 2d + 1 will
    not have a middle value encoding if they are even
    in length, and will have one (to break the tie) if
    they are odd in length.

    Args:
        depth (int): how far into the front and back
            of the sequence to track uniquely, rest will
            be coded to a middle value

    e.g.
        MiddleOut(2).transform([1,2,3,4,5,6,7]) =>
        [1, 2, 3, 3, 3, 4, 5]

    """
    
    def __init__(self, column, name=None, depth=None):
        super(MiddleOut, self).__init__(column, name)
        self.depth = depth
    
    def transform(self, data):
        with timer('transform %s:' % self.name, logging.DEBUG):
            series = self.series(data)
            max_seq = len(series)
            depth = min(self.depth, max_seq // 2)

            res = numpy.full(max_seq, self.depth, dtype=int)
            res[:depth] = numpy.arange(depth)
            res[max_seq - depth:max_seq] = self.depth * 2 - numpy.arange(depth)[::-1]
            
            return res

    def reverse_transform(self, data):
        pass
        # left as an excercise for the reader
    
    def cardinality(self):
        return self.depth * 2 + 1
