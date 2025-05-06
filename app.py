import streamlit as st
import pandas as pd
import os
from tkinter import Tk, filedialog
import io

# Função para abrir janela de seleção de pasta
def selecionar_pasta():
    root = Tk()
    root.withdraw()
    pasta = filedialog.askdirectory()
    root.destroy()
    return pasta

st.set_page_config(page_title="Conversor Excel para CSV com Aba", layout="centered")
st.title("📄 Conversor de Excel para CSV (com escolha de aba)")

# Upload de um arquivo
uploaded_file = st.file_uploader("📁 Envie um arquivo Excel (.xlsx)", type=["xlsx"])

# Botão para selecionar pasta
if st.button("📂 Escolher pasta para salvar o CSV"):
    pasta = selecionar_pasta()
    if pasta:
        st.session_state["pasta_destino"] = pasta
        st.success(f"Pasta selecionada: `{pasta}`")

# Exibe pasta salva
pasta_destino = st.session_state.get("pasta_destino", "")

# Quando há arquivo e pasta
if uploaded_file and pasta_destino:
    try:
        xls = pd.ExcelFile(uploaded_file)
        abas = xls.sheet_names
        aba_escolhida = st.selectbox("🗂️ Selecione a aba para converter:", abas)

        separador = st.selectbox("🧱 Separador:", [",", ";", "\t"], index=1)
        codificacao = st.selectbox("🌐 Codificação:", ["utf-8", "utf-8-sig", "latin1"], index=1)

        if st.button("🚀 Converter e salvar CSV"):
            df = pd.read_excel(xls, sheet_name=aba_escolhida)
            df.dropna(how='all', inplace=True)

            nome_base = os.path.splitext(uploaded_file.name)[0]
            nome_csv = f"{nome_base}_{aba_escolhida.replace(' ', '_')}.csv"
            caminho_csv = os.path.join(pasta_destino, nome_csv)

            df.to_csv(caminho_csv, index=False, sep=separador, encoding=codificacao)

            st.success(f"✅ CSV salvo com sucesso em: `{caminho_csv}`")

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
