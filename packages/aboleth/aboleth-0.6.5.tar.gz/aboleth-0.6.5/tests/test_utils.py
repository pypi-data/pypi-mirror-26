"""Test the aboleth utilities."""

from types import GeneratorType

import numpy as np
import tensorflow as tf

import aboleth as ab


def test_batch():
    """Test the batch feed dict generator."""
    X = np.arange(100)
    fd = {'X': X}

    data = ab.batch(fd, batch_size=10, n_iter=10)

    # Make sure this is a generator
    assert isinstance(data, GeneratorType)

    # Make sure we get a dict back of a length we expect
    d = next(data)
    assert isinstance(d, dict)
    assert 'X' in d
    assert len(d['X']) == 10

    # Test we get all of X back in one sweep of the data
    accum = list(d['X'])
    for ds in data:
        assert len(ds['X']) == 10
        accum.extend(list(ds['X']))

    assert len(accum) == len(X)
    assert set(X) == set(accum)


def test_batch_predict():
    """Test the batch prediction feed dict generator."""
    X = np.arange(100)
    fd = {'X': X}

    data = ab.batch_prediction(fd, batch_size=10)

    # Make sure this is a generator
    assert isinstance(data, GeneratorType)

    # Make sure we get a dict back of a length we expect with correct indices
    for ind, d in data:
        assert isinstance(d, dict)
        assert 'X' in d
        assert len(d['X']) == 10
        assert all(X[ind] == d['X'])


def test_predict_samples():
    """Test the predict_samples aggregator."""
    X = np.ones((10, 100, 1), dtype=np.float32)
    X_ = tf.placeholder(tf.float32, (10, None, 1))
    Xt = tf.identity(X_)

    tc = tf.test.TestCase()
    with tc.test_session():
        samps = ab.predict_samples(Xt, {X_: X}, n_groups=10)  # 10 replicates
        assert samps.shape == (100, 100, 1)
        assert np.allclose(samps, 1.)


def test_predict_expected():
    """Test the predict_expected computation."""
    X = np.ones((10, 100, 1), dtype=np.float32)
    X_ = tf.placeholder(tf.float32, (10, None, 1))
    Xt = tf.identity(X_)

    tc = tf.test.TestCase()
    with tc.test_session():
        samps = ab.predict_expected(Xt, {X_: X}, n_groups=10)  # 10 replicates
        assert samps.shape == (100, 1)
        assert np.allclose(samps, np.ones((100, 1)))  # test average on axis 0
