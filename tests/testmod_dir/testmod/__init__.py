import funcnodes as fn


@fn.NodeDecorator(
    node_id="testmod.node2test",
)
def node2test():
    pass


@fn.NodeDecorator(
    node_id="testmod.node2ignore",
)
def node2ignore():
    pass


NODE_SHELF = fn.Shelf(
    nodes=[
        node2test,
        node2ignore,
    ],
    name="Testmod",
    description="The nodes of Testmod package",
    subshelves=[],
)
