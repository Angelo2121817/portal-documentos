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

# Verificar se é modo cliente (tem parâmetros na URL)
params = st.query_params
is_cliente = bool(params)

# --- CSS MINIMALISTA & PROFISSIONAL (TEMA SUAVE) ---
# Define margem diferente: Admin (topo) vs Cliente (topo também, sem descida)
margin_top = "20px" if is_cliente else "40px"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Reset e Fonte Global */
    * {{ font-family: 'Inter', sans-serif; color: #334155; }}

    /* Fundo da Página: Cinza Claro Suave */
    [data-testid="stAppViewContainer"] {{
        background-color: #f8fafc !important; 
        background-image: none !important;
    }}

    /* Container Principal: Branco Puro com Sombra Suave */
    .main .block-container {{
        background-color: #ffffff !important;
        border-radius: 12px !important;
        padding: 2rem !important;  /* Reduzido de 3rem para 2rem */
        margin-top: 1rem !important;  /* Reduzido de 2rem para 1rem */
        box-shadow: 0 4px 20px rgba(0,0,0,0.05) !important;
        max-width: 1200px !important;
        border: 1px solid #e2e8f0;
    }}

    /* Títulos */
    h1, h2, h3 {{
        color: #1e293b !important;
        font-weight: 700 !important;
    }}
    
    /* Header Unificado - MARGEM MÍNIMA (TOPO DA PÁGINA) */
    .header-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: {margin_top};  /* <--- 20px para cliente (topo), 40px para admin */
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 1px solid #e2e8f0;
    }}
    
    /* LOGO - TAMANHO REDUZIDO PARA CABER MELHOR NO TOPO */
    .header-logo {{
        height: auto;
        width: 400px;  /* <--- REDUZIDO de 550px para 400px */
        max-width: 100%; 
        margin-bottom: 0px;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.05));
    }}

    /* Cards de Documentos - Estilo "Clean" */
    .doc-card {{
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 5px solid #94a3b8;
        border-radius: 8px;
        padding: 1rem;  /* Reduzido de 1.2rem */
        margin-bottom: 0.8rem;  /* Reduzido de 1rem */
        transition: all 0.2s ease;
    }}
    
    .doc-card:hover {{
        border-color: #cbd5e1;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transform: translateY(-2px);
    }}

    .doc-title {{
        font-weight: 700;
        color: #334155;
        font-size: 1rem;  /* Reduzido de 1.1rem */
        display: block;
    }}

    /* BOTÕES SUAVIZADOS (Cinza Nuvem) */
    .stButton > button {{
        background-color: #64748b !important;
        color: #ffffff !important;
        border: none !important;
        padding: 0.8rem 1.5rem !important;  /* Reduzido */
        font-size: 1rem !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
        width: 100%;
        letter-spacing: 0.5px;
    }}
    
    .stButton > button:hover {{
        background-color: #475569 !important;
        box-shadow: 0 6px 15px rgba(0,0,0,0.10) !important;
        transform: translateY(-2px);
        color: #ffffff !important;
    }}

    /* Inputs */
    .stTextInput > div > div > input, .stMultiSelect > div > div > div {{
        background-color: #f8fafc;
        border: 1px solid #cbd5e1;
        color: #334155;
        border-radius: 6px;
        font-size: 1rem;
    }}

    /* Rodapé Limpo */
    .footer-container {{
        margin-top: 40px;  /* Reduzido de 60px */
        padding-top: 20px;  /* Reduzido de 30px */
        border-top: 1px solid #e2e8f0;
        text-align: center;
        background-color: transparent;
    }}
    
    .footer-text {{
        color: #94a3b8;
        font-size: 0.9rem;  /* Reduzido de 0.95rem */
        margin-bottom: 8px;
    }}
    
    .footer-links a {{
        color: #64748b;
        text-decoration: none;
        font-weight: 600;
        margin: 0 15px;
        font-size: 0.95rem;  /* Reduzido de 1rem */
        transition: color 0.2s;
        display: inline-block;
        padding: 5px;
    }}
    
    .footer-links a:hover {{
        color: #334155;
        text-decoration: underline;
    }}

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

LOGO_URL = "https://generated-images.adapta.one/metalquimicaconsultoria%40gmail.com/019c5261-cf87-7648-a8f1-b054e6597b25/2026-02-12T20-00-06-149Z_Modern_minimalist_vector_logo_for_METAL_QUIMICA_CO.png"

# --- HEADER SÓ COM LOGO ---
st.markdown(f"""
    <div class="header-container">
        <img src="{LOGO_URL}" class="header-logo">
    </div>
""", unsafe_allow_html=True)


# MODO 1: ADMIN (sem parâmetros)
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
            
            URL_BASE_DA_SUA_APP = "app-documentos-7l5ecrvyv7lhjl3ska9e3t.streamlit.app"
            url_gerada = f"https://{URL_BASE_DA_SUA_APP}?cliente={cliente_param}&docs={docs_param}"
            
            st.success("✅ Link gerado com sucesso!")
            st.code(url_gerada)

# MODO 2: CLIENTE (TOPO DA PÁGINA - SEM ESPAÇAMENTO EXCESSIVO)
else:
    nome_cliente = urllib.parse.unquote(params.get("cliente", "Não identificado"))
    docs_string = urllib.parse.unquote(params.get("docs", ""))
    documentos_necessarios = docs_string.split(',') if docs_string else []

    # Títulos compactos no topo
    st.markdown(f"<p style='text-align: center; color: #94a3b8; font-weight: 400; font-size: 0.95rem; margin: 0 0 2px 0;'>Portal de Envio de Documentos</p>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center; color: #334155; margin: 0 0 15px 0; font-size: 1.8rem;'>{nome_cliente}</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    if not documentos_necessarios:
        st.error("Link inválido ou expirado.")
    else:
        arquivos_anexados = {}
        num_colunas = 3 if len(documentos_necessarios) > 4 else 2
        cols = st.columns(num_colunas)

        for i, documento in enumerate(documentos_necessarios):
            with cols[i % num_colunas]:
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
                    st.markdown("<div style='text-align: center; margin-top: 3px;'><span style='color: #10b981; font-size: 0.85rem; font-weight: 700; background-color: #ecfdf5; padding: 3px 6px; border-radius: 4px;'>✓ Pronto</span></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

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
                            st.error(f"Erro ao enviar: {', '.join(erros)}")

# --- RODAPÉ CLEAN E SUAVE ---
st.markdown("""
<div class="footer-container">
    <div class="footer-links">
        <a href="https://wa.me/5517991434883" target="_blank">📱 (17) 99143-4883</a>
        <a href="mailto:metalquimicaconsultoria@gmail.com">📧 metalquimicaconsultoria@gmail.com</a>
    </div>
    <br>
    <p class="footer-text">Soluções Ambientais e Regularizações</p>
    <p class="footer-text" style="font-size: 0.75rem; color: #cbd5e1;">© 2026 Todos os direitos reservados.</p>
</div>
""", unsafe_allow_html=True)
