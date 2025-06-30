import networkx as nx
from nlp_utils import TextProcessor

class KnowledgeGraphBuilder:
    def __init__(self):
        self.processor = TextProcessor()
        
    def build_from_sentences(self, sentences):
        kg = nx.DiGraph()
        
        for i, sent in enumerate(sentences):
            triplets = self.processor.extract_svo_triplets(sent)
            self._add_triplets_to_kg(kg, triplets, i)
            
        return kg
    
    def _add_triplets_to_kg(self, kg, triplets, sent_id):
        for subj, verb, obj in triplets:
            if not kg.has_node(subj):
                kg.add_node(subj, sentence_id=sent_id, node_type='entity')
            if not kg.has_node(obj):
                kg.add_node(obj, sentence_id=sent_id, node_type='entity')
                
            kg.add_edge(subj, obj, relation=verb, sentence_id=sent_id)
    
    def get_sentence_nodes(self, kg, sent_id):
        return [n for n, d in kg.nodes(data=True) if d.get('sentence_id') == sent_id]
    
    def get_sentence_edges(self, kg, sent_id):
        return [(u, v) for u, v, d in kg.edges(data=True) if d.get('sentence_id') == sent_id]
    
    def get_node_neighbors(self, kg, node):
        predecessors = list(kg.predecessors(node))
        successors = list(kg.successors(node))
        return predecessors + successors
    
    def compute_node_features(self, kg, node):
        degree = kg.degree(node)
        in_degree = kg.in_degree(node)
        out_degree = kg.out_degree(node)
        
        return {
            'degree': degree,
            'in_degree': in_degree,
            'out_degree': out_degree,
            'centrality': degree / max(1, len(kg.nodes))
        }
    
    def get_edge_relations(self, kg, node1, node2):
        if kg.has_edge(node1, node2):
            return kg[node1][node2].get('relation', '')
        if kg.has_edge(node2, node1):
            return kg[node2][node1].get('relation', '')
        return None