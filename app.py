# ======================================================================
# PORTAL DE DOCUMENTOS - METAL QUÍMICA CONSULTORIA
# Tema Oficial Azul → Ciano | Layout Moderno Premium
# ======================================================================

import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import urllib.parse

# -----------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# -----------------------------------------------------------
st.set_page_config(
    page_title="Portal de Documentos - Metal Química",
    page_icon="⚗️",
    layout="wide"
)

# -----------------------------------------------------------
# TEMA OFICIAL METAL QUÍMICA (GRADIENTES PREMIUM)
# -----------------------------------------------------------
st.markdown("""
<style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    * { font-family: 'Inter', sans-serif; }

    /* Plano de fundo principal */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 50%, #06b6d4 100%) !important;
        padding: 0 !important;
    }

    /* Caixa principal */
    .main {
        background-color: rgba(255,255,255,0.85) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 12px !important;
        padding: 2rem !important;
        margin: 2rem !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }

    /* Títulos */
    h1, h2, h3 {
        color: #0f172a;
        font-weight: 700;
    }

    h1 { font-size: 2.8rem !important; }
    h2 { font-size: 1.9rem !important; }
    h3 { font-size: 1.3rem !important; }

    /* Botões */
    .stButton > button {
        background: linear-gradient(135deg, #0284c7, #3b82f6);
        border-radius: 8px;
        border: none;
        color: white;
        padding: 0.7rem 1.3rem;
        font-size: 1rem;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
        transition: 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        background: linear-gradient(135deg, #0369a1, #2563eb);
        box-shadow: 0 6px 18px rgba(0,0,0,0.35);
    }

    /* Cards elegantes */
    .metal-card {
        background: rgba(255,255,255,0.9);
        border-left: 5px solid #0284c7;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    }

    /* Documento */
    .documento {
        background: rgba(255,255,255,0.9);
        padding: 1rem;
        border-radius: 6px;
        border-left: 4px solid #0ea5e9;
        margin-bottom: 1rem;
        transition: 0.25s;
    }
    .documento:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------
# FUNÇÃO DE EMAIL
# -----------------------------------------------------------
def enviar_email_com_anexo(nome_documento, conteudo_arquivo, nome_arquivo_original):
    """
    Envia um email com anexo usando as credenciais armazenadas em st.secrets.
    Retorna True se bem-sucedido, False caso contrário.
    """
    try:
        # Verificação de secrets
        if "SENDER_EMAIL" not in st.secrets or "SENDER_PASSWORD" not in st.secrets or "RECIPIENT_EMAIL" not in st.secrets:
            st.error("❌ Erro: Credenciais de email não configuradas no Streamlit Secrets.")
            return False

        sender_email = st.secrets["SENDER_EMAIL"]
        sender_password = st.secrets["SENDER_PASSWORD"]
        recipient_email = st.secrets["RECIPIENT_EMAIL"]

        # Montagem do email
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = f"Novo Documento Recebido: {nome_documento}"

        corpo_email = f"""Olá Angelo,

Novo documento recebido:

Documento: {nome_documento}
Arquivo: {nome_arquivo_original}

Segue o anexo.

— Portal Metal Química"""

        msg.attach(MIMEText(corpo_email, "plain"))

        # Anexo
        anexo = MIMEApplication(conteudo_arquivo, Name=nome_arquivo_original)
        anexo["Content-Disposition"] = f'attachment; filename="{nome_arquivo_original}"'
        msg.attach(anexo)

        # Envio
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        return True

    except smtplib.SMTPAuthenticationError:
        st.error("❌ Erro de autenticação: Verifique o email e a senha de aplicativo.")
        return False
    except smtplib.SMTPException as e:
        st.error(f"❌ Erro SMTP: {e}")
        return False
    except Exception as e:
        st.error(f"❌ Erro inesperado ao enviar email: {e}")
        return False

# -----------------------------------------------------------
# MODO CLIENTE / MODO ADMIN
# -----------------------------------------------------------
params = st.query_params

# ===========================================================
# ========================= ADMIN ===========================
# ===========================================================
if len(params) == 0:

    col1, col2 = st.columns([1.3, 3])
    with col1:
        st.image(
            "https://generated-images.adapta.one/metalquimicaconsultoria%40gmail.com/"
            "019c5261-cf87-7648-a8f1-b054e6597b25/"
            "2026-02-12T20-00-06-149Z_Modern_minimalist_vector_logo_for_METAL_QUIMICA_CO.png",
            width=300
        )
    with col2:
        st.title("⚗️ Portal de Gestão de Documentos")
        st.subheader("Metal Química Consultoria")

    st.markdown('<div class="metal-card"><h3>⚙️ Configuração do Link do Cliente</h3></div>', unsafe_allow_html=True)

    MASTER_LISTA = [
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

    nome_cliente = st.text_input("Nome do Cliente", placeholder="Ex: Metalúrgica Alfa LTDA")

    documentos = st.multiselect(
        "Documentos necessários:",
        options=sorted(MASTER_LISTA)
    )

    if st.button("🔗 GERAR LINK", use_container_width=True):

        if not nome_cliente.strip():
            st.error("❌ Digite o nome do cliente.")
        elif not documentos:
            st.error("❌ Selecione pelo menos um documento.")
        else:
            # Codificação correta dos parâmetros
            docs_param = ",".join([urllib.parse.quote(doc) for doc in documentos])
            cliente_param = urllib.parse.quote(nome_cliente)

            # URL base (ajuste conforme seu deploy)
            URL_BASE = "app-documentos-7l5ecrvyv7lhjl3ska9e3t.streamlit.app"
            link_final = f"https://{URL_BASE}?cliente={cliente_param}&docs={docs_param}"

            st.success("✅ Link gerado com sucesso!")
            st.code(link_final, language="text")

            st.info("💡 Copie o link acima e envie ao cliente.")


# ===========================================================
# ======================== CLIENTE ===========================
# ===========================================================
else:
    # Decodificação dos parâmetros
    nome_cliente = urllib.parse.unquote(params.get("cliente", ["Cliente"])[0])
    docs_str = urllib.parse.unquote(params.get("docs", [""])[0])
    lista_docs = [doc.strip() for doc in docs_str.split(",") if doc.strip()]

    st.title("📄 Portal de Envio de Documentos")
    st.subheader(f"Cliente: **{nome_cliente}**")

    if not lista_docs:
        st.error("❌ Nenhum documento foi especificado no link. Entre em contato com a Metal Química.")
    else:
        st.markdown('<div class="metal-card"><h3>📤 Envie seus documentos</h3></div>', unsafe_allow_html=True)

        arquivos = {}
        colunas = st.columns(2)

        for i, doc in enumerate(lista_docs):
            with colunas[i % 2]:
                st.markdown(f'<div class="documento">📄 <b>{doc}</b></div>', unsafe_allow_html=True)
                up = st.file_uploader(f"Selecione: {doc}", key=doc, label_visibility="collapsed")
                if up:
                    arquivos[doc] = up

        st.markdown("---")

        if st.button("🚀 ENVIAR TODOS OS ARQUIVOS", use_container_width=True):
            if not arquivos:
                st.error("❌ Nenhum arquivo foi enviado.")
            else:
                sucesso = 0
                falhas = []

                with st.spinner("📤 Enviando documentos..."):
                    for doc, arq in arquivos.items():
                        ok = enviar_email_com_anexo(doc, arq.getvalue(), arq.name)
                        if ok: 
                            sucesso += 1
                        else: 
                            falhas.append(doc)

                if not falhas:
                    st.success(f"🎉 Sucesso! {sucesso} arquivo(s) enviado(s) com sucesso!")
                else:
                    st.warning(f"⚠️ {sucesso} arquivo(s) enviado(s), mas houve falha em: {', '.join(falhas)}")


# -----------------------------------------------------------
# Rodapé
# -----------------------------------------------------------
st.markdown("""
<hr>
<center>
<p style='color:#0f172a'>Desenvolvido por <b>Metal Química Consultoria</b></p>
</center>
""", unsafe_allow_html=True)
