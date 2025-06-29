from unittest import TestCase

import networkx as nx

import networkx_linegraph as nxlg


class TestLineGraphView(TestCase):
    def test_nodes_digraph(self):
        directed_graph = nx.DiGraph()
        directed_graph.add_edges_from([(1, 2), (2, 3), (3, 4)])
        line_graph_view = nxlg.LineGraphView(directed_graph)
        expected_node_list = [(1, 2), (2, 3), (3, 4)]
        self.assertCountEqual(list(line_graph_view), expected_node_list)

    def test_edges_digraph(self):
        directed_graph = nx.DiGraph()
        directed_graph.add_edges_from([(1, 2), (2, 3), (3, 4)])
        line_graph_view = nxlg.LineGraphView(directed_graph)
        expected_edge_list = [((1, 2), (2, 3)), ((2, 3), (3, 4))]
        self.assertEqual(list(line_graph_view.edges), expected_edge_list)

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

    def test_len_graph(self):
        undirected_graph = nx.Graph()
        undirected_graph.add_edges_from([(1, 2), (2, 3), (3, 1)])
        line_graph_view = nxlg.LineGraphView(undirected_graph)
        self.assertEqual(len(line_graph_view), 3)

    def test_contains_graph(self):
        undirected_graph = nx.Graph()
        undirected_graph.add_edges_from([(1, 2), (2, 3), (3, 1)])
        line_graph_view = nxlg.LineGraphView(undirected_graph)
        self.assertIn((1, 2), line_graph_view)
        self.assertNotIn((4, 5), line_graph_view)
