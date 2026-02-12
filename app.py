# --- INÍCIO DO BLOCO 1: IMPORTAÇÕES ---
import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
# --- FIM DO BLOCO 1: IMPORTAÇÕES ---
# --- CONFIGURAÇÃO DA PÁGINA ---
# --- INÍCIO DO BLOCO 2: CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Portal de Upload de Documentos",
    page_icon="📄"
)
# --- FIM DO BLOCO 2: CONFIGURAÇÃO DA PÁGINA ---

# --- FUNÇÃO DE ENVIO DE E-MAIL ---
# --- INÍCIO DO BLOCO 3: FUNÇÃO DE ENVIO DE E-MAIL ---
def enviar_email_com_anexo(nome_documento, conteudo_arquivo, nome_arquivo_original):
    try:
        # Pega as credenciais dos Secrets do Streamlit
        sender_email = st.secrets["SENDER_EMAIL"]
        sender_password = st.secrets["SENDER_PASSWORD"]
        recipient_email = st.secrets["RECIPIENT_EMAIL"]

        # Cria a mensagem de e-mail
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"Novo Documento Recebido: {nome_documento}"

        # Corpo do e-mail
        corpo = f"Olá Angelo,\n\nUm novo documento foi enviado através do portal.\n\nTipo de Documento: {nome_documento}\nNome Original do Arquivo: {nome_arquivo_original}\n\nO arquivo está em anexo."
        msg.attach(MIMEText(corpo, 'plain'))

        # Anexa o arquivo
        anexo = MIMEApplication(conteudo_arquivo, Name=nome_arquivo_original)
        anexo['Content-Disposition'] = f'attachment; filename="{nome_arquivo_original}"'
        msg.attach(anexo)

        # Conecta ao servidor SMTP do Gmail e envia o e-mail
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        return True
    except Exception as e:
        st.error(f"Ocorreu um erro ao enviar o e-mail: {e}")
        return False
# --- FIM DO BLOCO 3: FUNÇÃO DE ENVIO DE E-MAIL ---
# --- INTERFACE DA APLICAÇÃO ---
st.title('📄 Portal de Upload de Documentos')
st.write("Por favor, envie os documentos necessários para o licenciamento ambiental.")

# Adiciona um campo para o nome do cliente/empresa
nome_cliente = st.text_input("Nome do Cliente ou Empresa*", help="Este nome será usado para organizar os documentos.")

documentos_necessarios = [
    'Contrato Social',
    'Cartão CNPJ',
    'Procuração',
    'Memorial Descritivo',
    'ART do Responsável Técnico'
]

# Loop para cada documento
for documento in documentos_necessarios:
    st.subheader(f'Upload para: {documento}')
    
    uploaded_file = st.file_uploader(
        f'Selecione o arquivo para {documento}', 
        type=['pdf', 'jpg', 'png', 'docx', 'jpeg'], 
        key=documento
    )
    
    if uploaded_file is not None:
        if nome_cliente: # Verifica se o nome do cliente foi preenchido
            with st.spinner(f'Enviando {documento}...'):
                # Lê o conteúdo do arquivo
                file_content = uploaded_file.getvalue()
                
                # Envia o e-mail
                sucesso = enviar_email_com_anexo(f"{documento} ({nome_cliente})", file_content, uploaded_file.name)
                
                if sucesso:
                    st.success(f'O documento "{documento}" foi enviado com sucesso para seu e-mail!')
        else:
            st.warning("Por favor, preencha o campo 'Nome do Cliente ou Empresa' antes de enviar os arquivos.")

st.markdown("---")
st.write("Desenvolvido para agilizar o seu processo.")
