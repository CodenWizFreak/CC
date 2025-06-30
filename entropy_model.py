import numpy as np
from collections import Counter, defaultdict
import networkx as nx

class EntropyBoundaryDetector:
    def __init__(self, threshold=0.8, window_size=3):
        self.threshold = threshold
        self.window_size = window_size
        self.relation_probs = {}
        self.node_probs = {}
        
    def compute_local_entropy(self, kg, current_node, visited_nodes):
        neighbors = list(kg.neighbors(current_node))
        if not neighbors:
            return 1.0
            
        relations = []
        for neighbor in neighbors:
            if kg.has_edge(current_node, neighbor):
                rel = kg[current_node][neighbor].get('relation', 'unknown')
            elif kg.has_edge(neighbor, current_node):
                rel = kg[neighbor][current_node].get('relation', 'unknown')
            else:
                rel = 'unknown'
            relations.append(rel)
        
        rel_counts = Counter(relations)
        total = sum(rel_counts.values())
        
        entropy = 0.0
        for count in rel_counts.values():
            p = count / total
            entropy -= p * np.log2(p + 1e-8)
            
        return entropy
    
    def compute_semantic_divergence(self, kg, path):
        if len(path) < 2:
            return 0.0
            
        divergences = []
        for i in range(1, len(path)):
            curr_node = path[i]
            prev_node = path[i-1]
            
            curr_neighbors = set(kg.neighbors(curr_node))
            prev_neighbors = set(kg.neighbors(prev_node))
            
            if not curr_neighbors or not prev_neighbors:
                divergences.append(1.0)
                continue
                
            intersection = len(curr_neighbors & prev_neighbors)
            union = len(curr_neighbors | prev_neighbors)
            
            jaccard_sim = intersection / union if union > 0 else 0.0
            divergence = 1.0 - jaccard_sim
            divergences.append(divergence)
        
        return np.mean(divergences) if divergences else 0.0
    
    def compute_structural_entropy(self, kg, node, context_nodes):
        features = []
        
        degree = kg.degree(node)
        features.append(degree)
        
        clustering = nx.clustering(kg.to_undirected(), node)
        features.append(clustering)
        
        neighbors = set(kg.neighbors(node))
        context_set = set(context_nodes)
        
        if context_set:
            overlap = len(neighbors & context_set) / len(neighbors | context_set)
            features.append(overlap)
        else:
            features.append(0.0)
        
        if len(features) == 0:
            return 1.0
            
        normalized_features = [(f - min(features)) / (max(features) - min(features) + 1e-8) 
                              for f in features]
        
        entropy = -sum(p * np.log2(p + 1e-8) for p in normalized_features 
                      if p > 0)
        
        return entropy
    
    def is_boundary(self, entropy, path_length):
        base_threshold = self.threshold
        
        if path_length > 10:
            base_threshold *= 0.9
        elif path_length < 3:
            base_threshold *= 1.2
            
        return entropy > base_threshold
    
    def compute_node_entropy(self, kg, node, path, context):
        local_ent = self.compute_local_entropy(kg, node, path)
        struct_ent = self.compute_structural_entropy(kg, node, context)
        
        if len(path) >= 2:
            semantic_div = self.compute_semantic_divergence(kg, path[-self.window_size:])
        else:
            semantic_div = 0.0
        
        combined_entropy = 0.4 * local_ent + 0.4 * struct_ent + 0.2 * semantic_div
        
        return combined_entropy
    
    def update_context(self, context, new_node, max_size=10):
        context.append(new_node)
        if len(context) > max_size:
            context.pop(0)
        return context