from start_link import StartLink
class Automaton:
    def __init__(self, nodes, links, string):
        self.nodes = nodes
        self.links = links
        self.node_cursors = []
        self.link_cursors = []
        for l in self.links:
            if isinstance(l, StartLink):
                self.link_cursors.append((l, 0))
        self.selected_links = True
        self.string = string
        self.steps = 0
        print('init', string)

        # visualization has 2 steps:
        # 1. standing at a node, choosing links
        # 2. traversing links, choosing nodes
        # we start by placing cursors at start links,
        # then traversing them to reach the start nodes.
    
    def step(self):
        self.steps += 1
        print(self.steps, self.selected_links)
        if self.selected_links:
            self.put_cursors_at_nodes()
        else:
            self.select_links_to_traverse()

        self.selected_links = not self.selected_links


    def put_cursors_at_nodes(self):
        self.node_cursors.clear()
        for l, word_pos in self.link_cursors:
            self.node_cursors.append((l.nodeB, word_pos))
            if word_pos == len(self.string) and l.nodeB.is_accept_state:
                l.nodeB.text = 'OK'

        self.link_cursors.clear()

    def select_links_to_traverse(self):
        outgoing_links = []
        for l in self.links:
            for n, word_pos in self.node_cursors:
                if l.nodeA is n:
                    outgoing_links.append((l, word_pos))

        self.link_cursors.clear()
        for l, word_pos in outgoing_links:
            if self.string[word_pos:].startswith(l.text):
                self.link_cursors.append( (l, word_pos + len(l.text)) )
