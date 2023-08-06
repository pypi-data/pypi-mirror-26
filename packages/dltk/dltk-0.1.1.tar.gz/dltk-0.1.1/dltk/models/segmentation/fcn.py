from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import tensorflow as tf
import numpy as np
from tensorflow.python.ops import control_flow_ops
from tensorflow.python.training import moving_averages

from dltk.core.modules import *


class Upscore(AbstractModule):
    """Upscore module according to J. Long.

    """
    def __init__(self, out_filters, strides, name='upscore'):
        """Constructs an Upscore module

        Parameters
        ----------
        out_filters : int
            number of output filters
        strides : list or tuple
            strides to use for upsampling
        name : string
            name of the module
        """
        self.out_filters = out_filters
        self.strides = strides
        self.in_filters = None
        self.rank = None
        super(Upscore, self).__init__(name)

    def _build(self, x, x_up, is_training=True):
        """Applies the upscore operation

        Parameters
        ----------
        x : tf.Tensor
            tensor to be upsampled
        x_up : tf.Tensor
            tensor from the same scale to be convolved and added to the upsampled tensor
        is_training : bool
            flag for specifying whether this is training - passed to batch normalization

        Returns
        -------
        tf.Tensor
            output of the upscore operation
        """

        # Compute an up-conv shape dynamically from the input tensor. Input filters are required to be static.
        if self.in_filters is None:
            self.in_filters = x.get_shape().as_list()[-1]
        assert self.in_filters == x.get_shape().as_list()[-1], 'Module was initialised for a different input shape'

        if self.rank is None:
            self.rank = len(self.strides)
        assert len(x.get_shape().as_list()) == self.rank + 2, \
            'Stride gives rank {} input is rank {}'.format(self.rank, len(x.get_shape().as_list()) - 2)

        # Account for differences in input and output filters
        if self.in_filters != self.out_filters:
            x = Convolution(self.out_filters, name='up_score_filter_conv', strides=[1] * self.rank)(x)

        t_conv = BilinearUpsample(strides=self.strides)(x)

        conv = Convolution(self.out_filters, 1, strides=[1] * self.rank)(x_up)
        conv = BatchNorm()(conv, is_training)

        return tf.add(t_conv, conv)


class ResNetFCN(AbstractModule):
    """FCN module with residual encoder

    This module builds a FCN for segmentation using a residual encoder.
    """
    def __init__(self, num_classes, num_residual_units=3, filters=(16, 64, 128, 256, 512),
                 strides=((1, 1, 1), (2, 2, 2), (2, 2, 2), (2, 2, 2), (1, 1, 1)), relu_leakiness=0.1,
                 name='resnetfcn'):
        """Builds a residual FCN for segmentation

        Parameters
        ----------
        num_classes : int
            number of classes to segment
        num_residual_units : int
            number of residual units per scale
        filters : tuple or list
            number of filters per scale. The first is used for the initial convolution without residual connections
        strides : tuple or list
            strides per scale. The first is used for the initial convolution without residual connections
        relu_leakiness : float
            leakiness of the relus used
        name : string
            name of the network
        """
        self.num_classes = num_classes
        self.num_residual_units = num_residual_units
        self.filters = filters
        self.strides = strides
        self.relu_leakiness = relu_leakiness
        self.rank = None
        super(ResNetFCN, self).__init__(name)

    def _build(self, inp, is_training=True):
        """Constructs a ResNetFCN using the input tensor

        Parameters
        ----------
        inp : tf.Tensor
            input tensor
        is_training : bool
            flag to specify whether this is training - passed to batch normalization

        Returns
        -------
        dict
            output dictionary containing:
                - `logits` - logits of the classification
                - `y_prob` - classification probabilities
                - `y_` - prediction of the classification

        """
        outputs = {}
        filters = self.filters
        strides = self.strides

        assert len(strides) == len(filters)

        if self.rank is None:
            self.rank = len(strides[0])
        assert len(inp.get_shape().as_list()) == self.rank + 2, \
            'Stride gives rank {} input is rank {}'.format(self.rank, len(inp.get_shape().as_list()) - 2)

        x = inp

        x = Convolution(filters[0], strides=strides[0])(x)
        tf.logging.info('Init conv tensor shape %s', x.get_shape())

        # residual feature encoding blocks with num_residual_units at different scales defined via strides
        scales = [x]
        saved_strides = []
        for scale in range(1, len(filters)):
            with tf.variable_scope('unit_%d_0' % (scale)):
                x = VanillaResidualUnit(filters[scale], stride=strides[scale])(x, is_training=is_training)
            saved_strides.append(strides[scale])
            for i in range(1, self.num_residual_units):
                with tf.variable_scope('unit_%d_%d' % (scale, i)):
                    x = VanillaResidualUnit(filters[scale], stride=[1] * self.rank)(x, is_training=is_training)
            scales.append(x)
            tf.logging.info('Encoder at scale %d tensor shape: %s', scale, x.get_shape())

        # Decoder / upscore
        for scale in range(len(filters) - 2, -1, -1):
            with tf.variable_scope('upscore_%d' % scale):
                x = Upscore(self.num_classes, saved_strides[scale])(x, scales[scale], is_training=is_training)
            tf.logging.info('Decoder at scale %d tensor shape: %s', scale, x.get_shape())

        with tf.variable_scope('last'):
            x = Convolution(self.num_classes, 1, strides=[1] * self.rank)(x)

        outputs['logits'] = x
        tf.logging.info('Logits tensor shape %s', x.get_shape())

        with tf.variable_scope('pred'):
            y_prob = tf.nn.softmax(x)
            outputs['y_prob'] = y_prob
            y_ = tf.argmax(x, axis=-1) if self.num_classes > 1 else tf.cast(tf.greater_equal(x[..., 0], 0.5), tf.int32)
            outputs['y_'] = y_

        return outputs