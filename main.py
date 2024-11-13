class Vertex:

    def __init__(self, label: int | str):
        self.label: int | str = label
        self.found: bool = False
        self.minDistance: float = float("infinity")
        self.previous: Vertex | None = None


if __name__ == "__main__":

    numVertices = 10
    numEdges = 20
