import streamlit as st
import google.generativeai as genai
from streamlit_option_menu import option_menu

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA (UI/UX)
# ==========================================
st.set_page_config(
    page_title="EngFis UFV - All in One",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. MENU LATERAL (SIDEBAR COM LOGO E EMOJIS)
# ==========================================
with st.sidebar:
    import os
    from PIL import Image
    
    try:
        # 1. Mapeia o caminho absoluto do arquivo
        caminho_imagem = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
        
        # 2. Força a leitura do arquivo binário para a memória RAM (Bypass no bug do Windows)
        logo_img = Image.open(caminho_imagem)
        
        # 3. Entrega a imagem já processada para o Streamlit
        st.image(logo_img, use_container_width=True)
        
    except Exception as e:
        st.markdown("<h2 style='text-align: center;'>⚛️ EngFis UFV</h2>", unsafe_allow_html=True)
        # st.error(f"Debug: {e}") # Descomente esta linha se a imagem ainda não carregar para ler o erro exato
        
    st.markdown("---")
    
    # Menu vertical restaurando a temática de emojis nativos
    from streamlit_option_menu import option_menu
    modulo_selecionado = option_menu(
        menu_title=None, 
        options=[
            "🏠 Home & Dashboard", 
            "📊 Tratamento de Dados", 
            "🧮 Orientador Simbólico", 
            "⚡ Bancada de Eletrônica",
            "🌌 Simulador Multifísica"
        ],
        icons=['', '', '', '', ''], # Lista vazia para desativar o Bootstrap
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "nav-link": {
                "font-size": "15px", 
                "text-align": "left", 
                "margin": "0px", 
                "padding": "12px",
                "border-radius": "5px"
            },
            "nav-link-selected": {
                "background-color": "rgba(0, 255, 204, 0.15)", # Fundo translúcido (funciona no claro e escuro)
                "border-left": "4px solid #00FFCC"
           },
        }
    )
    
    st.markdown("---")
    st.caption("© 2026 - Shin | Physical Engineering")

# ==========================================
# 3. CONFIGURAÇÃO DA INTELIGÊNCIA ARTIFICIAL (ADV-Gem)
# ==========================================
MINHA_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=MINHA_API_KEY)

instrucoes_sistema = """
Você é o ADV-Gem (Assistente Didático Virtual), um modelo de inteligência artificial 
atuando como tutor avançado para um estudante de Engenharia Física da UFV. 
Você domina Cálculo, Física (Teórica e Experimental), Eletrônica e Biorrobótica.
Seu objetivo é guiar o aluno usando rigor matemático e científico.
Sempre que o usuário pedir para estudar um conceito, ative o "Loop de Feynman" em 6 fases.
"""

try:
    modelo_ia = genai.GenerativeModel(
        model_name="gemini-3.5-flash-lite", 
        system_instruction=instrucoes_sistema
    )
except Exception as e:
    st.error(f"Erro ao carregar o modelo de IA: {e}")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
if "chat_session" not in st.session_state:
    try:
        st.session_state.chat_session = modelo_ia.start_chat(history=[])
    except Exception as e:
        st.error("Aguardando configuração da Chave API...")

# ==========================================
# 4. RENDERIZAÇÃO DAS PÁGINAS (ROTEAMENTO)
# ==========================================

