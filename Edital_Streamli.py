import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader

# Função para ler o arquivo PDF e procurar o nome
def procurar_nome_pdf(nome, arquivo_pdf, progresso):
    reader = PdfReader(arquivo_pdf)
    num_pages = len(reader.pages)
    
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        for j, line in enumerate(text.split('\n'), start=1):
            if nome.lower() in line.lower():
                return (i+1, line)  # Retorna o número da página (i+1) e a linha onde foi encontrado o nome
        progresso.progress((i + 1) / num_pages)
        if st.session_state.stop_searching:
            st.session_state.stop_searching = False
            st.warning("Busca interrompida.")
            return None
    
    return None
  
# Função para processar o arquivo Excel
def processar_arquivo_excel(arquivo_excel):
    df = pd.read_excel(arquivo_excel)  # Lê todas as colunas
    return df

# Função principal
def main():
    st.title("Procurar Nomes em PDF")
    
    # Sidebar
    st.sidebar.title("Selecionar Arquivos")
    arquivo_excel = st.sidebar.file_uploader("Carregar arquivo Excel", type=["xlsx"])
    arquivo_pdf = st.sidebar.file_uploader("Carregar arquivo PDF", type=["pdf"])
    progresso = st.sidebar.progress(0)  # Barra de progresso
    st.session_state.stop_searching = False
    
    # DataFrame para armazenar resultados
    resultados = pd.DataFrame(columns=["Nome", "Arquivo", "Página", "Informações"])
    
    # Botão para parar a busca
    btn_parar_busca = st.sidebar.button("Parar Busca")
    
    # Botão para iniciar a busca
    if st.sidebar.button("Procurar"):
        st.sidebar.text("Procurando nomes no PDF...")
        if arquivo_excel is not None and arquivo_pdf is not None:
            # Processar arquivo Excel
            df_excel = processar_arquivo_excel(arquivo_excel)
            
            # Iterar sobre os nomes no arquivo Excel
            for index, row in df_excel.iterrows():
                nome = row["Nome Completo"]
                # Procurar nome no arquivo PDF
                resultado = procurar_nome_pdf(nome, arquivo_pdf, progresso)
                if resultado:
                    # Se encontrado, adicionar ao DataFrame de resultados
                    pagina, info_pdf = resultado
                    info_excel = ";".join(str(value) for value in row.values)
                    resultados = pd.concat([resultados, pd.DataFrame({"Nome": [nome], "Arquivo": [arquivo_pdf.name], "Página": [pagina], "Informações": [info_pdf]})], ignore_index=True)
                if st.session_state.stop_searching:
                    break
            
            # Mostrar resultados
            st.success("Procura concluída!")
            st.write(resultados)
    
    # Verifica se o botão "Parar Busca" foi pressionado
    if btn_parar_busca:
        st.session_state.stop_searching = True


if __name__ == "__main__":
    main()
