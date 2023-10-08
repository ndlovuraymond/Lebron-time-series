import pandas as pd
from sklearn import metrics
import plotly.express as px
from statsmodels.tsa.arima.model import ARIMA
from dash import Dash, dcc, html, callback, Output, Input
import numpy as np

lebron_reg_url = "https://raw.githubusercontent.com/ndlovuraymond/Lebron-vs-Jordan/main/data/lebron_career.csv"
lebron_stats = pd.read_csv(lebron_reg_url,parse_dates=["date"])
lebron_stats["Year"] = lebron_stats.date.dt.year
lebron_stats["Month"] = lebron_stats.date.dt.month

app = Dash(__name__)
server = app.server

years = lebron_stats.Year.unique()
np.delete(years, 0)

app.layout = html.Div(children=[
    html.H1(children='Lebron Statistics'),
    dcc.Dropdown(years,2011,id="dropdown"),
    dcc.Graph(
        id="graph")
])

@callback(
    Output('graph', 'figure'),
    Input('dropdown', 'value')
)
def update_graph(value):
    forecast_csv = f"https://raw.githubusercontent.com/ndlovuraymond/Lebron-vs-Jordan/main/data/forecast{value}.csv"
    forecast_df = pd.read_csv(forecast_csv)
    forecast_df.set_index("date",inplace=True)
    
    fig = px.line(lebron_stats.query(f"Year == {value} and Month < 6"),x="date",y="pts",
        labels={"pts":"Points Per Game"},title="Points Per Game").update_layout(
        paper_bgcolor="white",plot_bgcolor="white",title={"x":.5,"y":.85,"font":{"size":30}}
        ).update_yaxes(
        gridcolor="black")
    
    fig.add_scatter(x=forecast_df.index,y=forecast_df["pts"],mode="lines")
    
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