if modulo_selecionado == "🏠 Home & Dashboard":
    st.title("⚛️ QG de Engenharia Física - UFV")
    st.markdown("Bem-vindo ao seu ambiente integrado de simulação, metrologia e inteligência artificial.")
    
    st.markdown("### 📊 Status do Sistema")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Módulos Ativos", "4/4", "100% Operacional")
    col2.metric("Motor IA", "Gemini 3.5 Flash-Lite", "Online")
    col3.metric("Inspeção 3D", "WebGL", "Otimizado")
    col4.metric("Cálculo Simbólico", "SymPy", "Pronto")
    
    st.markdown("---")
    
    chat_col, info_col = st.columns([2, 1])
    
    with chat_col:
        st.subheader("🤖 ADV-Gem (Tutor IA)")
        st.caption("Ative o 'Loop de Feynman' para qualquer dúvida teórica ou resolução de listas da UFV.")
        
        chat_container = st.container(height=450)
        
        with chat_container:
            for mensagem in st.session_state.chat_history:
                with st.chat_message(mensagem["role"]):
                    st.markdown(mensagem["content"])
                    
        if prompt := st.chat_input("Digite sua dúvida de Cálculo, Física ou Eletrônica..."):
            with chat_container:
                with st.chat_message("user"):
                    st.markdown(prompt)
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                
                with st.chat_message("assistant"):
                    with st.spinner("Processando (ADV-Gem)..."):
                        resposta = st.session_state.chat_session.send_message(prompt)
                        st.markdown(resposta.text)
                st.session_state.chat_history.append({"role": "assistant", "content": resposta.text})
                st.rerun() 
                
    with info_col:
        st.subheader("📌 Acesso Rápido")
        st.info("**Física Experimental:**\nUse a Estação 2 para propagação de incertezas pelo método da derivada parcial.")
        st.warning("**Cálculo Avançado:**\nNa sintaxe do SymPy, use `**` para potências (ex: `x**2`) e `*` para multiplicação.")
        st.success("**Eletrônica (Falstad):**\nPressione 'R' para adicionar um resistor e 'C' para capacitor na bancada 2D.")
        st.error("**Quântica:**\nA renderização da Nuvem de Probabilidade 3D exige alto processamento do navegador.")
    
