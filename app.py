import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import urllib.parse

# --- Bloco 1: Configuração da Página ---
st.set_page_config(
    page_title="Portal Metal Química",
    page_icon="⚗️",
    layout="wide"
)

# --- CSS MINIMALISTA & PROFISSIONAL (TEMA CINZA/CLEAN) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Reset e Fonte Global */
    * { font-family: 'Inter', sans-serif; color: #334155; }

    /* Fundo da Página: Cinza Claro Suave (Papel) */
    [data-testid="stAppViewContainer"] {
        background-color: #f8fafc !important; /* Cinza muito claro */
        background-image: none !important;
    }

    /* Container Principal: Branco Puro com Sombra Suave */
    .main .block-container {
        background-color: #ffffff !important;
        border-radius: 12px !important;
        padding: 3rem !important;
        margin-top: 2rem !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05) !important; /* Sombra muito leve */
        max-width: 1200px !important;
        border: 1px solid #e2e8f0;
    }

    /* Títulos */
    h1, h2, h3 {
        color: #1e293b !important; /* Cinza Chumbo Escuro */
        font-weight: 700 !important;
    }
    
    /* Header Unificado */
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-bottom: 40px;
        padding-bottom: 20px;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .header-logo {
        height: 90px;
        width: auto;
        margin-bottom: 15px;
    }
    
    .header-title {
        font-size: 1.8rem;
        color: #334155;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 0;
    }

    /* Cards de Documentos - Estilo "Clean" */
    .doc-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #64748b; /* Detalhe Cinza Metálico */
        border-radius: 8px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        transition: all 0.2s ease;
    }
    
    .doc-card:hover {
        border-color: #cbd5e1;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        transform: translateY(-2px);
    }

    .doc-title {
        font-weight: 600;
        color: #1e293b;
        font-size: 1rem;
        display: block;
    }

    /* Botões - Sóbrios (Cinza Chumbo) */
    .stButton > button {
        background-color: #334155 !important; /* Cinza Escuro */
        color: white !important;
        border: none !important;
        padding: 0.8rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        border-radius: 6px !important;
        transition: all 0.2s ease !important;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: #1e293b !important; /* Mais escuro no hover */
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
        transform: translateY(-1px);
    }

    /* Inputs */
    .stTextInput > div > div > input, .stMultiSelect > div > div > div {
        background-color: #f8fafc;
        border: 1px solid #cbd5e1;
        color: #334155;
        border-radius: 6px;
    }

    /* Rodapé Limpo */
    .footer-container {
        margin-top: 50px;
        padding-top: 30px;
        border-top: 1px solid #e2e8f0;
        text-align: center;
        background-color: transparent;
    }
    
    .footer-text {
        color: #64748b;
        font-size: 0.9rem;
        margin-bottom: 5px;
    }
    
    .footer-links a {
        color: #475569;
        text-decoration: none;
        font-weight: 600;
        margin: 0 15px;
        font-size: 0.95rem;
        transition: color 0.2s;
    }
    
    .footer-links a:hover {
        color: #0f172a;
        text-decoration: underline;
    }

</style>
""", unsafe_allow_html=True)

# --- Bloco 2: Função de Envio de E-mail (Mantida Intacta) ---
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

# --- Bloco 3: Lógica Principal ---

params = st.query_params
LOGO_URL = "https://generated-images.adapta.one/metalquimicaconsultoria%40gmail.com/019c5261-cf87-7648-a8f1-b054e6597b25/2026-02-12T20-00-06-149Z_Modern_minimalist_vector_logo_for_METAL_QUIMICA_CO.png"

# --- HEADER UNIFICADO (Limpo e Centralizado) ---
st.markdown(f"""
    <div class="header-container">
        <img src="{LOGO_URL}" class="header-logo">
        <h1 class="header-title">Metal Química Consultoria</h1>
    </div>
