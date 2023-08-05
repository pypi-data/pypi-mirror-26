#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# File: model_desc.py
# Author: Yuxin Wu <ppwwyyxx@gmail.com>

from abc import ABCMeta, abstractmethod
from collections import namedtuple
import tensorflow as tf
import six

from ..utils.argtools import memoized
from ..input_source import InputSource
from ..models.regularize import regularize_cost_from_collection

__all__ = ['InputDesc', 'ModelDesc', 'ModelDescBase']


class InputDesc(
        namedtuple('InputDescTuple', ['type', 'shape', 'name'])):
    """
    Metadata about an input entry point to the graph.
    This metadata can be later used to build placeholders or other types of
    input source.
    """

    def __new__(cls, type, shape, name):
        """
        Args:
            type (tf.DType):
            shape (tuple):
            name (str):
        """
        shape = tuple(shape)    # has to be tuple for "self" to be hashable
        self = super(InputDesc, cls).__new__(cls, type, shape, name)
        self._cached_placeholder = None
        return self

    def build_placeholder(self, prefix=''):
        """
        Build a tf.placeholder from the metadata, with an optional prefix.

        Args:
            prefix(str): the name of the placeholder will be ``prefix + self.name``

        Returns:
            tf.Tensor:
        """
        with tf.name_scope(None):   # clear any name scope it might get called in
            ret = tf.placeholder(
                self.type, shape=self.shape,
                name=prefix + self.name)
        if prefix == '' and self._cached_placeholder is None:
            self._cached_placeholder = ret  # cached_placeholder only caches the prefix='' case
        return ret

    # cannot memoize here, because InputDesc is hashed by its fields.
    def build_placeholder_reuse(self):
        """
        Build a tf.placeholder from the metadata, or return an old one.

        Returns:
            tf.Tensor:
        """
        if self._cached_placeholder is not None:
            return self._cached_placeholder
        return self.build_placeholder()


@six.add_metaclass(ABCMeta)
class ModelDescBase(object):
    """ Base class for a model description.
    """
    @memoized
    def get_inputs_desc(self):
        """
        Returns:
            list[:class:`InputDesc`]: list of the underlying :class:`InputDesc`.
        """
        return self._get_inputs()

    @abstractmethod
    def _get_inputs(self):
        """
        :returns: a list of InputDesc
        """

    # TODO only use InputSource in the future? Now only used in predictor_factory
    def build_graph(self, inputs):
        """
        Build the whole symbolic graph.

        Args:
            inputs (list[tf.Tensor] or InputSource): a list of tensors, or an :class:`InputSource`,
                that match the list of :class:`InputDesc` defined by ``_get_inputs``.
        """
        if isinstance(inputs, InputSource):
            inputs = inputs.get_input_tensors()
        assert len(inputs) == len(self.get_inputs_desc()), \
            "Number of inputs passed to the graph != number of inputs defined " \
            "in ModelDesc! ({} != {})".format(len(inputs), len(self.get_inputs_desc()))
        self._build_graph(inputs)

    @abstractmethod
    def _build_graph(self, inputs):
        pass


class ModelDesc(ModelDescBase):
    """
    A ModelDesc with single cost and single optimizer.
    """

    def get_cost(self):
        """
        Return the cost tensor in the graph.

        It calls :meth:`ModelDesc._get_cost()` which by default returns
        ``self.cost``. You can override :meth:`_get_cost()` if needed.

        This function also applies the collection
        ``tf.GraphKeys.REGULARIZATION_LOSSES`` to the cost automatically.
        """
        cost = self._get_cost()
        reg_cost = regularize_cost_from_collection()
        if reg_cost is not None:
            return tf.add(cost, reg_cost, name='cost_with_regularizer')
        else:
            return cost

    def _get_cost(self, *args):
        return self.cost

    @memoized
    def get_optimizer(self):
        """
        Return the memoized optimizer returned by `_get_optimizer`.

        Users of :class:`ModelDesc` will need to implement `_get_optimizer()`,
        which will only be called once per each model.

        Returns:
            a :class:`tf.train.Optimizer` instance.
        """
        return self._get_optimizer()

    def _get_optimizer(self):
        raise NotImplementedError()

    def build_graph_get_cost(self, *inputs):
        """
        Build the graph from inputs and return the cost tensor.
        This is useful for most of the :class:`GraphBuilder` which expects
        such a function.
        """
        self.build_graph(inputs)
        return self.get_cost()
