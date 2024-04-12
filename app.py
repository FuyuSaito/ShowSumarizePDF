import streamlit as st
from transformers import BartForConditionalGeneration, BartTokenizer
import pdfplumber

def extract_text_from_pdf(uploaded_file):
    text_blocks = []
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                text_blocks.append(text)
    except Exception as e:
        st.error(f"Error occurred: {e}")
    return text_blocks

def summarize_text(text, length=300):
    model_name = "facebook/bart-large-cnn"
    model = BartForConditionalGeneration.from_pretrained(model_name)
    tokenizer = BartTokenizer.from_pretrained(model_name)

    inputs = tokenizer([text], max_length=1024, return_tensors="pt", truncation=True)
    summary_ids = model.generate(inputs['input_ids'], max_length=length, min_length=max(50, length - 50), early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    return summary

def main():
    st.title("PDF Text Extraction & Text Summarization App")
    st.write("Upload a PDF file to extract its text and generate a summary.")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        text_blocks = extract_text_from_pdf(uploaded_file)
        text = "\n\n".join(text_blocks)
        
        # Split text on '.' only once
        text_blocks = text.split('.', 1)
        if len(text_blocks) > 1:
            first_sentence, remaining_text = text_blocks
            remaining_text = remaining_text.split('.')
            text_blocks = [first_sentence] + [sentence.strip() + '.' for sentence in remaining_text if sentence.strip()]
        else:
            text_blocks = [text]

        # 2つの列を定義
        left_column, right_column = st.columns(2)
        
        with left_column:
            default_length = 300
            length_input = st.number_input("Length of Summary", min_value=100, max_value=500, value=default_length, step=10)
            
            # Generate summary
            if st.button("Summarize"):
                summarized_text = summarize_text(text, length=length_input)
                st.session_state['summarized_text'] = summarized_text
                
            if 'summarized_text' in st.session_state:
                st.header(f"Summarized Text: {len(st.session_state['summarized_text'].split(' '))} words")
                st.write(st.session_state['summarized_text'])

        with right_column:
            num_text_blocks = st.slider("Number of text blocks to display", 1, len(text_blocks), len(text_blocks))
        
            st.header(f"Extracted Text: {len(text.split(' '))} words")
            for i in range(num_text_blocks):
                st.write(text_blocks[i])

if __name__ == "__main__":
    main()
