import pickle

import pytest

import networkx as nx
from networkx.utils.configs import Config


# Define this at module level so we can test pickling
class ExampleConfig(Config):
    """Example configuration."""

    x: int
    y: str

    def _check_config(self, key, value):
        if key == "x" and value <= 0:
            raise ValueError("x must be positive")
        if key == "y" and not isinstance(value, str):
            raise TypeError("y must be a str")


class EmptyConfig(Config):
    pass


@pytest.mark.parametrize("cfg", [EmptyConfig(), Config()])
def test_config_empty(cfg):
    assert dir(cfg) == []
    with pytest.raises(AttributeError):
        cfg.x = 1
    with pytest.raises(KeyError):
        cfg["x"] = 1
    with pytest.raises(AttributeError):
        cfg.x
    with pytest.raises(KeyError):
        cfg["x"]
    assert len(cfg) == 0
    assert "x" not in cfg
    assert cfg == cfg
    assert cfg.get("x", 2) == 2
    assert set(cfg.keys()) == set()
    assert set(cfg.values()) == set()
    assert set(cfg.items()) == set()
    cfg2 = pickle.loads(pickle.dumps(cfg))
    assert cfg == cfg2


def test_config_subclass():
    with pytest.raises(ValueError, match="x must be positive"):
        ExampleConfig(x=0, y="foo")
    with pytest.raises(AttributeError, match="Invalid config name: 'z'"):
        ExampleConfig(x=1, y="foo", z="bad config")
    with pytest.raises(AttributeError, match="Invalid config name: 'z'"):
        EmptyConfig(z="bad config")
    cfg = ExampleConfig(x=1, y="foo")
    assert cfg.x == 1
    assert cfg["x"] == 1
    assert cfg["y"] == "foo"
    assert cfg.y == "foo"
    assert "x" in cfg
    assert "y" in cfg
    assert "z" not in cfg
    assert len(cfg) == 2
    assert set(iter(cfg)) == {"x", "y"}
    assert set(cfg.keys()) == {"x", "y"}
    assert set(cfg.values()) == {1, "foo"}
    assert set(cfg.items()) == {("x", 1), ("y", "foo")}
    assert dir(cfg) == ["x", "y"]
    cfg.x = 2
    cfg["y"] = "bar"
    assert cfg["x"] == 2
    assert cfg.y == "bar"
    with pytest.raises(TypeError, match="can't be deleted"):
        del cfg.x
    with pytest.raises(TypeError, match="can't be deleted"):
        del cfg["y"]
    assert cfg.x == 2
    assert cfg == cfg
    assert cfg == ExampleConfig(x=2, y="bar")
    assert cfg != ExampleConfig(x=3, y="baz")
    assert cfg != Config(x=2, y="bar")
    with pytest.raises(TypeError, match="y must be a str"):
        cfg["y"] = 5
    with pytest.raises(ValueError, match="x must be positive"):
        cfg.x = -5
    assert cfg.get("x", 10) == 2
    with pytest.raises(AttributeError):
        cfg.z = 5
    with pytest.raises(KeyError):
        cfg["z"] = 5
    with pytest.raises(AttributeError):
        cfg.z
    with pytest.raises(KeyError):
        cfg["z"]
    cfg2 = pickle.loads(pickle.dumps(cfg))
    assert cfg == cfg2
    assert cfg.__doc__ == "Example configuration."
    assert cfg2.__doc__ == "Example configuration."


def test_nxconfig():
    assert isinstance(nx.config.backend_priority, list)
    assert isinstance(nx.config.backends, Config)
    with pytest.raises(TypeError, match="must be a list of backend names"):
        nx.config.backend_priority = "nx_loopback"
    with pytest.raises(ValueError, match="Unknown backend when setting"):
        nx.config.backend_priority = ["this_almost_certainly_is_not_a_backend"]
    with pytest.raises(TypeError, match="must be a Config of backend configs"):
        nx.config.backends = {}
    with pytest.raises(TypeError, match="must be a Config of backend configs"):
        nx.config.backends = Config(plausible_backend_name={})
    with pytest.raises(ValueError, match="Unknown backend when setting"):
        nx.config.backends = Config(this_almost_certainly_is_not_a_backend=Config())
