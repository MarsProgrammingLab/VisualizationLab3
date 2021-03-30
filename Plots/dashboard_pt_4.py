import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Load CSV file from Datasets folder
df1 = pd.read_csv('C:/Users/marta/OneDrive/'
                  'Desktop/Coursework/SoftwareEngineeringITCS-3315/datasets/Olympic2016Rio.csv')
df2 = pd.read_csv('C:/Users/marta/OneDrive/'
                  'Desktop/Coursework/SoftwareEngineeringITCS-3315/datasets/Weather2014-15.csv')

app = dash.Dash()

# Bar chart data
#barchart_df = df1[df1['NOC'] == 'United States(USA)']
#barchart_df = barchart_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
barchart_df = df1.groupby(['NOC'])['Gold'].sum().reset_index()
barchart_df = barchart_df.sort_values(by=['Gold'], ascending=[False]).head(20)
data_barchart = [go.Bar(x=barchart_df['NOC'], y=barchart_df['Gold'])]

# Stack bar chart data
stackbarchart_df = df1.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
stackbarchart_df = stackbarchart_df.groupby(['NOC']).agg(
    {'Gold': 'sum', 'Silver': 'sum', 'Bronze': 'sum', 'Total': 'sum'}).reset_index()
stackbarchart_df = stackbarchart_df.sort_values(by=['Total'], ascending=[False]).head(20).reset_index()
trace1_stackbarchart = go.Bar(x=stackbarchart_df['NOC'], y=stackbarchart_df['Gold'], name='Gold',
                              marker={'color': '#CD7F32'})
trace2_stackbarchart = go.Bar(x=stackbarchart_df['NOC'], y=stackbarchart_df['Silver'], name='Silver',
                              marker={'color': '#9EA0A1'})
trace3_stackbarchart = go.Bar(x=stackbarchart_df['NOC'], y=stackbarchart_df['Bronze'], name='Bronze',
                              marker={'color': '#FFD700'})
data_stackbarchart = [trace1_stackbarchart, trace2_stackbarchart, trace3_stackbarchart]

# Line Chart
line_df = df2
line_df['date'] = pd.to_datetime(line_df['date'])
data_linechart = [go.Scatter(x=line_df['date'], y=line_df['average_precipitation'], mode='lines', name='average_precipitation')]

# Multi Line Chart
multiline_df = df2
multiline_df['date'] = pd.to_datetime(multiline_df['date'])
trace1_multiline = go.Scatter(x=multiline_df['date'], y=multiline_df['record_min_temp'], mode='lines', name='record_min_temp')
trace2_multiline = go.Scatter(x=multiline_df['date'], y=multiline_df['record_max_temp'], mode='lines', name='record_max_temp')
trace3_multiline = go.Scatter(x=multiline_df['date'], y=multiline_df['record_precipitation'], mode='lines', name='record_precipitation')
data_multiline = [trace1_multiline, trace2_multiline, trace3_multiline]

# Bubble chart
bubble_df = df2.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
# bubble_df['Unrecovered'] = bubble_df['Confirmed'] - bubble_df['Deaths'] - bubble_df['Recovered']
# bubble_df = bubble_df[(bubble_df['Date'] != 'China')]
bubble_df = bubble_df.groupby(['date']).agg(
    {'month': 'sum', 'record_max_temp': 'sum'}).reset_index()
data_bubblechart = [
    go.Scatter(x=bubble_df['date'],
               y=bubble_df['record_max_temp'],
               text=bubble_df['date'],
               mode='markers',
               marker=dict(size=bubble_df['record_max_temp'], color=bubble_df['record_max_temp'], showscale=True))
]

# Heatmap
data_heatmap = [go.Heatmap(x=df2['month'],
                           y=df2['day'],
                           z=df2['record_max_temp'].values.tolist(),
                           colorscale='Jet')]

