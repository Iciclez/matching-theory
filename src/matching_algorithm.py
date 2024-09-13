import collections
import copy
import itertools


class matching_algorithm:
    def __init__(self, preferences, group_names):
        self.group_1 = dict()
        self.group_2 = dict()
        self.capacity = collections.defaultdict(int)

        for entity in preferences[group_names[0]]:
            self.group_1[entity['name']] = entity['preference']
            self.capacity[entity['name']] = entity['capacity']

        for entity in preferences[group_names[1]]:
            self.group_2[entity['name']] = entity['preference']
            self.capacity[entity['name']] = entity['capacity']

    def match(self, a, b, algorithm='deferred', verbose=False):
        match algorithm:
            case 'deferred' | 'immediate':
               return self.acceptance(a, b, algorithm, verbose)
            case 'top_trading_cycle':
                return self.top_trading_cycle(a, b, verbose)

        raise 'no such algorithm'

    def acceptance(self, a, b, algorithm='deferred', verbose=False):
        res = {k:list() for k in b.keys()}
        adq = {k:collections.deque(v) for k,v in a.items()}

        # initial proposal
        for k in adq.keys():
            for _ in range(self.capacity[k]):
                res[adq[k].popleft()].append(k)

        if verbose:
            print(res)

        while True:
            unpaired = list(map(lambda kv: kv[0], filter(lambda kv: len(kv[1]) == 0, res.items())))

            if len(unpaired) == 0:
                break

            # itertools.chain.from_iterable flattens nested lists
            # while one 'group_b' is unpaired and hasn't been proposed to by every one in 'group_a'
            currently_proposed = set(itertools.chain.from_iterable(adq.values()))
            if not any(map(lambda k: k in currently_proposed, unpaired)):
                break

            for k in res.keys():
                while len(res[k]) > self.capacity[k]:
                    # sort based on preference
                    res[k].sort(key=lambda key:b[k].index(key))
                    
                    request_to = res[k].pop()
                    request_from = adq[request_to].popleft()

                    if algorithm == 'immediate':
                        while self.capacity[request_from] == len(res[request_from]):
                            request_from = adq[request_to].popleft()

                    res[request_from].append(request_to)
                    if verbose:
                        print(res)

        return res

    def top_trading_cycle(self, a, b, verbose=False):

        if verbose:
            print('Initial', (a, b), end='\n\n')
 
        def get_cycle(prefs):
            # get the first (random) key and start looking for cycles there
            dq = collections.deque([(list(prefs.keys())[0], collections.deque([]))])
            visited = set()

            while dq:
                current_node, current_path = dq.popleft()

                # cycle found
                if current_node in visited:
                    cycles_removed = 0
                    # removes head of current_path if they do not contribute to the found cycle
                    while current_path[0] != current_node:
                        current_path.popleft()
                        cycles_removed += 1
                    return current_path, cycles_removed

                visited.add(current_node)
                
                # get the first preference of current_node
                # e.g. m1: [w1], w1: [m2]
                # when m1 is current_node, w1 is appended
                # when w1 is current_node, m2 is appended
                dq.append((prefs[current_node][0], current_path + collections.deque([current_node])))

            return None, None
        
        # e.g. [m1, w1, m3, w4] => {m1: w1, m3: w4}
        def cycle_to_pairs(cycle, cycles_removed):
            res = collections.defaultdict(list)
            while len(cycle) > 0:
                a, b = cycle.popleft(), cycle.popleft()
                if cycles_removed % 2 == 0:
                    res[a] = [b]
                else:
                    res[b] = [a]
            return res

        def join_prefs(a, b):
            for k in b.keys():
                a[k] += b[k]
            return a

        res = collections.defaultdict(list)
        capacities = copy.deepcopy(self.capacity)

        while len(a) > 0 and len(b) > 0:
            cycle, cycles_removed = get_cycle(a | b)
            assert len(cycle) % 2 == 0, 'Cycles should come in pairs.'

            if verbose:
                print('Cycle found', cycle)

            visited = set(cycle)
            res = join_prefs(res, cycle_to_pairs(cycle, cycles_removed))

            for node in visited:
                capacities[node] -= 1

            # cycles are now visited, so we need to remove them if their capacities hit 0
            a = {k:list(filter(lambda pref_item: capacities[pref_item] > 0, v)) for k,v in a.items() if capacities[k] > 0}
            b = {k:list(filter(lambda pref_item: capacities[pref_item] > 0, v)) for k,v in b.items() if capacities[k] > 0}

            if verbose:
                print('Remaining', (a, b)) 

        if verbose:
            print('\nResults:', res, end='\n\n')

        return res
