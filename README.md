# networkx-linegraph

[![PyPI - Version](https://img.shields.io/pypi/v/networkx-linegraph.svg)](https://pypi.org/project/networkx-linegraph)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/networkx-linegraph.svg)](https://pypi.org/project/networkx-linegraph)

-----

A Python package to efficiently compute the [line graph](https://en.wikipedia.org/wiki/Line_graph) of a graph with [NetworkX](https://networkx.org/) via a view on the underlying graph.

Useful for graph theory, network analysis, and related applications.

## Table of Contents

- [Installation](#installation)
- [Requirements](#requirements)
- [Usage](#usage)
- [Build](#build)
- [License](#license)

## Installation

```console
pip install networkx-linegraph
```

## Requirements

- Python >= 3.11
- networkx

## Usage

```python
import networkx as nx
import networkx_linegraph as nxlg
graph = nx.cycle_graph(4)
line_graph = nxlg.LineGraphView(graph)
print(list(line_graph.edges))
line_graph.has_edge((0, 1), (1, 2))
```

## Build

Install [`hatch`](https://hatch.pypa.io/latest/install/), then:

```console
hatch build
pip install dist/networkx_linegraph-`hatch version`-py3-none-any.whl
```

## License

`networkx-linegraph` is distributed under the terms of the
[BSD 3-Clause](https://spdx.org/licenses/BSD-3-Clause.html) license.
