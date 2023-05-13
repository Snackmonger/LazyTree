class LazyTree():

    '''
    The class navigates a tree structure in which each node may have
    an unlimited number of child nodes, but only one parent node.
    Nodes are ultimately stored as a list of dictionaries, so this system is 
    really just meant as a lazy way to handle a small number of nodes in a 
    tree-like structure. The more nodes in a tree, the slower it will run,
    and it's totally unsuitable for any large-scale data set.

    - Needs to be customized in a subclass to add functionality and vailidation!-

    By default nodes should be formatted like this:
        self.node_list = [{'SYMBOL': 'node_01', 'PARENT NODE': 'ROOT'}, {'SYMBOL': 'node_02', 'PARENT NODE': 'node_01'}]

        SYMBOL = unique ID to find the node (MUST be unique or the tree will break)
        PARENT NODE = the single node that governs one or more dependant nodes

    addParameterToNode() 
        add additional parameters as {key:value} for your use case, 
        depending on what the node is supposed to represent.
            
    detatchNode() 
        detatch a node and all of its children from the tree.

    removeNode() 
        transfer all of a node's children to its own parent, and then detatch the node.

    getSiblings()
        return a list of all nodes that share a parent with the specified node

    getNodeDepth()
        return the number of nodes from the selected node to the root node (inclusive)

    getNodePathway()
        return a list of nodes from the selected node to the root node (inclusive)
    
    '''

    def __init__(self, node_list=None, root_node=None, current_node=None, previous_node=None):
        self.node_list = []
        if node_list is not None:
            self.node_list = node_list
        self.root_node = root_node
        self.current_node = current_node
        self.previous_node = previous_node


    def addNodeList(self, node_list) -> None:
        self.node_list = node_list


    def setCurrentNode(self, new_current_node) -> None:
        if self.current_node is not None:
            self.previous_node = self.current_node
        self.current_node = new_current_node


    def setRoot(self, new_root) -> None:
        self.root_node = new_root


    def getParentOfNode(self, node_symbol) -> str:
        for node in self.node_list:
            if node['SYMBOL'] == node_symbol:
                return node['PARENT NODE']


    def getChildrenOfNode(self, node_symbol) -> list:
        children = []
        for node in self.node_list:
            if node['PARENT NODE'] == node_symbol:
                children.append(node['SYMBOL'])
        return children


    def getParentOfCurrentNode(self) -> str:
        return self.getParentOfNode(self.current_node)


    def getChildrenOfCurrentNode(self) -> list:
        return self.getChildrenOfNode(self.current_node)
        

    def goToParentOfCurrentNode(self) -> None:
        for node in self.node_list:
            if node['SYMBOL'] == self.current_node:
                self.previous_node = self.current_node
                self.current_node = node['PARENT NODE']


    def goToPreviousNode(self) -> None:
        # By default, previous_node is set to None.
        # Changing the current_node will update the previous_node.

        # Reminder to self: I wrote it this way in case we set a current_node
        # that doesn't follow the tree structure, where the previous node would
        # logically always be the same as the parent node. 

        # Note: Currently only preserves the last visited node, but could
        # make a list of previous nodes and pop LIFO until they run out.
        new_current_node = self.previous_node
        self.previous_node = self.current_node
        self.current_node = new_current_node


    def addNode(self, node_symbol, node_parent) -> None:
        node_data = {}
        node_data.update({'SYMBOL': node_symbol, 'PARENT NODE': node_parent})
        self.node_list.append(node_data)


    def addParameterToNode(self, node_symbol, key_value_pair) -> None:
        for node in self.node_list:
            if node['SYMBOL'] == node_symbol:
                # If the key already exists in the node's parameters, it will be overwritten here.
                # Maybe this should be avoided, but don't optimize until there's a reason to do so?
                node.update(key_value_pair)


    def detatchNode(self, node_symbol) -> None:
        for node in self.node_list:
            if node['SYMBOL'] == node_symbol:
                node['PARENT NODE'] = 'DETATCHED'


    def removeNode(self, node_symbol) -> None:
        children = self.getChildrenOfNode(node_symbol)
        parent = self.getParentOfNode(node_symbol)
        for child in children:
            for node in self.node_list:
                if node['SYMBOL'] == child:
                    node['PARENT NODE'] = parent
        self.detatchNode(node_symbol)
     

    def getNodePathway(self, node_symbol) -> list:
        node_pathway = []
        found_root = False
        while found_root == False:
            for node in self.node_list:
                if node['SYMBOL'] == node_symbol:
                    node_pathway.append(node['SYMBOL'])
                    node_symbol = node['PARENT NODE']
                    if node['PARENT NODE'] == 'ROOT':
                        node_pathway.append('ROOT')
                        found_root = True
        return node_pathway


    def getNodeDepth(self, node_symbol) -> int:
        node_pathway = self.getNodePathway(node_symbol)
        node_depth = len(node_pathway)
        return node_depth


    def getSiblings(self, node_symbol):
        for node in self.node_list:
            if node['SYMBOL'] == node_symbol:
                siblings = self.getChildrenOfNode(node['PARENT NODE'])
        return siblings







    