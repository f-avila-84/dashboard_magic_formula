import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import datetime
import io

# --- Funções Auxiliares para Formatação e Leitura de Números BR ---
def format_thousands(number):
    """
    Formata um número inteiro com ponto como separador de milhares.
    Ex: 1234567 -> '1.234.567'
    """
    s = str(abs(int(number)))
    parts = []
    while s:
        parts.append(s[-3:])
        s = s[:-3]
    return ('' if number >= 0 else '-') + '.'.join(reversed(parts))

def format_br_float(value, decimals=2):
    """
    Formata um float em uma string com o padrão BR (ponto para milhares, vírgula para decimal).
    Ex: 12345.67 -> '12.345,67'
    """
    if pd.isna(value) or value is None:
        return ""
    
    sign = '-' if value < 0 else ''
    abs_value = abs(value)

    integer_part = int(abs_value)
    
    formatted_integer = format_thousands(integer_part)

    if decimals > 0:
        frac_str = f"{abs_value - integer_part:.{decimals}f}".split('.')[-1]
        if frac_str == f"{0:0{decimals}d}":
            frac_str = '0' * decimals
        
        return f"{sign}{formatted_integer},{frac_str}"
    else:
        return f"{sign}{formatted_integer}"

def format_br_int(value):
    """
    Formata um número (inteiro ou float) em uma string com o padrão BR (ponto para milhares).
    Ex: 20000000 -> '20.000.000'
    """
    if pd.isna(value) or value is None:
        return ""
    return format_thousands(int(value))

def parse_br_number(text_input):
    """
    Converte uma string formatada no padrão BR (ponto para milhares, vírgula para decimal)
    em um float. Retorna 0.0 se a entrada for vazia ou inválida.
    """
    if not isinstance(text_input, str):
        return float(text_input) if pd.notna(text_input) else 0.0
    if not text_input.strip():
        return 0.0
    cleaned_text = text_input.replace('.', '')
    cleaned_text = cleaned_text.replace(',', '.')
    try:
        return float(cleaned_text)
    except ValueError:
        print(f"Erro de conversão: '{text_input}' não pode ser convertido para número. Retornando 0.0.")
        return 0.0


# --- Mapeamento de todas as colunas possíveis e seus nomes de exibição ---
ALL_COLUMNS_MAP = {
    'ticker': 'Ticker',
    'empresa': 'Empresa',
    'setor': 'Setor',
    'subsetor': 'Subsetor',
    'roic_clean': 'ROIC (%)',
    'earnings_yield_clean': 'EY (%)',
    'rank_roic': 'Rank ROIC',
    'rank_ey': 'Rank EY',
    'magic_formula_rank': 'Rank MF',
    'cotacao': 'Cotação (R\$)',
    'vol_med_2m': 'Vol. Médio 2M (R\$)',
    'pl': 'P/L',
    'pvp': 'P/VP',
    'div_yield': 'Div. Yield (%)',
    'lpa': 'LPA (R\$)',
    '_30_dias': 'Ret. 30D (%)',
    '_12_meses': 'Ret. 12M (%)',
    'marg_liquida': 'Margem Líquida (%)',
    'valor_alocado': 'Valor Alocado (R\$)',
    'qtd_acoes': 'Qtd. Ações',
    'peso_carteira': '% na Carteira',
    'data_execucao': 'Data Execução',
}

# --- Regras de Formatação para os nomes de exibição das colunas ---
FORMATTING_RULES = {
    'ROIC (%)': lambda x: format_br_float(x, decimals=2),
    'EY (%)': lambda x: format_br_float(x, decimals=2),
    'Cotação (R\$)': lambda x: f'R\$ {format_br_float(x, decimals=2)}',
    'Vol. Médio 2M (R\$)': lambda x: f'R\$ {format_br_int(x)}',
    'P/L': lambda x: format_br_float(x, decimals=2),
    'P/VP': lambda x: format_br_float(x, decimals=2),
    'Div. Yield (%)': lambda x: f'{format_br_float(x, decimals=2)}%',
    'LPA (R\$)': lambda x: f'R\$ {format_br_float(x, decimals=2)}',
    'Ret. 30D (%)': lambda x: f'{format_br_float(x, decimals=2)}%',
    'Ret. 12M (%)': lambda x: f'{format_br_float(x, decimals=2)}%',
    'Margem Líquida (%)': lambda x: f'{format_br_float(x, decimals=2)}%',
    'Valor Alocado (R\$)': lambda x: f'R\$ {format_br_float(x, decimals=2)}',
    'Qtd. Ações': lambda x: format_br_int(x),
    '% na Carteira': lambda x: f'{format_br_float(x, decimals=2)}%',
    'Data Execução': lambda x: pd.to_datetime(x).strftime('%d/%m/%Y') if pd.notna(x) else 'N/A',
}

