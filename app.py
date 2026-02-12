# --- INÍCIO DO CÓDIGO COMPLETO - app.py (VERSÃO CORRIGIDA COM LINK FUNCIONAL) ---

import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import urllib.parse

# --- Bloco 1: Configuração da Página ---
st.set_page_config(
    page_title="Portal de Documentos - Metal Química",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Bloco 1.5: Estilo CSS Moderno e Profissional ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --primary-color: #3b82f6;
        --primary-dark: #1e40af;
        --secondary-color: #0f172a;
        --accent-color: #06b6d4;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
        --light-bg: #f8fafc;
        --card-bg: #ffffff;
        --border-color: #e2e8f0;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
    }

    * {
        font-family: 'Inter', sans-serif !important;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
    }

    [data-testid="stAppViewContainer"] > .main {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
        padding: 2rem !important;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #0f172a !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px !important;
    }

    h1 {
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem !important;
    }

    h2 {
        font-size: 1.875rem !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }

    h3 {
        font-size: 1.25rem !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.75rem !important;
    }

    p, span, div {
        color: #475569 !important;
        line-height: 1.6 !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px rgba(59, 130, 246, 0.2) !important;
        cursor: pointer !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        box-shadow: 0 8px 12px rgba(59, 130, 246, 0.4) !important;
        transform: translateY(-2px) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stMultiSelect > div > div > div {
        border: 2px solid #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        background-color: #ffffff !important;
    }

    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stMultiSelect > div > div > div:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }

    .stInfo, .stSuccess, .stWarning, .stError {
        border-radius: 8px !important;
        border-left: 4px solid !important;
        padding: 1rem !important;
        background-color: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(10px) !important;
    }

    .stInfo {
        border-left-color: #3b82f6 !important;
        background-color: rgba(59, 130, 246, 0.05) !important;
    }

    .stSuccess {
        border-left-color: #10b981 !important;
        background-color: rgba(16, 185, 129, 0.05) !important;
    }

    .stWarning {
        border-left-color: #f59e0b !important;
        background-color: rgba(245, 158, 11, 0.05) !important;
    }

    .stError {
        border-left-color: #ef4444 !important;
        background-color: rgba(239, 68, 68, 0.05) !important;
    }

    .stFileUploader {
        border: 2px dashed #3b82f6 !important;
        border-radius: 8px !important;
        padding: 1.5rem !important;
        background-color: rgba(59, 130, 246, 0.02) !important;
        transition: all 0.3s ease !important;
    }

    .stFileUploader:hover {
        border-color: #2563eb !important;
        background-color: rgba(59, 130, 246, 0.05) !important;
    }

    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent) !important;
        margin: 2rem 0 !important;
    }

    .stSpinner {
        color: #3b82f6 !important;
    }

    .stSubheader {
        color: #1e293b !important;
        font-weight: 600 !important;
    }

    .stMarkdown {
        color: #475569 !important;
    }

    code {
        background-color: #f1f5f9 !important;
        border-radius: 4px !important;
        padding: 0.25rem 0.5rem !important;
        color: #e11d48 !important;
        font-family: 'Courier New', monospace !important;
    }

    .document-card-highlight {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        margin: 0.75rem 0 !important;
        border: 2px solid #3b82f6 !important;
        transition: all 0.3s ease !important;
    }

    .document-card-highlight:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(59, 130, 246, 0.2) !important;
    }

    .document-icon-medium {
        font-size: 1.5rem !important;
        margin-right: 0.5rem !important;
        display: inline-block !important;
    }

    .document-name-medium {
        font-size: 1.125rem !important;
        font-weight: 600 !important;
        color: #1e293b !important;
        display: inline-block !important;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    [data-testid="stAppViewContainer"] {
        animation: fadeIn 0.5s ease-out !important;
    }

    @media (max-width: 768px) {
        h1 {
            font-size: 1.875rem !important;
        }
        
        h2 {
            font-size: 1.5rem !important;
        }
        
        .stButton > button {
            width: 100% !important;
        }

        .document-name-medium {
            font-size: 1rem !important;
        }

        .document-icon-medium {
            font-size: 1.25rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- Bloco 2: Função de Envio de E-mail ---
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

if not params:
    # MODO ADMIN
    col_logo, col_title = st.columns([1, 5])
    with col_logo:
        st.image("https://generated-images.adapta.one/metalquimicaconsultoria%40gmail.com/019c5261-cf87-7648-a8f1-b054e6597b25/2026-02-12T20-00-06-149Z_Modern_minimalist_vector_logo_for_METAL_QUIMICA_CO.png", width=250)
    with col_title:
        st.title("⚗️ Portal de Documentos")
        st.markdown("**Metal Química Consultoria** - Gerenciamento de Documentação")
    
    st.markdown("---")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%); 
                padding: 1.5rem; border-radius: 8px; border-left: 4px solid #3b82f6;">
        <h3 style="margin-top: 0; color: #1e40af;">📋 Configuração do Portal</h3>
        <p>Use esta área para criar links personalizados de upload para seus clientes. Selecione os documentos necessários e gere um link único.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    MASTER_LISTA_DOCUMENTOS = [
        'Matrícula do terreno ou IPTU mais recente', 'Contrato Social', 'Certificado do IBAMA',
        'Procuração Assinada', 'Documentação EPP assinada', 'Certidão Simplificada da JUSCESP',
        'Layout', 'Planta do Prédio', 'Cartão CNPJ', 'Certidão de Uso e Ocupação do Solo',
        'CICAR rural', 'Dados do Proprietário', 'Bombeiros (AVCB)', 'Contas de Agua ou Outorga',
        'Fluxograma do Processo Produtivo', 'CADRI', 'Laudo Analítico', 'Comprovante de Pagamento (CETESB)',
        'Copia CNH Representante Legal'
    ]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 Passo 1: Cliente")
        nome_cliente_config = st.text_input("Nome do Cliente ou Empresa", placeholder="Ex: Empresa XYZ Ltda")
    
    with col2:
        st.markdown("### 📋 Passo 2: Documentos")
        documentos_selecionados = st.multiselect(
            "Selecione os documentos necessários:",
            options=sorted(MASTER_LISTA_DOCUMENTOS),
            help="Escolha os documentos que o cliente precisa enviar"
        )
    
    st.markdown("")
    
    if st.button("🔗 GERAR LINK PARA O CLIENTE", use_container_width=True):
        if not nome_cliente_config:
            st.error("❌ Por favor, digite o nome do cliente.")
        elif not documentos_selecionados:
            st.error("❌ Por favor, selecione pelo menos um documento.")
        else:
            docs_param = ",".join(urllib.parse.quote(doc) for doc in documentos_selecionados)
            cliente_param = urllib.parse.quote(nome_cliente_config)
            URL_BASE_DA_SUA_APP = "app-documentos-7l5ecrvyv7lhjl3ska9e3t.streamlit.app"
            url_gerada = f"https://{URL_BASE_DA_SUA_APP}?cliente={cliente_param}&docs={docs_param}"
            
            st.success("✅ Link gerado com sucesso!")
            st.markdown("""
            <div style="background-color: #f1f5f9; padding: 1rem; border-radius: 8px; border: 2px solid #3b82f6; margin: 1rem 0;">
                <p style="margin: 0 0 0.75rem 0; color: #64748b; font-size: 0.875rem;"><strong>Link para o Cliente:</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            st.code(url_gerada, language="text")
            
            col_copy1, col_copy2, col_copy3 = st.columns([1, 1, 2])
            with col_copy1:
                if st.button("📋 Copiar Link", use_container_width=True, key="copy_btn"):
                    st.info(f"✅ Link copiado! Cole em qualquer lugar.")
            
            st.markdown("""
            <div style="background-color: #fff3cd; padding: 1rem; border-radius: 8px; border-left: 4px solid #f59e0b; margin-top: 1rem;">
                <p style="margin: 0; color: #856404; font-size: 0.875rem;"><strong>💡 Dica:</strong> Você pode copiar o link acima usando Ctrl+C (ou Cmd+C no Mac) e enviar para o cliente via WhatsApp, Email ou qualquer outro meio.</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; color: #64748b; font-size: 0.875rem;">
        <p>💡 <strong>Dica:</strong> Cada cliente recebe um link único com os documentos específicos que precisa enviar.</p>
    </div>
    """, unsafe_allow_html=True)

else:
    # MODO CLIENTE
    nome_cliente = urllib.parse.unquote(params.get("cliente", "Não identificado"))
    docs_string = urllib.parse.unquote(params.get("docs", ""))
    documentos_necessarios = docs_string.split(',') if docs_string else []
    
    # Header
    col_logo, col_title = st.columns([1, 5])
    with col_logo:
        st.image("https://generated-images.adapta.one/metalquimicaconsultoria%40gmail.com/019c5261-cf87-7648-a8f1-b054e6597b25/2026-02-12T20-00-06-149Z_Modern_minimalist_vector_logo_for_METAL_QUIMICA_CO.png", width=250)
    with col_title:
        st.title("⚗️ Portal de Envio de Documentos")
        st.markdown(f"**Cliente:** {nome_cliente}")
    
    st.markdown("---")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%); 
                padding: 1.5rem; border-radius: 8px; border-left: 4px solid #10b981;">
        <h3 style="margin-top: 0; color: #047857;">📤 Instruções de Envio</h3>
        <p>Por favor, anexe cada um dos documentos solicitados nos campos abaixo. O envio será realizado após você clicar no botão <strong>"ENVIAR TODOS OS DOCUMENTOS"</strong> no final da página.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    if not documentos_necessarios:
        st.error("❌ Link inválido ou nenhum documento foi solicitado.")
    else:
        st.markdown(f"""
        <div style="background-color: #f1f5f9; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;">
            <p style="margin: 0; color: #475569;"><strong>📊 Documentos a enviar:</strong> <span style="color: #3b82f6; font-weight: 700;">{len(documentos_necessarios)}</span></p>
        </div>
        """, unsafe_allow_html=True)
        
        arquivos_anexados = {}
        num_colunas = 3 if len(documentos_necessarios) > 5 else 2
        cols = st.columns(num_colunas)
        
        for i, documento in enumerate(documentos_necessarios):
            with cols[i % num_colunas]:
                st.markdown(f"""
                <div class="document-card-highlight">
                    <span class="document-icon-medium">📄</span>
                    <span class="document-name-medium">{documento}</span>
                </div>
                """, unsafe_allow_html=True)
                
                uploaded_file = st.file_uploader(
                    f'Selecione o arquivo',
                    type=['pdf', 'jpg', 'png', 'docx', 'jpeg'],
                    key=documento,
                    label_visibility="collapsed"
                )
                if uploaded_file is not None:
                    arquivos_anexados[documento] = uploaded_file
                    st.markdown(f"""
                    <div style="background-color: rgba(16, 185, 129, 0.1); padding: 0.5rem; border-radius: 4px; margin-top: 0.5rem;">
                        <p style="margin: 0; color: #047857; font-size: 0.875rem;">✅ {uploaded_file.name}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        progresso = len(arquivos_anexados) / len(documentos_necessarios)
        st.markdown(f"""
        <div style="background-color: #f1f5f9; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;">
            <p style="margin: 0 0 0.5rem 0; color: #475569; font-size: 0.875rem;"><strong>Progresso:</strong> {len(arquivos_anexados)}/{len(documentos_necessarios)} documentos</p>
            <div style="width: 100%; height: 8px; background-color: #e2e8f0; border-radius: 4px; overflow: hidden;">
                <div style="width: {progresso * 100}%; height: 100%; background: linear-gradient(90deg, #3b82f6, #06b6d4); transition: width 0.3s ease;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns([2, 1])
        
        with col_btn1:
            if st.button('🚀 ENVIAR TODOS OS DOCUMENTOS', use_container_width=True):
                if not arquivos_anexados:
                    st.warning("⚠️ Nenhum documento foi anexado.")
                else:
                    with st.spinner("📤 Enviando documentos... Por favor, aguarde."):
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
                            st.success(f"🎉 Sucesso! {sucessos} documento(s) foram enviados com sucesso!")
                            st.markdown("""
                            <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%); 
                                        padding: 1.5rem; border-radius: 8px; border-left: 4px solid #10b981; margin-top: 1rem;">
                                <p style="margin: 0; color: #047857;"><strong>✅ Obrigado!</strong> Seus documentos foram recebidos com sucesso. Entraremos em contato em breve.</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.error(f"❌ Falha no envio para: {', '.join(erros)}. Por favor, tente novamente.")
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; color: #64748b; font-size: 0.875rem;">
        <p>🔒 <strong>Segurança:</strong> Seus documentos são enviados de forma segura e criptografada.</p>
        <p style="margin-top: 1rem;">Desenvolvido por <strong>Angelo</strong> | Metal Química Consultoria</p>
    </div>
    """, unsafe_allow_html=True)

# --- FIM DO CÓDIGO COMPLETO ---
