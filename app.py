import streamlit as st
import pandas as pd
import networkx as nx
import os
from kg_builder import KnowledgeGraphBuilder
from entropy_model import EntropyBoundaryDetector
from traversal import GraphTraverser
from visualizer import GraphVisualizer
from nlp_utils import TextProcessor
from styles import apply_custom_styles

st.set_page_config(page_title="Sentence Boundary Detection via Entropy", layout="wide")

def load_book_data():
    """Load book data from CSV file"""
    csv_path = "src/data.csv"
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            return df
        except Exception as e:
            st.error(f"Error loading book data: {e}")
            return None
    else:
        st.warning("Book data file (src/data.csv) not found. Please run the data extraction notebook first.")
        return None

def init_session():
    if 'kg' not in st.session_state:
        st.session_state.kg = None
    if 'text' not in st.session_state:
        st.session_state.text = ""
    if 'results' not in st.session_state:
        st.session_state.results = []
    if 'book_data' not in st.session_state:
        st.session_state.book_data = load_book_data()

def main():
    init_session()
    apply_custom_styles()
    
    st.title("📚 Sentence Boundary Detection in Knowledge Graphs")
    st.caption("Detecting sentence boundaries using entropy-based graph traversal")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔨 Build KG", "🎯 Detect Boundaries", "📊 Visualize", "📈 Results"])
    
    with tab1:
        build_kg_interface()
    
    with tab2:
        detect_boundaries_interface()
    
    with tab3:
        visualize_interface()
    
    with tab4:
        results_interface()

def build_kg_interface():
    st.header("🏗️ Knowledge Graph Construction")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        input_method = st.radio("📝 Input method:", ["Text input", "Sample text", "Books"])
        
        if input_method == "Text input":
            text_input = st.text_area("Enter text or paragraph:", height=200, 
                                     placeholder="Paste your text here...")
        elif input_method == "Sample text":
            sample_texts = {
                "Sample 1": "The cat sat on the mat. The dog ran in the park. Birds flew over the trees.",
                "Sample 2": "John went to the store. He bought some milk and bread. Mary called him on the phone.",
                "Sample 3": "The scientist conducted an experiment. She observed the chemical reaction. The results were documented carefully."
            }
            
            selected_sample = st.selectbox("Choose sample text:", list(sample_texts.keys()))
            text_input = sample_texts[selected_sample]
            st.text_area("Selected text:", value=text_input, height=100, disabled=True)
        
        else:  # Books option
            if st.session_state.book_data is not None:
                df = st.session_state.book_data
                
                # Create book-chapter combinations
                book_options = {}
                for _, row in df.iterrows():
                    book_chapter = f"{row['Book']} - {row['Chapter']}"
                    book_options[book_chapter] = row['Text']
                
                selected_book_chapter = st.selectbox("📖 Choose from Books:", list(book_options.keys()))
                text_input = book_options[selected_book_chapter]
                
                # Show preview of selected text
                preview_text = text_input[:500] + "..." if len(text_input) > 500 else text_input
                st.text_area("Selected chapter preview:", value=preview_text, height=150, disabled=True)
                
                st.info(f"📄 Full text length: {len(text_input)} characters")
            else:
                st.error("📚 Book data not available. Please run the data extraction notebook first.")
                text_input = ""
        
        if st.button("🚀 Build Knowledge Graph", type="primary"):
            if text_input:
                with st.spinner("🔄 Processing text and building KG..."):
                    processor = TextProcessor()
                    builder = KnowledgeGraphBuilder()
                    
                    sents = processor.extract_sentences(text_input)
                    kg = builder.build_from_sentences(sents)
                    
                    st.session_state.kg = kg
                    st.session_state.text = text_input
                    
                st.success(f"✅ Built KG with {len(kg.nodes)} nodes and {len(kg.edges)} edges")
                
                with st.expander("👁️ View extracted sentences"):
                    for i, sent in enumerate(sents):
                        st.write(f"{i+1}. {sent}")
            else:
                st.error("⚠️ Please enter text or select a book chapter")
    
    with col2:
        st.markdown("### 📊 Graph Statistics")
        if st.session_state.kg:
            st.metric("🔵 Nodes", len(st.session_state.kg.nodes))
            st.metric("🔗 Edges", len(st.session_state.kg.edges))
            st.metric("📝 Sentences", len(TextProcessor().extract_sentences(st.session_state.text)))
            
            if st.checkbox("📈 Show detailed statistics"):
                kg = st.session_state.kg
                
                density = nx.density(kg)
                avg_degree = sum(dict(kg.degree()).values()) / len(kg.nodes)
                
                st.write(f"**Density:** {density:.3f}")
                st.write(f"**Avg Degree:** {avg_degree:.2f}")
                
                if nx.is_connected(kg.to_undirected()):
                    st.write("**Connected:** ✅ Yes")
                else:
                    st.write("**Connected:** ❌ No")
        else:
            st.info("🔨 Build a graph to see statistics")

