import itertools


class singlylinkedlistnode:
    def __init__(self, value=None, tag=None, next_node=None):
        self.value = value
        self.tag = tag
        self.next_node = next_node

    def get_cycle(self):
        visited = set()
        cycle = list()

        # set current node as head
        node = self

        while node:
            if node in visited:
                while cycle[0][0] != node.value:
                    cycle.pop(0)
                return dict(cycle)

            visited.add(node)
            cycle.append((node.value, node.next_node))
            node = node.next_node

        return None


class matching_algorithm:
    def __init__(self, preferences):
        self.group_1 = dict()
        self.group_2 = dict()
        self.capacity = dict()

        for x in preferences['group_1']:
            self.group_1[x['name']] = x['preference']
            self.capacity[x['name']] = x['capacity']

        for x in preferences['group_2']:
            self.group_2[x['name']] = x['preference']
            self.capacity[x['name']] = x['capacity']

    def match(self, a, b, algorithm='deferred', verbose=False):
        
        if algorithm == 'deferred' or algorithm == 'immediate':
            return self.acceptance(a, b, algorithm, verbose)

        if algorithm == 'top_trading_cycle':
            return self.top_trading_cycle(a, b, verbose)

        raise 'no such algorithm'        
    
    def acceptance(self, a, b, algorithm='deferred', verbose=False):
        matching = dict()

        for x in b.keys():
            matching[x] = list()

        for x in a.keys():
            for _ in range(self.capacity[x]):
                matching[a[x].pop(0)].append(x)

        if verbose:
            print(matching)

        while True:
            unmatched = list(filter(lambda x: len(x[1]) == 0, matching.items()))
            # while one 'group_b' is unmatched and hasn't been proposed to by every one in'group_a'
            if not (len(unmatched) > 0 and unmatched[0][0] in list(itertools.chain.from_iterable(a.values()))):
                break

            for x in matching.keys():
                while len(matching[x]) > self.capacity[x]:
                    # sort based on preference
                    matching[x] = [name for name in b[x]
                                   if name in matching[x]]
                    name = matching[x].pop()
                    request_from = a[name].pop(0)

                    if algorithm == 'immediate':
                        while self.capacity[request_from] == len(matching[request_from]):
                            request_from = a[name].pop(0)

                    matching[request_from].append(name)
                    if verbose:
                        print(matching)

        return matching

    def top_trading_cycle(self, a, b, verbose=False):

        matching = dict()
        nodes = list()

        for x in a.keys():
            matching[x] = list()

        if verbose:
            print('Initial', (a, b), end='\n\n')

        while len(a) > 0 and len(b) > 0:
                
            for x in a.keys():
                nodes.append(singlylinkedlistnode(x, a[x].pop(0)))

            for x in b.keys():
                nodes.append(singlylinkedlistnode(x, b[x].pop(0)))

            for x in nodes:
                select = list(filter(lambda v : v.value == x.tag, nodes))
                if len(select) == 1:
                    x.next_node = select.pop(0)

            for x in range(len(nodes)):
                cycle = nodes[x].get_cycle()
                if cycle != None:
                    if verbose:
                        print('Cycle')
                    for k, v in cycle.items():
                        if verbose:
                            print((k, v.value))
                        if k in matching:
                            matching[k].append(v.value)

                    nodes = list(
                        filter(lambda v: v.value not in cycle.keys(), nodes))
                    break

            # add unused nodes (that are not part of the cycle) back
            for x in nodes:
                if x.value in a.keys():
                    a[x.value].insert(0, x.tag)
                    continue
                if x.value in b.keys():
                    b[x.value].insert(0, x.tag)
                    continue

            # purge nodes that are already at capacity
            for k, v in matching.items():
                if len(v) == self.capacity[k]:
                    a.pop(k, None)
                    for _, n in b.items():
                        if k in n:
                            n.remove(k)

            # flatten matching values
            l = list(itertools.chain.from_iterable(
                matching.values()))
            for k in list(b.keys()):
                if len(list(filter(lambda x: x == k, l))) == self.capacity[k]:
                    b.pop(k, None)
                    for _, n in a.items():
                        if k in n:
                            n.remove(k)

            nodes.clear()

            if verbose:
                print('Remaining', (a, b))
                print(matching, end='\n\n')

        return matching