# --- Colunas selecionadas por padrão no multiselect (usando os nomes de exibição) ---
DEFAULT_SELECTED_COLUMNS_DISPLAY = [
    'Ticker', 
    'Empresa', 
    'Setor', 
    'Cotação (R\$)', 
    'Vol. Médio 2M (R\$)',
    'ROIC (%)', 
    'EY (%)', 
    'Rank MF', 
    'Valor Alocado (R\$)',
    'Qtd. Ações', 
    '% na Carteira',
]

# --- Função para carregar dados do arquivo CSV exportado ---
def get_magic_formula_data():
    try:
        df = pd.read_csv('fundamentus_data.csv') 
        
        if 'data_execucao' in df.columns:
            df['data_execucao'] = pd.to_datetime(df['data_execucao'], errors='coerce') 

        for col in ['_30_dias', '_12_meses']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        for alloc_col in ['valor_alocado', 'qtd_acoes', 'peso_carteira']:
            if alloc_col not in df.columns:
                df[alloc_col] = 0.0

        data_execucao_val = None
        if 'data_execucao' in df.columns and not df.empty and pd.notna(df['data_execucao'].iloc[0]):
            data_execucao_val = df['data_execucao'].iloc[0]

        return df, data_execucao_val
    except Exception as e:
        print(f"Erro ao carregar dados do arquivo: {e}")
        return pd.DataFrame(), None


# --- Função para calcular alocação para um dado DataFrame ---
def calculate_allocation_for_df(df_to_calc, total_invest, tipo_compra):
    df_to_calc['cotacao'] = pd.to_numeric(df_to_calc['cotacao'], errors='coerce')
    
    df_to_calc['qtd_acoes'] = 0.0
    df_to_calc['valor_alocado'] = 0.0
    df_to_calc['peso_carteira'] = 0.0

    df_selected_for_calc = df_to_calc[df_to_calc['_selected_for_allocation']].copy()

    if total_invest > 0 and not df_selected_for_calc.empty:
        num_empresas_selecionadas_para_alocacao = len(df_selected_for_calc)
        if num_empresas_selecionadas_para_alocacao > 0:
            investimento_por_empresa_ideal = total_invest / num_empresas_selecionadas_para_alocacao
            lot_size = 1 if tipo_compra == 'Fracionário (1+ ações)' else 100

            for index, row in df_selected_for_calc.iterrows():
                cotacao = row['cotacao']
                if pd.notna(cotacao) and cotacao > 0:
                    ideal_shares = investimento_por_empresa_ideal / cotacao
                    if tipo_compra == 'Fracionário (1+ ações)':
                        shares_to_buy = round(ideal_shares)
                    else:
                        shares_to_buy = round(ideal_shares / lot_size) * lot_size
                    if shares_to_buy < 0:
                        shares_to_buy = 0
                    df_to_calc.loc[index, 'qtd_acoes'] = shares_to_buy
                    df_to_calc.loc[index, 'valor_alocado'] = shares_to_buy * cotacao

            total_alocado_real = df_to_calc['valor_alocado'].sum()
            if total_alocado_real > 0:
                df_to_calc['peso_carteira'] = (df_to_calc['valor_alocado'] / total_alocado_real) * 100
    return df_to_calc

# --- Inicialização do App Dash ---
# Adicionando o link para o Font Awesome para ícones
app = dash.Dash(__name__, external_stylesheets=[
    '/assets/style.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css' 
])
server = app.server
app.title = "Fórmula Mágica de Joel Greenblatt"