# Layout
app.layout = html.Div(children=[
    html.H1(children='Python Dash',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Div('Web dashboard for Data Visualization using Python', style={'textAlign': 'center'}),
    html.Div('Olympics -  2016', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Interactive Bar chart', style={'color': '#df1e56'}),
    html.Div('This bar chart represent the number of medals from the selected country.'),
    dcc.Graph(id='graph1'),
    html.Div('Please select a country', style={'color': '#ef3e18', 'margin':'10px'}),
    dcc.Dropdown(
        id='select-noc',
        options=[
            {'label': 'United States(USA)', 'value': 'United States(USA)'},
            {'label': 'Great Britain(GBR)', 'value': 'Great Britain(GBR)'},
            {'label': 'China(CHN)', 'value': 'China(CHN)'},
            {'label': 'Russia(RUS)', 'value': 'Russia(RUS)'},
            {'label': 'Germany(GER)', 'value': 'Germany(GER)'},
            {'label': 'Japan(JPN)', 'value': 'Japan(JPN)'}
        ],
        value='Japan(JPN)'
    ),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bar chart', style={'color': '#df1e56'}),
    html.Div('This bar chart represent the number of gold medals from each country in the 2016 Olympics.'),
    dcc.Graph(id='graph2',
              figure={
                  'data': data_barchart,
                  'layout': go.Layout(title='Medals from each country in the 2016 Olympics',
                                      xaxis={'title': 'NOC'}, yaxis={'title': 'Number of medals'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Stack bar chart', style={'color': '#df1e56'}),
    html.Div(
        'This stack bar chart represents the number of gold, silver, and bronze from each country in the 2016 Olympics'),
    dcc.Graph(id='graph3',
              figure={
                  'data': data_stackbarchart,
                  'layout': go.Layout(title='Gold, silver, and bronze medals from each country in the 2016 Olympics',
                                      xaxis={'title': 'Country'}, yaxis={'title': 'Number of cases'},
                                      barmode='stack')
              }
              ),
html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Line chart', style={'color': '#df1e56'}),
    html.Div('This line chart represents the average precipitation of the given date'),
    dcc.Graph(id='graph4',
              figure={
                  'data': data_linechart,
                  'layout': go.Layout(title='Average precipitation of the given date',
                                      xaxis={'title': 'Date'}, yaxis={'title': 'Average precipitation'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Multi Line chart', style={'color': '#df1e56'}),
    html.Div(
        'This line chart represents the record min / max temperature, and record precipitation on a given date'),
    dcc.Graph(id='graph5',
              figure={
                  'data': data_multiline,
                  'layout': go.Layout(
                      title='Record min / max temperature, and record precipitation',
                      xaxis={'title': 'Date'}, yaxis={'title': 'Record min / max temperature, and record precipitation'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bubble chart', style={'color': '#df1e56'}),
    html.Div(
        'This bubble chart represents the record min / max temperature, and record precipitation on a given date'),
    dcc.Graph(id='graph6',
              figure={
                  'data': data_bubblechart,
                  'layout': go.Layout(title='Record min / max temperature, and record precipitation',
                                      xaxis={'title': 'date'}, yaxis={'title': 'record_max_temp'},
                                      hovermode='closest')
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Heat map', style={'color': '#df1e56'}),
    html.Div(
        'This heat map represents thr record max temp given the day and month'),
    dcc.Graph(id='graph7',
              figure={
                  'data': data_heatmap,
                  'layout': go.Layout(title='Record max temp',
                                      xaxis={'title': 'Month'}, yaxis={'title': 'Day'})
              }
              )

])


@app.callback(Output('graph1', 'figure'),
              [Input('select-noc', 'value')])
def update_figure(selected_noc):
    filtered_df = df1[df1['NOC'] == selected_noc]

    filtered_df = filtered_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    new_df = filtered_df.groupby(['NOC'])['Total'].sum().reset_index()
    new_df = new_df.sort_values(by=['Total'], ascending=[False]).head(20)
    data_interactive_barchart = [go.Bar(x=new_df['NOC'], y=new_df['Total'])]
    return {'data': data_interactive_barchart, 'layout': go.Layout(title='Total medals in '+ selected_noc,
                                                                   xaxis={'title': 'NOC'},
                                                                   yaxis={'title': 'Total medals'})}


if __name__ == '__main__':
    app.run_server()