elif modulo_selecionado == "📊 Tratamento de Dados":
    import pandas as pd
    import numpy as np
    import plotly.express as px
    import plotly.graph_objects as go
    from scipy.optimize import curve_fit
    import sympy as sp
    
    st.title("📊 Laboratório de Física Experimental")
    st.markdown("Tratamento automatizado de dados, estatística de incertezas e ajuste de curvas (Curve Fitting).")
    
    aba_selecionada = st.radio(
        "Escolha a Estação de Trabalho:", 
        ["Ajuste de Curvas (Curve Fitting)", "Estatística e Propagação de Incertezas"],
        horizontal=True
    )
    st.markdown("---")
    
    if aba_selecionada == "Ajuste de Curvas (Curve Fitting)":
        st.subheader("Ajuste Teórico de Dados Experimentais")
        
        col1, col2 = st.columns(2)
        with col1: nome_x = st.text_input("Nome da Grandeza X (Independente):", value="Tempo (s)")
        with col2: nome_y = st.text_input("Nome da Grandeza Y (Dependente):", value="Posição (m)")
        
        tipo_entrada = st.radio("Como deseja inserir os dados?", ("Digitar Tabela Manual", "Upload de Arquivo CSV"))
        df = pd.DataFrame()
        
        if tipo_entrada == "Digitar Tabela Manual":
            st.info("Insira os dados coletados. As colunas foram renomeadas automaticamente conforme as grandezas acima.")
            df_editado = st.data_editor(
                pd.DataFrame({nome_x: [1.0, 2.0, 3.0, 4.0, 5.0], nome_y: [2.1, 4.1, 5.9, 8.2, 10.1]}),
                num_rows="dynamic",
                use_container_width=True
            )
            df = df_editado
            
        elif tipo_entrada == "Upload de Arquivo CSV":
            arquivo = st.file_uploader("Envie seu arquivo de dados (.csv)", type=["csv"])
            if arquivo is not None:
                df = pd.read_csv(arquivo)
                st.dataframe(df, use_container_width=True)
                
        if not df.empty and len(df.columns) >= 2:
            st.markdown("---")
            st.subheader("Análise e Ajuste Físico")
            
            c_x, c_y = st.columns(2)
            with c_x: eixo_x = st.selectbox("Eixo X para Plotar:", df.columns, index=0)
            with c_y: eixo_y = st.selectbox("Eixo Y para Plotar:", df.columns, index=1 if len(df.columns)>1 else 0)
                
            tipo_ajuste = st.selectbox("Modelo Teórico para Ajuste de Curva:", ["Linear (y = ax + b)", "Quadrático (y = ax² + bx + c)", "Exponencial (y = a*e^(bx))"])
            
            if st.button("Processar Dados e Plotar", type="primary"):
                x_data = df[eixo_x].values
                y_data = df[eixo_y].values
                
                def modelo_linear(x, a, b): return a * x + b
                def modelo_quadratico(x, a, b, c): return a * x**2 + b * x + c
                def modelo_exponencial(x, a, b): return a * np.exp(b * x)
                
                try:
                    x_fit = np.linspace(min(x_data), max(x_data), 100)
                    if tipo_ajuste == "Linear (y = ax + b)":
                        popt, pcov = curve_fit(modelo_linear, x_data, y_data)
                        y_fit = modelo_linear(x_fit, *popt)
                        equacao_texto = f"y = {popt[0]:.4f}x + {popt[1]:.4f}"
                        
                    elif tipo_ajuste == "Quadrático (y = ax² + bx + c)":
                        popt, pcov = curve_fit(modelo_quadratico, x_data, y_data)
                        y_fit = modelo_quadratico(x_fit, *popt)
                        equacao_texto = f"y = {popt[0]:.4f}x² + {popt[1]:.4f}x + {popt[2]:.4f}"
                        
                    elif tipo_ajuste == "Exponencial (y = a*e^(bx))":
                        popt, pcov = curve_fit(modelo_exponencial, x_data, y_data)
                        y_fit = modelo_exponencial(x_fit, *popt)
                        equacao_texto = f"y = {popt[0]:.4f} * e^({popt[1]:.4f}x)"

                    st.success(f"**Ajuste Concluído! Equação Descoberta:** {equacao_texto}")
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='markers', name='Dados Experimentais', marker=dict(size=10, color='red')))
                    fig.add_trace(go.Scatter(x=x_fit, y=y_fit, mode='lines', name='Ajuste Teórico', line=dict(color='cyan', width=3)))
                    
                    fig.update_layout(title="Dispersão e Curve Fitting", xaxis_title=eixo_x, yaxis_title=eixo_y, template="plotly_dark")
                    st.plotly_chart(fig, use_container_width=True)
                    
                except Exception as e:
                    st.error(f"Erro no ajuste de curva. O modelo pode não convergir para esses dados. Detalhe: {e}")

    elif aba_selecionada == "Estatística e Propagação de Incertezas":
        st.subheader("A. Estatística de Medidas Repetidas")
        st.markdown("Calcule média, desvio padrão amostral e desvio médio a partir de leituras sucessivas de um mesmo instrumento.")
        
        df_leituras = st.data_editor(
            pd.DataFrame({"Leitura_Bruta": [10.2, 10.4, 10.1, 10.3, 10.2]}), 
            num_rows="dynamic",
            use_container_width=True
        )
        
        if st.button("Calcular Estatística Básica"):
            vals = df_leituras["Leitura_Bruta"].dropna().astype(float).values
            if len(vals) > 0:
                media = np.mean(vals)
                desvio_padrao = np.std(vals, ddof=1) if len(vals) > 1 else 0.0
                desvio_medio = np.mean(np.abs(vals - media))
                
                st.success("Estatísticas Calculadas com Sucesso!")
                col1, col2, col3 = st.columns(3)
                col1.metric("Média (x̄)", f"{media:.4f}")
                col2.metric("Desvio Padrão (σ)", f"{desvio_padrao:.4f}")
                col3.metric("Desvio Médio", f"{desvio_medio:.4f}")
            else:
                st.warning("Insira valores numéricos na tabela.")
                
        st.markdown("---")
        
        st.subheader("B. Propagação de Incertezas (Método da Derivada)")
        st.info("💡 Insira a Equação Física final (ex: para calcular a Área A = x*y, digite `x*y`). O SymPy calculará as derivadas parciais automaticamente.")
        
        func_str = st.text_input("Fórmula Física F(x, y, ...):", value="x**2 * y")
        
        st.markdown("**Defina as variáveis usadas na fórmula, seus valores médios e a incerteza de cada uma:**")
        df_vars = st.data_editor(
            pd.DataFrame({
                "Variavel": ["x", "y"],
                "Valor_Medio": [2.0, 3.0],
                "Incerteza_Absoluta": [0.1, 0.2]
            }), 
            num_rows="dynamic",
            use_container_width=True
        )
        
        if st.button("Calcular Incerteza Propagada", type="primary"):
            try:
                f_sym = sp.sympify(func_str)
                variaveis_nomes = df_vars["Variavel"].dropna().astype(str).values
                valores_medios = df_vars["Valor_Medio"].dropna().astype(float).values
                incertezas = df_vars["Incerteza_Absoluta"].dropna().astype(float).values
                
                subs_dict = {sp.Symbol(var): val for var, val in zip(variaveis_nomes, valores_medios)}
                valor_f = f_sym.subs(subs_dict).evalf()
                
                variancia_total = 0
                st.write("**Demonstração das Derivadas Parciais Calculadas:**")
                
                for var_name, incerteza in zip(variaveis_nomes, incertezas):
                    sym_var = sp.Symbol(var_name)
                    derivada = sp.diff(f_sym, sym_var)
                    derivada_num = derivada.subs(subs_dict).evalf()
                    termo = (derivada_num * incerteza)**2
                    variancia_total += termo
                    
                    st.latex(f"\\frac{{\\partial F}}{{\\partial {var_name}}} = {sp.latex(derivada)} \\quad \\rightarrow \\quad {derivada_num:.4f}")
                    
                incerteza_final = sp.sqrt(variancia_total).evalf()
                
                st.success("Cálculo de Propagação Concluído!")
                st.markdown("### Resultado Final para o Relatório:")
                st.latex(f"F = {valor_f:.4f} \\pm {incerteza_final:.4f}")
                
            except Exception as e:
                st.error(f"Erro no cálculo simbólico. Verifique se as letras na fórmula conferem exatamente com as letras na tabela. Detalhe: {e}")

