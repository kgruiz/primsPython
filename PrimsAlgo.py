from typing import List, Set, Tuple, Union

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

    while not allFound:

        minDistance = float("inf")
        minVertex = None

        allFound = True

        for vertexNum, vertex in enumerate(vertices):

            if vertex.minDistance < minDistance and not vertex.found:

                minDistance = vertex.minDistance
                minVertex = vertex
                vertices[vertexNum].found = True

                allFound = False

        if minVertex is not None:

            minVertexConnections = adjacencyMatrix[minVertex]

            for destinationName, weight in zip(
                adjacencyMatrix.matrix.columns, minVertexConnections
            ):

                destination = vertices[vertices.index(Vertex(destinationName))]

                distance = adjacencyMatrix[minVertex, destination]

                if distance < destination.minDistance:

                    vertices[vertices.index(destination)].previous = minVertex
                    vertices[vertices.index(destination)].minDistance = distance

    mstAdjancency = AdjacencyMatrix(vertices=vertices)

    for vertex in vertices:

        print(f"Adding Edges")

        source = vertex.previous
        destination = vertex

        if source is None:

            continue

        print(f"\n\nNOT CONTINUING\n\n")

        minDistance = vertex.minDistance
        prevMinDistance = source.minDistance

        print(source)

        print(destination)

        print(minDistance)

        print("\n\n")

        mstAdjancency.AddEdge(
            source=source, destination=destination, weight=minDistance
        )

    return mstAdjancency
