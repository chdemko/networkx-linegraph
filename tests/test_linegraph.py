from unittest import TestCase

import networkx as nx

import networkx_linegraph as nxlg


class TestLineGraphView(TestCase):
    def test_nodes_digraph(self):
        directed_graph = nx.DiGraph()
        directed_graph.add_edges_from([(1, 2), (2, 3), (3, 4)])
        line_graph_view = nxlg.LineGraphView(directed_graph)
        expected_node_list = [(1, 2), (2, 3), (3, 4)]
        self.assertEqual(list(line_graph_view), expected_node_list)

    def test_edges_digraph(self):
        directed_graph = nx.DiGraph()
        directed_graph.add_edges_from([(1, 2), (2, 3), (3, 4)])
        line_graph_view = nxlg.LineGraphView(directed_graph)
        expected_edge_list = [((1, 2), (2, 3)), ((2, 3), (3, 4))]
        self.assertEqual(list(line_graph_view.edges), expected_edge_list)
        self.assertEqual(len(line_graph_view.edges), 2)
        self.assertIn(((1, 2), (2, 3)), line_graph_view.edges)
        self.assertIn(((2, 3), (3, 4)), line_graph_view.edges)

    def test_len_digraph(self):
        directed_graph = nx.DiGraph()
        directed_graph.add_edges_from([(1, 2), (2, 3), (3, 4)])
        line_graph_view = nxlg.LineGraphView(directed_graph)
        self.assertEqual(len(line_graph_view), 3)

    def test_contains_digraph(self):
        directed_graph = nx.DiGraph()
        directed_graph.add_edges_from([(1, 2), (2, 3), (3, 4)])
        line_graph_view = nxlg.LineGraphView(directed_graph)
        self.assertIn((1, 2), line_graph_view)
        self.assertNotIn((4, 5), line_graph_view)

    def test_has_edge_digraph(self):
        undirected_graph = nx.DiGraph()
        undirected_graph.add_edges_from([(1, 2), (2, 3), (3, 1)])
        line_graph_view = nxlg.LineGraphView(undirected_graph)
        self.assertTrue(line_graph_view.has_edge((1, 2), (2, 3)))

    def test_neighbors_graph(self):
        undirected_graph = nx.Graph()
        undirected_graph.add_edges_from([(1, 2), (2, 3), (3, 1)])
        line_graph_view = nxlg.LineGraphView(undirected_graph)
        self.assertEqual(
            list(line_graph_view.neighbors((1, 2))),
            [(3, 1), (2, 3)],
        )
        self.assertEqual(
            len(line_graph_view.neighbors((1, 2))),
            2,
        )
        self.assertIn(
            (3, 1),
            line_graph_view.neighbors((2, 3)),
        )
        self.assertEqual(
            list(line_graph_view.neighbors((3, 1))),
            [(2, 3), (1, 2)],
        )

    def test_edges_graph(self):
        undirected_graph = nx.Graph()
        undirected_graph.add_edges_from([(1, 2), (2, 3), (3, 1)])
        line_graph_view = nxlg.LineGraphView(undirected_graph)
        expected_edge_list = [
            ((1, 2), (3, 1)),
            ((1, 2), (2, 3)),
            ((1, 3), (3, 2)),
        ]
        self.assertEqual(list(line_graph_view.edges), expected_edge_list)
        self.assertEqual(len(line_graph_view.edges), 3)
        self.assertIn(((1, 2), (3, 1)), line_graph_view.edges)
        self.assertIn(((1, 2), (2, 3)), line_graph_view.edges)
        self.assertIn(((1, 3), (3, 2)), line_graph_view.edges)
        self.assertNotIn(((1, 5), (3, 2)), line_graph_view.edges)
        self.assertNotIn(1, line_graph_view.edges)

    def test_len_graph(self):
        undirected_graph = nx.Graph()
        undirected_graph.add_edges_from([(1, 2), (2, 3), (3, 1)])
        line_graph_view = nxlg.LineGraphView(undirected_graph)
        self.assertEqual(len(line_graph_view), 3)
        self.assertEqual(line_graph_view.number_of_nodes(), 3)
        self.assertEqual(line_graph_view.order(), 3)

    def test_contains_graph(self):
        undirected_graph = nx.Graph()
        undirected_graph.add_edges_from([(1, 2), (2, 3), (3, 1)])
        line_graph_view = nxlg.LineGraphView(undirected_graph)
        self.assertIn((1, 2), line_graph_view)
        self.assertTrue(line_graph_view.has_node((1, 2)))
        self.assertNotIn((4, 5), line_graph_view)
        self.assertNotIn(4, line_graph_view)

    def test_has_edge_graph(self):
        undirected_graph = nx.Graph()
        undirected_graph.add_edges_from([(1, 2), (2, 3), (3, 1)])
        line_graph_view = nxlg.LineGraphView(undirected_graph)
        self.assertTrue(line_graph_view.has_edge((1, 2), (2, 3)))
        self.assertTrue(line_graph_view.has_edge((2, 1), (3, 2)))
        self.assertFalse(line_graph_view.has_edge((2, 1), (5, 6)))

    def test___str__(self):
        directed_graph = nx.DiGraph()
        directed_graph.add_edges_from([(1, 2), (2, 3), (3, 4)])
        line_graph_view = nxlg.LineGraphView(directed_graph)
        expected_str = "LineGraphView of DiGraph with 4 nodes and 3 edges"
        self.assertEqual(str(line_graph_view), expected_str)

    def test_is_multigraph(self):
        undirected_graph = nx.Graph()
        undirected_graph.add_edges_from([(1, 2), (2, 3), (3, 1)])
        line_graph_view = nxlg.LineGraphView(undirected_graph)
        self.assertFalse(line_graph_view.is_multigraph())
