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

# --- CSS OTIMIZADO (BOTÕES COMPACTOS, LOGO E NOME ORIGINAIS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    * { font-family: 'Inter', sans-serif; color: #334155; }

    [data-testid="stAppViewContainer"] {
        background-color: #f8fafc !important;
    }

    .main .block-container {
        background-color: #ffffff !important;
        border-radius: 12px !important;
        padding: 2rem !important;
        margin-top: 1rem !important;
        max-width: 1200px !important;
        border: 1px solid #e2e8f0;
    }

    /* Header - LOGO E NOME PRÓXIMOS */
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin: 20px 0 5px 0;  /* Reduzido margin-bottom */
        padding-bottom: 5px;    /* Reduzido padding-bottom */
        border-bottom: 1px solid #e2e8f0;
    }
    
    .header-logo {
        width: 550px;
        max-width: 100%;
        margin-bottom: 0px;  /* REMOVIDO espaço abaixo da logo */
    }

    /* Cards compactos */
    .doc-card {
        background: #fff;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #64748b;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 8px;
    }

    .doc-title {
        font-weight: 600;
        color: #334155;
        font-size: 15px;
    }

    /* BOTÕES COMPACTOS */
    .stButton > button {
        background: #64748b !important;
        color: #fff !important;
        border: none !important;
        padding: 8px 16px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
        width: 100%;
        min-height: 36px !important;
    }
    
    .stButton > button:hover {
        background: #475569 !important;
    }

    /* File uploader mais compacto */
    .stFileUploader > div > div {
        padding: 6px !important;
    }
    
    .stFileUploader small {
        font-size: 12px !important;
    }

    /* Títulos - PRÓXIMOS DA LOGO */
    .cliente-subtitulo {
        text-align: center;
        color: #94a3b8;
        font-size: 16px;
        margin: 5px 0 2px 0;  /* Margem superior reduzida */
    }
    
    .cliente-nome {
        text-align: center;
        color: #334155;
        font-size: 32px;
        font-weight: 700;
        margin: 0 0 10px 0;  /* Margem superior zerada */
    }

    /* Rodapé */
    .footer-container {
        margin-top: 30px;
        padding-top: 20px;
        border-top: 1px solid #e2e8f0;
        text-align: center;
    }
    
    .footer-links a {
        color: #64748b;
        text-decoration: none;
        font-weight: 600;
        margin: 0 12px;
        font-size: 14px;
    }

    /* Alerts e info compactos */
    .stAlert {
        padding: 10px 14px !important;
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
LOGO_URL = "https://generated-images.adapta.one/metalquimicaconsultoria%40gmail.com/019c5261-cf87-7648-a8f1-b054e6597b25/2026-02-12T20-00-06-149Z_Modern_minimalist_vector_logo_for_METAL_QUIMICA_CO.png"

st.markdown(f'<div class="header-container"><img src="{LOGO_URL}" class="header-logo"></div>', unsafe_allow_html=True)

# MODO ADMIN
if not is_cliente:
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
    
    c1, c2 = st.columns(2)
    with c1:
        nome_cliente_config = st.text_input("Nome do Cliente / Empresa")
    with c2:
        documentos_selecionados = st.multiselect("Selecione os documentos:", options=sorted(MASTER_LISTA_DOCUMENTOS))

    if st.button("🔗 GERAR LINK"):
        if not nome_cliente_config or not documentos_selecionados:
            st.error("Preencha todos os campos.")
        else:
            docs_param = ",".join(urllib.parse.quote(d) for d in documentos_selecionados)
            cliente_param = urllib.parse.quote(nome_cliente_config)
            url = f"https://app-documentos-7l5ecrvyv7lhjl3ska9e3t.streamlit.app?cliente={cliente_param}&docs={docs_param}"
            st.success("Link gerado com sucesso!")
            st.code(url)

# MODO CLIENTE
else:
    nome_cliente = urllib.parse.unquote(params.get("cliente", "Não identificado"))
    docs = urllib.parse.unquote(params.get("docs", "")).split(',') if params.get("docs") else []

    st.markdown(f'<p class="cliente-subtitulo">Portal de Envio de Documentos</p>', unsafe_allow_html=True)
    st.markdown(f'<h2 class="cliente-nome">{nome_cliente}</h2>', unsafe_allow_html=True)
    st.markdown("---")
    
    if not docs:
        st.error("Link inválido ou expirado.")
    else:
        arquivos = {}
        cols = st.columns(3) if len(docs) > 4 else st.columns(2)

        for i, doc in enumerate(docs):
            with cols[i % len(cols)]:
                st.markdown(f'<div class="doc-card"><span class="doc-title">📄 {doc}</span></div>', unsafe_allow_html=True)
                
                up = st.file_uploader(f"Arquivo {i}", type=['pdf','jpg','png','docx','jpeg'], key=doc, label_visibility="collapsed")
                if up:
                    arquivos[doc] = up
                    st.markdown("<p style='color:#10b981;font-size:12px;margin:4px 0;text-align:center'>✓ Arquivo anexado</p>", unsafe_allow_html=True)

        if arquivos:
            c1, c2, c3 = st.columns([1,2,1])
            with c2:
                if st.button('📤 ENVIAR DOCUMENTOS'):
                    with st.spinner("Enviando..."):
                        erros, ok = [], 0
                        for d, a in arquivos.items():
                            if enviar_email_com_anexo(f"{d} ({nome_cliente})", a.getvalue(), a.name):
                                ok += 1
                            else:
                                erros.append(d)
                        
                        if not erros:
                            st.balloons()
                            st.success(f"Sucesso! {ok} documento(s) enviados.")
                        else:
                            st.error(f"Erro ao enviar: {', '.join(erros)}")

# Rodapé
st.markdown("""
<div class="footer-container">
    <div class="footer-links">
        <a href="https://wa.me/5517991434883">📱 (17) 99143-4883</a>
        <a href="mailto:metalquimicaconsultoria@gmail.com">✉️ metalquimicaconsultoria@gmail.com</a>
    </div>
    <p style="color:#94a3b8;font-size:13px;margin:10px 0 0 0">Metal Química Consultoria © 2026</p>
</div>
""", unsafe_allow_html=True)
