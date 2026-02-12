import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import urllib.parse

# Configuração da página
st.set_page_config(
    page_title="Portal de Documentos - Metal Química Consultoria",
    page_icon="📄",
    layout="wide"
)

# Estilos CSS personalizados
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 50%, #06b6d4 100%) !important;
    padding: 0 !important;
}

.main {
    background-color: rgba(255,255,255,0.85) !important;
    backdrop-filter: blur(10px) !important;
    border-radius: 12px !important;
    padding: 2rem !important;
    margin: 2rem !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
}

h1, h2, h3 {
    color: #0f172a;
    font-weight: 700;
}

h1 { font-size: 2.8rem !important; }
h2 { font-size: 1.9rem !important; }
h3 { font-size: 1.3rem !important; }

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

.metal-card {
    background: rgba(255,255,255,0.9);
    border-left: 5px solid #0284c7;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
}

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

.footer {
    background: linear-gradient(135deg, rgba(14,165,233,0.1) 0%, rgba(59,130,246,0.1) 100%);
    border-top: 1px solid rgba(255,255,255,0.3);
    padding: 2rem 1rem;
    margin-top: 3rem;
    border-radius: 0 0 12px 12px;
    text-align: center;
    backdrop-filter: blur(8px);
}
.footer-content {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
    gap: 2rem;
}

.footer-logo {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 1rem;
    flex-wrap: wrap;
}

.footer-logo img {
    height: 40px;
    width: auto;
}

.footer-info {
    color: #475569;
    font-size: 0.95rem;
    margin: 0.5rem 0;
    font-weight: 400;
}

.footer-social {
    display: flex;
    justify-content: center;
    gap: 2rem;
    flex-wrap: wrap;
    margin-top: 1rem;
}

.footer-social a {
    color: #3b82f6;
    text-decoration: none;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# Função de envio de e-mail
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

# Lógica principal da aplicação
params = st.query_params

# Modo Admin
if not params:
    col1, col2 = st.columns([1.3, 3])
    with col1:
        st.image(
            "https://generated-images.adapta.one/metalquimicaconsultoria%40gmail.com/019c5261-cf87-7648-a8f1-b054e6597b25/2026-02-12T20-00-06-149Z_Modern_minimalist_vector_logo_for_METAL_QUIMICA_CO.png",
            width=300
        )
    with col2:
        st.title("⚗️ Portal de Gestão de Documentos")
        st.subheader("Metal Química Consultoria")

    st.markdown('<div class="metal-card"><h3>⚙️ Configuração do Link do Cliente</h3></div>', unsafe_allow_html=True)

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
        'Cópia da CNH do Representante Legal'
    ]
    
    st.markdown("### PASSO 1: Nome do Cliente")
    nome_cliente_config = st.text_input("Nome da Empresa", placeholder="Ex: Metalúrgica Alfa LTDA")

    st.markdown("### PASSO 2: Documentos Necessários")
    documentos_selecionados = st.multiselect(
        "Selecione os documentos pendentes:",
        options=sorted(MASTER_LISTA_DOCUMENTOS)
    )

    if st.button("🔗 GERAR LINK PARA O CLIENTE"):
        if not nome_cliente_config:
            st.error("Por favor, digite o nome do cliente.")
        elif not documentos_selecionados:
            st.error("Por favor, selecione pelo menos um documento.")
        else:
            docs_param = ",".join(urllib.parse.quote(doc) for doc in documentos_selecionados)
            cliente_param = urllib.parse.quote(nome_cliente_config)
            
            URL_BASE_DA_SUA_APP = "app-documentos-7l5ecrvyv7lhjl3ska9e3t.streamlit.app"
            url_gerada = f"https://{URL_BASE_DA_SUA_APP}?cliente={cliente_param}&docs={docs_param}"
            
            st.success("✅ Link gerado com sucesso!")
            st.code(url_gerada)
            if st.button("📋 Copiar Link"):
                st.info("Use CTRL+C para copiar o link acima.")

# Modo Cliente
else:
    nome_cliente = urllib.parse.unquote(params.get("cliente", "Cliente"))
    documentos_necessarios = urllib.parse.unquote(params.get("docs", "")).split(',') if params.get("docs") else []

    col1, col2 = st.columns([1, 6])
    with col1:
        st.image("https://generated-images.adapta.one/metalquimicaconsultoria%40gmail.com/019c5261-cf87-7648-a8f1-b054e6597b25/2026-02-12T20-00-06-149Z_Modern_minimalist_vector_logo_for_METAL_QUIMICA_CO.png", width=120)
    with col2:
        st.title('Portal de Envio de Documentos')
        st.subheader(f"Cliente: **{nome_cliente}**")

    st.markdown('<div class="metal-card"><h3>📤 Envie seus documentos</h3></div>', unsafe_allow_html=True)
    st.info("Por favor, anexe cada um dos documentos solicitados nos campos correspondentes abaixo. O envio só será realizado após você clicar no botão 'ENVIAR' no final da página.")

    if not documentos_necessarios:
        st.error("Link inválido ou nenhum documento foi solicitado.")
    else:
        arquivos_anexados = {}
        num_colunas = 3 if len(documentos_necessarios) > 5 else 2
        cols = st.columns(num_colunas)

        for i, documento in enumerate(documentos_necessarios):
            with cols[i % num_colunas]:
                st.markdown(f'<div class="documento">📄 <b>{documento}</b></div>', unsafe_allow_html=True)
                uploaded_file = st.file_uploader(
                    f'Selecione o arquivo {documento}',
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

# Rodapé
st.markdown('''
<div class="footer">
    <div class="footer-content">
        <div class="footer-logo">
            <img src="https://generated-images.adapta.one/metalquimicaconsultoria%40gmail.com/019c5261-cf87-7648-a8f1-b054e6597b25/2026-02-12T20-00-06-149Z_Modern_minimalist_vector_logo_for_METAL_QUIMICA_CO.png" 
                 alt="Logo Metal Química"
                 onerror="this.style.display='none';">
            <h3 style="color: #0f172a; margin: 0; font-size: 1.4rem; font-weight: 700;">
                Metal Química Consultoria
            </h3>
        </div>
        <div class="footer-info">
            Portal de Gestão de Documentos | Licenças Ambientais e Regularizações
        </div>
        <div class="footer-social">
            <a href="mailto:metalquimicaconsultoria@gmail.com" style="color: #3b82f6; text-decoration: none; font-weight: 500;">📧 Contato</a>
            <a href="tel:+551234567890" style="color: #3b82f6; text-decoration: none; font-weight: 500;">📞 Telefone</a>
            <span style="color: #64748b; font-size: 0.85rem;">© 2026 Metal Química. Todos os direitos reservados.</span>
        </div>
    </div>
</div>
''', unsafe_allow_html=True)
