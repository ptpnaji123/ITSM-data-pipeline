from _typeshed import Incomplete
from collections.abc import Generator

from networkx.utils.backends import _dispatchable

@_dispatchable
def node_attribute_xy(G, attribute, nodes: Incomplete | None = None) -> Generator[Incomplete, None, None]: ...
@_dispatchable
def node_degree_xy(
    G, x: str = "out", y: str = "in", weight: Incomplete | None = None, nodes: Incomplete | None = None
) -> Generator[Incomplete, None, None]: ...
