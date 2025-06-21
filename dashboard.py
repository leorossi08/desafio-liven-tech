import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="Análise do Brasileirão",
    page_icon="⚽",
    layout="wide"
)

ESCUDOS_TIMES = {
    'Athletico-PR': 'https://logodetimes.com/times/atletico-paranaense/logo-atletico-paranaense-512.png',
    'Atletico-GO': 'https://logodetimes.com/times/atletico-goianiense/logo-atletico-goianiense-com-estrela-512.png',
    'Atletico-MG': 'https://logodetimes.com/times/atletico-mineiro/logo-atletico-mineiro-512.png',
    'Bahia': 'https://logodetimes.com/times/bahia/logo-bahia-512.png',
    'Botafogo': 'https://logodetimes.com/times/botafogo/logo-botafogo-512.png',
    'Bragantino': 'https://logodetimes.com/times/red-bull-bragantino/logo-red-bull-bragantino-512.png',
    'Ceara': 'https://logodetimes.com/times/ceara/logo-ceara-512.png',
    'Corinthians': 'https://logodetimes.com/times/corinthians/logo-corinthians-512.png',
    'Coritiba': 'https://logodetimes.com/times/coritiba/logo-coritiba-512.png',
    'Cuiaba': 'https://logodetimes.com/times/cuiaba/logo-cuiaba-512.png',
    'Flamengo': 'https://logodetimes.com/times/flamengo/logo-flamengo-512.png',
    'Fluminense': 'https://logodetimes.com/times/fluminense/logo-fluminense-512.png',
    'Fortaleza': 'https://logodetimes.com/times/fortaleza/logo-fortaleza-512.png',
    'Goias': 'https://logodetimes.com/times/goias/logo-goias-512.png',
    'Gremio': 'https://logodetimes.com/times/gremio/logo-gremio-512.png',
    'Internacional': 'https://logodetimes.com/times/internacional/logo-internacional-512.png',
    'Palmeiras': 'https://logodetimes.com/times/palmeiras/logo-palmeiras-512.png',
    'Santos': 'https://logodetimes.com/times/santos/logo-santos-512.png',
    'Sao Paulo': 'https://logodetimes.com/times/sao-paulo/logo-sao-paulo-512.png',
    'Sport': 'https://logodetimes.com/times/sport/logo-sport-512.png',
    'Vasco': 'https://logodetimes.com/times/vasco/logo-vasco-512.png',
    'Default': 'https://logospng.org/download/brasileirao-serie-a/logo-brasileirao-512.png'
}

@st.cache_data
def carregar_dados():
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
        st.error("Arquivo 'partidas_com_estatisticas_completas.csv' não encontrado.")
        return None

def get_resultado_perspectiva(row, time_analisado):
    if row['mandante'] == time_analisado:
        return row['resultado_mandante']
    elif row['visitante'] == time_analisado:
        if row['resultado_mandante'] == 'Vitória': return 'Derrota'
        if row['resultado_mandante'] == 'Derrota': return 'Vitória'
        return 'Empate'
    return None

df = carregar_dados()

