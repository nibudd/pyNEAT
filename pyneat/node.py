class Node:
    def __init__(self, id: int, parents: list['Node']=None, children: list['Node']=None):
        self.id = id
        self.parents = parents if parents else []
        self.children = children if children else []

    def add_child(self, child: 'Node') -> None:
        self.children.append(child)
        child.parents.append(self)

    def add_parent(self, parent: 'Node') -> None:
        self.parents.append(parent)
        parent.children.append(self)

    def unlink_child(self, child: 'Node') -> None:
        self.children = [c for c in self.children if c is not child]
        child.parents = [p for p in child.parents if p is not self]

    def unlink_parent(self, parent: 'Node') -> None:
        self.parents = [p for p in self.parents if p is not parent]
        parent.children = [c for c in parent.children if c is not self]

    def has_parents(self) -> bool:
        return len(self.parents) > 0

    def has_children(self) -> bool:
        return len(self.children) > 0

    def __repr__(self) -> str:
        children_list = ", ".join([str(c.id) for c in self.children])
        parents_list = ", ".join([str(p.id) for p in self.parents])
        return f"Node(id={str(self.id)}, parents=[{parents_list}], children=[{children_list}])"
