import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- CONFIGURAÇÃO DA PÁGINA ------------------------------------------------
st.set_page_config(
    page_title="Análise do Brasileirão",
    page_icon="⚽",
    layout="wide"
)

# --- CONSTANTES GLOBAIS ----------------------------------------------------
COLOR_RESULTADO = {
    'Vitória': 'green',
    'Derrota': 'red',
    'Empate': 'yellow'
}

ESCUDOS_TIMES = {

    'Vitoria': 'https://logodetimes.com/times/vitoria/logo-vitoria-512.png',
    'Parana': 'https://logodetimes.com/times/parana/logo-parana-512.png',
    'Juventude': 'https://logodetimes.com/times/juventude/logo-juventude-512.png',
    'Cruzeiro': 'https://logodetimes.com/times/cruzeiro/logo-cruzeiro-512.png',
    'Chapecoense': 'https://logodetimes.com/times/chapecoense/logo-chapecoense-512.png',
    'CSA': 'https://logodetimes.com/times/csa/logo-csa-512.png',
    'Avai': 'https://logodetimes.com/times/avai/logo-avai-512.png',
    'America-MG': 'https://logodetimes.com/times/america-mineiro/logo-america-mineiro-512.png',
    'Athletico-PR': 'https://logodetimes.com/times/atletico-paranaense/logo-atletico-paranaense-512.png',
    'Atletico-GO': 'https://logodetimes.com/times/atletico-goianiense/logo-atletico-goianiense-com-estrela-512.png',
    'Atletico-MG': 'https://logodetimes.com/times/atletico-mineiro/logo-atletico-mineiro-512.png',
    'Bahia': 'https://logodetimes.com/times/bahia/logo-bahia-512.png',
    'Botafogo-RJ': 'https://logodetimes.com/times/botafogo/logo-botafogo-512.png',
    'Bragantino': 'https://logodetimes.com/times/red-bull-bragantino/logo-red-bull-bragantino-512.png',
    'Ceara': 'https://logodetimes.com/times/ceara/logo-ceara-512.png',
    'Corinthians': 'https://logodetimes.com/times/corinthians/logo-corinthians-512.png',
    'Coritiba': 'https://logodetimes.com/times/coritiba/logo-coritiba-512.png',
    'Cuiaba': 'https://logodetimes.com/times/cuiaba/logo-cuiaba-512.png',
    'Flamengo': 'https://logodetimes.com/times/flamengo/logo-flamengo-512.png',
    'Fluminense': 'https://logodetimes.com/times/fluminense/logo-fluminense-512.png',
    'Fortaleza': 'https://logodetimes.com/times/fortaleza/logo-fortaleza-512.png',
    'Goias': 'https://logodetimes.com/times/goias/logo-goias-esporte-clube-512.png',
    'Gremio': 'https://logodetimes.com/times/gremio/logo-gremio-512.png',
    'Internacional': 'https://logodetimes.com/times/internacional/logo-internacional-512.png',
    'Palmeiras': 'https://logodetimes.com/times/palmeiras/logo-palmeiras-512.png',
    'Santos': 'https://logodetimes.com/times/santos/logo-santos-512.png',
    'Sao Paulo': 'https://logodetimes.com/times/sao-paulo/logo-sao-paulo-512.png',
    'Sport': 'https://logodetimes.com/times/sport-recife/logo-sport-recife-512.png',
    'Vasco': 'https://logodetimes.com/times/vasco-da-gama/logo-vasco-da-gama-512.png',
    'Default': 'https://logospng.org/download/brasileirao-serie-a/logo-brasileirao-512.png'
}

# --- FUNÇÕES DE PROCESSAMENTO DE DADOS -------------------------------------
@st.cache_data
def carregar_dados():
    """
    Carrega e pré-processa os dados do Brasileirão a partir de um arquivo CSV.
    A função é armazenada em cache para melhorar o desempenho.
    """
    try:
        df = pd.read_csv('Brasileirao_Dataset/partidas_com_estatisticas_completas.csv')
        df.columns = df.columns.str.lower().str.strip()
        for col in ['vencedor', 'mandante', 'visitante']:
            df[col] = df[col].str.strip()
        
        conditions = [
            df['vencedor'] == df['mandante'],
            df['vencedor'] == '-'
        ]
        choices = ['Vitória', 'Empate']
        df['resultado_mandante'] = np.select(conditions, choices, default='Derrota')
        return df
    except FileNotFoundError:
        st.error("Arquivo 'partidas_com_estatisticas_completas.csv' não encontrado. Verifique o caminho do arquivo.")
        return None

