# --- INÍCIO DO CÓDIGO COMPLETO - app.py ---

import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import urllib.parse

# --- Bloco 1: Configuração da Página ---
st.set_page_config(
    page_title="Portal de Documentos",
    page_icon="📄"
)

# --- Bloco 2: Função de Envio de E-mail (O "Motor") ---
# Esta função não muda. Ela é o nosso sistema de envio.
def enviar_email_com_anexo(nome_documento, conteudo_arquivo, nome_arquivo_original):
    try:
        sender_email = st.secrets["SENDER_EMAIL"]
        sender_password = st.secrets["SENDER_PASSWORD"]
        recipient_email = st.secrets["RECIPIENT_EMAIL"]

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"Novo Documento Recebido: {nome_documento}"

        corpo = f"Olá Angelo,\n\nUm novo documento foi enviado através do portal.\n\nTipo de Documento: {nome_documento}\nNome Original do Arquivo: {nome_arquivo_original}\n\nO arquivo está em anexo."
        msg.attach(MIMEText(corpo, 'plain'))

        anexo = MIMEApplication(conteudo_arquivo, Name=nome_arquivo_original)
        anexo['Content-Disposition'] = f'attachment; filename="{nome_arquivo_original}"'
        msg.attach(anexo)

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        return True
    except Exception as e:
        # Mostra um erro detalhado para você (Angelo), mas não para o cliente.
        print(f"Erro no envio de e-mail: {e}")
        return False

# --- Bloco 3: Lógica Principal da Aplicação ---

# Pega os parâmetros da URL (a parte depois do "?")
params = st.query_params

# MODO 1: MODO DE CONFIGURAÇÃO (Se não houver parâmetros na URL)
# Esta é a tela que SÓ VOCÊ (Angelo) vai usar para criar o link para o cliente.
if not params:
    st.header("⚙️ Modo de Configuração")
    st.info("Esta é a sua área de administrador. Use-a para criar um link personalizado para cada cliente.")

    # Lista MESTRA de todos os documentos possíveis. Você pode adicionar mais aqui.
    MASTER_LISTA_DOCUMENTOS = [
        'Contrato Social', 'Cartão CNPJ', 'Procuração', 'Memorial Descritivo', 
        'ART do Responsável Técnico', 'RG e CPF dos Sócios', 'Comprovante de Endereço',
        'Licença de Operação Anterior', 'Outros'
    ]
    
    st.markdown("#### PASSO 1: Digite o nome do cliente")
    nome_cliente_config = st.text_input("Nome do Cliente ou Empresa")

    st.markdown("#### PASSO 2: Selecione os documentos pendentes")
    documentos_selecionados = st.multiselect(
        "Selecione os documentos que você precisa que este cliente envie:",
        options=MASTER_LISTA_DOCUMENTOS
    )

    if st.button("🔗 GERAR LINK PARA O CLIENTE"):
        if not nome_cliente_config:
            st.error("Por favor, digite o nome do cliente.")
        elif not documentos_selecionados:
            st.error("Por favor, selecione pelo menos um documento.")
        else:
            # Codifica os parâmetros para serem seguros na URL
            docs_param = ",".join(urllib.parse.quote(doc) for doc in documentos_selecionados)
            cliente_param = urllib.parse.quote(nome_cliente_config)
            
            # Gera a URL completa
            # ATENÇÃO: Se você tiver um domínio personalizado, troque a base da URL.
            base_url = st.get_option("server.baseUrlPath") # Pega a URL base do Streamlit
            url_gerada = f"https://{base_url}?cliente={cliente_param}&docs={docs_param}"
            
            st.success("✅ Link gerado com sucesso! Copie e envie para o seu cliente.")
            st.code(url_gerada)

# MODO 2: MODO CLIENTE (Se a URL tiver parâmetros)
# Esta é a tela que o seu cliente vai ver ao acessar o link que você gerou.
else:
    # Pega o nome do cliente e a lista de documentos da URL
    nome_cliente = urllib.parse.unquote(params.get("cliente", "Não identificado"))
    docs_string = urllib.parse.unquote(params.get("docs", ""))
    documentos_necessarios = docs_string.split(',') if docs_string else []

    # --- Interface do Cliente ---
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("https://i.imgur.com/3z2e20a.png", width=100)
    with col2:
        st.title('Portal de Documentos')
        st.write(f"Enviado para: **{nome_cliente}**")
    
    st.markdown("---")
    st.info("Por favor, anexe cada um dos documentos solicitados nos campos correspondentes abaixo.")

    if not documentos_necessarios:
        st.error("Link inválido ou nenhum documento foi solicitado.")
    else:
        arquivos_anexados = {}
        num_colunas = 2
        cols = st.columns(num_colunas)

        for i, documento in enumerate(documentos_necessarios):
            with cols[i % num_colunas]:
                st.subheader(f'{documento}')
                uploaded_file = st.file_uploader(
                    f'Selecione o arquivo',
                    type=['pdf', 'jpg', 'png', 'docx', 'jpeg'],
                    key=documento
                )
                if uploaded_file is not None:
                    arquivos_anexados[documento] = uploaded_file

        st.markdown("---")

        if st.button('🚀 ENVIAR TODOS OS DOCUMENTOS'):
            if not arquivos_anexados:
                st.warning("Nenhum documento foi anexado.")
            else:
                with st.spinner("Enviando documentos... Por favor, aguarde."):
                    erros = []
                    sucessos = 0
                    for doc, arquivo in arquivos_anexados.items():
                        file_content = arquivo.getvalue()
                        sucesso = enviar_email_com_anexo(f"{doc} ({nome_cliente})", file_content, arquivo.name)
                        if sucesso:
                            sucessos += 1
                        else:
                            erros.append(doc)
                    
                    if not erros:
                        st.success(f"🎉 Sucesso! {sucessos} documento(s) foram enviados.")
                    else:
                        st.error(f"Falha no envio para: {', '.join(erros)}. Por favor, tente novamente.")
    
    # Rodapé
    st.markdown("""
        <div style="text-align: center; margin-top: 40px; font-size: 12px; color: grey;">
            <p>Desenvolvido por Angelo</p>
        </div>
    """, unsafe_allow_html=True)

# --- FIM DO CÓDIGO COMPLETO ---
