import random
import string
from typing import List, Set, Tuple, Union

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

from Vertex import Vertex


class AdjacencyMatrix:
    def __init__(self, vertices: List[Vertex]):

        self.numVertices: int = len(vertices)

        labels = [vertex.label for vertex in vertices]

        self.matrix = pd.DataFrame(
            float("infinity"),
            index=labels,
            columns=labels,
            dtype=float,
        )

        for vertex in vertices:

            self.matrix.loc[vertex.label, vertex.label] = 0.0

    def NumUnconnectedNodes(self) -> int:

        numUnconnected = 0

        for index, row in self.matrix.iterrows():

            if ((row == 0) | np.isinf(row)).all():

                numUnconnected += 1

        return numUnconnected

    def NumOutgoingEdges(self, vertex: Union[int, str, Vertex]):

        label = vertex

        if isinstance(vertex, Vertex):

            label = vertex.label

        numOutgoing = 0

        for elem in self.matrix.loc[label, :]:

            if elem != 0 and not np.isinf(elem):

                numOutgoing += 1

        return numOutgoing

    def __getattr__(self, name):

        if name == "columns":
            return self.matrix.columns

        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )

    def TotalWeight(self) -> int | float:

        weightSum = 0

        for weight in self.matrix.values.flatten():

            if not np.isinf(weight):

                weightSum += weight

        return weightSum / 2

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

            raise ValueError("Vertex labels must be integers or strings.")

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
        value: float,
    ) -> None:

        if isinstance(indices, (list, tuple)) and len(indices) == 2:

            fromIndex, toIndex = indices

            fromIndex = fromIndex.label if isinstance(fromIndex, Vertex) else fromIndex
            toIndex = toIndex.label if isinstance(toIndex, Vertex) else toIndex

            if not isinstance(fromIndex, (int, str)) or not isinstance(
                toIndex, (int, str)
            ):

                raise ValueError("Vertex labels must be integers or strings.")

            self.matrix.loc[fromIndex, toIndex] = value
            self.matrix.loc[toIndex, fromIndex] = value

        else:

            raise TypeError("Index must be a list or tuple of two vertex labels.")

    def __str__(self):

        return self.matrix.to_string()
