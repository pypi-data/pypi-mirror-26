from __future__ import print_function
from __future__ import absolute_import

from functools import wraps
import inspect
import os
from io import BytesIO

from flask import Flask
from flask import Response
from flask import request

from PIL import Image
import numpy as np
import bson

from .client import BSONModel

import foolbox
from . import __version__


def mnist_model_server(model, port=None):
    """Starts an HTTP server that provides access to a Foolbox MNIST model.

    Parameters
    ----------
    model : `foolbox.model.Model` instance
        The model that should be run.
    port : int
        The TCP port used by the HTTP server. Defaults to the PORT environment
        variable or 62222 if not set.
    """
    return _model_server('MNIST', model, image_size=32, port=port)


def cifar_model_server(model, channel_order, port=None):
    """Starts an HTTP server that provides access to a Foolbox CIFAR model.

    Parameters
    ----------
    model : `foolbox.model.Model` instance
        The model that should be run.
    channel_order : str
        The color channel ordering expected by the model ('RGB' or 'BGR')
    port : int
        The TCP port used by the HTTP server. Defaults to the PORT environment
        variable or 62222 if not set.

    """
    assert channel_order in ['RGB', 'BGR']
    return _model_server(
        'CIFAR', model, channel_order=channel_order, image_size=32, port=port)


def imagenet_model_server(model, channel_order, image_size, port=None):
    """Starts an HTTP server that provides access to a Foolbox model.

    Parameters
    ----------
    model : `foolbox.model.Model` instance
        The model that should be run.
    channel_order : str
        The color channel ordering expected by the model ('RGB' or 'BGR')
    image_size : int
        The image size expected by the model (e.g. 224 or 299)
    port : int
        The TCP port used by the HTTP server. Defaults to the PORT environment
        variable or 62222 if not set.

    """
    assert channel_order in ['RGB', 'BGR']
    assert isinstance(image_size, int)
    return _model_server(
        'IMAGENET', model, channel_order=channel_order,
        image_size=image_size, port=port)


def _model_server(
        dataset, model, channel_order=None, image_size=None, port=None):
    """Starts an HTTP server that provides access to a Foolbox model.

    Parameters
    ----------
    dataset : str
        The dataset the model is compatible with (MNIST, CIFAR or IMAGENET)
    model : `foolbox.model.Model` instance
        The model that should be run.
    channel_order : str
        The color channel ordering expected by the model
        (None for MNIST, 'RGB' or 'BGR' for CIFAR and ImageNet)
    image_size : int
        The image size expected by the model (for ImageNet only!)
    port : int
        The TCP port used by the HTTP server. Defaults to the PORT environment
        variable or 62222 if not set.

    """

    assert dataset in ['MNIST', 'CIFAR', 'IMAGENET']

    if port is None:
        port = os.environ.get('PORT')
    if port is None:
        port = 62222

    app = Flask(__name__)

    _batch_predictions = _wrap(
        model.batch_predictions, ['predictions'])
    _predictions_and_gradient = _wrap(
        model.predictions_and_gradient, ['predictions', 'gradient'])
    _backward = _wrap(
        model.backward, ['gradient'])

    @app.route("/")
    def main():  # pragma: no cover
        return Response(
            'Robust Vision Benchmark Model Server\n',
            mimetype='text/plain')

    @app.route("/server_version", methods=['GET'])
    def server_version():
        v = __version__
        return Response(str(v), mimetype='text/plain')

    @app.route("/dataset", methods=['GET'])
    def r_dataset():
        return Response(dataset, mimetype='text/plain')

    @app.route("/bounds", methods=['GET'])
    def bounds():
        min_, max_ = model.bounds()
        return Response(
            '{}\n{}'.format(min_, max_), mimetype='text/plain')

    @app.route("/channel_axis", methods=['GET'])
    def channel_axis():
        result = model.channel_axis()
        assert result == int(result)
        result = str(int(result))
        return Response(result, mimetype='text/plain')

    @app.route("/num_classes", methods=['GET'])
    def num_classes():
        result = model.num_classes()
        assert result == int(result)
        result = str(int(result))
        return Response(result, mimetype='text/plain')

    @app.route("/image_size", methods=['GET'])
    def r_iimage_size():
        assert int(image_size) == image_size
        return Response(str(image_size), mimetype='text/plain')

    @app.route("/channel_order", methods=['GET'])
    def r_channel_order():
        return Response(channel_order, mimetype='text/plain')

    @app.route("/batch_predictions", methods=['POST'])
    def batch_predictions():
        return _batch_predictions(request)

    @app.route("/predictions_and_gradient", methods=['POST'])
    def predictions_and_gradient():
        return _predictions_and_gradient(request)

    @app.route("/backward", methods=['POST'])
    def backward():
        return _backward(request)

    @app.route("/shutdown", methods=['GET'])
    def shutdown():
        _shutdown_server()
        return 'Shutting down ...'

    app.run(host='0.0.0.0', port=port)


