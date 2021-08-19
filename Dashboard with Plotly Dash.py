# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                dcc.Dropdown(id='site-dropdown',
                                            options=[{'label':'CCAFS LC-40', 'value':'LC40'},
                                                    {'label':'CCAFS SLC-40', 'value':'SLC40'},
                                                    {'label':'KSC LC-39A', 'value':'LC39A'},
                                                    {'label':'VAFB SLC-4E', 'value':'SLC4E'},
                                                    {'label':'ALL', 'value':'ALL'}
                                                    ],
                                            value='ALL',
                                            placeholder='Select a Launch Site here',
                                            searchable=True
                                            ),
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P('Payload range (Kg):'),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=min_payload,
                                                max=max_payload,
                                                step=1000,
                                                value=[min_payload, max_payload]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))

def get_piechart(site):

    df =  spacex_df[spacex_df['Launch Site']==str(site)]

    if site == 'ALL':

        pie_chart=px.pie(spacex_df, values='class', names='Launch Site', title='% of success')
    
    else:
        pie_chart=px.pie(df, values='class', names='Launch Site', title='% of success')

    return pie_chart

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
                [Input(component_id='site-dropdown', component_property='value'), 
                Input(component_id='payload-slider', component_property='value')])

def get_scatter(site, payload_range):

    low, high = payload_range
    df2=spacex_df[(spacex_df['Payload Mass (kg)']>low) & (spacex_df['Payload Mass (kg)']<high)]
    df3 =  df2[df2['Launch Site']==str(site)]

    if site == 'ALL':
        scatter=px.scatter(df2, 
                            x='Payload Mass (kg)', 
                            y='class', 
                            color='Booster Version Category',  
                            title='Success per Payload Mass and Booster used',
                            )
    
    else:
        scatter=px.scatter(df3, 
                            x='Payload Mass (kg)', 
                            y='class', 
                            color='Booster Version Category',  
                            title='Success per Payload Mass and Booster used',
                            )

    return scatter

# Run the app
if __name__ == '__main__':
    app.run_server()