import streamlit as st
from langchain_community.llms import OpenAI as OpenAIModel
import spacy
from transformers import pipeline

st.title('NLP Application')

# Function to handle ChatGPT interaction
def chat_with_gpt():
    st.title('Chat with AI')
    openai_api_key = st.sidebar.text_input('OpenAI API Key')

    def generate_response(input_text):
        llm = OpenAIModel(temperature=0.7, openai_api_key=openai_api_key)
        response = llm(input_text)
        st.info(response)

    with st.form('my_form'):
        text = st.text_area('Enter text:', 'What are the three key pieces of advice for learning how to code?')
        submitted = st.form_submit_button('Submit')
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠️')
        if submitted and openai_api_key.startswith('sk-'):
            generate_response(text)

# Load NLP models
nlp = spacy.load('en_core_web_sm')
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# NLP function implementations
def nlp_summary(text):
    summary = summarizer(text, max_length=50, min_length=25, do_sample=False)
    return summary[0]['summary_text']

def nlp_sentiment(text):
    sentiment = sentiment_analyzer(text)
    return sentiment[0]

def nlp_ner(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def nlp_tokenize(text):
    doc = nlp(text)
    tokens = [(token.text, token.lemma_) for token in doc]
    return tokens

# Function to handle NLP tasks
def nlp_tasks():
    st.title('Process Text')
    st.subheader('Natural Language Processing for everyone')
    st.write("""
        This is a Natural Language Processing(NLP) Based App useful for basic NLP tasks: Tokenization, Lemmatization, 
        Named Entity Recognition (NER), Sentiment Analysis, Text Summarization.
        Click any of the checkboxes to get started.
    """)

    input_text = st.text_area("Enter your text here:")

    if st.checkbox("Get the summary of your text"):
        summary = nlp_summary(input_text)
        st.write("Summary:")
        st.info(summary)

    if st.checkbox("Get the Sentiment Score of your text"):
        sentiment = nlp_sentiment(input_text)
        st.write("Sentiment Score:")
        st.info(sentiment)

    if st.checkbox("Get the Named Entities of your text"):
        entities = nlp_ner(input_text)
        st.write("Named Entities:")
        st.info(entities)

    if st.checkbox("Get the Tokens and Lemma of text"):
        tokens = nlp_tokenize(input_text)
        st.write("Tokens and Lemma:")
        st.info(tokens)

# Page navigation
page = st.sidebar.selectbox("Choose a page", ["Chat with GPT", "NLP Tasks"])

if page == "Chat with GPT":
    chat_with_gpt()
else:
    nlp_tasks()