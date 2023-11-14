from collections import deque

class Path:
    def __init__(self, lines) -> None:
        self.graph = {}
        for line in lines:
            _, _, _, stations = line
            for index in range(len(stations)):
                adj = []
                id, _, _, _, _ = stations[index]
                if id in self.graph:
                    adj = self.graph[id]
                if index != 0:
                    adj.append(stations[index - 1][0])
                else:
                    adj.append("")
                if index < len(stations) - 1:
                    adj.append(stations[index + 1][0])
                else:
                    adj.append("")
                self.graph[id] = adj
    
    def shortest_path(self, start, end):
        graph = self.graph
        if start not in graph or end not in graph:
            return None, None
        if len(graph[start]) * len(graph[end]) == 0:
            return None, None
        
        queue = deque()
        queue.append((start, [start], [start]))
        visited = set()
            
        while queue:
            current, path, pathf = queue.popleft()
            visited.add(current)
                
            if current == end:
                if path[-1] != end:
                    path += [end]
                return path, pathf
                
            try:
                for index, neighbour in enumerate(graph[current]):
                    if neighbour not in visited and len(neighbour) > 0:
                        if index > 1:
                            queue.append((neighbour, path + [neighbour], pathf + [neighbour]))
                        else:
                            queue.append((neighbour, path, pathf + [neighbour]))
            except:
                return None
        
        return None
    