# --- Layout do Dashboard ---
app.layout = html.Div([
    dcc.Store(id='raw-data-store'),
    dcc.Store(id='filtered-data-store'),
    dcc.Store(id='calculated-data-store'),
    dcc.Store(id='sidebar-status-store', data=True),

    html.Div(id='fixed-header-container', children=[
        html.Div(className='golden-line'),
        html.H1("A FÓRMULA MÁGICA", className='header-title-text', style={'color': '#EFC448'}),
        html.H1("de JOEL GREENBLATT", className='header-subtitle-text', style={'color': 'white'}),
        html.Div(className='golden-line'),
    ]),

    html.Button(
        id='toggle-sidebar-button',
        children='<<<',
        className='toggle-sidebar-button-class'
    ),

    html.Div(className='main-content-wrapper', children=[
        html.Div(id='sidebar', children=[
            html.H3("Configurações do Ranking"),
            html.Div([
                html.P("Número de empresas a exibir e pré-selecionar:", className='sidebar-label'),
                dcc.Slider(
                    id='num-empresas-slider',
                    min=1, max=50, step=1, value=20,
                    marks={i: str(i) for i in range(0, 51, 10)},
                    className='dash-slider-custom'
                )
            ]),
            html.Div([
                html.P("Volume Médio Negociado (últimos 2 meses) Mínimo (R\$):", className='sidebar-label'),
                dcc.Input(
                    id='min-volume-input',
                    type='text',
                    value="20.000.000", # Definindo valor inicial como string formatada
                    className='dash-input-custom',
                    placeholder="Ex: 20.000.000"
                )
            ]),
            html.Hr(),
            html.H3("Configurações de Investimento"),
            html.Div([
                html.P("Valor a Investir (R\$):", className='sidebar-label'),
                dcc.Input(
                    id='total-investimento-input',
                    type='text',
                    value="10.000", # Definindo valor inicial como string formatada e sem decimais
                    className='dash-input-custom',
                    placeholder="Ex: 10.000"
                )
            ]),
            html.Div([
                html.P("Tipo de Lote de Compra:", className='sidebar-label'),
                dcc.RadioItems(
                    id='tipo-compra-radio',
                    options=[
                        {'label': 'Fracionário (1+ ações)', 'value': 'Fracionário (1+ ações)'},
                        {'label': 'Padrão (100+ ações)', 'value': 'Padrão (100+ ações)'}
                    ],
                    value='Fracionário (1+ ações)',
                    className='dash-radioitems-custom'
                )
            ]),
            html.Hr(),
            html.H3("Colunas a Exibir"),
            html.Div([
                html.P("Selecione as colunas para exibir (a ordem de seleção define a ordem na tabela):", className='sidebar-label'),
                dcc.Dropdown(
                    id='selected-columns-dropdown',
                    options=[{'label': col, 'value': col} for col in ALL_COLUMNS_MAP.values() if col not in ['Data Execução', 'Valor Alocado (R\$)', 'Qtd. Ações', '% na Carteira']],
                    value=DEFAULT_SELECTED_COLUMNS_DISPLAY,
                    multi=True,
                    className='dash-dropdown-custom'
                )
            ]),
        ]),

        html.Div(id='main-content', children=[
            html.H2("Dashboard de Ranking e Alocação de Investimento"),
            html.P("Marque as caixas para incluir as empresas no cálculo de alocação de investimento. Os valores de 'Qtd. Ações', 'Valor Alocado' e 'Peso na Carteira' serão atualizados dinamicamente."),

            dash_table.DataTable(
                id='magic-formula-table',
                row_selectable='multi',
                style_as_list_view=True,
                style_table={'overflowX': 'auto', 'border': '1px solid #1E3D82', 'borderRadius': '8px', 'boxShadow': '0 4px 8px rgba(0,0,0,0.1)'},
                style_header={
                    'backgroundColor': '#EEEEEE',
                    'fontWeight': 'bold',
                    'color': '#1E3D82',
                    'borderBottom': '2px solid #1E3D82',
                    'fontFamily': 'Montserrat',
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#F8F8F8'
                    },
                    {
                        'if': {'row_index': 'even'},
                        'backgroundColor': '#EEEEEE'
                    },
                ],
                style_cell={
                    'textAlign': 'center',
                    'fontFamily': 'Open Sans',
                    'fontSize': 14,
                    'padding': '8px 12px',
                    'color': 'var(--text-color-dark)',
                },
                style_cell_conditional=[
                    {
                        'if': {'column_id': 'ticker'},
                        'textAlign': 'left'
                    },
                    {
                        'if': {'column_id': 'empresa'},
                        'textAlign': 'left'
                    },
                    {
                        'if': {'column_id': 'setor'},
                        'textAlign': 'left'
                    },
                    {
                        'if': {'column_id': 'subsetor'},
                        'textAlign': 'left'
                    },
                    {
                        'if': {'column_id': 'Nº'},
                        'textAlign': 'center'
                    }
                ],
            ),

            html.Div(id='info-box', className='info-box-container', children=[
                html.P(id='last-updated-date-text'),
                html.P(id='source-text')
            ]),

            html.Hr(),
            html.H3("Resumo da Alocação de Investimento"),
            html.Div(id='allocation-summary'),

            html.Hr(),
            html.H3("Entendendo as Métricas:"),
            html.Ul([
                html.Li([
                    html.B("ROIC (Return on Invested Capital):"),
                    " Mede a eficiência com que uma empresa usa o capital investido para gerar lucro. Quanto maior, melhor."
                ]),
                html.Li([
                    html.B("EY:"),
                    ' É o inverso do P/L (Preço/Lucro), ou seja, Lucro por Ação / Preço por Ação. Indica o retorno percentual que o lucro da empresa representa em relação ao preço da ação. Quanto maior, mais "barata" a empresa em relação aos seus lucros.'
                ]),
                html.Li([
                    html.B("Rank MF:"),
                    " Ranking da Fórmula Mágica. É a soma dos rankings de ROIC e Earnings Yield. Empresas com menor soma são consideradas as melhores pela Fórmula Mágica."
                ]),
                html.Li([
                    html.B("Cotação (R\$):"),
                    " Preço da ação no fechamento do dia anterior."
                ]),
                html.Li([
                    html.B("Vol. Médio 2M (R\$):"),
                    " Volume médio negociado da ação nos últimos 2 meses. Importante para avaliar a liquidez."
                ]),
                html.Li([
                    html.B("P/L (Preço/Lucro):"),
                    ' Relação entre o preço da ação e o lucro por ação. Indica quantos anos de lucro são necessários para "pagar" o preço da ação.'
                ]),
                html.Li([
                    html.B("P/VP (Preço/Valor Patrimonial):"),
                    " Relação entre o preço da ação e o valor patrimonial por ação. Indica o quanto o mercado está pagando pelo patrimônio líquido da empresa."
                ]),
                html.Li([
                    html.B("Div. Yield (%):"),
                    " Dividendo por ação dividido pelo preço da ação. Indica o retorno em dividendos em relação ao preço da ação."
                ]),
                html.Li([
                    html.B("LPA (Lucro Por Ação):"),
                    " Lucro líquido da empresa dividido pelo número de ações."
                ]),
                html.Li([
                    html.B("Ret. 30D (%):"),
                    " Variação percentual do preço da ação nos últimos 30 dias."
                ]),
                html.Li([
                    html.B("Ret. 12M (%):"),
                    " Variação percentual do preço da ação nos últimos 12 meses."
                ]),
                html.Li([
                    html.B("Margem Líquida (%):"),
                    " Lucro líquido dividido pela receita líquida. Indica a porcentagem de cada real de receita que se transforma em lucro."
                ]),
                html.Li([
                    html.B("Valor Alocado (R\$):"),
                    " O valor real alocado para a empresa, considerando a cotação e a quantidade de ações compradas."
                ]),
                html.Li([
                    html.B("Qtd. Ações:"),
                    " A quantidade de ações a serem compradas da empresa, arredondada para a unidade ou lote mais próxima."
                ]),
                html.Li([
                    html.B("% na Carteira:"),
                    " O peso percentual real da empresa na carteira, com base no valor alocado."
                ]),
            ]), # Fim do html.Ul

            # --- NOVA SEÇÃO DE CONTATO ---
            html.Hr(), # Separador para a seção de contato
            html.Div(className='contact-section', children=[
                html.H3("Criado por: Felipe Avila", style={'margin': '0'}), # Ajuste aqui para remover margens padrão
                html.Div(className='contact-links', children=[
                    html.A(
                        html.Span([
                            html.I(className='fab fa-linkedin'), # Ícone do LinkedIn
                            html.Span(" LinkedIn")
                        ]),
                        href="https://www.linkedin.com/in/avilafelipe/", 
                        ,
                        className='contact-link'
                    ),
                    html.A(
                        html.Span([
                            html.I(className='fab fa-github'), # Ícone do GitHub
                            html.Span(" GitHub")
                        ]),
                        href="https://github.com/f-avila-84", 
                        ,
                        className='contact-link'
                    )
                ])
            ]),
            # --- FIM DA NOVA SEÇÃO DE CONTATO ---

        ]) # Fim de main-content
    ]) # Fim de main-content-wrapper
]) # Fim do app.layout

