import dash
import dash_core_components as dcc
import dash_html_components as html

import dash_cytoscape as cyto

########### Define your variables
import json
import dash
import urllib.request
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_cytoscape as cyto

app = dash.Dash(__name__)
app.title = "Food Graphs"
server = app.server
tabtitle='Food from allrecipes.com!'
mytitle='Recipes graph from allrecipes.com'
myheading='Recipes\' Graph'
githublink='https://github.com/kovashikawa/flying-dog-beers'
sourceurl='https://www.allrecipes.com/'

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True


with open('./food.json', 'r') as f:
    data = json.loads(f.read())
    
#https://github.com/plotly/dash-cytoscape/blob/master/demos/data/edge-types/cy-style.json
with open('cy-style.json') as f:
    stylesheet = json.loads(f.read())

styles = {
    'container': {
        'position': 'fixed',
        'display': 'flex',
        'flex-direction': 'column',
        'height': '100%',
        'width': '100%'
    },
    'cy-container': {
        'flex': '1',
        'position': 'relative'
    },
    'cytoscape': {
        'position': 'absolute',
        'width': '100%',
        'height': '100%',
        'z-index': 999
    }
}


# App
app.layout = html.Div(style=styles['container'], children=[
    html.Div([
        html.Button("Responsive Toggle", id='toggle-button'),
        html.Div(id='toggle-text')
    ]),
    html.Div(className='cy-container', style=styles['cy-container'], children=[
        cyto.Cytoscape(
            id='cytoscape',
            elements=data['elements'],
            stylesheet=stylesheet,
            style=styles['cytoscape'],
            layout={
                'name': 'cose',
                'idealEdgeLength': 100,
                'nodeOverlap': 20,
                'refresh': 20,
                'fit': True,
                'padding': 30,
                'randomize': False,
                'componentSpacing': 100,
                'nodeRepulsion': 400000,
                'edgeElasticity': 100,
                'nestingFactor': 5,
                'gravity': 80,
                'numIter': 1000,
                'initialTemp': 200,
                'coolingFactor': 0.95,
                'minTemp': 1.0
            },
            responsive=True
        )
    ])
])


@app.callback(Output('cytoscape', 'responsive'), [Input('toggle-button', 'n_clicks')])
def toggle_responsive(n_clicks):
    n_clicks = 2 if n_clicks is None else n_clicks
    toggle_on = n_clicks % 2 == 0
    return toggle_on


@app.callback(Output('toggle-text', 'children'), [Input('cytoscape', 'responsive')])
def update_toggle_text(responsive):
    return '\t' + 'Responsive ' + ('On' if responsive else 'Off')


########### Initiate the app
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# server = app.server
# app.title=tabtitle

# ########### Set up the layout
# app.layout = html.Div(children=[
#     html.H1(myheading),
#     dcc.Graph(
#         id='allrecipes',
#         figure='assets\\allrecipes_logo.png'
#     ),
#     html.A('Code on Github', href=githublink),
#     html.Br(),
#     html.A('Data Source', href=sourceurl),
#     ]
# )

if __name__ == '__main__':
    app.run_server()
