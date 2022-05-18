import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import Input, Output, html
import model.sql_loader as sl
import model.data as data
import view.GUI as view

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

sl.tableInitialize()
sl.databaseInitialize()
sl.databaseAddCoordinate()

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
			view.navbar(),
			html.Div(
				[
					html.Div(
						[
							html.H1("Projet programmation - CMI L2")
						],
					className='align box margin'),
					html.Div(
						[
							view.lottie('https://assets3.lottiefiles.com/packages/lf20_rc0btai6.json'),
							html.H1("Hamad Tria\nAlexandre Leys")
						],
					className='box align')
				],
			className='page')
		]
	if pathname == '/stats':
		return [
		view.navbar(),
		html.Div(
		[
			html.Div(
				[
					html.H5("Select the desired valley(s) :", className='align'),
					view.button_group(data.get_valley())
				],
				className='box'),
			html.Div(
				[
					dcc.Graph(id='histogram_figure'),
					dcc.Graph(id='error_bar'),
				],
				className='box graphs'),
			html.Div(
				[
					view.list_group()
				],
				className='box variable_selector'),
			dcc.Interval(id='auto_refresh', interval=50, n_intervals=0, max_intervals=9)	
		],
		className='page')]
	elif pathname == '/map':
		return [
		view.navbar(),
		html.Div(
			[
			html.H5("Geographic representation of harvest stations", className='box'),
    		html.Div(
				[
				html.Div(
					[
						html.H5("Select a valley :"),
						view.build_dropdown(data.get_dropdown_values()),
						view.lottie('https://assets6.lottiefiles.com/private_files/lf30_noclpt6t.json'),
						html.Div(
							[
								html.Hr(),
								view.init_figure('timeseries', 'map timeseries')
							],
						className='box map')
					],
					className='data box'),
				html.Div(
					[
						view.init_map(),
						html.Hr(),
						html.Div(id='data_table')
					],
					className='data box map')
				],
				className='box variable_selector')
        	],
			className='page')
		]
	elif pathname == '/data':
		return [
			view.navbar(),
		]
	else:
		return [
			'The page you request does not exist...'
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
		df = data.error_Bar_data(column, 'Josbaig')
		return view.error_Bar_figure(df, column, n_intervals, 'Josbaig'), n_intervals
	hover = hover['points'][0]['x']

	df = data.error_Bar_data(column, hover)

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
	list_valley = data.get_valley()
	df = data.histogram_data(list_valley[value]['label'])
	return view.histogram_figure(df)

@app.callback(
    Output('map', 'figure'),
    Input('dropdown', 'value'))
def update_map(value):
    dff_map = data.get_unique_values_map(value)
    fig = view.build_map(dff_map)
    return fig

@app.callback(
    Output('timeseries', 'figure'),
    Input('map', 'hoverData'))
def update_timeseries(hoverData):
    station_name = hoverData['points'][0]['hovertext']
    sub_df = data.get_groupby_values_df(station_name,'DD','Ntot')
    fig = view.build_timeseries(sub_df, station_name)
    return fig

@app.callback(
    Output('data_table', 'children'),
    Input('map', 'hoverData'))
def data_table(hoverData):
    station_name = hoverData['points'][0]['hovertext']
    sub_df = data.get_groupby_values_df(station_name,'Station',('Altitude', 'SH','VH','H'))
    table = view.build_table(sub_df, station_name)
    return table

if __name__=='__main__':
	app.run_server(debug=True)
sl.get_connexion().close()