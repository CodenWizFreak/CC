import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
import numpy as np

class GraphVisualizer:
    def __init__(self):
        self.colors = px.colors.qualitative.Set3
        
    def create_graph_plot(self, kg, highlight_nodes=None, show_labels=True, layout='spring'):
        pos = self._get_layout(kg, layout)
        
        edge_x, edge_y = self._get_edge_coordinates(kg, pos)
        node_x, node_y, node_colors, node_text = self._get_node_coordinates(
            kg, pos, highlight_nodes)
        
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1, color='#888'),
            hoverinfo='none',
            mode='lines'
        )
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text' if show_labels else 'markers',
            hoverinfo='text',
            text=node_text if show_labels else None,
            textposition="middle center",
            hovertext=node_text,
            marker=dict(
                showscale=False,
                color=node_colors,
                size=10,
                line=dict(width=2, color='white')
            )
        )
        
        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                title='Knowledge Graph Visualization',
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=self._get_annotations(),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                plot_bgcolor='white'
            )
        )
        
        return fig
    
    def _get_layout(self, kg, layout_type):
        if layout_type == 'spring':
            return nx.spring_layout(kg, k=1, iterations=50)
        elif layout_type == 'circular':
            return nx.circular_layout(kg)
        elif layout_type == 'random':
            return nx.random_layout(kg)
        else:
            return nx.spring_layout(kg)
    
    def _get_edge_coordinates(self, kg, pos):
        edge_x = []
        edge_y = []
        
        for edge in kg.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            
        return edge_x, edge_y
    
    def _get_node_coordinates(self, kg, pos, highlight_nodes):
        node_x = []
        node_y = []
        node_colors = []
        node_text = []
        
        highlight_set = set(highlight_nodes) if highlight_nodes else set()
        
        for node in kg.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            
            if node in highlight_set:
                node_colors.append('red')
            else:
                sent_id = kg.nodes[node].get('sentence_id', 0)
                color_idx = sent_id % len(self.colors)
                node_colors.append(self.colors[color_idx])
            
            node_text.append(str(node)[:15])
        
        return node_x, node_y, node_colors, node_text
    
    def _get_annotations(self):
        return [
            dict(
                text="Graph nodes colored by sentence ID<br>Red nodes are highlighted results",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.005, y=-0.002,
                xanchor="left", yanchor="bottom",
                font=dict(size=10, color="gray")
            )
        ]
    
    def create_entropy_plot(self, entropies, node_names):
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=list(range(len(entropies))),
            y=entropies,
            mode='lines+markers',
            name='Entropy',
            line=dict(color='blue', width=2),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title='Entropy Along Traversal Path',
            xaxis_title='Step',
            yaxis_title='Entropy',
            showlegend=False,
            height=400
        )
        
        return fig
    
    def create_subgraph_plot(self, kg, nodes, title="Subgraph"):
        subgraph = kg.subgraph(nodes)
        pos = nx.spring_layout(subgraph)
        
        edge_x, edge_y = self._get_edge_coordinates(subgraph, pos)
        node_x, node_y, node_colors, node_text = self._get_node_coordinates(
            subgraph, pos, nodes)
        
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='#666'),
            hoverinfo='none',
            mode='lines'
        )
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=node_text,
            textposition="middle center",
            hovertext=node_text,
            marker=dict(
                color='lightblue',
                size=15,
                line=dict(width=2, color='darkblue')
            )
        )
        
        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                title=title,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                plot_bgcolor='white',
                height=400
            )
        )
        
        return fig