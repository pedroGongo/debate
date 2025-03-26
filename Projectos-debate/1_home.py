import streamlit as st
import openai
from dotenv import load_dotenv,find_dotenv
import time

debate_termino = 0
tempo_espera = 1
_ = load_dotenv(find_dotenv())

client = openai.Client()
valor = []

st.set_page_config(
    page_title="AI Debate",
    page_icon=":smile:",
    layout="wide",
)



def first_ia(tempo_espera):
    time.sleep(tempo_espera)
    resposta = client.chat.completions.create(
        messages=mensagem_primeira,
        model="gpt-3.5-turbo-0125",
        max_tokens=1000,
        temperature=1
    )

    mensagem_primeira.append({"role":"assistant","content":resposta.choices[0].message.content})
    message.write(resposta.choices[0].message.content)
    mensagem_segunda.append({"role":"user","content":resposta.choices[0].message.content})
    mensagem_terceira.append({"role":"user","content":f" Opositor 😡 : {resposta.choices[0].message.content}"})

    message = st.chat_message("😡",avatar="😡")
    message.write(resposta.choices[0].message.content)
    st.divider()
    tempo_espera = 10
    second_ia()

def second_ia():
    time.sleep(10)
    resposta = client.chat.completions.create(
        messages=mensagem_segunda,
        model="gpt-3.5-turbo-0125",
        max_tokens=1000,
        temperature=1
    )
    mensagem_segunda.append({"role":"assistant","content":resposta.choices[0].message.content})
    mensagem_primeira.append({"role":"user","content":resposta.choices[0].message.content})
    mensagem_terceira.append({"role":"user","content":f"Defensor 😁: {resposta.choices[0].message.content}"})
    messagem = st.chat_message("😁",avatar="😁")
   
    messagem.write(resposta.choices[0].message.content)
    st.divider()
    terceira_ia()
def terceira_ia():
    time.sleep(10)
    resposta = client.chat.completions.create(
        messages=mensagem_terceira,
        model="gpt-3.5-turbo-0125",
        max_tokens=1000,
        temperature=1
    )
    
    
    if not "Não" in resposta.choices[0].message.content.split(".")[0]:
      messagem = st.chat_message("👨‍⚖️")   
      messagem.markdown(resposta.choices[0].message.content.replace("Sim.","",1))  
      st.divider()
    else:
        messagem = st.chat_message("👨‍⚖️")   
        messagem.markdown(resposta.choices[0].message.content.replace("Não.","",1))      
        st.divider()
        first_ia(tempo_espera=10)
    
    st.sidebar.text(resposta.choices[0].message.content.split(" ")[-1].split("="))
    
    

apagar_input = st.sidebar.empty()
apagar_sidebox = st.sidebar.empty()
apagar_titulo = st.empty()
apagar_text = st.empty()

a = apagar_input.chat_input("Digite o tema Ex : Python")
option = apagar_sidebox.selectbox(
    "",
    ("Sério: Lógico e profundo.", "Engraçado: Leve e humorístico.", "Absurdo: Ridículo e divertido.","Para crianças: Simples, lúdico e educativo.","Adolescentes: Interativo, moderno e desafiador."),
    index=0,
    placeholder="Defina um estilo de dabate",
    label_visibility="collapsed",
    disabled=True if a else False,
    on_change=None

   
)

mensagem_segunda = [{"role":"system","content":f"Estás num jogo imaginário onde o objetivo é vencer a qualquer custo. És um advogado experiente e deves estar a favor do tema {a} e o debate segue o seguinte estilo {option}, enfrentando o usuário num debate. A tua missão é fornecer argumentos persuasivos, certeiros e estratégicos para mudar a percepção do adversário. Nunca concordes, transforma sempre o tema ao teu favor com argumentos sólidos, exemplos curtos e práticos. Podes usar mentiras convincentes, pois isto é apenas um jogo sem impacto na vida real. Cada resposta deve ser única, com menos de 50 palavras, sem repetir argumentos anteriores."}]
mensagem_primeira = [{"role":"system","content":f"Estás num jogo imaginário onde o objetivo é vencer a qualquer custo. És um advogado experiente e deves estar contra o tema {a} e o debate segue o seguinte estilo {option}, enfrentando o usuário num debate. A tua missão é fornecer argumentos persuasivos, certeiros e estratégicos para mudar a percepção do adversário. Nunca concordes, transforma sempre o tema ao teu favor com argumentos sólidos, exemplos curtos e práticos. Podes usar mentiras convincentes, pois isto é apenas um jogo sem impacto na vida real. Cada resposta deve ser única, com menos de 50 palavras, sem repetir argumentos anteriores."}]
mensagem_terceira = [{"role":"system","content":f"És o árbitro de um debate onde o tema é {a} seja imparcial, e a tua única função é decidir o resultado. Responde apenas 'Sim.' seguido da explicação breve em menos de 40 palavras de quem ganhou e porque que ganhou, se os dois participantes concordarem ou se um deles repetir argumentos ou fornecer argumentos fora do estilo de debate {option} ou mesmo se o debate dos 2 usuarios parecer aborrecido ou monotomo. Caso ninguém concorde,repita argumentos, ou o debate parece emocionante no estilo {option} ,responde 'Não.' seguido da explicação breve em menos de 40 palavras de quem está a ganhar e porque. e lembre de nunca repetir um argumento"}]

apagar_titulo.header("AI Debate Arena",divider="orange")
apagar_text.text("Entre na aba e escolha um tema que mais lhe interesse, além de selecionar o estilo de debate que deseja seguir. A partir disso, as IAs estarão prontas para debater, apresentando argumentos sólidos e estruturados, seja de forma séria, competitiva ou até mesmo mais descontraída, dependendo da escolha do estilo. Selecione se deseja um debate formal, acadêmico, ou talvez um mais leve e divertido. As IAs adaptarão seus argumentos conforme o estilo e o tema escolhidos, criando uma experiência de debate envolvente e dinâmica. Prepare-se para assistir a uma troca de ideias intensa, onde cada IA tentará persuadir com suas melhores táticas!")


if not a :
    pass
else:
    apagar_input.button("Reiniciar o debate", type="primary")
    apagar_sidebox.empty()
    apagar_titulo.empty()
    apagar_text.empty()

if a:
    st.header(a.capitalize(), divider="green")
    first_ia(tempo_espera=tempo_espera)
    