import dash, sqlite3
from dash import dcc
import dash_bootstrap_components as dbc
from dash import Input, Output, html
import model.sql_loader as sl
import model.data as data

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

con = sqlite3.connect('ABunchOfTrees.db', check_same_thread=False)
cur = con.cursor()

sl.tableInitialize(cur)
sl.databaseInitialize(cur)
con.commit()

content = html.Div(id="page-content", children=[])

list_group = dbc.ListGroup([
                dbc.ListGroupItem([
					html.Div([
							html.H5("Ntot ~", className="mb-n1"),
							html.Div([
								html.Small("Data sanity : "),
								html.Small("Clean !", className="text-success")
							])
						],
						className="d-flex w-100 justify-content-between"
					),
					html.Hr(style={'margin-top':'1px', 'margin-bottom':'5px'}),
					html.Small("Total quantity of acorns produced.", className="text-center")
					], id='Ntot', action=True, active=True),

				dbc.ListGroupItem([
					html.Div([
							html.H5("Oneacorn ~", className="mb-n1"),
							html.Div([
								html.Small("Data sanity : "),
								html.Small("Clean !", className="text-success")
							])
						],
						className="d-flex w-100 justify-content-between"
					),
					html.Hr(style={'margin-top':'1px', 'margin-bottom':'5px'}),
					html.Small("Average mass of an acorn (g).", className="text-center")
					], id='oneacorn', action=True),

				dbc.ListGroupItem([
					html.Div([
							html.H5("Ntot1 ~", className="mb-n1"),
							html.Div([
								html.Small("Data sanity : "),
								html.Small("Unfinished", className="text-danger")
							])
						],
						className="d-flex w-100 justify-content-between"
					),
					html.Hr(style={'margin-top':'1px', 'margin-bottom':'5px'}),
					html.Small("Total quantity of acorns produced without sprouted fruit and without deteriorated acorns.", className="d-flex align-items-center")
					], id='Ntot1', action=True),

				], horizontal=True, className="mb-0 w-50 p-1")

app.layout = html.Div([
	dcc.Location(id="url"),
	list_group,
	content
])

@app.callback(
	Output("page-content", "children"),
	[Input("url", "pathname")])
def render_page_content(pathname):
	if pathname == '/':
		return [dcc.Graph(id='graph'), 
		dcc.Interval(id='auto_refresh', interval=50, n_intervals=0, max_intervals=9)]

@app.callback(
	Output("graph", "figure"), Output("auto_refresh", "n_intervals"),
	[Input("Ntot", "active"), Input("oneacorn", "active"), Input("Ntot1", "active"),
	Input("auto_refresh", "n_intervals")])
def refresh(nbr1, nbr2, nbr3, nbr_auto):
	ctx = dash.callback_context
	input_id = ctx.triggered[0]["prop_id"].split(".")[0]
	call = 'Ntot' if nbr1 else 'oneacorn' if nbr2 else 'Ntot1' if nbr3 else 'Ntot'
	if input_id == 'auto_refresh':
		return data.call_figure(con, call, nbr_auto), nbr_auto
	return data.call_figure(con, call, 0), 0


@app.callback(
    Output("Ntot", "active"), Output("oneacorn", "active"), Output("Ntot1", "active"),
    [Input("Ntot", "n_clicks"), Input("oneacorn", "n_clicks"), Input("Ntot1", "n_clicks")])
def a(nbr1, nbr2, nbr3):
	ctx = dash.callback_context
	input_id = ctx.triggered[0]["prop_id"].split(".")[0]
	if input_id == 'oneacorn':
		return False, True, False
	elif input_id == 'Ntot1':
		return False, False, True
	return True, False, False

if __name__=='__main__':
	app.run_server(debug=True)
con.close()