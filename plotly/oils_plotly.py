import pandas as pd
from datetime import timedelta
import plotly.express as px 
import plotly.graph_objects as go
import datetime


import dash 
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


# initiating  Dash app
app = dash.Dash(__name__,external_stylesheets=['https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css',"https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"])

# loading data
df = pd.read_csv('oils_analysis/clean_oils_data.csv')

# getting frames for graphs and dropdowns
acids = df[df['Features'].str.contains('Kwasy')]

omegas = df[df['Features'].str.contains('Omega')]

fat = df[df['Features'] =='Tłuszcz']

# creating a list of products for dropdowns
oils =  [{'label':x,'value':x} for x in fat['Product'].to_list()]

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([
        html.Div([
            html.H1("Oils analysis",
                            style={"textAlign": "center",'color':"white",
                            'paddingBottom':"20px",'width':'100%'})
        ],className='row header'),
        html.Div([
                html.Div([
                    dcc.Dropdown(id='product_dropdown_fat',
                        options=oils,
                        multi=True,
                        value=['Olej Arganowy Nierafinowny'],
                        placeholder="Select oil..."
                    ),
                html.Div([
                    dcc.Graph(id='fat_chart'),
                ],className='mx-6')
                ],className='six columns'),

            

                html.Div([
                dcc.Dropdown(id='product_dropdown_omegas',
                    options=oils,
                    multi=True,
                    value=['Olej Arganowy Nierafinowny'],
                    placeholder="Select oil..."
                ),
                html.Div([
                    dcc.Graph(id='omega_chart'),
                ],className='mx-6')
                ],className='six columns'),

        ],className='row'),
        html.Div([
            html.Div([
                    dcc.Dropdown(id='product_dropdown_acids',
                        options=oils,
                        multi=True,
                        value=['Olej Arganowy Nierafinowny'],
                        placeholder="Select oil..."
                    ),
                    dcc.Checklist(id='acids_checklist',
                    options=[
                        {'label': 'Nasycone', 'value': 'Kwasy Tłuszczowe Nasycone'},
                        {'label': 'Jednonienasycone', 'value': 'Kwasy Tłuszczowe Jednonienasycone'},
                        {'label': 'Wielonienasycone', 'value': 'Kwasy Tłuszczowe Wielonienasycone'}
                    ],
                    value=['Kwasy Tłuszczowe Nasycone'], labelStyle={'display': 'block','color':'white'},
        style={"width":200, "overflow":"auto"}
                    ), 
                    html.Div([
                        dcc.Graph(id='acid_chart'),
                    ],className='mx-6')
                    ],className='six columns'),
        ],className='row')


],className='main_oil')




# ------------------------------------------------------------------------------
# Functions
@app.callback(
    [Output('fat_chart', 'figure'),
     Output('acid_chart', 'figure'),
     Output('omega_chart', 'figure')],
    [Input('acids_checklist','value'),
    Input('product_dropdown_fat', 'value'),
     Input('product_dropdown_acids', 'value'),
     Input('product_dropdown_omegas', 'value')]
)
def update_data(acids_check,fats_drop,acids_drop,omegas_drop):
    # filtering fats dataframe
    fat_filtered = fat[fat.Product.isin(fats_drop)]

    # filtering acids dataframe
    acids_filtered = acids[acids.Product.isin(acids_drop)]
    acids_filtered = acids_filtered[acids_filtered.Features.isin(acids_check)]
    print(acids_filtered)

    # filtering omega dataframe
    omega_filtered = omegas[omegas.Product.isin(omegas_drop)]


    
    # creating graphs
    if fat_filtered.empty:
        # if there is no data - show info to select at least one value for filterting
        fatchart = go.Figure()
        fatchart.update_layout(
            xaxis =  { "visible": False },
            yaxis = { "visible": False },
            annotations = [
                {   
                    "text": "Please select at least one oil",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 28
                    }
                }
            ]
        )
    else:
        fatchart= px.bar(fat_filtered, x='Details', y='Product',title='Amount of fat in selected oils',labels={'Product':'Oil','Details':'Content in grams (g)'},color='Product',
        text='Details')
        # fatchart.update_xaxes(visible=False,tickangle=90)
        fatchart.update_layout(xaxis_range=[0,fat['Details'].max()])

    if acids_filtered.empty:
        # if there is no data - show info to select at least one value for filterting
        acidchart = go.Figure()
        acidchart.update_layout(
            xaxis =  { "visible": False },
            yaxis = { "visible": False },
            annotations = [
                {   
                    "text": "Please select at least one oil and one acid type",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 22
                    }
                }
            ]
        )
    else:
        acidchart = px.bar(acids_filtered, x='Details', y='Product',title='Amount of selected acids in selected oils',labels={'Product':'Oil','Details':'Content in grams (g)'},
        barmode='group',color='Features',text='Details')
        acidchart.update_layout(xaxis_range=[0,acids['Details'].max()])
        # acidchart.update_xaxes(tickangle=90)

    if omega_filtered.empty:
        # if there is no data - show info to select at least one value for filterting
        omegachart = go.Figure()
        omegachart.update_layout(
            xaxis =  { "visible": False },
            yaxis = { "visible": False },
            annotations = [
                {   
                    "text": "Please select at least one oil",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 28
                    }
                }
            ]
        )
    else:
        omegachart = px.bar(omega_filtered, x='Details', y='Product',title='Amount of omega acids in selected oils',labels={'Product':'Oil','Details':'Content in grams (g)'},
        barmode='group',color='Features',text='Details')
        # omegachart.update_xaxes(tickangle=90)
        omegachart.update_layout(xaxis_range=[0,omegas['Details'].max()])
        omegachart.update_xaxes(ticklabelposition="inside top")
        
    

    return (fatchart,acidchart,omegachart)



# ------------------------------------------------------------------------------
# TO RUN THE APP
if __name__ == '__main__':
    app.run_server(debug=True)