def detect_boundaries_interface():
    st.header("🎯 Boundary Detection")
    
    if not st.session_state.kg:
        st.warning("⚠️ Build a knowledge graph first")
        return
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### ⚙️ Configuration")
        nodes = list(st.session_state.kg.nodes())
        start_nodes = st.multiselect("🎯 Select starting nodes:", nodes, max_selections=5)
        
        entropy_threshold = st.slider("🌡️ Entropy threshold:", 0.1, 2.0, 0.8, 0.1)
        max_depth = st.slider("🔍 Max traversal depth:", 3, 20, 10)
        
        if st.button("🔍 Detect Boundaries", type="primary"):
            if start_nodes:
                detector = EntropyBoundaryDetector(threshold=entropy_threshold)
                traverser = GraphTraverser(st.session_state.kg, detector)
                
                results = []
                progress_bar = st.progress(0)
                for i, node in enumerate(start_nodes):
                    with st.spinner(f"🔄 Processing {node}..."):
                        path, entropies = traverser.traverse_with_entropy(node, max_depth)
                        results.append({
                            'start_node': node,
                            'boundary_nodes': path,
                            'entropies': entropies
                        })
                    progress_bar.progress((i + 1) / len(start_nodes))
                
                st.session_state.results = results
                st.success(f"✅ Processed {len(start_nodes)} starting nodes")
            else:
                st.error("⚠️ Please select at least one starting node")
    
    with col2:
        st.markdown("### 📋 Results Preview")
        if st.session_state.results:
            for i, result in enumerate(st.session_state.results):
                with st.expander(f"📊 Result {i+1}: {result['start_node']}"):
                    st.write(f"🔵 Boundary nodes: {len(result['boundary_nodes'])}")
                    st.write(f"📈 Max entropy: {max(result['entropies']):.3f}")
                    st.write(f"📉 Min entropy: {min(result['entropies']):.3f}")
        else:
            st.info("🔍 Run detection to see results")

def visualize_interface():
    st.header("📊 Graph Visualization")
    
    if not st.session_state.kg:
        st.warning("⚠️ Build a knowledge graph first")
        return
    
    viz = GraphVisualizer()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 🎨 Visualization Options")
        show_labels = st.checkbox("🏷️ Show node labels", True)
        layout = st.selectbox("📐 Layout:", ["spring", "circular", "random"])
        
        if st.session_state.results:
            st.markdown("### 🎯 Highlight Results")
            selected_result = st.selectbox("📍 Highlight result:", 
                                         range(len(st.session_state.results)),
                                         format_func=lambda x: f"Result {x+1}: {st.session_state.results[x]['start_node']}")
            
            highlight_nodes = st.session_state.results[selected_result]['boundary_nodes']
        else:
            highlight_nodes = []
    
    with col2:
        if st.session_state.results and highlight_nodes:
            fig = viz.create_graph_plot(st.session_state.kg, highlight_nodes, 
                                       show_labels, layout)
        else:
            fig = viz.create_graph_plot(st.session_state.kg, [], show_labels, layout)
        
        st.plotly_chart(fig, use_container_width=True)

def results_interface():
    st.header("📈 Results Analysis")
    
    if not st.session_state.results:
        st.info("📊 No results to display. Run boundary detection first.")
        return
    
    # Results summary
    results_df = []
    for r in st.session_state.results:
        results_df.append({
            'Start Node': r['start_node'],
            'Boundary Nodes': len(r['boundary_nodes']),
            'Avg Entropy': sum(r['entropies']) / len(r['entropies']),
            'Max Entropy': max(r['entropies']),
            'Min Entropy': min(r['entropies']),
            'Final Nodes': ', '.join(r['boundary_nodes'][-3:])
        })
    
    df = pd.DataFrame(results_df)
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 Total Results", len(st.session_state.results))
    with col2:
        avg_boundary_size = sum(len(r['boundary_nodes']) for r in st.session_state.results) / len(st.session_state.results)
        st.metric("📏 Avg Boundary Size", f"{avg_boundary_size:.1f}")
    with col3:
        avg_max_entropy = sum(max(r['entropies']) for r in st.session_state.results) / len(st.session_state.results)
        st.metric("📈 Avg Max Entropy", f"{avg_max_entropy:.2f}")
    with col4:
        avg_min_entropy = sum(min(r['entropies']) for r in st.session_state.results) / len(st.session_state.results)
        st.metric("📉 Avg Min Entropy", f"{avg_min_entropy:.2f}")
    
    # Results table
    st.markdown("### 📋 Detailed Results")
    st.dataframe(df, use_container_width=True)
    
    # Entropy visualization
    st.markdown("### 📊 Entropy Visualization")
    
    if st.session_state.results:
        viz = GraphVisualizer()
        
        selected_idx = st.selectbox(
            "📍 Select result to visualize entropy:",
            range(len(st.session_state.results)),
            format_func=lambda x: f"Result {x+1}: {st.session_state.results[x]['start_node']}"
        )
        
        selected_result = st.session_state.results[selected_idx]
        entropy_fig = viz.create_entropy_plot(
            selected_result['entropies'], 
            selected_result['boundary_nodes']
        )
        st.plotly_chart(entropy_fig, use_container_width=True)
        
        if st.checkbox("🔍 Show boundary subgraph"):
            subgraph_fig = viz.create_subgraph_plot(
                st.session_state.kg,
                selected_result['boundary_nodes'],
                f"Boundary Subgraph for {selected_result['start_node']}"
            )
            st.plotly_chart(subgraph_fig, use_container_width=True)
    
    # Export functionality
    st.markdown("### 💾 Export Results")
    if st.button("📥 Export Results"):
        csv = df.to_csv(index=False)
        st.download_button(
            label="📄 Download CSV",
            data=csv,
            file_name="boundary_detection_results.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()