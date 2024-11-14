import random
import string
from typing import List, Set, Tuple, Union

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

from AdjMatrix import AdjacencyMatrix
from PrimsAlgo import PrimsAlgorithm
from Vertex import Vertex


def GetAlphabet(numVertices: int) -> list:

    if numVertices > 26:

        raise ValueError(
            "Number of vertices cannot exceed 26 (the length of the alphabet)."
        )

    return list(string.ascii_lowercase[:numVertices])


def RandomGraph(
    numVertices: int, filledPercent: float
) -> Tuple[AdjacencyMatrix, List[Vertex]]:

    labels = GetAlphabet(numVertices)
    vertices = [Vertex(label) for label in labels[:numVertices]]

    numPossibleEdges = numVertices * (numVertices - 1) // 2
    numEdges = int(numPossibleEdges * filledPercent)

    possiblePairs = [
        (vertices[i], vertices[j])
        for i in range(numVertices)
        for j in range(i + 1, numVertices)
    ]

    random.shuffle(possiblePairs)

    selectedPairs = possiblePairs[:numEdges]

    adjacencyMatrix = AdjacencyMatrix(vertices)

    for pair in selectedPairs:

        source, destination = pair

        weight = int(round(random.uniform(1, 1000), 2))

        adjacencyMatrix.AddEdge(source=source, destination=destination, weight=weight)

    if adjacencyMatrix.NumUnconnectedNodes() > 0:

        for vertex in vertices:

            if adjacencyMatrix.NumOutgoingEdges(vertex=vertex) == 0:

                destination = random.choice([v for v in vertices if v != vertex])

                weight = int(round(random.uniform(1, 1000), 2))

                adjacencyMatrix.AddEdge(
                    source=vertex, destination=destination, weight=weight
                )

    return adjacencyMatrix, vertices


def DrawGraph(adjacencyMatrix: AdjacencyMatrix, vertices: List[Vertex], saveName: str):

    matrix = adjacencyMatrix.matrix
    rowIndices = matrix.index.tolist()
    colNames = matrix.columns.tolist()

    graph = nx.Graph()

    for vertex in vertices:

        graph.add_node(vertex.label)

    for rowName in rowIndices:

        for colName in colNames:

            weight = matrix.loc[rowName, colName]

            if weight == float("infinity") or rowName == colName:
                continue

            elif not graph.has_edge(rowName, colName):

                graph.add_edge(rowName, colName, label=str(int(weight)))

    pos = nx.spring_layout(graph, seed=141)

    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color="lightblue",
        font_weight="bold",
        edge_color="gray",
        node_size=500,
    )

    edgeLabels = nx.get_edge_attributes(graph, "label")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edgeLabels)

    plt.savefig(f"{saveName}.png", format="png")
    plt.clf()


if __name__ == "__main__":

    random.seed(141)

    adjacencyMatrix, vertices = RandomGraph(numVertices=10, filledPercent=0.3)

    DrawGraph(adjacencyMatrix=adjacencyMatrix, vertices=vertices, saveName="zoriginal")

    print(f"Adjacency Matrix:\n{adjacencyMatrix}")

    print(f"Total Weight Original: {adjacencyMatrix.TotalWeight()}")

    mstAdjacency: AdjacencyMatrix = PrimsAlgorithm(
        adjacencyMatrix=adjacencyMatrix, vertices=vertices
    )

    DrawGraph(adjacencyMatrix=mstAdjacency, vertices=vertices, saveName="zmst")

    print(f"MST Adjacency Matrix:\n{mstAdjacency}")

    print(f"Total Weight MST: {mstAdjacency.TotalWeight()}")