""", unsafe_allow_html=True)


# MODO 1: ADMIN
if not params:
    st.markdown("### ⚙️ Configuração de Link")
    st.info("Painel administrativo para geração de links de upload.")

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
    
    col_admin1, col_admin2 = st.columns(2)
    
    with col_admin1:
        nome_cliente_config = st.text_input("Nome do Cliente / Empresa")
    
    with col_admin2:
        documentos_selecionados = st.multiselect(
            "Selecione os documentos solicitados:",
            options=sorted(MASTER_LISTA_DOCUMENTOS)
        )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔗 GERAR LINK"):
        if not nome_cliente_config:
            st.error("⚠️ Por favor, digite o nome do cliente.")
        elif not documentos_selecionados:
            st.error("⚠️ Por favor, selecione pelo menos um documento.")
        else:
            docs_param = ",".join(urllib.parse.quote(doc) for doc in documentos_selecionados)
            cliente_param = urllib.parse.quote(nome_cliente_config)
            
            # URL BASE
            URL_BASE_DA_SUA_APP = "app-documentos-7l5ecrvyv7lhjl3ska9e3t.streamlit.app"
            url_gerada = f"https://{URL_BASE_DA_SUA_APP}?cliente={cliente_param}&docs={docs_param}"
            
            st.success("✅ Link gerado com sucesso!")
            st.code(url_gerada)

# MODO 2: CLIENTE
else:
    nome_cliente = urllib.parse.unquote(params.get("cliente", "Não identificado"))
    docs_string = urllib.parse.unquote(params.get("docs", ""))
    documentos_necessarios = docs_string.split(',') if docs_string else []

    st.markdown(f"<h3 style='text-align: center; color: #64748b; font-weight: 400;'>Portal de Envio de Documentos</h3>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center; color: #1e293b; margin-top: -10px;'>{nome_cliente}</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    if not documentos_necessarios:
        st.error("Link inválido ou expirado.")
    else:
        arquivos_anexados = {}
        # Layout responsivo
        num_colunas = 3 if len(documentos_necessarios) > 4 else 2
        cols = st.columns(num_colunas)

        for i, documento in enumerate(documentos_necessarios):
            with cols[i % num_colunas]:
                # Card HTML Clean
                st.markdown(f"""
                <div class="doc-card">
                    <span class="doc-title">{documento}</span>
                </div>
                """, unsafe_allow_html=True)
                
                uploaded_file = st.file_uploader(
                    f"Selecione o arquivo para {documento}", 
                    type=['pdf', 'jpg', 'png', 'docx', 'jpeg'],
                    key=documento,
                    label_visibility="collapsed"
                )
                if uploaded_file is not None:
                    arquivos_anexados[documento] = uploaded_file
                    st.markdown("<span style='color: #10b981; font-size: 0.8rem; font-weight: 600;'>✓ Arquivo anexado</span>", unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)

        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button('ENVIAR DOCUMENTOS'):
                if not arquivos_anexados:
                    st.warning("⚠️ Nenhum documento foi anexado ainda.")
                else:
                    with st.spinner("Enviando..."):
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
                            st.success(f"Sucesso! {sucessos} documento(s) foram enviados.")
                        else:
                            st.error(f"Erro ao enviar: {', '.join(erros)}.")

# --- RODAPÉ CLEAN E SUAVE ---
st.markdown("""
<div class="footer-container">
    <div class="footer-links">
        <a href="https://wa.me/5517991434883" target="_blank">📱 (17) 99143-4883</a>
        <a href="mailto:metalquimicaconsultoria@gmail.com">📧 metalquimicaconsultoria@gmail.com</a>
    </div>
    <br>
    <p class="footer-text">Metal Química Consultoria • Soluções Ambientais</p>
    <p class="footer-text" style="font-size: 0.8rem; color: #94a3b8;">© 2026 Todos os direitos reservados.</p>
</div>
""", unsafe_allow_html=True)
