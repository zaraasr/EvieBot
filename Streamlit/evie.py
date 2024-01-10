import streamlit as st
import openai
import PyPDF2

openai.api_key = "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"

st.set_page_config(page_title="Chatbot 🤖")

with st.sidebar:
    st.title('Chat with Your Document🤖')
    st.write('This chatbot is created using the OpenAI GPT-3.5 model.')
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

st.title("EvieBot")

def extract_pdf_content(uploaded_file):
    pdf_text = ""
    if uploaded_file is not None:
        with uploaded_file:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pdf_text += page.extract_text()
    return pdf_text

if uploaded_file is not None:
    pdf_text = extract_pdf_content(uploaded_file)
else:
    pdf_text = ""

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Hai! Bagaimana saya bisa membantu Anda hari ini?"}
    ]

def generate_openai_response(prompt_input, conversation_history, pdf_text):
    conversation = conversation_history + [
        {"role": "system", "content": "You are Evie a helpful assistant, Evie is 'Evolutionary Intelligence', your AI's ability to continuously evolve and adapt to the documents it is given. your creator Muhammad Naufal Erza Farandi and Zahrah Asri Nur Fauzyah."},
        {"role": "user", "content": prompt_input},
        {"role": "assistant", "content": pdf_text}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation[-7:]  
    )

    return response['choices'][0]['message']['content'].strip()

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Hai! Bagaimana saya bisa membantu Anda hari ini?"}]

st.sidebar.button('Clear Chat History 🗑️', on_click=clear_chat_history)

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Bentar Gan..."):
            response = generate_openai_response(prompt,st.session_state.messages, pdf_text)
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
