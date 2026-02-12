import streamlit as st
import os

# Lista de documentos necessários para licenciamento ambiental
documentos_necessarios = [
    'Contrato Social',
    'Cartão CNPJ',
    'Procuração',
    'Memorial Descritivo',
    'ART do Responsável Técnico'
]

# Função para criar a pasta 'documentos_recebidos' se ela não existir
def criar_pasta():
    if not os.path.exists('documentos_recebidos'):
        os.makedirs('documentos_recebidos')

# Chamada da função para garantir que a pasta exista
criar_pasta()

# Título da aplicação
st.title('Portal de Upload de Documentos para Licenciamento Ambiental')

# Loop para cada documento na lista
for documento in documentos_necessarios:
    # Exibe o nome do documento
    st.subheader(f'Upload para: {documento}')
    
    # Componente de upload de arquivo
    uploaded_file = st.file_uploader(f'Selecione o arquivo para {documento}', type=['pdf', 'jpg', 'png', 'docx'], key=documento)
    
    # Verifica se um arquivo foi enviado
    if uploaded_file is not None:
        # Cria o nome do arquivo salvo: combinação do nome do documento e nome original
        nome_arquivo_salvo = f'{documento.replace(" ", "_")}-{uploaded_file.name}'
        
        # Caminho completo para salvar o arquivo
        caminho_arquivo = os.path.join('documentos_recebidos', nome_arquivo_salvo)
        
        # Salva o arquivo
        with open(caminho_arquivo, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        # Exibe mensagem de sucesso
        st.success(f'Arquivo "{nome_arquivo_salvo}" salvo com sucesso!')