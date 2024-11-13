import random
import string
from typing import List, Set, Tuple, Union

import pandas as pd


def GetAlphabet(numVertices: int) -> list:

    if numVertices > 26:

        raise ValueError(
            "Number of vertices cannot exceed 26 (the length of the alphabet)."
        )

    return list(string.ascii_lowercase[:numVertices])


class Vertex:

    def __init__(self, label: int | str, edges: Set[Tuple["Vertex", float]] = None):

        self.label: int | str = label
        self.found: bool = False
        self.edges: Set[Vertex] = edges
        self.minDistance: float = float("infinity")
        self.previous: Vertex | None = None

    def AddEdge(self, edge: Tuple["Vertex", float]) -> None:

        if self.edges is None:

            self.edges = set()

        self.edges.add(edge)

    def __str__(self) -> str:

        return str(self.label)


class AdjacencyMatrix:

    def __init__(self, vertices: List[Vertex]):

        self.numVertices: int = len(vertices)
        self.matrix = pd.DataFrame(
            float("infinity"),
            index=[vertex.label for vertex in vertices],
            columns=[vertex.label for vertex in vertices],
            dtype=float,
        )

        for vertex in vertices:

            self.matrix.loc[vertex.label, vertex.label] = 0.0

        for vertex in vertices:

            for edge in vertex.edges:

                destination = edge[0]
                weight = edge[1]

                self.AddEdge(source=vertex, destination=destination, weight=weight)

    def GetEdge(
        self, source: Union[int, str, Vertex], destination: Union[int, str, Vertex]
    ) -> float:

        source = source.label if isinstance(source, Vertex) else source
        destination = (
            destination.label if isinstance(destination, Vertex) else destination
        )

        if not isinstance(source, (int, str)) or not isinstance(
            destination, (int, str)
        ):

            raise ValueError(
                "Source and destination labels must be integers or strings."
            )

        return self.matrix.loc[source, destination]

    def AddEdge(
        self,
        source: Union[int, str, Vertex],
        destination: Union[int, str, Vertex],
        weight: float,
    ) -> None:

        if source == destination:

            return

        source = source.label if isinstance(source, Vertex) else source
        destination = (
            destination.label if isinstance(destination, Vertex) else destination
        )

        if not isinstance(source, (int, str)) or not isinstance(
            destination, (int, str)
        ):

            raise ValueError(
                "Source and destination labels must be integers or strings."
            )

        self.matrix.loc[source, destination] = weight
        self.matrix.loc[destination, source] = weight

    def __getitem__(
        self,
        indices: Union[
            int,
            str,
            List[Union[int, str, Vertex]],
            Tuple[Union[int, str, Vertex], Union[int, str, Vertex]],
            Vertex,
        ],
    ):

        if isinstance(indices, (list, tuple)) and len(indices) == 2:

            fromIndex, toIndex = indices

            fromIndex = fromIndex.label if isinstance(fromIndex, Vertex) else fromIndex
            toIndex = toIndex.label if isinstance(toIndex, Vertex) else toIndex

            if not isinstance(fromIndex, (int, str)) or not isinstance(
                toIndex, (int, str)
            ):

                raise ValueError("Vertex labels must be integers or strings.")

            return self.matrix.loc[fromIndex, toIndex]

        elif isinstance(indices, (int, str, Vertex)):

            indices = indices.label if isinstance(indices, Vertex) else indices

            if indices not in self.matrix.index:

                raise IndexError("Vertex label out of range.")

            return self.matrix.loc[indices]

        else:

            raise TypeError(
                "Index must be an integer, string, Vertex object, or a list or tuple of two vertex labels."
            )

    def __setitem__(
        self,
        indices: Union[
            List[Union[int, str, Vertex]],
            Tuple[Union[int, str, Vertex], Union[int, str, Vertex]],
        ],
        value: int,
    ) -> None:

        if isinstance(indices, (list, tuple)) and len(indices) == 2:

            fromIndex, toIndex = indices

            fromIndex = fromIndex.label if isinstance(fromIndex, Vertex) else fromIndex
            toIndex = toIndex.label if isinstance(toIndex, Vertex) else toIndex

            if not isinstance(fromIndex, (int, str)) or not isinstance(
                toIndex, (int, str)
            ):

                raise ValueError("Vertex labels must be integers or strings.")

            self.matrix[fromIndex, toIndex] = value

        else:

            raise TypeError("Index must be a list or tuple of two vertex labels.")

    def __str__(self):

        return self.matrix.to_string()


def PrimsAlgorithm(
    adjacencyMatrix: AdjacencyMatrix, vertices: List[Vertex]
) -> List[Tuple[Vertex, Vertex, float]]:

    pass


if __name__ == "__main__":

    numVertices = 5

    labels = GetAlphabet(numVertices)

    vertices = [Vertex(label) for label in labels[:numVertices]]

    for vertexNum in range(len(vertices)):

        numedges = random.randint(1, 3)

        destinations = set()

        while len(destinations) < numedges:

            destination = random.choice(vertices)

            if destination.label == vertices[vertexNum].label:

                continue

            else:

                destinations.add(destination)

        for destination in destinations:

            weight = float(int(random.random() * random.randint(1, 1000) * 100) / 100)

            vertices[vertexNum].AddEdge((destination, weight))

    adjacencyMatrix = AdjacencyMatrix(vertices)

    print(f"Adjacency Matrix:\n{adjacencyMatrix}")
