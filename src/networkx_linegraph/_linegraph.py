"""LineGraph module."""

from __future__ import annotations

import itertools
from collections.abc import Collection, Hashable
from functools import cached_property
from typing import TYPE_CHECKING, TypeVar, Generic

if TYPE_CHECKING:
    from collections.abc import Iterator

    from networkx import DiGraph, Graph

_N = TypeVar("_N", bound=Hashable)


class LineGraphView(Generic[_N]):
    """
    A read-only view of the line graph of a given graph.

    The line graph of a graph G is another graph L(G) that represents the adjacencies
    between edges of G. Each node in the line graph corresponds to an edge in the
    original graph, and two nodes in the line graph are adjacent if and only if their
    corresponding edges in G are incident to a common node (for undirected graphs),
    or if the target of one edge is the source of the other (for directed graphs).

    Parameters
    ----------
    graph
        The input graph for which the line graph view is constructed.

    Examples
    --------
    >>> import networkx as nx
    >>> import networkx_linegraph as nxlg
    >>> graph = nx.cycle_graph(4)
    >>> line_graph = nxlg.LineGraphView(graph)
    >>> list(line_graph.edges)
    [((0, 1), (3, 0)), ((0, 1), (1, 2)), ((0, 3), (3, 2)), ((1, 2), (2, 3))]
    >>> line_graph.has_edge((0, 1), (1, 2))
    True

    """

    def __init__(self, graph: Graph[_N] | DiGraph[_N]) -> None:
        self._graph = graph

    def __str__(self) -> str:
        """
        Return a short summary of the line graph.

        Returns
        -------
        str
            Graph information including the graph name (if any), graph type, and the
            number of nodes and edges.

        Examples
        --------
        >>> import networkx as nx
        >>> import networkx_linegraph as nxlg
        >>> graph = nx.Graph(name="foo")
        >>> str(nxlg.LineGraphView(graph))
        "LineGraphView of Graph named 'foo' with 0 nodes and 0 edges"
        >>> graph = nx.path_graph(3)
        >>> str(nxlg.LineGraphView(graph))
        'LineGraphView of Graph with 3 nodes and 2 edges'

        """
        return f"{type(self).__name__} of {self._graph}"

    def __iter__(self) -> Iterator[tuple[_N, _N]]:
        """
        Return an iterator over the edges of the underlying graph.

        Returns
        -------
        Iterator[tuple[_N, _N]]
            Tuples representing the edges of the graph, where each element is a node.

        Examples
        --------
        >>> import networkx as nx
        >>> import networkx_linegraph as nxlg
        >>> graph = nx.path_graph(4)
        >>> line_graph = nxlg.LineGraphView(graph)
        >>> [node for node in line_graph]
        [(0, 1), (1, 2), (2, 3)]
        >>> list(line_graph)
        [(0, 1), (1, 2), (2, 3)]
        """

        return iter(self._graph.edges)

    def __contains__(self, node: object) -> bool:
        """
        Return True if the given node (edge tuple) is present in the line graph.

        A node in the line graph corresponds to an edge in the original graph.
        This method checks if the provided node (expected to be a tuple representing
        an edge) exists as an edge in the underlying graph.

        Parameters
        ----------
        node
            The node to check for membership in the line graph.
            Typically, this should be a tuple representing an edge in the
            original graph.

        Returns
        -------
        bool
            True if node is in the line graph, False otherwise.
            Use: 'node in line_graph'.

        Examples
        --------
        >>> import networkx as nx
        >>> import networkx_linegraph as nxlg
        >>> graph = nx.path_graph(4)
        >>> line_graph = nxlg.LineGraphView(graph)
        >>> (0, 1) in line_graph
        True
        >>> (1, 0) in line_graph
        True
        >>> 0 in line_graph
        False

        """
        try:
            return self._graph.has_edge(*node)  # type: ignore[no-any-return]
        except TypeError:
            return False

    def __len__(self) -> int:
        """
        Return the number of nodes in the line graph. Use: 'len(line_graph)'.

        Returns
        -------
        int
            The number of nodes in the line graph, which corresponds to the number of
            edges in the original graph.

        See Also
        --------
        number_of_nodes: identical method
        order: identical method

        Examples
        --------
        >>> import networkx as nx
        >>> import networkx_linegraph as nxlg
        >>> graph = nx.path_graph(4)
        >>> line_graph = nxlg.LineGraphView(graph)
        >>> len(line_graph)
        3
        """
        return len(self._graph.edges)

    def number_of_nodes(self) -> int:
        """
        Return the number of nodes in the line graph.

        Use: 'line_graph.number_of_nodes()'.

        Returns
        -------
        int
            The number of nodes in the line graph, which corresponds to the number of
            edges in the original graph.

        See Also
        --------
        order: identical method
        __len__: identical method

        Examples
        --------
        >>> import networkx as nx
        >>> import networkx_linegraph as nxlg
        >>> graph = nx.path_graph(4)
        >>> line_graph = nxlg.LineGraphView(graph)
        >>> line_graph.number_of_nodes()
        3
        """
        return len(self._graph.edges)

    def order(self) -> int:
        """
        Return the number of nodes in the line graph. Use: 'line_graph.order()'.

        Returns
        -------
        int
            The number of nodes in the line graph, which corresponds to the number of
            edges in the original graph.

        See Also
        --------
        number_of_nodes: identical method
        __len__: identical method

        Examples
        --------
        >>> import networkx as nx
        >>> import networkx_linegraph as nxlg
        >>> graph = nx.path_graph(4)
        >>> line_graph = nxlg.LineGraphView(graph)
        >>> line_graph.order()
        3
        """
        return len(self._graph.edges)

    def has_node(self, node: tuple[_N, _N]) -> bool:
        """
        Return True if the line graph contains the specified node.

        This method checks whether the given node exists in the line graph. It is
        functionally equivalent to using the `in` operator on the line graph instance.

        Parameters
        ----------
        node
            The node to test for membership in the line graph.

        Returns
        -------
        bool
            True if the node is in the line graph, False otherwise.


        Examples
        --------
        >>> import networkx as nx
        >>> import networkx_linegraph as nxlg
        >>> graph = nx.path_graph(4)
        >>> line_graph = nxlg.LineGraphView(graph)
        >>> line_graph.has_node((0, 1))
        True

        It is more readable and simpler to use

        >>> (0, 1) in line_graph
        True

        """
        return node in self

    def has_edge(self, node: tuple[_N, _N], other: tuple[_N, _N]) -> bool:
        """
        Return True if the edge (node, other) is in the line graph.

        Parameters
        ----------
        node, other
            node and other are pairs of nodes representing edges in the original graph.

        Returns
        -------
        bool
            True if the edge (node, other) exists in the line graph, False otherwise.

        Examples
        --------
        >>> import networkx as nx
        >>> import networkx_linegraph as nxlg
        >>> graph = nx.path_graph(4)
        >>> line_graph = nxlg.LineGraphView(graph)
        >>> line_graph.has_node((0, 1))
        True
        >>> line_graph.has_node((1, 2))
        True
        >>> line_graph.has_edge((0, 1), (1, 2))  # using two nodes
        True
        >>> e = ((0, 1), (1, 2))
        >>> line_graph.has_edge(*e)  #  e is a 2-tuple (node, other)
        True

        Notes
        -----
        In a line graph, nodes represent edges of the original graph. An edge exists
        between two nodes (edges of the original graph) if they are consecutive
        (share a node) in the original graph. For directed graphs, the edge
        (node, other) exists if the target of node is the source of other.

        """
        if node in self._graph.edges and other in self._graph.edges:
            if self.is_directed():
                return node[1] == other[0]
            return len(set(node) & set(other)) == 1
        return False

    def neighbors(self, node: tuple[_N, _N]) -> Collection[tuple[_N, _N]]:
        """
        Returns the neighbors of node.

        Parameters
        ----------
        node
           A node in the line graph

        Returns
        -------
        Collection[tuple[_N, _N]]
            A collection of neighboring nodes in the line graph, where each neighbor
            is a tuple representing an edge in the original graph.

        Examples
        --------
        >>> import networkx as nx
        >>> import networkx_linegraph as nxlg
        >>> # Graph case
        >>> graph = nx.path_graph(4)
        >>> line_graph = nxlg.LineGraphView(graph)
        >>> list(line_graph)
        [(0, 1), (1, 2), (2, 3)]
        >>> neighbors = line_graph.neighbors((0, 1))
        >>> (1, 2) in neighbors
        True
        >>> len(neighbors)
        1
        >>> list(neighbors)
        [(1, 2)]
        >>> neighbors = line_graph.neighbors((1, 2))
        >>> (2, 3) in neighbors
        True
        >>> len(neighbors)
        2
        >>> list(neighbors)
        [(0, 1), (2, 3)]
        >>> # DiGraph case
        >>> digraph = nx.path_graph(4, create_using=nx.DiGraph)
        >>> line_graph = nxlg.LineGraphView(digraph)
        >>> list(line_graph)
        [(0, 1), (1, 2), (2, 3)]
        >>> neighbors = line_graph.neighbors((0, 1))
        >>> (1, 2) in neighbors
        True
        >>> len(neighbors)
        1
        >>> list(neighbors)
        [(1, 2)]
        >>> neighbors = line_graph.neighbors((1, 2))
        >>> (2, 3) in neighbors
        True
        >>> len(neighbors)
        1
        >>> list(neighbors)
        [(2, 3)]

        """

        class Neighbors:
            """
            A collection representing the neighbors of a node in a line graph.

            This class provides a read-only view of the neighboring nodes (edges)
            for a given node (edge) in the line graph.

            It implements the Collection interface, supporting membership tests,
            iteration, and length queries.

            Notes
            -----
            - For directed graphs, neighbors are determined by outgoing edges from the
              target node of the current edge.
            - For undirected graphs, neighbors are determined by all edges incident to
              either endpoint of the current edge, excluding the current edge itself.
            """

            def __repr__(self) -> str:
                return f"<{self.__class__.__name__} object at 0x{id(self):x}>"

            def __contains__(self, other: object) -> bool:
                return line_graph.has_edge(node, other)  # type: ignore[arg-type]

            def __len__(self) -> int:
                if line_graph.is_directed():
                    return len(line_graph.graph.adj[node[1]])
                return (
                    len(line_graph.graph.adj[node[0]])
                    + len(line_graph.graph.adj[node[1]])
                    - 2
                )

            def __iter__(self) -> Iterator[tuple[_N, _N]]:
                if line_graph.is_directed():
                    return ((node[1], dest) for dest in line_graph.graph.adj[node[1]])
                return itertools.chain(
                    (
                        (src, node[0])
                        for src in line_graph.graph.adj[node[0]]
                        if {node[0], src} != set(node)
                    ),
                    (
                        (node[1], dest)
                        for dest in line_graph.graph.adj[node[1]]
                        if {node[1], dest} != set(node)
                    ),
                )

        line_graph = self
        return Neighbors()

    @cached_property
    def edges(self) -> Collection[tuple[tuple[_N, _N], tuple[_N, _N]]]:
        """
        Get a collection-like view of the line graph edges.

        The returned object supports membership testing, iteration, and length queries,
        providing an interface similar to a set of edges. Each edge is represented as a
        tuple of two edges from the original graph, corresponding to adjacent edges in
        the line graph.

        Returns
        -------
        Collection[tuple[tuple[_N, _N], tuple[_N, _N]]]
            A view of edges.

        Examples
        --------
        >>> import networkx as nx
        >>> import networkx_linegraph as nxlg
        >>> # Graph case
        >>> graph = nx.path_graph(4)
        >>> line_graph = nxlg.LineGraphView(graph)
        >>> list(line_graph)
        [(0, 1), (1, 2), (2, 3)]
        >>> line_graph.edges
        <Edges object at 0x...>
        >>> ((0, 1), (1, 2)) in line_graph.edges
        True
        >>> ((0, 1), (2, 3)) in line_graph.edges
        False
        >>> "a" in line_graph.edges
        False
        >>>
        >>> len(line_graph.edges)
        2
        >>> list(line_graph.edges)
        [((0, 1), (1, 2)), ((1, 2), (2, 3))]
        >>> # DiGraph case
        >>> digraph = nx.path_graph(4, create_using=nx.DiGraph)
        >>> line_graph = nxlg.LineGraphView(digraph)
        >>> list(line_graph)
        [(0, 1), (1, 2), (2, 3)]
        >>> line_graph.edges
        <Edges object at 0x...>
        >>> ((0, 1), (1, 2)) in line_graph.edges
        True
        >>> ((0, 1), (2, 3)) in line_graph.edges
        False
        >>> "a" in line_graph.edges
        False
        >>>
        >>> len(line_graph.edges)
        2

        """

        class Edges:
            """
            A collection-like view of the edges in the line graph.

            This class provides methods to inspect and iterate over the edges of a
            line graph, supporting both directed and undirected graphs. Edges are
            represented as pairs of edges from the original graph, corresponding to
            adjacent edges in the line graph.

            Notes
            -----
            - For directed graphs, edges are represented as pairs of edges where the
              second edge starts where the first edge ends.
            - For undirected graphs, edges are represented as pairs of edges that share
              a common node.
            """

            def __repr__(self) -> str:
                return f"<{self.__class__.__name__} object at 0x{id(self):x}>"

            def __contains__(self, edge: object) -> bool:
                try:
                    if edge[0] in line_graph and edge[1] in line_graph:  # type: ignore[index]
                        if line_graph.is_directed():
                            return edge[0][1] == edge[1][0]  # type: ignore[index, no-any-return]
                        return len(set(edge[0]) & set(edge[1])) == 1  # type: ignore[index]
                    return False  # noqa: TRY300
                except TypeError:
                    return False

            def __iter__(self) -> Iterator[tuple[tuple[_N, _N], tuple[_N, _N]]]:
                if line_graph.is_directed():
                    for node in line_graph:
                        for dest in line_graph.neighbors(node):
                            yield node, dest
                else:
                    generated = set()
                    for node in line_graph:
                        for dest in line_graph.neighbors(node):
                            edge = frozenset([frozenset(node), frozenset(dest)])
                            if edge not in generated:
                                generated.add(edge)
                                yield node, dest

            def __len__(self) -> int:
                if line_graph.is_directed():
                    return sum(len(line_graph.neighbors(node)) for node in line_graph)
                return sum(len(line_graph.neighbors(node)) for node in line_graph) // 2

        line_graph = self
        return Edges()

    # noinspection PyMethodMayBeStatic
    def is_multigraph(self) -> bool:
        """
        Test multigraph property.

        Returns
        -------
        bool
            True if the line graph graph is a multigraph, False otherwise
        """
        return False

    def is_directed(self) -> bool:
        """
        Test directed property.

        Returns
        -------
        bool
            True if the line graph is directed, False otherwise."""
        return self._graph.is_directed()  # type: ignore[no-any-return]

    @property
    def graph(self) -> Graph[_N] | DiGraph[_N]:
        """
        Get the underlying graph.

        Returns
        -------
        Graph | DiGraph
            The underlying graph

        """
        return self._graph
