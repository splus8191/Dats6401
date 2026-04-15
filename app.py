import dash as html
import dash as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc
import math

app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server

url = "https://raw.githubusercontent.com/rjafari979/Information-Visualization-Data-Analytics-Dataset-/main/CONVENIENT_global_confirmed_cases.csv"
df = pd.read_csv(url)

df = df.drop(index=0).reset_index(drop=True).copy()
df = df.rename(columns={'Country/Region': 'Date'})
df['China_sum'] = df.filter(like='China').apply(pd.to_numeric, errors='coerce').sum(axis=1)
df['United Kingdom_sun'] = df.filter(like='United Kingdom').apply(pd.to_numeric, errors='coerce').sum(axis=1)
countries = ['US', 'Brazil', 'United Kingdom_sun', 'China_sum', 'India', 'Italy', 'Germany']

x = [i/250 - 2 for i in range(1000)]

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Q1 - COVID Cases', children=[
            html.H1("Global Confirmed COVID-19 Cases"),
            html.Label("Pick the country Name"),
            dcc.Dropdown(id='dd', options=countries, value=countries, multi=True),
            dcc.Graph(id='covid-graph')
        ]),
        dcc.Tab(label='Q2 - Quadratic', children=[
            html.H1("f(x) = ax² + bx + c"),
            html.Label("a"), dcc.Slider(id='a', min=-10, max=10, step=0.5, value=1),
            html.Label("b"), dcc.Slider(id='b', min=-10, max=10, step=0.5, value=0),
            html.Label("c"), dcc.Slider(id='c', min=-10, max=10, step=0.5, value=0),
            dcc.Graph(id='quad-graph')
        ]),
        dcc.Tab(label='Q3 - Calculator', children=[
            html.H1("Calculator"),
            html.Label("Operation"),
            dcc.Dropdown(
                id='calc-op',
                options=[
                    {'label': 'Addition', 'value': 'add'},
                    {'label': 'Subtraction', 'value': 'sub'},
                    {'label': 'Multiplication', 'value': 'mul'},
                    {'label': 'Division', 'value': 'div'},
                    {'label': 'Logarithm', 'value': 'log'},
                    {'label': 'b-th root', 'value': 'root'}
                ],
                value='add'
            ),
            html.Label("a"), dcc.Input(id='input-a', type='number', value=1),
            html.Label("b"), dcc.Input(id='input-b', type='number', value=1),
            html.Div(id='calc-res', style={'fontSize': '24px', 'marginTop': '20px'})
        ])
    ])
])

@app.callback(Output('covid-graph', 'figure'), Input('dd', 'value'))
def update_covid(selected):
    plot_df = df[['Date'] + selected].melt(id_vars='Date', var_name='Country', value_name='Cases')
    plot_df['Cases'] = pd.to_numeric(plot_df['Cases'])
    return px.line(plot_df, x='Date', y='Cases', color='Country')

@app.callback(Output('quad-graph', 'figure'), Input('a', 'value'), Input('b', 'value'), Input('c', 'value'))
def update_quad(a, b, c):
    return px.line(x=x, y=[a*i**2 + b*i + c for i in x], labels={'x': 'x', 'y': 'f(x)'})

@app.callback(
    Output('calc-res', 'children'),
    [Input('calc-op', 'value'), Input('input-a', 'value'), Input('input-b', 'value')]
)
def calculate(op, a, b):
    if a is None or b is None: return "Result: "
    try:
        if op == 'add': return f"Result: {a + b}"
        if op == 'sub': return f"Result: {a - b}"
        if op == 'mul': return f"Result: {a * b}"
        if op == 'div': return f"Result: {a / b}" if b != 0 else "Error: b ≠ 0"
        if op == 'log':
            if a > 0 and b > 1: return f"Result: {math.log(a, b)}"
            return "Error: a > 0, b > 1"
        if op == 'root':
            if a == 0 or b <= 0: return "Error: a ≠ 0, b > 0"
            if a < 0 and b % 2 == 0: return "Error: b must be odd if a < 0"
            res = abs(a)**(1/b)
            return f"Result: {res if a > 0 else -res}"
    except: return "Error"

if __name__ == '__main__':
    app.run(debug=True)
