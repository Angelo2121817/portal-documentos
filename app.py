# --- INÍCIO DO CÓDIGO COMPLETO - app.py (VERSÃO FINAL COM LISTA ATUALIZADA) ---

import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import urllib.parse

# --- Bloco 1: Configuração da Página ---
st.set_page_config(
    page_title="Portal de Documentos",
    page_icon="📄",
    layout="wide" # Deixa a página mais larga para caber mais colunas
)

# --- Bloco 2: Função de Envio de E-mail (O "Motor") ---
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
        print(f"Erro no envio de e-mail: {e}")
        return False

# --- Bloco 3: Lógica Principal da Aplicação ---

params = st.query_params

# MODO 1: MODO DE CONFIGURAÇÃO (SÓ VOCÊ VÊ)
if not params:
    st.header("⚙️ Modo de Configuração do Portal")
    st.info("Use esta área para criar um link de upload personalizado para cada cliente.")

    # Lista MESTRA atualizada com todos os seus documentos.
    MASTER_LISTA_DOCUMENTOS = [
        'Matrícula do terreno ou IPTU mais recente',
        'Contrato Social',
        'Certificado do IBAMA',
        'Procuração Assinada',
        'Documentação EPP assinada',
        'Certidão Simplificada da JUSCESP',
        'Layout',
        'Planta do Prédio',
        'Cartão CNPJ',
        'Certidão de Uso e Ocupação do Solo',
        'CICAR rural',
        'Dados do Proprietário',
        'Bombeiros (AVCB)',
        'Contas de Agua ou Outorga',
        'Fluxograma do Processo Produtivo',
        'CADRI',
        'Laudo Analítico',
        'Comprovante de Pagamento (CETESB)',
        'Copia CNH Representante Legal'
    ]
    
    st.markdown("#### PASSO 1: Digite o nome do cliente")
    nome_cliente_config = st.text_input("Nome do Cliente ou Empresa")

    st.markdown("#### PASSO 2: Selecione os documentos pendentes")
    documentos_selecionados = st.multiselect(
        "Selecione os documentos que você precisa que este cliente envie:",
        options=sorted(MASTER_LISTA_DOCUMENTOS) # Ordena a lista em ordem alfabética para facilitar
    )

    if st.button("🔗 GERAR LINK PARA O CLIENTE"):
        if not nome_cliente_config:
            st.error("Por favor, digite o nome do cliente.")
        elif not documentos_selecionados:
            st.error("Por favor, selecione pelo menos um documento.")
        else:
            docs_param = ",".join(urllib.parse.quote(doc) for doc in documentos_selecionados)
            cliente_param = urllib.parse.quote(nome_cliente_config)
            
            # Pega a URL base do Streamlit de forma dinâmica
            base_url = st.get_option("server.baseUrlPath")
            url_gerada = f"https://{base_url}?cliente={cliente_param}&docs={docs_param}"
            
            st.success("✅ Link gerado com sucesso! Copie e envie para o seu cliente.")
            st.code(url_gerada)

# MODO 2: MODO CLIENTE (O QUE O CLIENTE VÊ)
else:
    nome_cliente = urllib.parse.unquote(params.get("cliente", "Não identificado"))
    docs_string = urllib.parse.unquote(params.get("docs", ""))
    documentos_necessarios = docs_string.split(',') if docs_string else []

    col1, col2 = st.columns([1, 6])
    with col1:
        st.image("https://i.imgur.com/3z2e20a.png", width=120)
    with col2:
        st.title('Portal de Envio de Documentos')
        st.subheader(f"Cliente: {nome_cliente}")
    
    st.markdown("---")
    st.info("Por favor, anexe cada um dos documentos solicitados nos campos correspondentes abaixo. O envio só será realizado após você clicar no botão 'ENVIAR' no final da página.")

    if not documentos_necessarios:
        st.error("Link inválido ou nenhum documento foi solicitado.")
    else:
        arquivos_anexados = {}
        # Ajusta o número de colunas com base na quantidade de documentos
        num_colunas = 3 if len(documentos_necessarios) > 5 else 2
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
                        st.balloons()
                        st.success(f"🎉 Sucesso! {sucessos} documento(s) foram enviados.")
                    else:
                        st.error(f"Falha no envio para: {', '.join(erros)}. Por favor, tente novamente.")
    
    st.markdown("""
        <div style="text-align: center; margin-top: 40px; font-size: 12px; color: grey;">
            <p>Desenvolvido por Angelo</p>
        </div>
    """, unsafe_allow_html=True)

# --- FIM DO CÓDIGO COMPLETO ---
