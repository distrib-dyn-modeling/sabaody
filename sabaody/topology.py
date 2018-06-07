# Sabaody
# Copyright 2018 Shaik Asifullah and J Kyle Medley
from __future__ import print_function, division, absolute_import

from .pygmo_interf import Island

import networkx as nx
import pygmo as pg

from itertools import chain
from abc import ABC, abstractmethod
from uuid import uuid4
import collections
from random import choice
from typing import Union, Callable

class AlgorithmCtorFactory(ABC):
    @abstractmethod
    def __call__(self,island,topology):
        pass

class Topology(nx.Graph):
    def neighbor_ids(self, id):
        return self.neighbors(id)

    def outgoing_ids(self, id):
        '''
        For an undirected topology, the outgoing ids are just
        the neighbor ids.
        '''
        return self.neighbors(id)

    def neighbor_islands(self, id):
        return tuple(self.nodes[n]['island'] for n in chain(self.successors(id),self.predecessors(id)))

class DiTopology(nx.DiGraph,Topology):
    def outgoing_ids(self, id):
        '''
        For a directed topology, the outgoing ids can be
        different from the incomming ids.
        '''
        return tuple(self.successors(id))

    def outgoing_islands(self, id):
        return tuple(self.nodes[n]['island'] for n in self.successors(id))

    def neighbor_ids(self, id):
        return tuple(chain(self.successors(id),self.predecessors(id)))

class TopologyFactory:
    def __init__(self, problem_constructor, domain_qualifier, mc_host, mc_port=11211):
        self.problem_constructor = problem_constructor
        self.domain_qualifier = domain_qualifier
        self.mc_host = mc_host
        self.mc_port = mc_port


    def _getAlgorithmConstructor(self, algorithm_factory, node, graph):
        # type: (Union[AlgorithmCtorFactory,collections.abc.Sequence,Callable[[],pg.algorithm]], int, Union[nx.Graph,nx.DiGraph]) -> Callable[[],pg.algorithm]
        '''
        If algorithm_factory is a factory, call it with the node and graph.
        If instead it is a list of constructors, choose one at random.
        If it is simply a direct constructor for a pagmo algorithm,
        just return it.
        '''
        if isinstance(algorithm_factory, AlgorithmCtorFactory):
            return algorithm_factory(node, graph)
        elif isinstance(algorithm_factory, collections.abc.Sequence):
            return choice(algorithm_factory)
        else:
            return algorithm_factory


    def _processTopology(self,raw,algorithm_factory,island_size,topology_class):
        m = dict((k,Island(str(uuid4()),
                           self.problem_constructor,
                           self._getAlgorithmConstructor(algorithm_factory,k,raw),
                           island_size,
                           self.domain_qualifier,
                           self.mc_host,
                           self.mc_port)) for k in raw.nodes)
        g = topology_class()
        g.add_nodes_from(island.id for island in m.values())
        for k,i in m.items():
            g.nodes[m[k].id]['island'] = m[k]
        g.add_edges_from((m[u].id, m[v].id)
                         for u, nbrs in raw._adj.items()
                         for v, data in nbrs.items())
        g.island_ids = tuple(id for id in g.nodes)
        g.islands = tuple(g.nodes[i]['island'] for i in g.nodes)
        return g


    def createOneWayRing(self, algorithm_factory, number_of_islands = 100, island_size = 20):
        # type: (Union[AlgorithmCtorFactory,collections.abc.Sequence,Callable[[],pg.algorithm]], int, int) -> DiTopology
        '''
        Creates a one way ring topology.
        '''
        g = self._processTopology(nx.cycle_graph(number_of_islands, create_using=nx.DiGraph()), algorithm_factory, island_size, DiTopology)
        return g


    def createBidirChain(self, algorithm_factory, number_of_islands = 100, island_size = 20):
        # type: (Callable, int, int) -> DiTopology
        '''
        Creates a linear chain topology.
        '''
        g = self._processTopology(nx.path_graph(number_of_islands, create_using=nx.Graph()), algorithm_factory, island_size, Topology)
        # label head and tail nodes
        endpoints = set()
        for n in g.nodes:
            if len(tuple(g.neighbors(n))) == 1:
                endpoints.add(n)
        g.endpoints = tuple(endpoints)
        return g


    def createLollipop(self, algorithm_factory, complete_subgraph_size = 100, chain_size = 10, island_size = 20):
        # type: (Callable, int, int, int) -> DiTopology
        '''
        Creates a topology from a lollipop graph.
        '''
        # TODO: chain should be one-way
        g = self._processTopology(nx.lollipop_graph(complete_subgraph_size, chain_size, create_using=nx.Graph()), algorithm_factory, island_size, Topology)
        # label tail nodes
        endpoints = set()
        for n in g.nodes:
            if len(tuple(g.neighbors(n))) == 1:
                endpoints.add(n)
        g.endpoints = tuple(endpoints)
        return g


    def create_12_Ring(self, algorithm_factory, number_of_islands = 100, island_size = 20):
        g = nx.Graph()
        g.add_nodes_from(range(1, number_of_islands + 1))
        for each_island in range(1, number_of_islands + 1):
            for step in range(1,3):
                to_edge = each_island + step
                if to_edge > number_of_islands:
                    to_edge = to_edge % number_of_islands
                g.add_edge(each_island,to_edge)
        g = self._processTopology(g)
        return g


    def create_123_Ring(self, algorithm_factory, number_of_islands = 100, island_size = 20):
        g = nx.Graph()
        g.add_nodes_from(range(1, number_of_islands + 1))
        for each_island in range(1, number_of_islands + 1):
            for step in range(1, 4):
                to_edge = each_island + step
                if to_edge > number_of_islands:
                    to_edge = to_edge % number_of_islands
                g.add_edge(each_island, to_edge)
        g = self._processTopology(g)
        return g


    def createFullyConnected(self, algorithm_factory, number_of_islands = 100, central_node = 1, island_size = 20):
        g = nx.Graph()
        g.add_nodes_from(range(1, number_of_islands + 1))
        all_edges = itertools.combinations(range(1,number_of_islands+1),2)
        g.add_edges_from(all_edges)
        g = self._processTopology(g)
        return  g


    def createBroadcast(self, algorithm_factory, number_of_islands = 100, central_node = 1, island_size = 20):
        g = nx.Graph()
        g.add_nodes_from(range(1, number_of_islands + 1))
        for each_island in range(1,number_of_islands+1):
            if central_node == each_island:
                continue
            g.add_edge(central_node,each_island)
        g = self._processTopology(g)
        return g








