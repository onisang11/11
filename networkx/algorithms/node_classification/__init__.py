""" This module provides the functions for node classification problem.

The functions in this module are not imported
into the top level `networkx` namespace.
You can access these functions by importing
the `networkx.algorithms.node_classification` modules,
then accessing the functions as attributes of `node_classification`.
For example:

  >>> from networkx.algorithms import node_classification
  >>> G = nx.path_graph(4)
  >>> G.edges()
  EdgeView([(0, 1), (1, 2), (2, 3)])
  >>> G.nodes[0]["label"] = "A"
  >>> G.nodes[3]["label"] = "B"
  >>> node_classification.harmonic_function(G)
  ['A', 'A', 'B', 'B']

"""
__private__ = ["tests"]


def lazy_import(module_name, submodules, submod_attrs):
    import sys
    import importlib
    import importlib.util

    all_funcs = []
    for mod, funcs in submod_attrs.items():
        all_funcs.extend(funcs)
    name_to_submod = {
        func: mod for mod, funcs in submod_attrs.items() for func in funcs
    }

    def require(fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]
        spec = importlib.util.find_spec(fullname)
        try:
            module = importlib.util.module_from_spec(spec)
        except Exception:
            raise ImportError(
                "Could not lazy import module {fullname}".format(fullname=fullname)
            ) from None
        loader = importlib.util.LazyLoader(spec.loader)
        sys.modules[fullname] = module
        loader.exec_module(module)
        return module

    def __getattr__(name):
        if name in submodules:
            fullname = "{module_name}.{name}".format(module_name=module_name, name=name)
            attr = require(fullname)
        elif name in name_to_submod:
            modname = name_to_submod[name]
            module = importlib.import_module(
                "{module_name}.{modname}".format(
                    module_name=module_name, modname=modname
                )
            )
            attr = getattr(module, name)
        else:
            raise AttributeError(
                "No {module_name} attribute {name}".format(
                    module_name=module_name, name=name
                )
            )
        globals()[name] = attr
        return attr

    return __getattr__


__getattr__ = lazy_import(
    __name__,
    submodules={
        "hmn",
        "lgc",
        "tests",
        "utils",
    },
    submod_attrs={
        "hmn": [
            "harmonic_function",
        ],
        "lgc": [
            "local_and_global_consistency",
        ],
    },
)


def __dir__():
    return __all__


__all__ = [
    "harmonic_function",
    "hmn",
    "lgc",
    "local_and_global_consistency",
    "tests",
    "utils",
]
