import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Analisador de Slots Mobile", page_icon="📱", layout="centered")

st.title("🎰 Analisador de Volume de Slots")
st.caption("Registre os bônus para rastrear os momentos de maior atividade global.")

# Inicializar o banco de dados temporário no celular
if 'db_bonus' not in st.session_state:
    st.session_state.db_bonus = pd.DataFrame(columns=['Horario', 'Casa', 'Provedor', 'Jogo'])

# --- FORMULÁRIO DE REGISTRO ---
st.subheader("📝 Registrar Novo Bônus/Pico")

# Opções para você personalizar
casas = ["Esportes da Sorte", "EstrelaBet", "Betano"]
provedores = ["PG Soft", "Pragmatic Play", "Spribe"]
jogos = ["Fortune Tiger", "Fortune Ox", "Gates of Olympus", "Aviator"]

col1, col2 = st.columns(2)
with col1:
    casa_sel = st.selectbox("Casa de Aposta", casas)
    provedor_sel = st.selectbox("Provedor", provedores)
with col2:
    jogo_sel = st.selectbox("Jogo", jogos)
    # Pega a hora exata do clique no celular
    hora_atual = datetime.now().strftime("%H:%M:%S")
    st.text(f"Horário Atual: {hora_atual}")

if st.button("🚀 Registrar Bônus Agora", use_container_width=True):
    novo_registro = {
        'Horario': datetime.now().strftime("%H:%M"),
        'Casa': casa_sel,
        'Provedor': provedor_sel,
        'Jogo': jogo_sel
    }
    # Adiciona ao banco de dados do app
    st.session_state.db_bonus = pd.concat([st.session_state.db_bonus, pd.DataFrame([novo_registro])], ignore_index=True)
    st.success("Bônus registrado com sucesso!")

# --- PAINEL DE ANÁLISE ---
if not st.session_state.db_bonus.empty:
    st.subheader("📊 Gráfico de Volume por Horário")
    
    # Agrupa e conta quantos bônus saíram em cada minuto/hora
    df_analise = st.session_state.db_bonus
    contagem = df_analise.groupby(['Horario', 'Jogo']).size().reset_index(name='Quantidade')
    
    # Cria um gráfico de linhas dinâmico que funciona na tela do celular
    st.line_chart(data=contagem, x='Horario', y='Quantidade', color='Jogo')
    
    # Tabela com os dados brutos
    st.subheader("📋 Histórico Recente")
    st.dataframe(st.session_state.db_bonus[::-1], use_container_width=True)
    
    # Botão para limpar os dados se quiser recomeçar
    if st.button("🗑️ Limpar Dados"):
        st.session_state.db_bonus = pd.DataFrame(columns=['Horario', 'Casa', 'Provedor', 'Jogo'])
        st.rerun()
else:
    st.info("Nenhum bônus registrado ainda. Faça um registro acima para gerar os gráficos.")
