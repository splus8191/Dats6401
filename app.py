from dash import Dash, dcc, html
from dash.dependencies import Input, Output

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    dcc.Slider(id='my-input', min=0, max=90, step=1, value=70),
    html.Br(),
    dcc.Slider(id="second_slider", min=-10, max=35, step=0.5),
])

@app.callback(
    Output('second_slider', 'value'),
    Input('my-input', 'value')
)
def update_reza(value):
    return (value - 32) / 1.8

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
