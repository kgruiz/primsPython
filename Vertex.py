from typing import List, Set, Tuple, Union


class Vertex:
    def __init__(self, label: Union[int, str]):

        self.label: Union[int, str] = label
        self.found: bool = False
        self.minDistance: float = float("infinity")
        self.previous: Union["Vertex", None] = None

    def __eq__(self, otherVertex: "Vertex"):

        return self.label == otherVertex.label

    def __str__(self) -> str:

        return str(self.label)

    def __repr__(self):

        return f"Vertex {str(self.label)}"