# --- Callbacks ---

@app.callback(
    Output('raw-data-store', 'data'),
    Output('last-updated-date-text', 'children'),
    Output('source-text', 'children'),
    Input('raw-data-store', 'data')
)
def load_raw_data(dummy_input):
    df_raw, data_execucao = get_magic_formula_data()
    
    date_text = ""
    source_elem = html.Span()
    
    if data_execucao:
        formatted_date = data_execucao.strftime('%d/%m/%Y')
        date_text = f"Dados atualizados em: {formatted_date}"
        source_elem = html.Span([
            "Fonte: ",
            html.A("Fundamentus", href="https://www.fundamentus.com.br/", rel="noopener noreferrer")
        ])
    else:
        date_text = "Data de atualização dos dados não disponível."
        source_elem = html.Span()

    df_raw['_selected_for_allocation'] = True

    return df_raw.to_json(date_format='iso', orient='split'), date_text, source_elem

@app.callback(
    [Output('filtered-data-store', 'data'),
     Output('magic-formula-table', 'data'),
     Output('magic-formula-table', 'columns'),
     Output('magic-formula-table', 'selected_rows')],
    [Input('num-empresas-slider', 'value'),
     Input('min-volume-input', 'value'), 
     Input('selected-columns-dropdown', 'value'),
     Input('raw-data-store', 'data')] 
)
def update_filtered_data_and_table(num_empresas, min_volume_str, selected_cols_display, raw_data_json):
    if not raw_data_json:
        return pd.DataFrame().to_json(date_format='iso', orient='split'), [], [], []

    df_raw = pd.read_json(io.StringIO(raw_data_json), orient='split') 

    if df_raw.empty:
        return pd.DataFrame().to_json(date_format='iso', orient='split'), [], [], []

    min_volume = parse_br_number(min_volume_str) 

    df_filtered = df_raw[df_raw['vol_med_2m'] >= min_volume].copy()
    df_filtered = df_filtered.sort_values(by='magic_formula_rank')

    df_filtered = df_filtered.head(num_empresas)
    df_filtered.reset_index(drop=True, inplace=True)

    df_filtered['_selected_for_allocation'] = True 

    dash_table_columns = [
        {"name": "Nº", "id": "Nº"},
    ]
    
    reverse_map = {v: k for k, v in ALL_COLUMNS_MAP.items()}

    for col_display_name in selected_cols_display:
        original_col_name = reverse_map.get(col_display_name, col_display_name)
        if original_col_name in df_filtered.columns and original_col_name not in ['Nº', 'valor_alocado', 'qtd_acoes', 'peso_carteira', 'data_execucao']:
            dash_table_columns.append({"name": col_display_name, "id": original_col_name})
            
    fixed_cols_original_names = ['valor_alocado', 'qtd_acoes', 'peso_carteira'] 
    for original_name in fixed_cols_original_names:
        display_name = ALL_COLUMNS_MAP[original_name]
        if original_name in df_filtered.columns and original_name not in [col['id'] for col in dash_table_columns]:
            dash_table_columns.append({"name": display_name, "id": original_name})


    df_for_display = df_filtered.copy()
    df_for_display.insert(0, 'Nº', range(1, 1 + len(df_for_display)))

    for col_def in dash_table_columns:
        col_id = col_def['id']
        col_name_for_formatting = col_def['name']
        if col_name_for_formatting in FORMATTING_RULES and col_id in df_for_display.columns:
            df_for_display[col_id] = df_for_display[col_id].apply(FORMATTING_RULES[col_name_for_formatting])

    table_data = df_for_display.to_dict('records')

    initial_selected_rows_indices = list(range(len(df_filtered))) 

    return df_filtered.to_json(date_format='iso', orient='split'), table_data, dash_table_columns, initial_selected_rows_indices

@app.callback(
    [Output('calculated-data-store', 'data'),
     Output('allocation-summary', 'children')],
    [Input('magic-formula-table', 'selected_rows'),
     Input('total-investimento-input', 'value'), 
     Input('tipo-compra-radio', 'value')],
    [State('filtered-data-store', 'data')]
)
def update_allocation_and_summary(selected_rows_indices, total_investimento_str, tipo_compra, filtered_data_json):
    if not filtered_data_json:
        return pd.DataFrame().to_json(date_format='iso', orient='split'), html.P("Não há dados para calcular alocação.")

    df_filtered = pd.read_json(io.StringIO(filtered_data_json), orient='split') 

    if df_filtered.empty:
        return pd.DataFrame().to_json(date_format='iso', orient='split'), html.P("Nenhuma empresa atende aos critérios de filtro.")

    total_investimento = parse_br_number(total_investimento_str) 

    df_filtered['_selected_for_allocation'] = False
    if selected_rows_indices is not None:
        df_filtered.loc[selected_rows_indices, '_selected_for_allocation'] = True

    df_with_allocation = calculate_allocation_for_df(df_filtered.copy(), total_investimento, tipo_compra)

    df_selected_final = df_with_allocation[df_with_allocation['_selected_for_allocation']].copy()
    total_alocado_real_final = df_selected_final['valor_alocado'].sum()
    num_empresas_selecionadas_final = len(df_selected_final)

    summary_elements = []
    summary_elements.append(html.P(f"Valor a Investir: R\$ {format_br_float(total_investimento, decimals=2)}"))
    summary_elements.append(html.P(f"Número de Empresas Selecionadas para Alocação: {num_empresas_selecionadas_final}"))

    if num_empresas_selecionadas_final > 0:
        investimento_por_empresa_ideal_final = total_investimento / num_empresas_selecionadas_final 
        summary_elements.append(html.P(f"Valor Alocado por Empresa (Ideal): R\$ {format_br_float(investimento_por_empresa_ideal_final, decimals=2)}"))
    else:
        summary_elements.append(html.P(f"Valor Alocado por Empresa (Ideal): R\$ {format_br_float(0.0, decimals=2)}"))

    summary_elements.append(html.P(f"Valor Total Alocado (Real): R\$ {format_br_float(total_alocado_real_final, decimals=2)}"))
    summary_elements.append(html.P(f"Diferença (Não Alocado): R\$ {format_br_float(total_investimento - total_alocado_real_final, decimals=2)}"))

    return df_with_allocation.to_json(date_format='iso', orient='split'), html.Div(summary_elements)

