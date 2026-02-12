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

# --- CSS PREMIUM (VISUAL PROFISSIONAL) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    /* Reset e Fonte Global */
    * { font-family: 'Inter', sans-serif; }

    /* Fundo Fluido (Deep Ocean Gradient) */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(120deg, #0f172a 0%, #1e3a8a 40%, #0ea5e9 100%) !important;
        background-attachment: fixed !important;
    }

    /* Container Principal (Vidro Fosco Profissional) */
    .main .block-container {
        background-color: rgba(255, 255, 255, 0.96) !important; /* Branco quase sólido para leitura */
        border-radius: 16px !important;
        padding: 3rem !important;
        margin-top: 2rem !important;
        box-shadow: 0 20px 50px rgba(0,0,0,0.3) !important;
        max-width: 1200px !important;
    }

    /* Títulos */
    h1, h2, h3 {
        color: #0f172a !important; /* Azul Escuro Profundo */
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }
    
    p, li, label {
        color: #334155 !important; /* Cinza Chumbo para leitura confortável */
        font-size: 1rem;
    }

    /* Header Personalizado com Logo */
    .header-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
        margin-bottom: 40px;
        padding-bottom: 20px;
        border-bottom: 2px solid #e2e8f0;
        flex-wrap: wrap;
    }
    
    .header-logo {
        height: 80px;
        width: auto;
        filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));
    }
    
    .header-title {
        font-size: 2.2rem;
        color: #1e3a8a;
        font-weight: 800;
        text-transform: uppercase;
        margin: 0;
    }

    /* Cards de Documentos */
    .doc-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 5px solid #0ea5e9; /* Detalhe Ciano */
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .doc-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(14, 165, 233, 0.15);
        border-left-color: #3b82f6;
    }

    .doc-title {
        font-weight: 600;
        color: #1e40af;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        display: block;
    }

    /* Botões Estilizados */
    .stButton > button {
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.8rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.5) !important;
        filter: brightness(1.1);
    }

    /* Inputs e Selects */
    .stTextInput > div > div > input, .stMultiSelect > div > div > div {
        background-color: #f1f5f9;
        border-radius: 8px;
        border: 1px solid #cbd5e1;
        color: #0f172a;
    }

    /* Rodapé */
    .footer-container {
        margin-top: 4rem;
        padding-top: 2rem;
        border-top: 1px solid #e2e8f0;
        text-align: center;
    }
    
    .footer-link {
        color: #0ea5e9;
        text-decoration: none;
        font-weight: 600;
        margin: 0 10px;
        transition: color 0.2s;
    }
    
    .footer-link:hover {
        color: #1e3a8a;
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

# --- HEADER UNIFICADO (Aparece em ambas as telas) ---
st.markdown(f"""
    <div class="header-container">
        <img src="{LOGO_URL}" class="header-logo">
        <h1 class="header-title">Metal Química Consultoria</h1>
    </div>
""", unsafe_allow_html=True)


# MODO 1: ADMIN
if not params:
    st.markdown("### ⚙️ Painel de Controle - Gerador de Links")
    st.info("Configure abaixo o link exclusivo para seu cliente enviar os documentos.")

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

    if st.button("🔗 GERAR LINK SEGURO"):
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

    st.markdown(f"<h2 style='text-align: center; color: #334155;'>Portal de Envio de Documentos</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: #0ea5e9; margin-bottom: 30px;'>Cliente: {nome_cliente}</h3>", unsafe_allow_html=True)
    
    st.info("ℹ️ **Instruções:** Anexe os arquivos solicitados abaixo. O envio final é feito ao clicar no botão 'ENVIAR' no final da página.")

    if not documentos_necessarios:
        st.error("Link inválido ou expirado.")
    else:
        arquivos_anexados = {}
        # Layout responsivo inteligente
        num_colunas = 3 if len(documentos_necessarios) > 4 else 2
        cols = st.columns(num_colunas)

        for i, documento in enumerate(documentos_necessarios):
            with cols[i % num_colunas]:
                # Card HTML personalizado
                st.markdown(f"""
                <div class="doc-card">
                    <span class="doc-title">📄 {documento}</span>
                </div>
                """, unsafe_allow_html=True)
                
                uploaded_file = st.file_uploader(
                    f"Selecione o arquivo para {documento}", # Label simplificada
                    type=['pdf', 'jpg', 'png', 'docx', 'jpeg'],
                    key=documento,
                    label_visibility="collapsed" # Esconde label padrão para usar o card
                )
                if uploaded_file is not None:
                    arquivos_anexados[documento] = uploaded_file
                    st.success("Arquivo anexado!")

        st.markdown("---")

        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button('🚀 ENVIAR TODOS OS DOCUMENTOS'):
                if not arquivos_anexados:
                    st.warning("⚠️ Nenhum documento foi anexado ainda.")
                else:
                    with st.spinner("Enviando seus documentos com segurança..."):
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
                            st.success(f"🎉 Sucesso Absoluto! {sucessos} documento(s) foram enviados para nossa equipe.")
                        else:
                            st.error(f"Ocorreu um erro ao enviar: {', '.join(erros)}. Tente novamente.")

# --- RODAPÉ PROFISSIONAL ATUALIZADO ---
st.markdown("""
<div class="footer-container">
    <p style="font-weight: 600; color: #1e3a8a; margin-bottom: 10px;">METAL QUÍMICA CONSULTORIA</p>
    <p style="font-size: 0.9rem; color: #64748b;">Excelência em Gestão Ambiental e Regularizações</p>
    
    <div style="margin-top: 20px;">
        <a href="https://wa.me/5517991434883" target="_blank" class="footer-link">📱 (17) 99143-4883</a>
        <span style="color: #cbd5e1;">|</span>
        <a href="mailto:metalquimicaconsultoria@gmail.com" class="footer-link">📧 metalquimicaconsultoria@gmail.com</a>
    </div>
    
    <p style="margin-top: 30px; font-size: 0.8rem; color: #94a3b8;">
        © 2026 Metal Química. Todos os direitos reservados.
    </p>
</div>
""", unsafe_allow_html=True)
