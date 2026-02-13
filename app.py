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

# Verificar se é modo cliente
params = st.query_params
is_cliente = bool(params)

# --- CSS COMPACTO E OTIMIZADO ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    * { font-family: 'Inter', sans-serif; color: #334155; font-size: 14px; }

    [data-testid="stAppViewContainer"] {
        background-color: #f8fafc !important;
    }

    .main .block-container {
        background-color: #ffffff !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        margin-top: 0.5rem !important;
        max-width: 1200px !important;
        border: 1px solid #e2e8f0;
    }

    /* Header compacto */
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin: 10px 0 10px 0;
        padding-bottom: 8px;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .header-logo {
        width: 280px;
        max-width: 90%;
    }

    /* Cards super compactos */
    .doc-card {
        background: #fff;
        border: 1px solid #e2e8f0;
        border-left: 3px solid #64748b;
        border-radius: 6px;
        padding: 8px 10px;
        margin-bottom: 6px;
    }

    .doc-title {
        font-weight: 600;
        color: #334155;
        font-size: 13px;
    }

    /* Botões compactos */
    .stButton > button {
        background: #64748b !important;
        color: #fff !important;
        border: none !important;
        padding: 10px 16px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: #475569 !important;
    }

    /* File uploader compacto */
    .stFileUploader > div > div {
        padding: 4px !important;
    }
    
    .stFileUploader small {
        font-size: 11px !important;
    }

    /* Títulos compactos */
    h1 { font-size: 18px !important; }
    h2 { font-size: 16px !important; }
    h3 { font-size: 14px !important; }

    /* Rodapé compacto */
    .footer-container {
        margin-top: 20px;
        padding-top: 12px;
        border-top: 1px solid #e2e8f0;
        text-align: center;
        font-size: 12px;
    }
    
    .footer-links a {
        color: #64748b;
        text-decoration: none;
        font-weight: 600;
        margin: 0 10px;
        font-size: 12px;
    }

    /* Info e alerts compactos */
    .stAlert {
        padding: 8px 12px !important;
        font-size: 12px !important;
    }
    
    .stAlert > div {
        gap: 8px !important;
    }

    /* Multiselect compacto */
    .stMultiSelect > div > div {
        min-height: 36px !important;
    }

    /* Inputs compactos */
    .stTextInput > div > div > input {
        padding: 6px 10px !important;
        font-size: 13px !important;
    }

    /* Sucesso/erro compacto */
    .stSuccess, .stError, .stWarning {
        padding: 8px 12px !important;
        font-size: 12px !important;
    }

</style>
""", unsafe_allow_html=True)

# --- Bloco 2: Função de Envio ---
def enviar_email_com_anexo(nome_documento, conteudo_arquivo, nome_arquivo_original):
    try:
        sender_email = st.secrets["SENDER_EMAIL"]
        sender_password = st.secrets["SENDER_PASSWORD"]
        recipient_email = st.secrets["RECIPIENT_EMAIL"]

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"Doc: {nome_documento}"

        corpo = f"Olá Angelo,\n\nDocumento recebido: {nome_documento}\nArquivo: {nome_arquivo_original}"
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
        print(f"Erro: {e}")
        return False

# --- Bloco 3: Lógica Principal ---
LOGO_URL = "https://generated-images.adapta.one/metalquimicaconsultoria%40gmail.com/019c5261-cf87-7648-a8f1-b054e6597b25/2026-02-12T20-00-06-149Z_Modern_minimalist_vector_logo_for_METAL_QUIMICA_CO.png"

st.markdown(f'<div class="header-container"><img src="{LOGO_URL}" class="header-logo"></div>', unsafe_allow_html=True)

# MODO ADMIN
if not is_cliente:
    st.markdown("#### ⚙️ Gerar Link")
    st.info("Crie links personalizados para seus clientes.")

    MASTER_LISTA_DOCUMENTOS = [
        'Matrícula do terreno ou IPTU',
        'Contrato Social',
        'Certificado do IBAMA',
        'Procuração Assinada',
        'Documentação EPP',
        'Certidão JUSCESP',
        'Layout',
        'Planta do Prédio',
        'Cartão CNPJ',
        'Certidão Uso do Solo',
        'CICAR rural',
        'Dados do Proprietário',
        'Bombeiros (AVCB)',
        'Contas de Água/Outorga',
        'Fluxograma Produtivo',
        'CADRI',
        'Laudo Analítico',
        'Comprovante CETESB',
        'CNH Representante Legal'
    ]
    
    c1, c2 = st.columns(2)
    with c1:
        nome_cliente_config = st.text_input("Cliente", placeholder="Nome da empresa")
    with c2:
        documentos_selecionados = st.multiselect("Documentos:", options=sorted(MASTER_LISTA_DOCUMENTOS))

    if st.button("🔗 GERAR LINK"):
        if not nome_cliente_config or not documentos_selecionados:
            st.error("Preencha todos os campos.")
        else:
            docs_param = ",".join(urllib.parse.quote(d) for d in documentos_selecionados)
            cliente_param = urllib.parse.quote(nome_cliente_config)
            url = f"https://app-documentos-7l5ecrvyv7lhjl3ska9e3t.streamlit.app?cliente={cliente_param}&docs={docs_param}"
            st.success("Link gerado!")
            st.code(url)

# MODO CLIENTE
else:
    nome_cliente = urllib.parse.unquote(params.get("cliente", "Cliente"))
    docs = urllib.parse.unquote(params.get("docs", "")).split(',') if params.get("docs") else []

    st.markdown(f"<p style='text-align:center;color:#64748b;font-size:12px;margin:0'>Portal de Documentos</p>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align:center;margin:0 0 10px 0;font-size:20px'>{nome_cliente}</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    if not docs:
        st.error("Link inválido.")
    else:
        arquivos = {}
        cols = st.columns(3) if len(docs) > 4 else st.columns(2)

        for i, doc in enumerate(docs):
            with cols[i % len(cols)]:
                st.markdown(f'<div class="doc-card"><span class="doc-title">📄 {doc}</span></div>', unsafe_allow_html=True)
                
                up = st.file_uploader(f"Arquivo {i}", type=['pdf','jpg','png','docx','jpeg'], key=doc, label_visibility="collapsed")
                if up:
                    arquivos[doc] = up
                    st.markdown("<p style='color:#10b981;font-size:11px;margin:2px 0;text-align:center'>✓ OK</p>", unsafe_allow_html=True)

        if arquivos:
            c1, c2, c3 = st.columns([1,2,1])
            with c2:
                if st.button('📤 ENVIAR'):
                    with st.spinner("Enviando..."):
                        erros, ok = [], 0
                        for d, a in arquivos.items():
                            if enviar_email_com_anexo(f"{d} ({nome_cliente})", a.getvalue(), a.name):
                                ok += 1
                            else:
                                erros.append(d)
                        
                        if not erros:
                            st.balloons()
                            st.success(f"{ok} documento(s) enviados!")
                        else:
                            st.error(f"Erro: {', '.join(erros)}")

# Rodapé
st.markdown("""
<div class="footer-container">
    <div class="footer-links">
        <a href="https://wa.me/5517991434883">📱 (17) 99143-4883</a>
        <a href="mailto:metalquimicaconsultoria@gmail.com">✉️ metalquimicaconsultoria@gmail.com</a>
    </div>
    <p style="color:#94a3b8;font-size:11px;margin:8px 0 0 0">Metal Química Consultoria © 2026</p>
</div>
""", unsafe_allow_html=True)
