"""
Copyright 2016 Deepgram

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import logging

from . import Layer, ParsingError

logger = logging.getLogger(__name__)

###############################################################################
class Dense(Layer):						# pylint: disable=too-few-public-methods
	""" A fully-connected layer.
	"""

	DEFAULT_AUTO_FLATTEN = False

	###########################################################################
	def __init__(self, *args, **kwargs):
		""" Creates a new dense layer.
		"""
		super().__init__(*args, **kwargs)
		self.size = None
		self.auto_flatten = None
		self.highway = False
		self.highway_bias = None

	###########################################################################
	def _parse(self, engine):
		""" Parse the layer.
		"""
		if isinstance(self.args, dict):
			self.size = engine.evaluate(self.args['size'], recursive=True)
			self.auto_flatten = engine.evaluate(
				self.args.get('flatten', Dense.DEFAULT_AUTO_FLATTEN),
				recursive=True
			)
			self.highway = engine.evaluate(
				self.args.get('highway', False)
			)
			self.highway_bias = engine.evaluate(self.args.get('bias'))
		elif isinstance(self.args, list):
			self.size = engine.evaluate(self.args, recursive=True)
			self.auto_flatten = Dense.DEFAULT_AUTO_FLATTEN
		else:
			self.size = self.args
			self.auto_flatten = Dense.DEFAULT_AUTO_FLATTEN

		if not isinstance(self.size, (tuple, list)):
			self.size = [self.size]

		try:
			for i, v in enumerate(self.size):
				self.size[i] = int(v)
		except ValueError:
			raise ParsingError('Key "size" in Dense layer must be an integer '
				'or a list of integers. Received: {}'.format(self.size))

		if not isinstance(self.auto_flatten, bool):
			raise ParsingError('"auto_flatten" key in Dense layer must be '
				'boolean. Received: {}'.format(self.auto_flatten))

		if not isinstance(self.highway, bool):
			raise ParsingError('"highway" must be boolean.')

		if self.highway_bias is not None:
			try:
				self.highway_bias = float(self.highway_bias)
			except ValueError:
				raise ParsingError('"bias" term must be a floating-point '
					'number. Received: {}'.format(self.highway_bias))

			if not self.highway:
				logger.warning('"bias" term was specified, but is only used '
					'with "highway"-type convolutions. Ignoring this...')

	###########################################################################
	def _build(self, model):
		""" Create the backend-specific placeholder.
		"""
		backend = model.get_backend()
		if backend.get_name() == 'keras':

			if self.highway:
				raise ValueError('Backend does not support highway dense '
					'layers.')

			import keras.layers as L			# pylint: disable=import-error

			if self.auto_flatten:
				yield L.Flatten()

			if backend.keras_version() == 1:
				func = lambda x, **kwargs: L.Dense(output_dim=x, **kwargs)
			else:
				func = lambda x, **kwargs: L.Dense(units=x, **kwargs)

			for v in self.size[:-1]:
				yield func(v, trainable=not self.frozen)

			yield func(
				self.size[-1],
				name=self.name,
				trainable=not self.frozen
			)

		elif backend.get_name() == 'pytorch':

			# pylint: disable=import-error
			import torch.nn as nn
			import torch.nn.functional as F
			# pylint: enable=import-error

			from kur.backend.pytorch.modules import swap_channels

			def layer(in_features, bias=None):
				result = nn.Linear(in_features, self.size[-1])
				if bias is not None:
					result.bias.requires_grad = False
					result.bias.data.fill_(bias)
				return result

			if not self.highway:

				def connect(inputs):
					""" Connects the layer.
					"""
					assert len(inputs) == 1
					return {
						'shape' : self.shape([inputs[0]['shape']]),
						'layer' : model.data.add_layer(
							self.name,
							layer(inputs[0]['shape'][-1]),
							frozen=self.frozen
						)(inputs[0]['layer'])
					}

			else:

				def connect(inputs):
					""" Connects the layer.
					"""
					assert len(inputs) == 1

					# We need to define the layer now so that it is tracked by
					# the PyTorch module, but we want to apply it directly, so
					# we need the `op` attribute.
					H = model.data.add_layer(
						self.name + '_H',
						layer(inputs[0]['shape'][-1]),
						frozen=self.frozen
					).op

					T = model.data.add_layer(
						self.name + '_T',
						layer(
							inputs[0]['shape'][-1],
							bias=self.highway_bias
						),
						frozen=True if self.frozen else None
					).op

					def func(module, x):
						# This:
						#   H(module, x)
						# can also be written as:
						#   Layer.resolve(H)(module, x)
						# but since H is, itself, a Layer (because the `op`
						# attribute on an added layer is the Layer instance),
						# `resolve` does nothing more than return its argument.
						h = H(module, x)
						h = F.relu(h)
						t = T(module, x)
						t = F.sigmoid(t)
						return h*t + x*(1-t)
					# Make sure that `func` is "pure" so that it receives the
					# `module` argument.
					func.pure = True

					return {
						'shape' : self.shape([inputs[0]['shape']]),
						'layer' : model.data.add_operation(func)(
							inputs[0]['layer']
						)
					}

			yield connect

		else:
			raise ValueError(
				'Unknown or unsupported backend: {}'.format(backend))

	###########################################################################
	def shape(self, input_shapes):
		""" Returns the output shape of this layer for a given input shape.
		"""
		if len(input_shapes) > 1:
			raise ValueError('Dense layers only take a single input.')
		return (self.size[-1], )

### EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF
