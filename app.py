import streamlit as st
import pandas as pd
import numpy as np
import funcs as fc
import plotly.express as px



#st.set_page_config(page_title='Meus gastos', page_icon=':moneybag:', layout='wide', initial_sidebar_state='auto')

df_mika = fc.carregar_tratar_dados('gastosmika')
df_mae = fc.carregar_tratar_dados('gastosmae')

meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

st.title('Meus gastos')

st.divider()

with st.container():
    
    fatura_atual, fatura_anterior, fatura_proxima, fatura_mae = st.columns(4)

    with fatura_atual:
        st.metric('Fatural atual', fc.valor_formatado(fc.fatura_atual(df_mika)))

    with fatura_anterior:
        st.metric('Fatura anterior', fc.valor_formatado(fc.fatura_anterior(df_mika)))

    with fatura_proxima:
        st.metric('Próxima fatura', fc.valor_formatado(fc.fatura_proxima(df_mika)))

    with fatura_mae:
        st.metric('Fatural atual mãe', fc.valor_formatado(fc.fatura_atual(df_mae)))

st.divider()

with st.popover("Adicionar gastos"):

    with st.form(key='form_adicionar_dados', border= False):

        data = st.text_input('Digite a data')
        descricao = st.text_input('Digite a descrição')
        valor = st.text_input('Digite o valor')
        classificacao = st.text_input('Digite a classificação')
        st.selectbox('Ano', [2020, 2021, 2022])

        submit_button = st.form_submit_button('Adicionar')

        if submit_button:
            dados = [data, descricao, valor, classificacao]

            # Verifica se todos os campos estão preenchidos
            if all(dados):
                try:
                    fc.adicionar_dados()
                    st.success('Dados adicionados com sucesso!')
                except ValueError:
                    st.error('Erro: O valor deve ser numérico.')
            else:
                st.error('Preencha todos os campos!')

st.divider()

with st.container():

    st.subheader('Tabelas')

    tabela1, tabela2, tabela3 = st.columns([0.5,0.2,0.3])
    
    with tabela1:
        st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
            <h6 style="text-align: center;">Tabela de gastos</h6>
        </div>
        """, unsafe_allow_html=True
    )
        st.dataframe(df_mika, use_container_width=True, hide_index=True)
        
    with tabela2:
        st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
            <h6 style="text-align: center;">Gastos por mês</h6>
        </div>
        """, unsafe_allow_html=True
    )
        st.dataframe(fc.soma_valores_por_mes(df_mika), use_container_width=True)

    with tabela3:
        st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
            <h6 style="text-align: center;">Gastos por classificação</h6>
        </div>
        """, unsafe_allow_html=True
        )
        fig2 = px.bar(x=fc.soma_valores_por_classificacao(df_mika).values, y=fc.soma_valores_por_classificacao(df_mika).index.astype(str), orientation='h')
        st.plotly_chart(fig2, use_container_width=True)

with st.container():

    st.header('Filtros')

    st.selectbox('Ano', [2020, 2021, 2022], key='ano', on_change=lambda: st.session_state.update())

    st.selectbox('Mês', meses, key='mes', on_change=lambda: st.session_state.update())

    st.write(f"Você selecionou: {st.session_state.get('mes', 'Mês não selecionado')} de {st.session_state.get('ano', 'Ano não selecionado')}")
