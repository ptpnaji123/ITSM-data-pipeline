from _typeshed import Incomplete

from networkx.utils.backends import _dispatchable

@_dispatchable
def dinitz(
    G,
    s,
    t,
    capacity: str = "capacity",
    residual: Incomplete | None = None,
    value_only: bool = False,
    cutoff: Incomplete | None = None,
): ...
