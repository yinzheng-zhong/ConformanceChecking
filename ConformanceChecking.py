import numpy as np
from Tools import Tools


class ConformanceChecking:
    NODE_LABEL = 'label'
    NODE_ID = 'id'

    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        self.printed = []

    def print_msg(self, msg):
        if msg not in self.printed:
            self.printed.append(msg)
            print(msg)

    def _get_init_marking(self):
        """
        Find the id of the initial marking
        :return: id. Type=int
        """
        index = np.argwhere(self.nodes[self.NODE_LABEL] == 'initial_marking')[0, 0]
        return self.nodes[self.NODE_ID][index]

    def check_event_observed(self, trace):
        """
        Check if all the events in the trace are available in the process model.
        :param trace: the trace that is being checking. Type=str[:]
        :return: true or false. Type=bool
        """
        for event in trace:
            if not np.isin(event, self.nodes[self.NODE_LABEL]):
                self.print_msg('Event ' + event + ' wasn\'t observed in the model.')
                return False

        return True

    def successors_ids(self, starting_node):
        """
        Find the ids of all successor nodes of an node.
        :param starting_node: the id of an node. Type=int
        :return: ids of successors. Type=int[:]
        """
        # find the indices in source
        indices = np.argwhere(self.edges['source'] == starting_node)

        return self.edges['target'][indices][:, 0]

    def id_label(self, id_):
        """
        Convert node id to node label.
        :param id_: node id. Type=int
        :return: node label. Type=str
        """
        node_index = np.argwhere(self.nodes[self.NODE_ID] == id_)[0, 0]
        # find successor
        return self.nodes[self.NODE_LABEL][node_index]

    def label_id(self, label):
        """
        Convert node label to node id.
        :param label: node label. Type=str
        :return: node id. Type=int
        """
        node_index = np.argwhere(self.nodes[self.NODE_LABEL] == label)[0, 0]
        # find successor
        return self.nodes[self.NODE_ID][node_index]

    def dfs(self, visited, starting_node, dst_event_label):
        """
        The deep first search. Used to reply the trace.
        :param visited: node ids that were visited. Type=int
        :param starting_node: the id of the starting node. Type=int
        :param dst_event_label: the event label of destination. Type=str
        :return: boolean
        """
        next_ = self.successors_ids(starting_node)
        for node_id in next_:
            if node_id not in visited:
                label = self.id_label(node_id)
                if label == dst_event_label:
                    return True
                elif label == 'tau' or label == 'place':
                    visited.append(node_id)
                    starting_node = node_id
                    if self.dfs(visited, starting_node, dst_event_label) is True:
                        return True
                else:
                    visited.append(node_id)
        return False

    def verify_trace(self, trace):
        """
        Conformance checking of a trace. Will first check if all events are observed in the model, if they are, then
        reply the trace on the model.
        :param trace: the trace that is being checking. Type=str[:]
        :return: true or false. Type=bool
        """
        if self.check_event_observed(trace):
            trace = np.concatenate((trace, ['final_marking']))

            start = self._get_init_marking()
            for i in range(len(trace)):
                if self.dfs([], [start], trace[i]) is not True:
                    self.print_msg('Failed to find the path from ' + self.id_label(start) + ' to ' + trace[i] + '.')
                    return False
                start = self.label_id(trace[i])
        else:
            return False

        return True
