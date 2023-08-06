Convert ONNX models into Apple CoreML format.
=============================================

This tool converts `ONNX <https://onnx.ai/>`__ models to Apple CoreML
format.

Installation
------------

.. code:: bash

    pip install -U onnx-coreml

Dependencies
------------

-  click
-  numpy
-  coremltools (0.6.3+)
-  onnx (0.2.1+)

How to use
----------

Using this library you can implement converter for your models. To
implement converters you should use single function "convert" from
onnx\_coreml:

.. code:: python

    from onnx_coreml import convert

This function is simple enough to be self-describing:

.. code:: python

    def convert(model,
                mode=None,
                image_input_names=[],
                preprocessing_args={},
                image_output_names=[],
                deprocessing_args={},
                class_labels=None,
                predicted_feature_name='classLabel')

Parameters
~~~~~~~~~~

| **model**: ONNX model \| str
| An ONNX model with parameters loaded in onnx package or path to file
| with models.

| **mode**: str ('classifier', 'regressor' or None)
| Mode of the converted coreml model:
| 'classifier', a NeuralNetworkClassifier spec will be constructed.
| 'regressor', a NeuralNetworkRegressor spec will be constructed.

| **preprocessing\_args**: dict
| 'is\_bgr', 'red\_bias', 'green\_bias', 'blue\_bias', 'gray\_bias',
| 'image\_scale' keys with the same meaning as

https://apple.github.io/coremltools/generated/coremltools.models.neural\_network.html#coremltools.models.neural\_network.NeuralNetworkBuilder.set\_pre\_processing\_parameters

| **deprocessing\_args**: dict
| Same as 'preprocessing\_args' but for deprocessing.
| **class\_labels**: A string or list of strings.
| As a string it represents the name of the file which contains
| the classification labels (one per line).
| As a list of strings it represents a list of categories that map
| the index of the output of a neural network to labels in a classifier.
| **predicted\_feature\_name**: str
| Name of the output feature for the class labels exposed in the Core ML
| model (applies to classifiers only). Defaults to 'classLabel'

Returns
~~~~~~~

**model**: A coreml model.

CLI
~~~

Also you can use command-line script for simplicity:

::

    convert-onnx-to-coreml [OPTIONS] ONNX_MODEL

Currently supported
-------------------

Models
~~~~~~

Models from https://github.com/onnx/models are supported and tested.

Operators
~~~~~~~~~

List of ONNX operators that can be converted into their CoreML
equivalent:

-  Conv
-  Relu
-  Reshape
-  Transpose
-  MaxPool
-  AveragePool
-  FC
-  BatchNormalization
-  Add
-  Sum
-  Mul
-  LeakyRelu
-  Concat
-  GlobalAveragePool
-  GlobalMaxPool
-  Softmax
-  Gemm
-  LRN

Some of operators are partially compatible because CoreML doesn't
support broadcasting, gemm for arbitrary tensors, etc.

License
-------

Copyright (c) 2017 Prisma Labs, Inc. All rights reserved.

Use of this source code is governed by the `MIT
License <https://opensource.org/licenses/MIT>`__ that can be found in
the LICENSE.txt file.


