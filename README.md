# ⚛️ EngFis UFV - All in One

**O ecossistema digital definitivo para estudantes de Engenharia Física.**

Esta plataforma foi desenvolvida como um laboratório virtual e assistente matemático contínuo para suportar a carga analítica, experimental e teórica da graduação em Engenharia Física. O sistema integra inteligência artificial, cálculo simbólico e visualização de dados em um único Dashboard em nuvem.

## 🚀 Módulos Disponíveis

A plataforma está dividida em 5 estações de trabalho independentes:

*   **🏠 Home & Dashboard (ADV-Gem):** O QG principal. Integra telemetria do sistema e o **Tutor IA (ADV-Gem)**, configurado para aplicar o "Método de Feynman". Resolva dúvidas teóricas ou listas de exercícios com correção baseada no padrão de exigência da UFV.
*   **📊 Tratamento de Dados (Física Experimental):** Um laboratório de metrologia automatizado. Insira tabelas de dados para realizar *Curve Fitting* (Regressões lineares, quadráticas e exponenciais) via `SciPy`, ou utilize o motor analítico para calcular a Propagação de Incertezas pelo método das Derivadas Parciais.
*   **🧮 Orientador Simbólico (Cálculo Avançado):** Motor matemático alimentado por `SymPy`. Resolve analiticamente integrais (definidas e indefinidas), derivadas parciais, derivadas implícitas, limites e Equações Diferenciais Ordinárias (EDOs), devolvendo o passo a passo formatado em LaTeX.
*   **⚡ Bancada de Eletrônica:** Estação híbrida de hardware. Permite a simulação de circuitos via plataforma *Falstad*, análise matemática transitória de malhas RC/RLC com geração de gráficos no domínio do tempo, e inspeção WebGL tridimensional (CAD) de componentes eletrônicos.
*   **🌌 Simulador Multifísica (Quântica):** Ferramenta de visualização avançada para fenômenos de fronteira. Plota funções de onda solucionadas pela Equação de Schrödinger para poços de potencial 1D e gera mapas matriciais de nuvens de probabilidade eletrônica em 3D.

## 🛠️ Stack Tecnológico

*   **Linguagem Base:** Python 3.x
*   **Interface e Web Framework:** Streamlit (`streamlit-option-menu`)
*   **Matemática e Estatística:** `SymPy`, `SciPy`, `NumPy`, `Pandas`
*   **Visualização Gráfica:** `Plotly` (Gráficos 2D e 3D interativos)
*   **Inteligência Artificial:** Google Gemini API (Flash-Lite)
*   **Renderização 3D:** Google `<model-viewer>` (WebGL)

## 📖 Como Utilizar (Online)

A plataforma é hospedada em nuvem (*Software as a Service*) e não requer nenhuma instalação por parte do usuário final.
1. Acesse o link oficial do deploy: `[(https://s-all-in-one.streamlit.app)]`
2. Navegue pelo menu lateral para acessar os laboratórios.
3. Para cálculos no **Orientador Simbólico**, utilize a sintaxe nativa do Python (ex: `x**2` para potências e `*` para multiplicações).

## 💻 Como Rodar Localmente (Para Desenvolvedores)

Caso deseje clonar este repositório e rodar a plataforma em sua própria máquina:

1. Clone o repositório:
   ```bash
   git clone [https://github.com/Shin-ZeroSeven/EngFis-All-in-One.git](https://github.com/Shin-ZeroSeven/EngFis-All-in-One.git)
   cd EngFis-All-in-One

2. Instale as dependências num ambiente virtual:
  Bash
      pip install -r requirements.txt

3. Configure a sua Chave de API da Google:

  Crie uma pasta chamada .streamlit na raiz do projeto.
  Dentro dela, crie um arquivo secrets.toml e insira a sua chave: GEMINI_API_KEY = "SUA_CHAVE_AQUI"

4. Inicie o servidor local:

  Bash
    streamlit run app.py

    
© Desenvolvido por Shin | Physical Engineering - 2026
