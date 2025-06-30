import streamlit as st
import pandas as pd
import networkx as nx
import os
import re
from kg_builder import KnowledgeGraphBuilder
from entropy_model import EntropyBoundaryDetector
from traversal import GraphTraverser
from visualizer import GraphVisualizer
from nlp_utils import TextProcessor
from styles import apply_custom_styles

st.set_page_config(page_title="Sentence Boundary Detection via Entropy", layout="wide")

def extract_book_chapter_info(text):
    """Extract book and chapter information from text"""
    # Look for patterns like "BOOK ONE, CHAPTER I" or "BOOK TWO, CHAPTER III"
    book_pattern = r'BOOK\s+(\w+)(?:,\s*)?CHAPTER\s+([IVX]+|[0-9]+)'
    match = re.search(book_pattern, text, re.IGNORECASE)
    
    if match:
        book = match.group(1)
        chapter = match.group(2)
        return f"Book {book}, Chapter {chapter}"
    
    # Fallback: look for just "CHAPTER" 
    chapter_pattern = r'CHAPTER\s+([IVX]+|[0-9]+)'
    match = re.search(chapter_pattern, text, re.IGNORECASE)
    
    if match:
        chapter = match.group(1)
        return f"Chapter {chapter}"
    
    # If no pattern found, return a truncated version of the text
    return text[:50] + "..." if len(text) > 50 else text

def load_book_data():
    """Load book data from CSV file"""
    csv_path = "src/war_and_peace_full_chapters.csv"
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            
            # Add a display column for book/chapter selection
            df['display_name'] = df['text'].apply(extract_book_chapter_info)
            
            # Add row numbers for unique identification
            df['row_id'] = range(len(df))
            
            return df
        except Exception as e:
            st.error(f"Error loading book data: {e}")
            return None
    else:
        st.warning("Book data file (src/war_and_peace_full_chapters.csv) not found. Please run the data extraction notebook first.")
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
                
                # Create selection options using display names
                selection_options = {}
                for _, row in df.iterrows():
                    key = f"{row['row_id']}: {row['display_name']}"
                    selection_options[key] = {
                        'text': row['text'],
                        'word_count': row.get('word_count', 'N/A'),
                        'char_count': row.get('char_count', len(row['text']))
                    }
                
                selected_key = st.selectbox("📖 Choose from War and Peace chapters:", 
                                          list(selection_options.get('display_name', selection_options.keys())))
                
                if selected_key:
                    selected_data = selection_options[selected_key]
                    text_input = selected_data['text']
                    
                    # Show metadata
                    col_meta1, col_meta2 = st.columns(2)
                    with col_meta1:
                        st.info(f"📊 Word count: {selected_data['word_count']}")
                    with col_meta2:
                        st.info(f"📄 Character count: {selected_data['char_count']}")
                    
                    # Show preview of selected text
                    preview_text = text_input[:500] + "..." if len(text_input) > 500 else text_input
                    st.text_area("Selected chapter preview:", value=preview_text, height=150, disabled=True)
                else:
                    text_input = ""
            else:
                st.error("📚 Book data not available. Please check the CSV file path and format.")
                text_input = ""
        
        if st.button("🚀 Build Knowledge Graph", type="primary"):
            if text_input:
                with st.spinner("🔄 Processing text and building KG..."):
                    try:
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
                    except Exception as e:
                        st.error(f"❌ Error building knowledge graph: {str(e)}")
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
                avg_degree = sum(dict(kg.degree()).values()) / len(kg.nodes) if len(kg.nodes) > 0 else 0
                
                st.write(f"**Density:** {density:.3f}")
                st.write(f"**Avg Degree:** {avg_degree:.2f}")
                
                if nx.is_connected(kg.to_undirected()):
                    st.write("**Connected:** ✅ Yes")
                else:
                    st.write("**Connected:** ❌ No")
                    
                # Show node degree distribution
                degrees = dict(kg.degree())
                if degrees:
                    max_degree = max(degrees.values())
                    min_degree = min(degrees.values())
                    st.write(f"**Degree Range:** {min_degree} - {max_degree}")
        else:
            st.info("🔨 Build a graph to see statistics")
            
        # Show data preview if book data is loaded
        if st.session_state.book_data is not None:
            st.markdown("### 📚 Dataset Info")
            df = st.session_state.book_data
            st.metric("📖 Total Chapters", len(df))
            
            if len(df) > 0:
                total_chars = df['char_count'].sum() if 'char_count' in df.columns else sum(len(text) for text in df['text'])
                total_words = df['word_count'].sum() if 'word_count' in df.columns else 0
                
                st.write(f"**Total Characters:** {total_chars:,}")
                if total_words > 0:
                    st.write(f"**Total Words:** {total_words:,}")

