# Import required libraries
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

# Read the airline data into pandas dataframe
spacex_df =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})
# Create a dash application
app = dash.Dash(__name__)
                               
app.layout = html.Div(children=[ html.H1('SpaceX Launch Record Dashboard', 
                                style={'textAlign': 'center', 'color': '#503D36',
                                'font-size': 40}),
                                dcc.Dropdown(id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}

                                    ],
                                    value='ALL',
                                    placeholder="place holder here",
                                    searchable=True
                                    ),
                                 html.Div(dcc.Graph(id='success-pie-chart')),
                                 html.Div([   html.Label('Select Payload Mass Range (kg)', style={'font-size': 18, 'color': 'Black', 'margin-bottom': '10px'}),
                                           dcc.RangeSlider(
                                            id='payload-slider',
                                            min=0, 
                                            max=10000, 
                                            step=1000,
                                            marks={i: str(i) for i in range(0, 10001, 1000)},  # Markierungen für den Slider
                                            value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()]  # Aktueller Payload-Bereich
                                ),
                                           html.Div(dcc.Graph(id = 'scatter-plot'))])
                                ])


@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches by Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']== entered_site]
        site_counts = filtered_df['class'].value_counts().reset_index()
        site_counts.columns = ['class', 'count']
        fig = px.pie(site_counts,
                     values = 'count',
                     names = 'class',
                     title = f'Total Success Launches for Site {entered_site}')
        return fig
@app.callback(Output(component_id= 'scatter-plot', component_property = 'figure'),
              Input(component_id = 'payload-slider', component_property = 'value'))

def get_scatter_plot(entered_site):
    if entered_site == 'All':
        fig = px.scatter(data_frame = spacex_df,
                         x = 'Payload Mass (kg)',
                         y = 'class',
                         color = 'Booster Version',
                         title = 'Correlation between Payload and Success for all Sites')
        
        return fig
    else:
        min_payload, max_payload = entered_site

        # Filtere den DataFrame nach dem Payload-Bereich
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= min_payload) & 
                                (spacex_df['Payload Mass (kg)'] <= max_payload)]
        fig = px.scatter(data_frame = filtered_df,
                         x = 'Payload Mass (kg)',
                         y = 'class',
                         color = 'Booster Version')
        return fig
# Run the app
if __name__ == '__main__':
    app.run_server(port = 8052)