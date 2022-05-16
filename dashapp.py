import dash, sqlite3
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import model.sql_loader as sl
import model.data as data


app = dash.Dash(__name__, suppress_callback_exceptions=True)

con = sqlite3.connect('ABunchOfTrees.db', check_same_thread=False)
cur = con.cursor()

sl.tableInitialize(cur)
sl.databaseInitialize(cur)
con.commit()

content = html.Div(id="page-content", children=[])

app.layout = html.Div([
	dcc.Location(id="url"),
	content
])

@app.callback(
	Output("page-content", "children"),
	[Input("url", "pathname")])
def render_page_content(pathname):
	if pathname == '/':
		return [dcc.Graph(id='graph', figure=data.real_figure(con))]

if __name__=='__main__':
	app.run_server(debug=True)
con.close()