def attack_server(attack, port=None):
    """Starts an HTTP server that provides access to an attack.

    Parameters
    ----------
    attack : function or other callable, e.g. a `foolbox.attack.Attack`
        The function or callable (e.g. foolbox attack) that finds
        adversarials for a given instance of the foolbox Adversarial class.
    port : int
        The TCP port used by the HTTP server. Defaults to the PORT environment
        variable or 62222 if not set.

    """

    assert attack is not None

    if port is None:
        port = os.environ.get('PORT')
    if port is None:
        port = 52222

    app = Flask(__name__)

    def _run(model_url, image, label, criterion_name):
        # transform the arguments into an Adversarial object
        model = BSONModel(model_url)
        assert criterion_name == 'Misclassification'
        criterion = foolbox.criteria.Misclassification()
        adversarial = foolbox.Adversarial(model, criterion, image, label)

        # call the attack with the adversarial object
        attack(adversarial)
        return adversarial.image

    _run = _wrap(_run, ['adversarial_image'])

    @app.route("/")
    def main():  # pragma: no cover
        return Response(
            'Robust Vision Benchmark Attack Server\n',
            mimetype='text/plain')

    @app.route("/server_version", methods=['GET'])
    def server_version():
        v = __version__
        return Response(str(v), mimetype='text/plain')

    @app.route("/run", methods=['POST'])
    def run():
        return _run(request)

    @app.route("/shutdown", methods=['GET'])
    def shutdown():
        _shutdown_server()
        return 'Shutting down ...'

    app.run(host='0.0.0.0', port=port)


def _shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:  # pragma: no cover
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def _wrap(function, output_names):
    """A decorator that converts data between flask and python / numpy"""

    try:
        # Python 3
        sig = inspect.signature(function)
        params = sig.parameters
    except AttributeError:  # pragma: no cover
        # Python 2.7
        argspec = inspect.getargspec(function)
        params = dict(zip(argspec.args, [None] * len(argspec.args)))

    @wraps(function)
    def wrapper(request):
        verbose = request.args.get('verbose', False)

        if verbose:  # pragma: no cover
            print('headers', request.headers)
            print('args', list(request.args.keys()))
            print('form keys', list(request.form.keys()))
            print('files', list(request.files.keys()))
            print('is_json', request.is_json)
            print('data length', len(request.data))

        content_type = request.headers.get('content-type', '').lower()

        if content_type == 'application/bson':
            bson_args = bson.loads(request.data)
            bson_args = _decode_arrays(bson_args)
        else:  # pragma: no cover
            bson_args = {}

        args = {}

        def add_argument(name, value):
            if name in args:  # pragma: no cover
                print('ignoring {}, argument already exists'.format(name))
                return
            if name not in params:  # pragma: no cover
                print('ignoring {}, not accepted by function'.format(name))
                return
            args[name] = value

        for name, value in bson_args.items():
            add_argument(name, value)

        for name, value in request.args.items():  # pragma: no cover
            add_argument(name, value)

        for name, value in request.form.items():  # pragma: no cover
            add_argument(name, value)

        for name, value in request.files.items():  # pragma: no cover
            if name not in params:
                continue
            data = value.read()
            param = params[name]
            if param is not None and param.annotation == Image.Image:
                data = Image.open(BytesIO(data))
            add_argument(name, data)

        result = function(**args)
        if len(output_names) == 1:
            result = {output_names[0]: result}
        else:
            assert len(result) == len(output_names)
            result = dict(zip(output_names, result))
        result = _encode_arrays(result)
        result = bson.dumps(result)
        return Response(result, mimetype='application/bson')

    return wrapper


def _encode_arrays(d):
    for key in list(d.keys()):
        if isinstance(d[key], np.ndarray):
            array = d[key]
            d[key] = {
                'type': 'array',
                'shape': array.shape,
                'dtype': array.dtype.str,
                'data': array.tobytes(),
            }
    return d


def _decode_arrays(d):
    for key in list(d.keys()):
        if hasattr(d[key], 'get') \
                and d[key].get('type') == 'array':
            shape = d[key]['shape']
            dtype = d[key]['dtype']
            data = d[key]['data']
            array = np.frombuffer(data, dtype=dtype).reshape(shape)
            d[key] = array
    return d
