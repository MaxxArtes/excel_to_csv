import streamlit as st
import pandas as pd
import io
import os

st.set_page_config(page_title="Conversor Excel para CSV", layout="centered")
st.title("📄 Conversor de Excel para CSV (Streamlit Cloud)")

# Upload de um arquivo
uploaded_file = st.file_uploader("📁 Envie um arquivo Excel (.xlsx)", type=["xlsx"])

# Se o arquivo foi enviado
if uploaded_file:
    try:
        # Lê as abas da planilha
        xls = pd.ExcelFile(uploaded_file)
        abas = xls.sheet_names

        # Escolha da aba
        aba_escolhida = st.selectbox("🗂️ Escolha a aba:", abas)

        # Escolha do separador
        separador = st.selectbox("🧱 Separador:", [",", ";", "\t"], index=1)
        codificacao = st.selectbox("🌐 Codificação:", ["utf-8", "utf-8-sig", "latin1"], index=1)

        # Botão de conversão
        if st.button("🚀 Converter e Baixar CSV"):
            df = pd.read_excel(xls, sheet_name=aba_escolhida)
            df.dropna(how='all', inplace=True)

            # Gera CSV em memória
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False, sep=separador, encoding=codificacao)
            csv_bytes = io.BytesIO(csv_buffer.getvalue().encode(codificacao))

            # Botão de download
            st.download_button(
                label="📥 Baixar CSV",
                data=csv_bytes,
                file_name=f"{os.path.splitext(uploaded_file.name)[0]}_{aba_escolhida.replace(' ', '_')}.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