def get_resultado_perspectiva(row, time_analisado):
    """
    Determina o resultado de uma partida (Vitória, Empate, Derrota) 
    da perspectiva de um time específico.
    """
    if row['mandante'] == time_analisado:
        return row['resultado_mandante']
    elif row['visitante'] == time_analisado:
        if row['resultado_mandante'] == 'Vitória': return 'Derrota'
        if row['resultado_mandante'] == 'Derrota': return 'Vitória'
        return 'Empate'
    return None

# --- CARREGAMENTO INICIAL DOS DADOS ---
df = carregar_dados()

if df is not None:
    # --- BARRA LATERAL DE FILTROS ---
    st.sidebar.image(ESCUDOS_TIMES['Default'], width=100)
    st.sidebar.title("Filtros")

    times = sorted(pd.concat([df['mandante'], df['visitante']]).unique())
    time_selecionado = st.sidebar.selectbox(
        "Selecione um Time para Análise Detalhada:",
        options=times,
        index=None,
        placeholder="Análise Geral de todos os times"
    )

    # --- LÓGICA DE EXIBIÇÃO DA PÁGINA ---
    if time_selecionado:
        # --- MODO DE VISÃO: TIME ESPECÍFICO ---
        df_filtrado = df[(df['mandante'] == time_selecionado) | (df['visitante'] == time_selecionado)].copy()
        df_filtrado['resultado'] = df_filtrado.apply(get_resultado_perspectiva, args=(time_selecionado,), axis=1)
        
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(ESCUDOS_TIMES.get(time_selecionado, ESCUDOS_TIMES['Default']), width=120)
        with col2:
            st.title(f"Análise de Performance: {time_selecionado}")
        
        resumo_time = df_filtrado['resultado'].value_counts()
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Partidas Jogadas", int(resumo_time.sum()))
        c2.metric("Vitórias", resumo_time.get('Vitória', 0))
        c3.metric("Empates", resumo_time.get('Empate', 0))
        c4.metric("Derrotas", resumo_time.get('Derrota', 0))

        st.markdown("---")
        st.header("🏟️ Análise como Mandante vs. Visitante")

        resultados_casa = df_filtrado[df_filtrado['mandante'] == time_selecionado]['resultado'].value_counts()
        resultados_fora = df_filtrado[df_filtrado['visitante'] == time_selecionado]['resultado'].value_counts()

        df_comparativo = pd.DataFrame({
            'Casa': resultados_casa,
            'Fora': resultados_fora
        }).fillna(0).astype(int).reindex(['Vitória', 'Empate', 'Derrota'])
        
        # ***** INÍCIO DA CORREÇÃO *****
        # O índice de df_comparativo é nomeado 'resultado'. Usamos .reset_index() para transformá-lo em coluna.
        df_melted = df_comparativo.reset_index()
        # A nova coluna se chama 'resultado', então usamos ela como id_vars.
        df_plot = df_melted.melt(id_vars='resultado', var_name='Condição', value_name='Número de Partidas')
        # Renomeamos a coluna 'resultado' para 'Resultado' para o rótulo do gráfico.
        df_plot.rename(columns={'resultado': 'Resultado'}, inplace=True)
        # ***** FIM DA CORREÇÃO *****

        fig_comparativo = px.bar(df_plot, x='Resultado', y='Número de Partidas', color='Condição',
                                 barmode='group', title=f'Desempenho de {time_selecionado}: Casa vs. Fora',
                                 labels={'Número de Partidas': 'Total de Partidas', 'Resultado': 'Tipo de Resultado'},
                                 color_discrete_map={'Casa': '#1f77b4', 'Fora': '#ff7f0e'})
        
        fig_comparativo.update_layout(legend_title_text='Local da Partida')
        st.plotly_chart(fig_comparativo, use_container_width=True)

    else:
        # --- MODO DE VISÃO: GERAL DO CAMPEONATO ---
        df_filtrado = df.copy()
        df_filtrado['resultado'] = df_filtrado['resultado_mandante']

        st.title("📊 Análise Geral do Brasileirão")
        
        total_jogos = len(df_filtrado)
        total_gols = df_filtrado['mandante_placar'].sum() + df_filtrado['visitante_placar'].sum()
        media_gols_partida = total_gols / total_jogos if total_jogos > 0 else 0
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Total de Partidas", f"{total_jogos:,}".replace(",", "."))
        c2.metric("Total de Gols", f"{int(total_gols):,}".replace(",", "."))
        c3.metric("Média de Gols por Partida", f"{media_gols_partida:.2f}")

        st.markdown("---")
        st.header("🏆 Top 5 Clubes com Mais Vitórias (Geral)")
        
        vitorias = df[df['vencedor'] != '-']['vencedor'].value_counts().head(5)
        cols = st.columns(5)
        for i, (time, total_vitorias) in enumerate(vitorias.items()):
            with cols[i]:
                st.image(ESCUDOS_TIMES.get(time, ESCUDOS_TIMES['Default']), width=80)
                st.metric(label=time, value=f"{total_vitorias} Vitórias")

    # --- SEÇÃO DE GRÁFICOS (COMUM A AMBAS AS VISÕES) ---
    st.markdown("---")
    st.header("🔍 Análises de Performance no Jogo")

    def plotar_pizza(df_plot, title):
        if not df_plot.empty:
            fig = px.pie(
                df_plot, names='resultado', values='percentual', title=title, hole=.3,
                color='resultado', color_discrete_map=COLOR_RESULTADO
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"Não há dados suficientes para o gráfico: {title}")

    def gerar_resumo_e_plotar(df_base, condicao_vitoria, titulo, coluna_plot, colunas_para_validar=[]):
        with coluna_plot:
            df_temp = df_base.copy()

            if colunas_para_validar:
                for col in colunas_para_validar:
                    if df_temp[col].dtype == 'object':
                        df_temp[col] = pd.to_numeric(df_temp[col].str.replace('%', ''), errors='coerce')
                df_temp.dropna(subset=colunas_para_validar, inplace=True)

            if not df_temp.empty:
                cond_mandante = condicao_vitoria(df_temp, 'mandante')
                cond_visitante = condicao_vitoria(df_temp, 'visitante')
                df_temp['time_analisado'] = np.select([cond_mandante, cond_visitante], [df_temp['mandante'], df_temp['visitante']], default=None)
                
                df_final = df_temp.dropna(subset=['time_analisado']).copy()

                if not df_final.empty:
                    df_final['resultado_final'] = df_final.apply(lambda row: get_resultado_perspectiva(row, row['time_analisado']), axis=1)
                    resumo = df_final['resultado_final'].value_counts(normalize=True).mul(100).reset_index()
                    resumo.columns = ['resultado', 'percentual']
                    plotar_pizza(resumo, titulo)
                else:
                    st.warning(f"Não há dados para a condição do gráfico: {titulo}")
            else:
                st.warning(f"Não há dados após a limpeza para o gráfico: {titulo}")

    cond_maior_posse = lambda df, time: df[f'{time}_posse_de_bola'] > df[f'{"visitante" if time == "mandante" else "mandante"}_posse_de_bola']
    cond_mais_chutes = lambda df, time: df[f'{time}_chutes'] > df[f'{"visitante" if time == "mandante" else "mandante"}_chutes']
    cond_mais_chutes_alvo = lambda df, time: df[f'{time}_chutes_no_alvo'] > df[f'{"visitante" if time == "mandante" else "mandante"}_chutes_no_alvo']
    cond_contra_ataque = lambda df, time: (df[f'{time}_posse_de_bola'] < df[f'{"visitante" if time == "mandante" else "mandante"}_posse_de_bola']) & (df[f'{time}_chutes'] > df[f'{"visitante" if time == "mandante" else "mandante"}_chutes'])

    col1, col2 = st.columns(2)

    gerar_resumo_e_plotar(df_filtrado, cond_maior_posse, "Resultado p/ Time com Mais Posse de Bola", col1, colunas_para_validar=['mandante_posse_de_bola', 'visitante_posse_de_bola'])
    gerar_resumo_e_plotar(df_filtrado, cond_mais_chutes_alvo, "Resultado p/ Time com Mais Chutes no Alvo", col1)
    gerar_resumo_e_plotar(df_filtrado, cond_mais_chutes, "Resultado p/ Time com Mais Chutes Totais", col2)
    gerar_resumo_e_plotar(df_filtrado, cond_contra_ataque, "Eficácia da Estratégia de Contra-Ataque", col2, colunas_para_validar=['mandante_posse_de_bola', 'visitante_posse_de_bola', 'mandante_chutes', 'visitante_chutes'])

    # --- TABELA DE DADOS DETALHADOS ---
    st.markdown("---")
    st.header("Dados Detalhados das Partidas")
    st.dataframe(df_filtrado)