elif modulo_selecionado == "🧮 Orientador Simbólico":
    import sympy as sp
    
    st.title("🧮 Orientador Simbólico Avançado")
    st.markdown("Motor de Cálculo Analítico Multi-disciplinar. Suporta Cálculo 1, 2, 3 e Equações Diferenciais Ordinárias (EDO).")
    
    st.markdown("""
        <style>
        .katex { font-size: 1.5em !important; }
        </style>
        """, unsafe_allow_html=True)
    
    x, y, z, t = sp.symbols('x y z t')
    y_func = sp.Function('y')(x) 
    
    st.subheader("Operação Analítica")
    operacao = st.selectbox(
        "Selecione a operação desejada:",
        [
            "Integral Indefinida", 
            "Integral Definida", 
            "Derivada Simples", 
            "Derivada Parcial (Multivariável)",
            "Derivada Implícita",
            "Equação Diferencial Ordinária (EDO)",
            "Limite",
            "Série de Taylor"
        ]
    )
    
    st.subheader("Defina a Função / Equação")
    
    if operacao == "Derivada Implícita":
        st.info("💡 Para F(x,y) = 0, digite a expressão. Ex: para x² + y² = 25, digite `x**2 + y**2 - 25`")
        funcao_str = st.text_input("Expressão F(x,y):", value="x**2 + y**2 - 25")
        
    elif operacao == "Equação Diferencial Ordinária (EDO)":
        st.info("💡 Use `y(x)` para a função e `y(x).diff(x)` para a derivada. Ex: `y(x).diff(x, 2) + 4*y(x)` para y'' + 4y = 0")
        funcao_str = st.text_input("Equação Diferencial (igual a 0):", value="y(x).diff(x) - 2*x*y(x)")
        
    elif operacao == "Derivada Parcial (Multivariável)":
        st.info("💡 Você pode usar as variáveis x, y, z e t combinadas. Ex: `x**2 * sin(y) * z`")
        funcao_str = st.text_input("Função Multivariável f(x,y,z,t):", value="x**2 * y**3 * sin(z)")
        
    else:
        funcao_str = st.text_input("Digite a função f(x):", value="x**2 * sin(x)")

    if operacao == "Integral Definida":
        col1, col2 = st.columns(2)
        with col1: lim_inf_str = st.text_input("Limite Inferior (a):", value="0")
        with col2: lim_sup_str = st.text_input("Limite Superior (b):", value="pi")
        
    elif operacao == "Derivada Parcial (Multivariável)":
        var_alvo = st.selectbox("Derivar em relação a:", ["x", "y", "z", "t"])
        
    elif operacao == "Limite":
        ponto_limite = st.text_input("Ponto de aproximação (ex: 0, oo para infinito):", value="0")

    if st.button("Calcular Solução Analítica", type="primary"):
        try:
            f = sp.sympify(funcao_str)
            
            st.markdown("---")
            st.write("**Expressão Interpretada:**")
            
            if operacao in ["Equação Diferencial Ordinária (EDO)", "Derivada Implícita"]:
                st.latex(f"{sp.latex(f)} = 0")
            else:
                st.latex(f"f = {sp.latex(f)}")
                
            st.write("**Solução Analítica Exata:**")
            
            if operacao == "Integral Indefinida":
                resultado = sp.integrate(f, x)
                st.latex(f"\\int \\left( {sp.latex(f)} \\right) dx = {sp.latex(resultado)} + C")
                
            elif operacao == "Integral Definida":
                a = sp.sympify(lim_inf_str)
                b = sp.sympify(lim_sup_str)
                resultado = sp.integrate(f, (x, a, b))
                st.latex(f"\\int_{{{sp.latex(a)}}}^{{{sp.latex(b)}}} \\left( {sp.latex(f)} \\right) dx = {sp.latex(resultado)}")
                
            elif operacao == "Derivada Simples":
                resultado = sp.diff(f, x)
                st.latex(f"\\frac{{d}}{{dx}} \\left[ {sp.latex(f)} \\right] = {sp.latex(resultado)}")
                
            elif operacao == "Derivada Parcial (Multivariável)":
                var_sym = sp.Symbol(var_alvo)
                resultado = sp.diff(f, var_sym)
                st.latex(f"\\frac{{\\partial}}{{\\partial {var_alvo}}} \\left[ {sp.latex(f)} \\right] = {sp.latex(resultado)}")
                
            elif operacao == "Derivada Implícita":
                resultado = sp.idiff(f, y, x)
                st.latex(f"\\frac{{dy}}{{dx}} = {sp.latex(resultado)}")
                
            elif operacao == "Equação Diferencial Ordinária (EDO)":
                resultado = sp.dsolve(sp.Eq(f, 0), y_func)
                st.latex(sp.latex(resultado))
                
            elif operacao == "Limite":
                ponto = sp.sympify(ponto_limite)
                resultado = sp.limit(f, x, ponto)
                st.latex(f"\\lim_{{x \\to {sp.latex(ponto)}}} \\left( {sp.latex(f)} \\right) = {sp.latex(resultado)}")
                
            elif operacao == "Série de Taylor":
                resultado = sp.series(f, x, 0, 5)
                st.latex(f"\\approx {sp.latex(resultado)}")

        except Exception as e:
            st.error(f"Erro matemático ou de sintaxe: {e}. Verifique as instruções da caixa de informação (💡).")

