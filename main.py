# titulo
# input do chat (campo de mensagem)
# a cada mensagem que o usuario enviar
    # mostrar a mensagem q o usuario enviou no chat
    # pegar a pergunta e enviar para uma ia responder
    # exbir a reposta da ia na tela

# Streamlit -> apenas com python criar o front e o back 
# a ia que vamo usar: OpenIA
# pip install openai streamlit

import streamlit as st
from groq import Groq
import base64
from dotenv import load_dotenv
import os

# carregando as variaveis de ambiente do arquivo .env
load_dotenv()

def imagem_para_base64(caminho):
    with open(caminho, "rb") as f:
        return base64.b64encode(f.read()).decode()

imagem = imagem_para_base64("cachorro_onigiri.jpg")

st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{imagem}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    * {{
        color: black !important;
    }}
    .stChatInput textarea {{
        color: white !important;
    }}
    </style>
""", unsafe_allow_html=True)

# pegando a chave da api do arquivo .env (local) ou dos secrets do streamlit cloud (publicado)
modelo_ia = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.write("# Chatbot Onigiri com IA") # markdown
st.write("Converse com a IA Onigiri!🍙")

if not "lista_mensagens" in st.session_state:
    st.session_state["lista_mensagens"] = []

texto_usuario = st.chat_input("Mande mensagem para que onigiri dog te responda!")

#arquivo = st.file_uploader('Selecione um arquivo')

for mensagem in st.session_state["lista_mensagens"]:
    role = mensagem["role"]
    content = mensagem["content"]
    if role == "assistant":
        st.chat_message(role, avatar="🍙").write(content)
    else:
        st.chat_message(role, avatar="😋").write(content)

if texto_usuario:
    st.chat_message("user", avatar="😋").write(texto_usuario)
    mensagem_usuario = {"role": "user", "content": texto_usuario}
    st.session_state["lista_mensagens"].append(mensagem_usuario)

    #ia responder
    resposta_ia = modelo_ia.chat.completions.create(
        messages=st.session_state["lista_mensagens"],
        model="llama-3.3-70b-versatile"
    )

    texto_resposta_ia = resposta_ia.choices[0].message.content

    st.chat_message("assistant", avatar="🍙").write(texto_resposta_ia)
    mensagem_ia = {"role": "assistant", "content": texto_resposta_ia}
    st.session_state["lista_mensagens"].append(mensagem_ia)



