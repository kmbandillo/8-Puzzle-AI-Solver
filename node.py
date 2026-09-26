class Node:
    def __init__(self, state, g_value=0, parent=None, action=None):
        self.state = state
        self.g = g_value
        self.parent = parent
        self.action = action