elif modulo_selecionado == "⚡ Bancada de Eletrônica":
    import numpy as np
    import plotly.graph_objects as go
    import streamlit.components.v1 as components
    
    st.title("⚡ Bancada de Eletrônica e Instrumentação")
    st.markdown("Prototipagem de circuitos, análise transitória e inspeção de hardware 3D.")
    
    aba_eletronica = st.radio(
        "Selecione o Ambiente de Trabalho:", 
        [
            "Simulador Visual de Circuitos (Falstad)", 
            "Análise Transitória de Malhas (RC/RLC)",
            "Catálogo de Componentes 3D (CAD)"
        ],
        horizontal=True
    )
    st.markdown("---")
    
    if aba_eletronica == "Simulador Visual de Circuitos (Falstad)":
        st.subheader("Bancada de Prototipagem Interativa")
        st.info("💡 Desenhe o seu circuito, adicione osciloscópios e veja a corrente fluindo em tempo real.")
        components.iframe(src="https://www.falstad.com/circuit/circuitjs.html", width=None, height=700, scrolling=False)
        
    elif aba_eletronica == "Análise Transitória de Malhas (RC/RLC)":
        st.subheader("Simulação Matemática de Sinais no Tempo")
        st.markdown("Calcule e visualize a resposta de circuitos aos degraus de tensão baseando-se em EDOs lineares.")
        
        tipo_circuito = st.selectbox("Escolha o Sistema:", ["Circuito RC", "Circuito RLC Série"])
        col1, col2, col3, col4 = st.columns(4)
        
        if tipo_circuito == "Circuito RC":
            with col1: v_fonte = st.number_input("Tensão V (V):", value=5.0)
            with col2: r_val = st.number_input("Resistência R (Ω):", value=1000.0)
            with col3: c_val = st.number_input("Capacitor C (F):", value=0.001, format="%.6f")
            
            if st.button("Gerar Gráfico de Carga", type="primary"):
                tau = r_val * c_val
                t = np.linspace(0, 5 * tau, 500)
                v_c = v_fonte * (1 - np.exp(-t / tau))
                i_c = (v_fonte / r_val) * np.exp(-t / tau)
                
                from plotly.subplots import make_subplots
                fig = make_subplots(specs=[[{"secondary_y": True}]])
                fig.add_trace(go.Scatter(x=t, y=v_c, name="Tensão (V)", line=dict(color='cyan', width=3)), secondary_y=False)
                fig.add_trace(go.Scatter(x=t, y=i_c, name="Corrente (A)", line=dict(color='orange', width=2, dash='dot')), secondary_y=True)
                fig.update_layout(title=f"Carga RC (τ = {tau:.4f} s)", template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
                
        elif tipo_circuito == "Circuito RLC Série":
            with col1: v_fonte = st.number_input("Tensão Carga V0 (V):", value=10.0)
            with col2: r_val = st.number_input("Resistência R (Ω):", value=10.0)
            with col3: l_val = st.number_input("Indutância L (H):", value=0.1)
            with col4: c_val = st.number_input("Capacitor C (F):", value=0.001, format="%.6f")
            
            if st.button("Gerar Gráfico de Descarga", type="primary"):
                alpha = r_val / (2 * l_val)
                omega_0 = 1 / np.sqrt(l_val * c_val)
                t = np.linspace(0, 0.5, 1000)
                
                if alpha > omega_0:
                    s1 = -alpha + np.sqrt(alpha**2 - omega_0**2)
                    s2 = -alpha - np.sqrt(alpha**2 - omega_0**2)
                    A1 = v_fonte / (1 - s1/s2)
                    v_c = A1 * np.exp(s1 * t) + (v_fonte - A1) * np.exp(s2 * t)
                elif alpha == omega_0:
                    v_c = (v_fonte + alpha * v_fonte * t) * np.exp(-alpha * t)
                else:
                    omega_d = np.sqrt(omega_0**2 - alpha**2)
                    v_c = np.exp(-alpha * t) * (v_fonte * np.cos(omega_d * t) + (alpha / omega_d) * v_fonte * np.sin(omega_d * t))
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=t, y=v_c, name="Tensão Vc(t)", line=dict(color='#00ffcc', width=3)))
                fig.update_layout(title="Descarga RLC", template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

    elif aba_eletronica == "Catálogo de Componentes 3D (CAD)":
        st.subheader("Inspecione o Encapsulamento Real (WebGL)")
        st.markdown("Rotacione e aproxime os componentes para estudar sua estrutura física antes de ir ao laboratório.")
        
        peca_selecionada = st.selectbox("Selecione o Componente:", ["Placa Arduino Uno", "Microcontrolador (Chip DIP)", "Resistor PTH"])
        
        modelos_3d = {
            "Placa Arduino Uno": "link_ou_arquivo_arduino.gltf", 
            "Microcontrolador (Chip DIP)": "link_ou_arquivo_microcontrolador.gltf", 
            "Resistor PTH": "link_ou_arquivo_resistor.gltf" 
            "Meu Novo Capacitor": "capacitor_ufv.glb"
        }
        
        url_modelo = modelos_3d[peca_selecionada]
        
        codigo_html_3d = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.1.1/model-viewer.min.js"></script>
            <style>
                model-viewer {{
                    width: 100%;
                    height: 500px;
                    background-color: #1E1E1E;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.5);
                }}
            </style>
        </head>
        <body>
            <model-viewer 
                src="{url_modelo}" 
                alt="Modelo 3D de {peca_selecionada}" 
                auto-rotate 
                camera-controls
                shadow-intensity="1">
            </model-viewer>
        </body>
        </html>
        """
        
        st.info("💡 Arraste com o mouse para girar a peça. Use o scroll para dar zoom.")
        components.html(codigo_html_3d, height=520)

elif modulo_selecionado == "🌌 Simulador Multifísica":
    import numpy as np
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    
    st.title("🌌 Física Quântica e Nanotecnologia")
    st.markdown("Soluções da Equação de Schrödinger para funções de onda e níveis de energia em poços de potencial.")
    
    aba_quantica = st.radio(
        "Selecione o Experimento Quântico:", 
        ["Poço de Potencial 1D (Função de Onda)", "Caixa 3D (Nuvem de Probabilidade)"],
        horizontal=True
    )
    st.markdown("---")
    
    if aba_quantica == "Poço de Potencial 1D (Função de Onda)":
        st.subheader("Confinamento Unidimensional")
        # O prefixo 'r' força o Python a ler o LaTeX perfeitamente, sem quebrar os símbolos de módulo '|'
        st.info(r"💡 Visualize a função de onda $\psi(x)$ e a densidade de probabilidade $|\psi(x)|^2$ de um elétron confinado.")
        
        col1, col2 = st.columns(2)
        with col1: L = st.number_input("Largura do Poço L (nm):", value=1.0, min_value=0.1)
        with col2: n = st.number_input("Número Quântico Principal (n):", value=1, min_value=1, step=1)
        
        if st.button("Simular Estado Quântico", type="primary"):
            x = np.linspace(0, L, 500)
            
            psi = np.sqrt(2/L) * np.sin(n * np.pi * x / L)
            probabilidade = psi**2
            
            fig = make_subplots(rows=1, cols=2, subplot_titles=("Função de Onda Ψ(x)", "Densidade de Probabilidade |Ψ(x)|²"))
            
            fig.add_trace(go.Scatter(x=x, y=psi, mode='lines', name='Ψ(x)', line=dict(color='cyan', width=2)), row=1, col=1)
            fig.add_trace(go.Scatter(
                x=x, 
                y=probabilidade, 
                mode='lines', 
                name='|Ψ(x)|²', 
                line=dict(color='magenta', width=2), 
                fill='tozeroy' 
            ), row=1, col=2)
            
            fig.update_layout(template="plotly_dark", title_text=f"Nível de Energia: Estado n={n}")
            fig.update_xaxes(title_text="Posição x (nm)")
            st.plotly_chart(fig, use_container_width=True)
            
    elif aba_quantica == "Caixa 3D (Nuvem de Probabilidade)":
        st.subheader("Confinamento Tridimensional e Degeneração")
        st.markdown("Modelagem do estado estacionário em três dimensões com os números quânticos $n_X, n_Y, n_Z$.")
        
        col1, col2, col3 = st.columns(3)
        with col1: nx = st.number_input("n_X:", value=1, min_value=1, step=1)
        with col2: ny = st.number_input("n_Y:", value=1, min_value=1, step=1)
        with col3: nz = st.number_input("n_Z:", value=1, min_value=1, step=1)
        
        if st.button("Gerar Nuvem de Probabilidade 3D", type="primary"):
            with st.spinner("Calculando densidade matricial..."):
                grid_size = 30
                x = np.linspace(0, 1, grid_size)
                y = np.linspace(0, 1, grid_size)
                z = np.linspace(0, 1, grid_size)
                X, Y, Z = np.meshgrid(x, y, z)
                
                P = (np.sin(nx * np.pi * X) * np.sin(ny * np.pi * Y) * np.sin(nz * np.pi * Z))**2
                
                limite_probabilidade = 0.15
                mascara = P > limite_probabilidade
                
                fig = go.Figure(data=[go.Scatter3d(
                    x=X[mascara], y=Y[mascara], z=Z[mascara],
                    mode='markers',
                    marker=dict(
                        size=5,
                        color=P[mascara],
                        colorscale='Plasma',
                        opacity=0.6,
                        colorbar=dict(title="Probabilidade")
                    ),
                    name="Nuvem Eletrônica"
                )])
                
                fig.update_layout(
                    title=f"Densidade Volumétrica de Probabilidade ({nx}, {ny}, {nz})",
                    scene=dict(xaxis_title='X (L)', yaxis_title='Y (L)', zaxis_title='Z (L)'),
                    template="plotly_dark",
                    height=700
                )
                st.plotly_chart(fig, use_container_width=True)