@app.callback(
    Output('magic-formula-table', 'data', allow_duplicate=True),
    [Input('calculated-data-store', 'data')],
    [State('selected-columns-dropdown', 'value')],
    prevent_initial_call=True
)
def update_table_with_calculated_data(calculated_data_json, selected_cols_display):
    if not calculated_data_json:
        return []

    df_calculated = pd.read_json(io.StringIO(calculated_data_json), orient='split') 

    dash_table_columns_ids = ["Nº"] # Lista de IDs de colunas (strings)
    reverse_map = {v: k for k, v in ALL_COLUMNS_MAP.items()}

    for col_display_name in selected_cols_display:
        original_col_name = reverse_map.get(col_display_name, col_display_name)
        if original_col_name in df_calculated.columns and original_col_name not in ['Nº', 'valor_alocado', 'qtd_acoes', 'peso_carteira', 'data_execucao']:
            dash_table_columns_ids.append(original_col_name) # Adiciona apenas o ID da coluna (string)
            
    fixed_cols_original_names = ['valor_alocado', 'qtd_acoes', 'peso_carteira'] 
    for original_name in fixed_cols_original_names:
        display_name = ALL_COLUMNS_MAP[original_name]
        # Verifica se a coluna está no DataFrame e se ainda não foi adicionada (como um ID de string)
        if original_name in df_calculated.columns and original_name not in dash_table_columns_ids:
            dash_table_columns_ids.append(original_name) # Adiciona apenas o ID da coluna (string)


    df_for_display = df_calculated.copy()
    df_for_display.insert(0, 'Nº', range(1, 1 + len(df_for_display)))

    for col_id in dash_table_columns_ids: # col_id é uma string aqui, como esperado
        col_name_for_formatting = ALL_COLUMNS_MAP.get(col_id, col_id)
        if col_name_for_formatting in FORMATTING_RULES and col_id in df_for_display.columns:
            df_for_display[col_id] = df_for_display[col_id].apply(FORMATTING_RULES[col_name_for_formatting])


    return df_for_display[dash_table_columns_ids].to_dict('records')

