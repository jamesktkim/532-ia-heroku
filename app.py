from dash import Dash, html, dcc, Input, Output
import altair as alt
import pandas as pd
import numpy as np

# Read gapminder data
url = "https://raw.githubusercontent.com/UofTCoders/workshops-dc-py/master/data/processed/world-data-gapminder.csv"
gm = pd.read_csv(url)

# Setup app and layout/frontend
app = Dash(__name__,  external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server

app.layout = html.Div([
    html.H1('Life Expectancy Top 10 countries'),
    html.Iframe(
        id = 'barchart',
        style={'border-width': '0', 
        'width': '100%',
        'height': '400px',
        "top": "50%",
        "left": "50%",}),
    html.H3('Year'),
    html.P('The user can slide over the years'),
    dcc.Slider(
        min=1970,
        max=2010,
        step=5,
        value=2010,
        id='year',
        marks={i: str(i) for i in range(1970, 2015, 5)},
        ),
])


# Set up callbacks/backend
@app.callback(
    Output('barchart', 'srcDoc'),
    Input('year', 'value'))

def plot_country(year):
    country = (
        alt.Chart(gm.query('year == @year'), title='Top 10 Countries').mark_bar().encode(
            y=alt.Y('country', sort='-x', title='Country'),
            x=alt.X('life_expectancy', title='Life Expectancy'),
            color=alt.Color('life_expectancy')
        ).transform_window(
            rank='rank(life_expectancy)',
            sort=[alt.SortField('life_expectancy', order='descending')]
        ).transform_filter(
            (alt.datum.rank < 10))
    )
    return country.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)