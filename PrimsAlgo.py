from typing import List, Set, Tuple, Union

from numpy import isinf

from AdjMatrix import AdjacencyMatrix
from Vertex import Vertex

# Set starting point dv to 0.
# Loop v times (until every kv is true):
# 1. From the set of vertices for which kv is
# false, select the vertex v having the
# smallest tentative distance dv.
# 2. Set kv to true.
# 3. For each vertex w adjacent to v for
# which kw is false, test whether dw is
# greater than distance(v,w). If it is,
# set dw to distance(v,w) and set pw to v.


def PrimsAlgorithm(
    adjacencyMatrix: AdjacencyMatrix, vertices: List[Vertex]
) -> List[Tuple[Vertex, Vertex, float]]:

    vertices[0].minDistance = 0

    minDistance = float("inf")
    minVertex = None

    allFound = False

    nonFound = [None]

    while len(nonFound) > 0:

        nonFound = [vertex for vertex in vertices if not vertex.found]

        minDistance = float("inf")
        minVertex = None

        for vertex in nonFound:

            if vertex.minDistance < minDistance:

                minDistance = vertex.minDistance
                minVertex = vertex

        if minVertex is not None:

            vertices[vertices.index(minVertex)].found = True

            minVertexConnections = adjacencyMatrix[minVertex]

            for destinationName, weight in zip(
                adjacencyMatrix.columns, minVertexConnections
            ):

                destination = vertices[vertices.index(Vertex(destinationName))]

                if (
                    weight < destination.minDistance
                    and weight != 0
                    and not isinf(weight)
                    and not destination.found
                ):

                    destination.minDistance = weight
                    destination.previous = vertices[vertices.index(minVertex)]

    mstAdjancency = AdjacencyMatrix(vertices=vertices)

    for vertex in vertices:

        source = vertex.previous
        destination = vertex

        if source is None:

            continue

        minDistance = vertex.minDistance

        mstAdjancency.AddEdge(
            source=source, destination=destination, weight=minDistance
        )

    return mstAdjancency
