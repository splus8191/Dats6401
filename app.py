from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import math

app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# --- Data Setup (Q1) ---
url = "https://raw.githubusercontent.com/rjafari979/Information-Visualization-Data-Analytics-Dataset-/main/CONVENIENT_global_confirmed_cases.csv"
df = pd.read_csv(url).drop(index=0).reset_index(drop=True)
df = df.rename(columns={'Country/Region': 'Date'})
df['China_sum'] = df.filter(like='China').apply(pd.to_numeric).sum(axis=1)
df['United Kingdom_sum'] = df.filter(like='United Kingdom').apply(pd.to_numeric).sum(axis=1)
countries = ['US', 'Brazil', 'United Kingdom_sum', 'China_sum', 'India', 'Italy', 'Germany']
x_vals = [i/250 - 2 for i in range(1000)]

# --- Layout ---
app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Q1 - COVID Cases', children=[
            html.H1("COVID-19 Cases"),
            dcc.Dropdown(id='dd', options=countries, value=['US'], multi=True),
            dcc.Graph(id='covid-graph')
        ]),
        dcc.Tab(label='Q2 - Quadratic', children=[
            html.H1("f(x) = ax² + bx + c"),
            *[html.Div([html.Label(v), dcc.Slider(id=v, min=-10, max=10, value=1 if v=='a' else 0)]) for v in 'abc'],
            dcc.Graph(id='quad-graph')
        ]),
        dcc.Tab(label='Q3 - Calculator', children=[
            html.H1("Simple Calculator"),
            html.Label("Select Operation"),
            dcc.Dropdown(id='op', options=['+', '-', '*', '/', 'log', 'root'], value='+'),
            html.Label("Input a"), dcc.Input(id='num-a', type='number', value=1),
            html.Label("Input b"), dcc.Input(id='num-b', type='number', value=1),
            html.H3(id='calc-result')
        ])
    ])
])

# --- Callbacks ---
@app.callback(Output('covid-graph', 'figure'), Input('dd', 'value'))
def update_covid(selected):
    return px.line(df, x='Date', y=selected)

@app.callback(Output('quad-graph', 'figure'), [Input(v, 'value') for v in 'abc'])
def update_quad(a, b, c):
    return px.line(x=x_vals, y=[a*i**2 + b*i + c for i in x_vals])

@app.callback(Output('calc-result', 'children'), [Input('op', 'value'), Input('num-a', 'value'), Input('num-b', 'value')])
def calculate(op, a, b):
    try:
        if op == '+': return f"Result: {a + b}"
        if op == '-': return f"Result: {a - b}"
        if op == '*': return f"Result: {a * b}"
        if op == '/': return f"Result: {a / b}" if b != 0 else "Error: Div by 0"
        if op == 'log':
            if a > 0 and b > 1: return f"Result: {math.log(a, b)}"
            return "Error: a > 0 and b > 1 required"
        if op == 'root':
            if a == 0 or b <= 0 or (a < 0 and b % 2 == 0): return "Error: Invalid Input"
            # Handling negative roots:
            res = abs(a)**(1/b)
            return f"Result: {res if a > 0 else -res}"
    except: return "Error: Invalid calculation"

if __name__ == '__main__':
    app.run(debug=True)
