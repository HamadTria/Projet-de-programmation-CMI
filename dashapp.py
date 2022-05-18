import dash, sqlite3
from dash import dcc
import dash_bootstrap_components as dbc
from dash import Input, Output, html
import model.sql_loader as sl
import model.data as data
import view.GUI as view

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

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
		return [
			html.Div(
				[
					view.button_group(dbc, html, data.get_valley(con)),
					view.list_group(dbc, html)
				], style={'display':'inline-flex', 'width':'100%', 'justify-content':'center'}),
			html.Div(
				[
					dcc.Graph(id='histogram_figure'),
					dcc.Graph(id='error_bar'), 
				], style={'display':'inline-flex', 'width':'100%', 'justify-content':'center'}),
			dcc.Interval(id='auto_refresh', interval=50, n_intervals=0, max_intervals=9)	
		]

@app.callback(
	Output("error_bar", "figure"),
	Output("auto_refresh", "n_intervals"),
	[Input("Ntot", "active"),
	Input("oneacorn", "active"),
	Input("Ntot1", "active"),
	Input("auto_refresh", "n_intervals"),
	Input("histogram_figure", "hoverData")])
def refresh_error_bar(nbr1, nbr2, nbr3, n_intervals, hover):
	ctx = dash.callback_context
	input_id = ctx.triggered[0]["prop_id"].split(".")[0]
	column = 'Ntot' if nbr1 else 'oneacorn' if nbr2 else 'Ntot1' if nbr3 else 'Ntot'

	if hover is None:
		return {}, n_intervals
	hover = hover['points'][0]['x']

	df = data.error_Bar_data(con, column, hover)

	if input_id == 'auto_refresh':
		return view.error_Bar_figure(df, column, n_intervals, hover), n_intervals
	return view.error_Bar_figure(df, column, 0, hover), 0


@app.callback(
    Output("Ntot", "active"),
	Output("oneacorn", "active"),
	Output("Ntot1", "active"),
    [Input("Ntot", "n_clicks"),
	Input("oneacorn", "n_clicks"),
	Input("Ntot1", "n_clicks")])
def active_setter(nbr1, nbr2, nbr3):
	ctx = dash.callback_context
	input_id = ctx.triggered[0]["prop_id"].split(".")[0]
	if input_id == 'oneacorn':
		return False, True, False
	elif input_id == 'Ntot1':
		return False, False, True
	return True, False, False

@app.callback(
	Output("histogram_figure", "figure"),
	[Input("radios", "value")])
def histogram(value):
	list_valley = data.get_valley(con)
	df = data.histogram_data(con, list_valley[value]['label'])

	return view.histogram_figure(df)

if __name__=='__main__':
	app.run_server(debug=True)
con.close()