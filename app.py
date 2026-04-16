from dash import Dash
import dash as html
import dash as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import math
from scipy.fft import fft
import random

app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server

url = "https://raw.githubusercontent.com/rjafari979/Information-Visualization-Data-Analytics-Dataset-/main/CONVENIENT_global_confirmed_cases.csv"
df = pd.read_csv(url)
df = df.drop(index=0).reset_index(drop=True)
df = df.rename(columns={'Country/Region': 'Date'})
df['China_sum'] = df.filter(like='China').apply(pd.to_numeric, errors='coerce').sum(axis=1)
df['United Kingdom_sun'] = df.filter(like='United Kingdom').apply(pd.to_numeric, errors='coerce').sum(axis=1)

countries = ['US', 'Brazil', 'United Kingdom_sun', 'China_sum', 'India', 'Italy', 'Germany']
x = [i/250 - 2 for i in range(1000)]

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Question 1', children=[
            html.H1("Covid Cases per Country"),
            html.Label("Pick the country name"),
            dcc.Dropdown(id='dd', options=countries, value=countries, multi=True),
            dcc.Graph(id='covid-graph')
        ]),
        dcc.Tab(label='Question 2', children=[
            html.H1("f(x) = ax^2 + bx + c"),
            html.Label("a"), dcc.Slider(id='a', min=-10, max=10, step=0.5, value=1),
            html.Label("b"), dcc.Slider(id='b', min=-10, max=10, step=0.5, value=0),
            html.Label("c"), dcc.Slider(id='c', min=-10, max=10, step=0.5, value=0),
            dcc.Graph(id='quad-graph')
        ]),
        dcc.Tab(label='Question 3', children=[
            html.H1("Calculator"),
            html.Label("Operation"),
            dcc.Dropdown(id='calc-op', options=[
                {'label': 'Addition', 'value': 'add'},
                {'label': 'Subtraction', 'value': 'sub'},
                {'label': 'Multiplication', 'value': 'mul'},
                {'label': 'Division', 'value': 'div'},
                {'label': 'Logarithm', 'value': 'log'},
                {'label': 'b-th root', 'value': 'root'}
            ], value='add'),
            html.Label("a"), dcc.Input(id='input-a', type='number', value=1),
            html.Label("b"), dcc.Input(id='input-b', type='number', value=1),
            html.Div(id='calc-res', style={'fontSize': '24px', 'marginTop': '20px'})
        ]),
        dcc.Tab(label='Question 4', children=[
            html.H1("Polynomial Plotter"),
            html.Label("Please enter the polynomial order"),
            dcc.Input(id='poly-order', type='number', value=2),
            dcc.Graph(id='poly-graph')
        ]),
        dcc.Tab(label='Question 5', children=[
            html.Label("Please enter the number of sinusoidal cycle"),
            dcc.Input(id='cycles', type='number', value=4),
            html.Label("Please enter the mean of the white noise"),
            dcc.Input(id='noise-mean', type='number', value=0),
            html.Label("Please enter the standard deviation of the white noise"),
            dcc.Input(id='noise-std', type='number', value=1),
            html.Label("Please enter the number of samples"),
            dcc.Input(id='samples', type='number', value=1000),
            dcc.Graph(id='sig-graph'),
            html.H3("The fast fourier transform of above generated data"),
            dcc.Graph(id='fft-graph')
        ]),
        dcc.Tab(label='Question 6', children=[
            html.H1("Two Layer Neural Network"),
            html.Img(src='/assets/nn.png', style={'width': '40%', 'display': 'block', 'margin': 'auto'}),
            html.Div([
                html.Div([
                    html.Label("b11"), dcc.Slider(id='b11', min=-10, max=10, step=0.001, value=0),
                    html.Label("b12"), dcc.Slider(id='b12', min=-10, max=10, step=0.001, value=0),
                    html.Label("w11"), dcc.Slider(id='w11', min=-10, max=10, step=0.001, value=1),
                    html.Label("w211"), dcc.Slider(id='w211', min=-10, max=10, step=0.001, value=1),
                ], style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'middle'}),
                html.Div([dcc.Graph(id='nn-graph')],
                    style={'width': '40%', 'display': 'inline-block', 'vertical-align': 'middle'}),
                html.Div([
                    html.Label("b2"), dcc.Slider(id='b2', min=-10, max=10, step=0.001, value=0),
                    html.Label("w112"), dcc.Slider(id='w112', min=-10, max=10, step=0.001, value=1),
                    html.Label("w212"), dcc.Slider(id='w212', min=-10, max=10, step=0.001, value=1),
                ], style={'width': '40%', 'display': 'inline-block', 'vertical-align': 'middle'}),
            ])
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

@app.callback(Output('calc-res', 'children'),
    Input('calc-op', 'value'), Input('input-a', 'value'), Input('input-b', 'value'))
def calculate(op, a, b):
    if a is None or b is None:
        return "Result: "
    try:
        if op == 'add': return f"Result: {a + b}"
        if op == 'sub': return f"Result: {a - b}"
        if op == 'mul': return f"Result: {a * b}"
        if op == 'div': return f"Result: {a / b}" if b != 0 else "Error: b ≠ 0"
        if op == 'log':
            if a > 0 and b > 1: return f"Answer: {math.log(a, b)}"
            return "Error: a > 0, b > 1"
        if op == 'root':
            if a == 0 or b <= 0: return "Not Valid"
            if a < 0 and b % 2 == 0: return "Not Valid"
            res = abs(a) ** (1 / b)
            return f"Result: {res if a > 0 else -res}"
    except:
        return "Error"

@app.callback(Output('poly-graph', 'figure'), Input('poly-order', 'value'))
def update_poly(n):
    if n is None: n = 0
    return px.line(x=x, y=[i**n for i in x], labels={'x': 'x', 'y': f'x^{n}'})

@app.callback(
    [Output('sig-graph', 'figure'), Output('fft-graph', 'figure')],
    [Input('cycles', 'value'), Input('noise-mean', 'value'), Input('noise-std', 'value'), Input('samples', 'value')]
)
def update_fft(c, m, s, n):
    if None in [c, m, s, n]: return {}, {}
    n = int(n)
    t = [math.pi * (2*i/(n-1) - 1) for i in range(n)]
    y = [math.sin(c * t[i]) + random.gauss(m, s) for i in range(n)]
    return px.line(x=t, y=y), px.line(x=t, y=[abs(v) for v in fft(y)])

@app.callback(Output('nn-graph', 'figure'),
    Input('b11', 'value'), Input('b12', 'value'), Input('w11', 'value'), Input('w211', 'value'),
    Input('b2', 'value'), Input('w112', 'value'), Input('w212', 'value'))
def update_nn(b11, b12, w11, w211, b2, w112, w212):
    p = [i/999*10 - 5 for i in range(1000)]
    sig = lambda x: 1 / (1 + math.exp(-x))
    a2 = [w112*sig(pi*w11+b11) + w212*sig(pi*w211+b12) + b2 for pi in p]
    return px.line(x=p, y=a2, labels={'x': 'p', 'y': 'a^2'})

if __name__ == '__main__':
    app.run(debug=True)
