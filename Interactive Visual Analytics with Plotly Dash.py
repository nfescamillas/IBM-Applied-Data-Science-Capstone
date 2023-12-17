# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options=
                                [{'label':'All Sites','value':'ALL'},
                                {'label':'KSC LC-39A','value':'KSC LC-39A'},
                                {'label':'CCAFS LC-40','value':'CCAFS LC-40'},
                                {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'},
                                {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'},],
                                value='ALL', placeholder='Select a Launch Site here',searchable = True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0,max=10000,value=[min_payload,max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property ='figure'), 
    Input(component_id ='site-dropdown',component_property='value')  
)

def update_plot(site):
    df=spacex_df
    if site =='ALL':
        fig=px.pie(df, values='class', names='Launch Site', title ='Total Success Launches by All Sites')
    else:
        df1=df[df['Launch Site'] == site]
        fig=px.pie(df1, values=df1['class'].value_counts(normalize=True), names=df1['class'].unique(), title ='Total Success Launches by {}'.format(site))
    
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart',component_property='figure'),
    Input(component_id ='site-dropdown', component_property='value'),
    Input(component_id ='payload-slider', component_property='value')
)

def update_plot2(site,payload):
    df=spacex_df
    if site =='ALL':
        fig=px.scatter(df[df['Payload Mass (kg)'].between(payload[0],payload[1])], x='Payload Mass (kg)', y='class', color='Booster Version Category')
    else:
        df1=df[df['Launch Site'] == site]
        fig=px.scatter(df1[df1['Payload Mass (kg)'].between(payload[0],payload[1])], x='Payload Mass (kg)', y='class',color='Booster Version Category')
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