@app.callback(
    Output('sidebar', 'style'),
    Output('toggle-sidebar-button', 'children'),
    Output('toggle-sidebar-button', 'style'),
    Output('sidebar-status-store', 'data'),
    Input('toggle-sidebar-button', 'n_clicks'),
    State('sidebar-status-store', 'data'),
    prevent_initial_call=True
)
def toggle_sidebar(n_clicks, is_sidebar_open):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate

    sidebar_width_open = '280px'
    sidebar_padding_open = '20px'
    
    sidebar_style_closed = {
        'width': '0px',
        'padding': '0px',
        'overflow': 'hidden',
        'borderRight': 'none'
    }
    sidebar_style_open = {
        'width': sidebar_width_open,
        'padding': sidebar_padding_open,
        'overflowY': 'auto',
        'backgroundColor': 'var(--primary-color)'
    }

    button_left_open = '10px' 
    button_left_closed = '10px' 
    button_top = '80px'

    if is_sidebar_open:
        sidebar_style = sidebar_style_closed
        button_text = '>>>'
        button_style = {'left': button_left_closed, 'top': button_top, 'position': 'fixed', 'z-index': 10000}
        new_state = False
    else:
        sidebar_style = sidebar_style_open
        button_text = '<<<'
        button_style = {'left': button_left_open, 'top': button_top, 'position': 'fixed', 'z-index': 10000}
        new_state = True
    
    return sidebar_style, button_text, button_style, new_state


# --- CLIENTSIDE CALLBACKS ---
# Estes callbacks rodam no navegador (JavaScript) para formatação em tempo real
# e gerenciamento do cursor.

# Callback para formatar o campo 'min-volume-input' (inteiro)
app.clientside_callback(
    """
    function(inputValue) {
        // Chama a função JS 'formatInputLive' que está em assets/clientside.js
        // Passa o ID do input para que a função saiba qual input está sendo formatado
        // e se é inteiro ou float.
        return window.dash_clientside.clientside_functions.formatInputLive(
            'min-volume-input', inputValue
        );
    }
    """,
    Output('min-volume-input', 'value'),
    Input('min-volume-input', 'value'),
    prevent_initial_call=False # Necessário para formatar o valor inicial ao carregar
)

# Callback para formatar o campo 'total-investimento-input' (float)
app.clientside_callback(
    """
    function(inputValue) {
        // Chama a função JS 'formatInputLive' que está em assets/clientside.js
        return window.dash_clientside.clientside_functions.formatInputLive(
            'total-investimento-input', inputValue
        );
    }
    """,
    Output('total-investimento-input', 'value'),
    Input('total-investimento-input', 'value'),
    prevent_initial_call=False # Necessário para formatar o valor inicial ao carregar
)
# --- FIM CLIENTSIDE CALLBACKS ---


if __name__ == '__main__':
    app.run_server(debug=True)