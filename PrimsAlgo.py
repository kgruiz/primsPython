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

    i = 0

    while not allFound:

        print(f"{i=}")

        i += 1

        minDistance = float("inf")
        minVertex = None

        allFound = True

        for vertexNum, vertex in enumerate(vertices):

            print(f"{vertexNum=}")

            if vertex.minDistance < minDistance and not vertex.found:

                minDistance = vertex.minDistance
                minVertex = vertex
                vertices[vertexNum].found = True

                allFound = False

        if minVertex is not None:

            j = 0

            for edge in minVertex.edges:

                print(f"EDGE: Source: {minVertex} Destination: {edge[0]}")

                # print(f"{j=}")

                # j += 1

                destination: Vertex = edge[0]

                distance = adjacencyMatrix[minVertex, destination]

                if distance < destination.minDistance:

                    print(f"Current: {destination} Previous: {minVertex}")

                    vertices[vertices.index(destination)].previous = minVertex

    blankVertices: List[Vertex] = []

    for vertex in vertices:

        blankVertices.append(vertex.WithoutEdges())

    mstAdjancency = AdjacencyMatrix(vertices=blankVertices)

    for vertex in blankVertices:

        source = vertex.previous
        destination = vertex

        print(source)

        if source is None:

            continue

        minDistance = vertex.minDistance
        prevMinDistance = source.minDistance

        mstAdjancency.AddEdge(
            source=source, destination=destination, weight=minDistance
        )

    return mstAdjancency
