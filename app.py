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
           # --- INÍCIO DO NOVO BLOCO DE GERAÇÃO DE LINK (CORRIGIDO) ---
            docs_param = ",".join(urllib.parse.quote(doc) for doc in documentos_selecionados)
            cliente_param = urllib.parse.quote(nome_cliente_config)
            
            # =======================================================================
            # ATENÇÃO, ANGELO: COLOQUE A URL BASE DA SUA APLICAÇÃO AQUI
            # Exemplo: se a sua URL é "https://meu-portal-docs.streamlit.app",
            # você deve escrever: URL_BASE_DA_SUA_APP = "meu-portal-docs.streamlit.app"
            # =======================================================================
            URL_BASE_DA_SUA_APP = "app-documentos-7l5ecrvyv7lhjl3ska9e3t.streamlit.app"
            # =======================================================================

            # Monta o link final e correto
            url_gerada = f"https://{URL_BASE_DA_SUA_APP}?cliente={cliente_param}&docs={docs_param}"
            
            st.success("✅ Link gerado com sucesso! Copie e envie para o seu cliente.")
            st.code(url_gerada)
# --- FIM DO NOVO BLOCO DE GERAÇÃO DE LINK (CORRIGIDO) ---
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
    
    # --- RODAPÉ PROFISSIONAL ---
st.markdown("""
<div style="
    background: linear-gradient(135deg, rgba(14,165,233,0.1) 0%, rgba(59,130,246,0.1) 100%);
    border-top: 1px solid rgba(255,255,255,0.3);
    padding: 2rem 1rem;
    margin-top: 3rem;
    border-radius: 0 0 12px 12px;
    text-align: center;
    backdrop-filter: blur(8px);
">
    <div style="max-width: 1200px; margin: 0 auto;">
        <div style="
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
            margin-bottom: 1rem;
            flex-wrap: wrap;
        ">
            <img src="https://generated-images.adapta.one/metalquimicaconsultoria%40gmail.com/019c5261-cf87-7648-a8f1-b054e6597b25/2026-02-12T20-00-06-149Z_Modern_minimalist_vector_logo_for_METAL_QUIMICA_CO.png" 
                 alt="Logo Metal Química" 
                 style="height: 40px; width: auto;"
                 onerror="this.style.display='none';">
            <h3 style="color: #0f172a; margin: 0; font-size: 1.4rem; font-weight: 700;">
                Metal Química Consultoria
            </h3>
        </div>
        <p style="color: #475569; font-size: 0.95rem; margin: 0.5rem 0; font-weight: 400;">
            Portal de Gestão de Documentos | Licenças Ambientais e Regularizações
        </p>
        <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; margin-top: 1rem;">
            <a href="mailto:metalquimicaconsultoria@gmail.com" style="color: #3b82f6; text-decoration: none; font-weight: 500;">📧 Contato</a>
            <a href="tel:+551234567890" style="color: #3b82f6; text-decoration: none; font-weight: 500;">📞 Telefone</a>
            <span style="color: #64748b; font-size: 0.85rem;">© 2026 Metal Química. Todos os direitos reservados.</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
