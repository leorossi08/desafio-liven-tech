# Desafio de Dados – Liven: **Análise do Brasileirão** ⚽

## Visão Geral do Projeto 📝

Este projeto aplica **Data Science** ao Campeonato Brasileiro de Futebol para descobrir quais fatores mais influenciam o resultado das partidas.As principais perguntas respondidas foram:

* **Mandante tem vantagem?** → _Sim._ O time da casa vence **52 %** das partidas.
* **Posse de bola decide jogo?** → _Não necessariamente._ O time com mais posse perde ou empata em **63 %** dos casos.
* **Volume e qualidade de finalizações?** → _Sim._ Chutar **no alvo** é o indicador isolado mais forte de vitória (_59,2%_).
* **Contra‑ataque funciona?** → _Muito._ Quando um time aposta em contra‑ataques (menos posse + mais chutes) ele vence **54,2 %** dos jogos e perde apenas **23,9 %.**

A análise foi organizada em **três grandes atividades**:

1. **Limpeza & Preparação** – garantir consistência entre 4 bases distintas.
2. **Construção da Tabela Mestra** – unir todas as estatísticas de cada partida em uma única linha.
3. **Investigação dos Fatores de Sucesso** – responder às hipóteses com *Pandas* e *SQL (DuckDB)*.

Por fim, foi criado um **dashboard interativo** em Streamlit para visualização executiva.

---

## Estrutura do Repositório 🚀

```text
.
├── Brasileirao_Dataset/
│   ├── campeonato-brasileiro-full.csv
│   ├── campeonato-brasileiro-estatisticas-full.csv
│   ├── campeonato-brasileiro-cartoes.csv
│   ├── campeonato-brasileiro-gols.csv
│   └── partidas_com_estatisticas_completas.csv   # gerado na etapa 2
├── Liven_Desafio_Dados.ipynb   # notebook completo
├── dashboard.py                # aplicação Streamlit
└── README.md                   # (você está aqui!)
```

---

## Atividade 1 – Limpeza & Preparação ⚙️

* **Carga inicial** das 4 tabelas com _pandas_.
* **Filtro de qualidade**: removidas partidas sem estatísticas.
* **Interseção de IDs**: mantidas apenas partidas presentes em **todas** as tabelas.
* **Tratamento de nulos**
  * `posse_de_bola`, `precisao_passes` → “Sem Info”
  * `tipo_de_gol` ausente → “Gol Normal”
  * colunas irrelevantes removidas (`formacao_*`, `num_camisa`).

---

## Atividade 2 – Construção da Tabela Mestra 🔀

* Estatísticas separadas em **mandante** × **visitante** com prefixos claros (`mandante_chutes`, `visitante_posse_de_bola`).
* Junção final pelo `partida_id`, resultando em `partidas_com_estatisticas_completas.csv`.

---

## Atividade 3 – Análise de Fatores de Sucesso 📊

| Pergunta                                 | Métrica‑chave            | Resultado                                          |
| ---------------------------------------- | -------------------------- | -------------------------------------------------- |
| **Vantagem de jogar em casa?**     | Mandante vence?            | 52 % Vitórias · 27 % Derrotas · 21 % Empates |
| **Posse de bola decide?**          | Quem teve + posse         | 36,7 % Vitórias · 42,6 % Derrotas              |
| **Chutes influenciam?**            | + chutes (total)          | 46% Vitórias                                      |
|                                          | + chutes**no alvo** | 59,2 % Vitórias                                  |
| **Estratégia de contra‑ataque?** | menos posse e mais chutes  | 54,2 % Vitórias · 23,9 % Derrotas              |

> **Insight:** objetividade e transições rápidas superam mero controle de bola.

---

## Dashboard Interativo (Streamlit) 🖥️

O arquivo `dashboard.py` gera uma aplicação web onde você pode:

* Selecionar **qualquer time** e ver métricas específicas (vitórias, empates, derrotas, casa × fora).
* Analisar efeitos de **posse**, **chutes**, **chutes no alvo** e **contra‑ataque** em gráficos de pizza _color‑coded_:
  * 🟩 **Vitória** – verde
  * 🟥 **Derrota** – vermelho
  * 🟨 **Empate** – amarelo

```bash
streamlit run dashboard.py
```

1. O navegador abrirá automaticamente em `http://localhost:8501`.

> ⚠️ **Pré‑requisitos**: Python 3.8 ou superior e os arquivos CSV dentro de `Brasileirao_Dataset/`.

Analise Geral do Campeonado pelo Dashboard com ranking:

![image](https://github.com/user-attachments/assets/27a2f594-804f-46f7-801e-fc30ccb5b285)


Performance Geral do Campeonato Brasileiro:

![image](https://github.com/user-attachments/assets/ea63a814-336b-46c2-b89b-947f28c014fd)

Filtre pelo seu time:

![image](https://github.com/user-attachments/assets/735e5802-3bb7-4cd8-bce8-6682dcc53381)

Seu time é um bom mandante?

![image](https://github.com/user-attachments/assets/f8229b71-5e60-4353-9b41-7b7de46236e2)

Performance específica para cada time do nosso amado Brasileirão:

![image](https://github.com/user-attachments/assets/278fa42c-577e-48b7-a1e7-ac1a37010edb)


---

## Próximos Passos 🔮

* Incluir métricas de **xG (Expected Goals)**.
* Analisar gols contra (há algum padrão entre eles?)
* Treinar modelo de classificação para prever resultado em tempo real.

*"⁠Eu perdoarei os jogadores se eles não puderem fazer algo direito, mas não perdoarei se eles não tentarem para valer." (Pep Guardiola) ⚽📈*
