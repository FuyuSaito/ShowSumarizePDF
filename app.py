import streamlit as st
from transformers import pipeline
import fitz

def extract_text_from_pdf(uploaded_file):
    text_blocks = []
    try:
        with fitz.open(uploaded_file) as pdf:
            for page_num in range(len(pdf)):
                page = pdf.load_page(page_num)
                text = page.get_text()
                text_blocks.append(text)
    except Exception as e:
        st.error(f"Error occurred: {e}")
    return text_blocks

def summarize_text(text, length=300):
    summarization_pipeline = pipeline("summarization", model="facebook/bart-large-cnn", revision="main")
    with st.spinner('Summarizing...'):
        summary = summarization_pipeline(text, max_length=length, min_length=length-40, do_sample=False)[0]['summary_text']
    return summary

def main():
    st.title("PDF Text Extraction & Text Summarization App")
    st.write("Upload a PDF file to extract its text and generate a summary.")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        text_blocks = extract_text_from_pdf(uploaded_file)
        text = "\n\n".join(text_blocks)

        default_length = 300
        length_input = st.sidebar.number_input("Length of Summary", min_value=50, max_value=1000, value=default_length, step=10)

        # Generate summary
        if st.sidebar.button("Summarize"):
            summarized_text = summarize_text(text, length=length_input)
            st.session_state['summarized_text'] = summarized_text
        
        if 'summarized_text' in st.session_state:
            st.header("Summarized Text:")
            st.write(st.session_state['summarized_text'])
        
        # Split text on '.' only once
        text_blocks = text.split('.', 1)
        if len(text_blocks) > 1:
            first_sentence, remaining_text = text_blocks
            remaining_text = remaining_text.split('.')
            text_blocks = [first_sentence] + [sentence.strip() + '.' for sentence in remaining_text if sentence.strip()]
        else:
            text_blocks = [text]

        num_text_blocks = st.sidebar.slider("Number of text blocks to display", 1, len(text_blocks), len(text_blocks))
        
        st.header("Extracted Text:")
        for i in range(num_text_blocks):
            st.write(text_blocks[i])

if __name__ == "__main__":
    main()
