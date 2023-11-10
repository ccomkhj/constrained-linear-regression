"""
Huijo Kim (huijo@hexafarms.com)
"""
import numpy as np
from sklearn.datasets import load_linnerud
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor

from constrained_linear_regression.constrained_linear_regression import (
    ConstrainedLinearRegression,
)
from constrained_linear_regression.constrained_multi_layer_perceptron import (
    ConstrainedMultilayerPerceptron,
)
from constrained_linear_regression.selective_drop_linear_regression import (
    SelectiveDropLinearRegression,
)


def test_unconstrained():
    X, Y = load_linnerud(return_X_y=True)
    y = Y[:, 0]
    model = ConstrainedLinearRegression(nonnegative=False)
    model.fit(X, y)
    baseline = LinearRegression()
    baseline.fit(X, y)
    assert model.coef_.min() < 0
    assert np.allclose(baseline.coef_, model.coef_)
    assert np.isclose(baseline.intercept_, model.intercept_)


def test_nodrop():
    X, Y = load_linnerud(return_X_y=True)
    y = Y[:, 0]
    model = SelectiveDropLinearRegression(nonnegative=False)
    model.fit(X, y)
    baseline = LinearRegression()
    baseline.fit(X, y)
    assert model.coef_.min() < 0
    assert np.allclose(baseline.coef_, model.coef_)
    assert np.isclose(baseline.intercept_, model.intercept_)


def test_positive():
    X, Y = load_linnerud(return_X_y=True)
    y = Y[:, 0]
    model = ConstrainedLinearRegression(nonnegative=True)
    model.fit(X, y)
    assert np.all(model.coef_ >= 0)


def test_constrainedmlp():
    X, Y = load_linnerud(return_X_y=True)
    y = Y[:, 0]
    min_coef = np.repeat(0, 3)
    random_state = 7
    hidden_layer_sizes = (3,)
    model = ConstrainedMultilayerPerceptron(
        hidden_layer_sizes=hidden_layer_sizes, random_state=random_state
    )
    model.fit(X, y, min_coef=min_coef)
    assert np.all(model.coefs_[0][0] >= 0)  # Not sure if the indexing is corret.


def test_unconstrainedmlp_sgd(solver="sgd"):
    X, Y = load_linnerud(return_X_y=True)
    y = Y[:, 0]
    random_state = 7
    hidden_layer_sizes = (3,)
    model = ConstrainedMultilayerPerceptron(
        solver=solver, hidden_layer_sizes=hidden_layer_sizes, random_state=random_state
    )
    model.fit(X, y)
    baseline = MLPRegressor(
        solver=solver,
        shuffle=False,
        hidden_layer_sizes=hidden_layer_sizes,
        random_state=random_state,
    )
    baseline.fit(X, y)
    for baseline_coef, model_coef in zip(baseline.coefs_, model.coefs_):
        assert np.allclose(baseline_coef, model_coef)

    for baseline_intercept, model_intercept in zip(
        baseline.intercepts_, model.intercepts_
    ):
        assert np.allclose(baseline_intercept, model_intercept)


def test_unconstrainedmlp_lbfgs(solver="lbfgs"):
    X, Y = load_linnerud(return_X_y=True)
    y = Y[:, 0]
    random_state = 7
    hidden_layer_sizes = (3,)
    model = ConstrainedMultilayerPerceptron(
        solver=solver, hidden_layer_sizes=hidden_layer_sizes, random_state=random_state
    )
    model.fit(X, y)
    baseline = MLPRegressor(
        solver=solver,
        shuffle=False,
        hidden_layer_sizes=hidden_layer_sizes,
        random_state=random_state,
    )
    baseline.fit(X, y)
    for baseline_coef, model_coef in zip(baseline.coefs_, model.coefs_):
        assert np.allclose(baseline_coef, model_coef)

    for baseline_intercept, model_intercept in zip(
        baseline.intercepts_, model.intercepts_
    ):
        assert np.allclose(baseline_intercept, model_intercept)


if __name__ == "__main__":
    test_unconstrainedmlp_lbfgs()
    # test_unconstrainedmlp_sgd()