if df is not None:
    st.sidebar.image(ESCUDOS_TIMES['Default'], width=100)
    st.sidebar.title("Filtros")

    times = sorted(pd.concat([df['mandante'], df['visitante']]).unique())
    time_selecionado = st.sidebar.selectbox(
        "Selecione um Time para Análise Detalhada:",
        options=times,
        index=None,
        placeholder="Análise Geral de todos os times"
    )

    if time_selecionado:
        df_filtrado = df[(df['mandante'] == time_selecionado) | (df['visitante'] == time_selecionado)].copy()
        df_filtrado['resultado'] = df_filtrado.apply(get_resultado_perspectiva, args=(time_selecionado,), axis=1)
        
        # --- LAYOUT PARA TIME SELECIONADO ---
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

    else:
        df_filtrado = df.copy()
        df_filtrado['resultado'] = df_filtrado['resultado_mandante']

        # --- LAYOUT PARA VISÃO GERAL ---
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

    # --- GRÁFICOS DE ANÁLISE (COMUM A AMBAS AS VISÕES) ---
    st.markdown("---")
    st.header("🔍 Análises de Performance no Jogo")

    df_analise = df_filtrado.copy()
    for col in ['mandante_posse_de_bola', 'visitante_posse_de_bola']:
        df_analise[col] = pd.to_numeric(df_analise[col].astype(str).str.replace('%', ''), errors='coerce')
    df_analise.dropna(subset=['mandante_posse_de_bola', 'visitante_posse_de_bola'], inplace=True)

    df_analise['maior_posse'] = np.where(df_analise['mandante_posse_de_bola'] > df_analise['visitante_posse_de_bola'], df_analise['mandante'], df_analise['visitante'])
    df_analise['mais_chutes'] = np.where(df_analise['mandante_chutes'] > df_analise['visitante_chutes'], df_analise['mandante'], df_analise['visitante'])
    df_analise['mais_chutes_alvo'] = np.where(df_analise['mandante_chutes_no_alvo'] > df_analise['visitante_chutes_no_alvo'], df_analise['mandante'], df_analise['visitante'])
    
    cond_ca_mandante = (df_analise['mandante_posse_de_bola'] < df_analise['visitante_posse_de_bola']) & (df_analise['mandante_chutes'] > df_analise['visitante_chutes'])
    cond_ca_visitante = (df_analise['visitante_posse_de_bola'] < df_analise['mandante_posse_de_bola']) & (df_analise['visitante_chutes'] > df_analise['mandante_chutes'])
    df_analise['time_contra_ataque'] = np.select([cond_ca_mandante, cond_ca_visitante], [df_analise['mandante'], df_analise['visitante']], default=None)

    def plotar_pizza(df_plot, title):
        if not df_plot.empty:
            fig = px.pie(df_plot, names='resultado', values='percentual', title=title, hole=.3)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"Não há dados suficientes para o gráfico: {title}")

    col1, col2 = st.columns(2)

    with col1:
        df_posse = df_analise[df_analise['maior_posse'].notna()].copy()
        df_posse['resultado_final'] = df_posse.apply(lambda row: get_resultado_perspectiva(row, row['maior_posse']), axis=1)
        resumo_posse = df_posse['resultado_final'].value_counts(normalize=True).mul(100).reset_index()
        resumo_posse.columns = ['resultado', 'percentual']
        plotar_pizza(resumo_posse, "Resultado p/ Time com Mais Posse de Bola")

        df_alvo = df_analise[df_analise['mais_chutes_alvo'].notna()].copy()
        df_alvo['resultado_final'] = df_alvo.apply(lambda row: get_resultado_perspectiva(row, row['mais_chutes_alvo']), axis=1)
        resumo_alvo = df_alvo['resultado_final'].value_counts(normalize=True).mul(100).reset_index()
        resumo_alvo.columns = ['resultado', 'percentual']
        plotar_pizza(resumo_alvo, "Resultado p/ Time com Mais Chutes no Alvo")

    with col2:
        df_chutes = df_analise[df_analise['mais_chutes'].notna()].copy()
        df_chutes['resultado_final'] = df_chutes.apply(lambda row: get_resultado_perspectiva(row, row['mais_chutes']), axis=1)
        resumo_chutes = df_chutes['resultado_final'].value_counts(normalize=True).mul(100).reset_index()
        resumo_chutes.columns = ['resultado', 'percentual']
        plotar_pizza(resumo_chutes, "Resultado p/ Time com Mais Chutes Totais")

        df_ca = df_analise[df_analise['time_contra_ataque'].notna()].copy()
        df_ca['resultado_final'] = df_ca.apply(lambda row: get_resultado_perspectiva(row, row['time_contra_ataque']), axis=1)
        resumo_ca = df_ca['resultado_final'].value_counts(normalize=True).mul(100).reset_index()
        resumo_ca.columns = ['resultado', 'percentual']
        plotar_pizza(resumo_ca, "Eficácia da Estratégia de Contra-Ataque")

    st.markdown("---")
    st.header("Dados Detalhados das Partidas")
    st.dataframe(df_filtrado)