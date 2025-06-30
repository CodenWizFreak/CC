import numpy as np
from collections import deque
import networkx as nx

class GraphTraverser:
    def __init__(self, kg, entropy_detector):
        self.kg = kg
        self.detector = entropy_detector
        
    def traverse_with_entropy(self, start_node, max_depth=10):
        visited = set()
        path = [start_node]
        entropies = []
        context = []
        
        current = start_node
        visited.add(current)
        
        for depth in range(max_depth):
            entropy = self.detector.compute_node_entropy(self.kg, current, path, context)
            entropies.append(entropy)
            
            if self.detector.is_boundary(entropy, len(path)):
                break
                
            next_node = self._select_next_node(current, visited)
            if not next_node:
                break
                
            path.append(next_node)
            visited.add(next_node)
            context = self.detector.update_context(context, next_node)
            current = next_node
        
        return path, entropies
    
    def _select_next_node(self, current, visited):
        neighbors = list(self.kg.neighbors(current))
        unvisited = [n for n in neighbors if n not in visited]
        
        if not unvisited:
            return None
            
        if len(unvisited) == 1:
            return unvisited[0]
            
        scores = []
        for neighbor in unvisited:
            score = self._compute_node_score(current, neighbor)
            scores.append(score)
        
        best_idx = np.argmax(scores)
        return unvisited[best_idx]
    
    def _compute_node_score(self, current, candidate):
        degree_score = self.kg.degree(candidate) / max(1, max(dict(self.kg.degree()).values()))
        
        relation_score = 0.5
        if self.kg.has_edge(current, candidate):
            relation = self.kg[current][candidate].get('relation', '')
            if relation in ['has', 'is', 'was', 'were']:
                relation_score = 0.8
        
        return 0.6 * degree_score + 0.4 * relation_score
    
    def bfs_traversal(self, start_node, max_depth=5):
        visited = set()
        queue = deque([(start_node, 0)])
        path = []
        
        while queue:
            node, depth = queue.popleft()
            
            if node in visited or depth > max_depth:
                continue
                
            visited.add(node)
            path.append(node)
            
            entropy = self.detector.compute_node_entropy(self.kg, node, path, [])
            
            if self.detector.is_boundary(entropy, len(path)):
                break
                
            for neighbor in self.kg.neighbors(node):
                if neighbor not in visited:
                    queue.append((neighbor, depth + 1))
        
        return path
    
    def dfs_traversal(self, start_node, max_depth=10):
        visited = set()
        path = []
        entropies = []
        
        def dfs_helper(node, depth):
            if depth > max_depth or node in visited:
                return False
                
            visited.add(node)
            path.append(node)
            
            entropy = self.detector.compute_node_entropy(self.kg, node, path, [])
            entropies.append(entropy)
            
            if self.detector.is_boundary(entropy, len(path)):
                return True
                
            for neighbor in self.kg.neighbors(node):
                if dfs_helper(neighbor, depth + 1):
                    return True
                    
            return False
        
        dfs_helper(start_node, 0)
        return path, entropies
    
    def guided_traversal(self, start_node, target_sent_id=None):
        if target_sent_id is None:
            return self.traverse_with_entropy(start_node)
            
        visited = set()
        path = [start_node]
        current = start_node
        visited.add(current)
        
        while True:
            current_sent_id = self.kg.nodes[current].get('sentence_id', -1)
            
            if current_sent_id != target_sent_id and len(path) > 1:
                break
                
            neighbors = [n for n in self.kg.neighbors(current) if n not in visited]
            if not neighbors:
                break
                
            same_sent_neighbors = [n for n in neighbors 
                                 if self.kg.nodes[n].get('sentence_id') == target_sent_id]
            
            if same_sent_neighbors:
                next_node = same_sent_neighbors[0]
            else:
                next_node = neighbors[0]
                
            path.append(next_node)
            visited.add(next_node)
            current = next_node
        
        return path