import streamlit as st
import string
import random
from graph import Graph, Vertex

# Extract words from text
def extract_words(text):
    try:
        text = text.decode("utf-8")  # Decode bytes to string
    except UnicodeDecodeError:
        st.error("❌ Unable to decode file. Use UTF-8 encoded text files.")
        return []

    text = text.lower().translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    return words if words else []

# Build Markov Chain graph using full sequence
def build_graph(words):
    if not words:
        return None
    
    graph = Graph()
    prev_vertex = None
    
    for word in words:
        word_vertex = graph.get_vertex(word)
        if prev_vertex:
            prev_vertex.increment_edge(word_vertex)
        prev_vertex = word_vertex
    
    graph.generate_probability_mappings()
    return graph

# Generate text by following exact sequence
def generate_text(graph, words):
    if not words or not graph:
        return "⚠ Not enough words to generate. Upload a valid text file."
    
    formatted_text = "\n".join(words)  # Add line breaks between words
    return formatted_text

# Streamlit UI
st.title("🎵 Lyrics Generator with Markov Chains")

uploaded_files = st.file_uploader("📂 Upload text files", type=["txt"], accept_multiple_files=True)

all_words = []
for file in uploaded_files or []:
    all_words.extend(extract_words(file.read()))

if all_words:
    st.success(f"✅ Processed {len(uploaded_files)} file(s).")
    graph = build_graph(all_words)
    
    if st.button("🚀 Generate Lyrics"):
        st.subheader("📝 Generated Lyrics:")
        st.markdown(f"<pre style='white-space: pre-wrap; font-size: 18px; background-color: #f9f9f9; padding: 10px; border-radius: 5px;'>{generate_text(graph, all_words)}</pre>", unsafe_allow_html=True)
else:
    st.info("📄 Upload at least one text file to generate lyrics.")

st.markdown("---")
st.markdown("💻 **Developed by Muhammad Mudasir** 🎨")