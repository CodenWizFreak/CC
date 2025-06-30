# 🧠 Entropy-Based Sentence Boundary Detection via Knowledge Graphs

An interactive Streamlit-based application that uses **Knowledge Graphs** and **multi-modal entropy** to detect sentence boundaries with contextual and semantic awareness.

---

## 🔥 Unique Selling Proposition (USP)

> 🎯 **A next-generation NLP tool that combines Knowledge Graph intelligence with entropy-based reasoning to detect sentence boundaries more meaningfully than traditional tokenizers—while remaining fully interactive, explainable, and robust.**

---

## 📦 Key Features

- 🔄 **Knowledge Graph Construction** from SVO (Subject-Verb-Object) triplets  
- 📏 **Entropy Computation** using:
  - Local entropy (`H_local = -∑p(r)log₂p(r)`)
  - Structural entropy (`H_struct = -∑p(d)log₂p(d)`)
  - Semantic divergence (`D_cos = 1 - cos(θ)`)
- 🧠 **Entropy-Guided Graph Traversal** that dynamically stops at semantic boundaries
- 📊 **Interactive Visualization** with graph views and entropy progression
- ⚙️ **Streamlit Interface** with real-time parameter tuning and result export
- 🛡️ **Robust NLP fallback handling** for NLTK resource issues

---

## 📁 Project Structure

```

.
├── app.py                 # Streamlit UI controller
├── kg_builder.py           # Knowledge graph construction from text
├── entropy_model.py        # Entropy and scoring logic
├── traversal.py            # Entropy-guided graph traversal
├── visualizer.py           # Graph and entropy visualization
├── nlp_utils.py            # NLP tokenization & POS tagging with fallbacks
├── setup_nlp.py           # Script to download necessary NLTK data

````

## 🔄 Workflow

```mermaid
flowchart LR
    %% Nodes
    A[User Input Text]:::input
    B[Sentence Tokenization<br/>NLTK or fallback]:::nlp
    C[SVO Triplet Extraction<br/>Subject-Verb-Object]:::nlp
    D["Build Knowledge Graph<br/>Nodes = Entities<br/>Edges = Relations"]:::graphbuild
    E["Compute Entropies<br/>H_local = -Σp*log₂p<br/>H_struct = -Σp*log₂p"]:::entropy
    F["Semantic Divergence<br/>D_cos = 1 - cosine similarity"]:::entropy
    G["Combined Score<br/>S = α*H_local + β*H_struct + γ*D"]:::entropy
    H["Entropy-Guided Traversal<br/>Stop if ΔS ≥ threshold"]:::entropy
    I[Visualize Graph + Entropy]:::vis
    J["Export Results"]:::output
    
    %% Connections
    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    H --> I
    I --> J
    
    %% Define styles
    classDef input fill:#D0F0C0,stroke:#333,stroke-width:2px,color:#000
    classDef nlp fill:#C7CEEA,stroke:#333,stroke-width:2px,color:#000
    classDef graphbuild fill:#FDFD96,stroke:#333,stroke-width:2px,color:#000
    classDef entropy fill:#FFB347,stroke:#333,stroke-width:2px,color:#000
    classDef vis fill:#AEC6CF,stroke:#333,stroke-width:2px,color:#000
    classDef output fill:#B0E0E6,stroke:#333,stroke-width:2px,color:#000
```

---

## 🚀 Getting Started

### 📥 Installation

```bash
git clone https://github.com/Anidipta/cc.git
cd cc
pip install -r requirements.txt
````

### 📦 NLTK Setup (Run Once)

```bash
python setup_nlp.py
```

> 💡 This ensures `punkt`, `punkt_tab`, and taggers are downloaded correctly, even in restricted environments.

---

## 🧪 Running the App

```bash
streamlit run app.py
```

---

## ✨ How It Works

1. **Input Text** 📝
   → User provides raw paragraph text.

2. **Tokenization & SVO Extraction** 🔍
   → Text is split into sentences, POS-tagged, and SVO triplets are extracted.

3. **Knowledge Graph Construction** 📈
   → Entities become nodes, verbs become edges.

4. **Entropy Calculation** 🔬
   → Each node gets:

   * Local entropy from relation diversity
   * Structural entropy from connectivity
   * Semantic divergence between path segments

5. **Graph Traversal** 🧭
   → Uses entropy scores to determine where sentence boundaries occur.

6. **Visualization** 🖼️
   → Graph, paths, and entropy plots are rendered interactively via Streamlit.

7. **Export Results** 📤
   → Users can download boundary predictions and plots.

---

## 🧠 Entropy Formulas

* **Local Entropy**
  `H_local = -∑ p(r) log₂ p(r)`

* **Structural Entropy**
  `H_struct = -∑ p(d) log₂ p(d)`

* **Semantic Divergence**
  `D_cos = 1 - (v1 · v2) / (||v1|| ||v2||)`

* **Combined Score**
  `Score = α * H_local + β * H_struct + γ * D`

* **Stopping Condition**
  `ΔScore ≥ θ` ⇒ Sentence boundary


---

## 📬 Contact
* 💻 [GitHub](https://github.com/Anidipta)
