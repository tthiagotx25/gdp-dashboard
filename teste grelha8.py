import streamlit as st
import pandas as pd


# Função para calcular velocidade
def calcular_velocidade(vazao, area_efetiva):
    return vazao / area_efetiva

# Função para calcular alcance (simplificado baseado em catálogo)
def calcular_alcance(velocidade):
    return velocidade * 3.6  # ajuste baseado no catálogo VAT (exemplo)

# URL do Google Sheets (exemplo) — substitua pelo seu
url = 'https://docs.google.com/spreadsheets/d/1G7asOZa4gUCG5J3lPKlJo12HQb9iL5WSpYe9pr9KUAE/export?format=csv'

# Carregar dados do Google Sheets
@st.cache_data
def carregar_dados():
    return pd.read_csv(url)

df = carregar_dados()

st.title("Seleção de Grelha VAT - TROX")

# Entradas do usuário
vazao = st.number_input("Digite a Vazão (m³/h):", min_value=0.0)
alcance_desejado = st.number_input("Digite o Alcance Desejado (m):", min_value=0.0)
altura_grelha = st.number_input("Digite a Altura de Instalação (m):", min_value=0.0)

if st.button("Selecionar Grelha"):
    if vazao > 0 and alcance_desejado > 0 and altura_grelha > 0:
        df["Velocidade_saida"] = calcular_velocidade(vazao / 3600, df["Área Efetiva (m²)"])  # m³/h para m³/s
        df["Alcance_calculado"] = calcular_alcance(df["Velocidade_saida"])

        # Filtros
        df_filtrado = df[
            (df["Velocidade_saida"] <= 2.5) &
            (df["Velocidade_saida"] >= 0.5) &
            (df["Alcance_calculado"] >= alcance_desejado)
        ]

        if not df_filtrado.empty:
            grelha_ideal = df_filtrado.iloc[0]
            st.success(f"Modelo Ideal: {grelha_ideal['Modelo']}")
            st.write(f"Área Efetiva: {grelha_ideal['Área Efetiva (m²)']} m²")
            st.write(f"Velocidade de Saída: {grelha_ideal['Velocidade_saida']:.2f} m/s")
            st.write(f"Alcance Calculado: {grelha_ideal['Alcance_calculado']:.2f} m")
        else:
            st.error("Nenhuma grelha encontrada com esses parâmetros.")
    else:
        st.warning("Preencha todos os campos acima.")