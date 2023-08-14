import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Create app
app = dash.Dash(__name__)

# Read the wildfire data into a pandas dataframe
df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv')

# Extract year and month from the date column
df['Month'] = pd.to_datetime(df['Date']).dt.month_name()
df['Year'] = pd.to_datetime(df['Date']).dt.year

# Layout Section of Dash
app.layout = html.Div(children=[
    html.H1('Australia Wildfire Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': '26px'}),

    # First inner division for region selection
    html.Div([
        html.H2('Select Region:', style={'margin-right': '2em'}),
        dcc.RadioItems(
            options=[
                {"label": "New South Wales", "value": "NSW"},
                {"label": "Northern Territory", "value": "NT"},
                {"label": "Queensland", "value": "QL"},
                {"label": "South Australia", "value": "SA"},
                {"label": "Tasmania", "value": "TA"},
                {"label": "Victoria", "value": "VI"},
                {"label": "Western Australia", "value": "WA"}
            ],
            value="NSW",
            id='region',
            inline=True
        ),
    ]),

    # Second inner division for year selection
    html.Div([
        html.H2('Select Year:', style={'margin-right': '2em'}),
        dcc.Dropdown(
            options=[{'label': year, 'value': year} for year in df['Year'].unique()],
            value="2005",
            id='year'
        ),
    ]),

    # Third inner division for plots
    html.Div([
        dcc.Graph(id='plot1'),
        dcc.Graph(id='plot2')
    ])
])

# Callback function
@app.callback(
    [Output(component_id='plot1', component_property='figure'),
     Output(component_id='plot2', component_property='figure')],
    [Input(component_id='region', component_property='value'),
     Input(component_id='year', component_property='value')]
)
def reg_year_display(input_region, input_year):
    # Data
    region_data = df[df['Region'] == input_region]
    y_r_data = region_data[region_data['Year'] == input_year]

    # Plot one - Monthly Average Estimated Fire Area
    est_data = y_r_data.groupby('Month')['Estimated_fire_area'].mean().reset_index()
    fig1 = px.pie(est_data, values='Estimated_fire_area', names='Month',
                  title="{}: Monthly Average Estimated Fire Area in year {}".format(input_region, input_year))

    # Plot two - Monthly Average Count of Pixels for Presumed Vegetation Fires
    veg_data = y_r_data.groupby('Month')['Count'].mean().reset_index()
    fig2 = px.bar(veg_data, x='Month', y='Count',
                  title='{}: Average Count of Pixels for Presumed Vegetation Fires in year {}'.format(input_region, input_year))

    return [fig1, fig2]


if __name__ == '__main__':
    app.run_server(debug=True)
