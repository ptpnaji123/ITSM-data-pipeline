from _typeshed import Incomplete

from networkx.utils.backends import _dispatchable

@_dispatchable
def local_node_connectivity(G, source, target, cutoff: Incomplete | None = None): ...
@_dispatchable
def node_connectivity(G, s: Incomplete | None = None, t: Incomplete | None = None): ...
@_dispatchable
def all_pairs_node_connectivity(G, nbunch: Incomplete | None = None, cutoff: Incomplete | None = None): ...