def detect_boundaries_interface():
    st.header("🎯 Boundary Detection")
    
    if not st.session_state.kg:
        st.warning("⚠️ Build a knowledge graph first")
        return
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### ⚙️ Configuration")
        nodes = list(st.session_state.kg.nodes())
        
        # Filter nodes to show only meaningful ones (not too short)
        meaningful_nodes = [node for node in nodes if len(str(node)) > 2]
        
        # Add "Select All" option
        all_nodes = ["Select All"] + meaningful_nodes
        
        selected_options = st.multiselect(
            "🎯 Select starting nodes:", 
            all_nodes, 
            max_selections=20,
            format_func=lambda x: "All nodes" if x == "Select All" else x
        )
        
        # Handle "Select All" selection
        if "Select All" in selected_options:
            start_nodes = meaningful_nodes  
            st.info("Showing ALL nodes in the graph. This may take longer to process.")
        else:
            start_nodes = selected_options
        
        entropy_threshold = st.slider("🌡️ Entropy threshold:", 0.1, 2.0, 0.8, 0.1)
        max_depth = st.slider("🔍 Max traversal depth:", 3, 20, 10)
        
        if st.button("🔍 Detect Boundaries", type="primary"):
            if start_nodes:
                try:
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
                    
                except Exception as e:
                    st.error(f"❌ Error during boundary detection: {str(e)}")
            else:
                st.error("⚠️ Please select at least one starting node")
    
    with col2:
        st.markdown("### 📋 Results Preview")
        if st.session_state.results:
            for i, result in enumerate(st.session_state.results):
                with st.expander(f"📊 Result {i+1}: {result['start_node']}"):
                    st.write(f"🔵 Boundary nodes: {len(result['boundary_nodes'])}")
                    if result['entropies']:
                        st.write(f"📈 Max entropy: {max(result['entropies']):.3f}")
                        st.write(f"📉 Min entropy: {min(result['entropies']):.3f}")
                        st.write(f"📊 Avg entropy: {sum(result['entropies'])/len(result['entropies']):.3f}")
                    else:
                        st.write("📊 No entropy data available")
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
        try:
            if st.session_state.results and highlight_nodes:
                fig = viz.create_graph_plot(st.session_state.kg, highlight_nodes, 
                                           show_labels, layout)
            else:
                fig = viz.create_graph_plot(st.session_state.kg, [], show_labels, layout)
            
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Error creating visualization: {str(e)}")

def results_interface():
    st.header("📈 Results Analysis")
    
    if not st.session_state.results:
        st.info("📊 No results to display. Run boundary detection first.")
        return
    
    # Results summary
    results_df = []
    for r in st.session_state.results:
        if r['entropies']:
            avg_entropy = sum(r['entropies']) / len(r['entropies'])
            max_entropy = max(r['entropies'])
            min_entropy = min(r['entropies'])
        else:
            avg_entropy = max_entropy = min_entropy = 0
            
        results_df.append({
            'Start Node': r['start_node'],
            'Boundary Nodes': len(r['boundary_nodes']),
            'Avg Entropy': avg_entropy,
            'Max Entropy': max_entropy,
            'Min Entropy': min_entropy,
            'Final Nodes': ', '.join(str(node) for node in r['boundary_nodes'][-3:])
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
        valid_results = [r for r in st.session_state.results if r['entropies']]
        if valid_results:
            avg_max_entropy = sum(max(r['entropies']) for r in valid_results) / len(valid_results)
            st.metric("📈 Avg Max Entropy", f"{avg_max_entropy:.2f}")
        else:
            st.metric("📈 Avg Max Entropy", "N/A")
    with col4:
        if valid_results:
            avg_min_entropy = sum(min(r['entropies']) for r in valid_results) / len(valid_results)
            st.metric("📉 Avg Min Entropy", f"{avg_min_entropy:.2f}")
        else:
            st.metric("📉 Avg Min Entropy", "N/A")
    
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
        
        if selected_result['entropies']:
            entropy_fig = viz.create_entropy_plot(
                selected_result['entropies'], 
                selected_result['boundary_nodes']
            )
            st.plotly_chart(entropy_fig, use_container_width=True)
        else:
            st.warning("No entropy data available for this result")
        
        if st.checkbox("🔍 Show boundary subgraph"):
            try:
                subgraph_fig = viz.create_subgraph_plot(
                    st.session_state.kg,
                    selected_result['boundary_nodes'],
                    f"Boundary Subgraph for {selected_result['start_node']}"
                )
                st.plotly_chart(subgraph_fig, use_container_width=True)
            except Exception as e:
                st.error(f"❌ Error creating subgraph: {str(e)}")
    
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