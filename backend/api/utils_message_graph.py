import uuid

# Utility functions for message graph operations

def add_message_to_graph(graph, message_id, parent_id=None):
    """
    Add a new message node to the graph.
    - message_id: str (UUID)
    - parent_id: str (UUID) or None
    """
    graph = graph.copy() if graph else {}
    graph[str(message_id)] = {"parent": parent_id, "children": []}
    if parent_id:
        if parent_id not in graph:
            graph[parent_id] = {"parent": None, "children": []}
        graph[parent_id]["children"].append(str(message_id))
    return graph

def edit_message_in_graph(graph, edited_message_id, original_message_id):
    """
    Add an edited message as a sibling (fork) of the original message.
    - edited_message_id: str (UUID)
    - original_message_id: str (UUID)
    """
    graph = graph.copy() if graph else {}
    parent_id = graph.get(original_message_id, {}).get("parent")
    graph[str(edited_message_id)] = {"parent": parent_id, "children": []}
    if parent_id:
        if parent_id not in graph:
            graph[parent_id] = {"parent": None, "children": []}
        graph[parent_id]["children"].append(str(edited_message_id))
    return graph

def get_branch_from_head(graph, head_id):
    """
    Traverse the graph from head to root, returning the message chain (root to head).
    - graph: dict
    - head_id: str (UUID)
    """
    chain = []
    current = str(head_id)
    while current:
        chain.append(current)
        parent = graph.get(current, {}).get("parent")
        if parent:
            current = parent
        else:
            break
    chain.reverse()
    return chain

def get_heads(graph):
    """
    Return all message IDs that are not a parent of any other message (i.e., leaves/heads).
    """
    all_ids = set(graph.keys())
    parent_ids = set()
    for node in graph.values():
        parent_ids.update(node.get("children", []))
    return list(all_ids - parent_ids) 