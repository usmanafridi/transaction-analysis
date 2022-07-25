import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import numpy as np


df= pd.read_csv("Transactions.csv")

df['Date'] = pd.to_datetime(df['Date'])

df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
# year = [2019, 2020, 2021, 2022]
companies= df["Company"].unique()

app = dash.Dash(__name__, meta_tags = [{"name": "viewport", "content": "width=device-width"}])
server = app.server

# Build the layout
app.layout = html.Div(
	children = [
		# (First row) Header: Logo - Title - Last updated



		html.Div(
			children = [


						html.Div(
					children = [
						
						html.P(
							children = "Select Company: ",
							className = "fix_label",
							style = {
								"color": "white"
							}
						),
						dcc.Dropdown(
							id = "w_countries",
							multi = False,
							searchable = True,
							value = companies[0],
							placeholder = "Select Company",
							options = [{"label": c, "value": c} for c in companies],
							className = "dcc_compon"
						),
						# (Row 2) New cases title
			
					
					],
					className = "create_container three columns"
				),

			
				html.Div(
					children = [
						# Title and subtitle
						html.Div(
							children = [
								html.H3(
									children = "TRANSACTIONS OF COMPANIES",
									style = {
										"margin-bottom": "0",
										"color": "white"
									}
								),
								html.H5(
									children = "A Visual Analysis",
									style = {
										"margin-bottom": "0",
										"color": "white"
									}
								)
							]
						)
					],
					className = "one-half column",
					id = 'title'
				),
			],
			id = "header",
			className = "row flex-display",
			style = {
				"margin-bottom": "25px"
			}
		),
		# (Second row) Cards: Global cases - Global deaths - Global recovered - Global active
		html.Div(
			children = [
				# (Column 1): Global cases
				html.Div(
					children = [
						# Title
						html.H6(
							children = "Total Categories",
							style = {
								"textAlign": "center",
								"color": "white"
							}
						),
						# Total value
						html.P(
							id="cat",
							children = "000",
							style = {
								"textAlign": "center",
								"color": "orange",
								"fontSize": 40
							}
						),

					],
					className = "card_container three columns"
				),
				
				html.Div(
					children = [
						# Title
						html.H6(
							children = "Overall Amount",
							style = {
								"textAlign": "center",
								"color": "white"
							}
						),
						# Total value
						html.P(
							id="amount",
							children = "000",
							style = {
								"textAlign": "center",
								"color": "#dd1e35",
								"fontSize": 40
							}
						),

					],
					className = "card_container three columns"
				),
				
				html.Div(
					children = [
						# Title
						html.H6(
							children = "Unique Transactions",
							style = {
								"textAlign": "center",
								"color": "white"
							}
						),
						# Total recovered
						html.P(
							id="transactions",
							children = "000",
							style = {

								"textAlign": "center",
								"color": "green",
								"fontSize": 40
							}
						),

					],
					className = "card_container three columns"
				),
				# (Column 4): Global active
				html.Div(
					children = [
						# Title
						html.H6(
							children = "Trans Amount (Avg)",
							style = {
								"textAlign": "center",
								"color": "white"
							}
						),
						# Total v
						html.P(
							id="avg_trans",
							children = "000",
							style = {
								"textAlign": "center",
								"color": "#e55467",
								"fontSize": 40
							}
						),

					],
					className = "card_container three columns"
				)
			],
			className = "row flex-display"
		),
		# (Third row): Value boxes - Donut chart - Line & Bars
		html.Div(
			children = [
				# (Column 1) Value boxes

				# (Column 2) Donut chart
				html.Div(
					children = [
						# Donut chart
						dcc.Graph(
							id = "pie_chart",
							config = {
								"displayModeBar": "hover"
							}
						)
					],
					className = "create_container six columns",
				
				),
				# (Columns 3 & 4) Line and bars plot
				html.Div(
					children = [
						dcc.Graph(
							id = "line_chart",
							config = {
								"displayModeBar": "hover"
							}
						)
					],
					className = "create_container six columns"
				)
			],
			className = "row flex-display"
		),

		#Fourth Row
				html.Div(
			children = [
				# (Column 1) Value boxes

				# (Column 2) Donut chart
				html.Div(
					children = [
						# Donut chart
						dcc.Graph(
							id = "pie_chart_2",
							config = {
								"displayModeBar": "hover"
							}
						)
					],
					className = "create_container six columns",
				
				),
				# (Columns 3 & 4) Line and bars plot
				html.Div(
					children = [
						dcc.Graph(
							id = "line_chart_2",
							config = {
								"displayModeBar": "hover"
							}
						)
					],
					className = "create_container six columns"
				)
			],
			className = "row flex-display"
		),

	],
	id = "mainContainer",
	style = {
		"display": "flex",
		"flex-direction": "column"
	}
)

# Build the callbacks

# New confirmed cases value box
@app.callback(
	Output(
		component_id = "cat",
		component_property = "children"
	),

	Output(
		component_id = "amount",
		component_property = "children"
	),

	Output(
		component_id = "transactions",
		component_property = "children"
	),

	Output(
		component_id = "avg_trans",
		component_property = "children"
	),
	Input(
		component_id = "w_countries",
		component_property = "value"
	)
)
def update_confirmed(w_countries):

	df1=df.copy()
	df2= df1[df1["Company"]== w_countries]

	unique_categories= df2.Category.nunique()

	amount_spend= round(df2.Amount.sum(),2)

	unique_trans= df2.Date.nunique()

	df_new= df2.groupby("Date")["Amount"].mean().reset_index()
	df_new_avg= round(df_new["Amount"].sum(), 2)
	



	return unique_categories, amount_spend, unique_trans, df_new_avg

	



# Donut chart
@app.callback(
	Output(
		component_id = "pie_chart",
		component_property = "figure"
	),
	Input(
		component_id = "w_countries",
		component_property = "value"
	)
)
def update_pie_chart(w_countries):
	# Filter the data

	df1=df.copy()
	df2= df1[df1["Company"]== w_countries]
	

	df_expense= df2.groupby("Category")["Expense By Category"].first().reset_index()

	df_total_expense= abs(df_expense["Expense By Category"].sum())

	df_revenue= df2.groupby("Category")["Revenue By Category"].first().reset_index()

	df_total_revenue= abs(df_revenue["Revenue By Category"].sum())
	# List of colors
	colors = ["orange", "#dd1e35", "green", "#e55467"]
	# Build the figure
	fig = {
		"data": [
			go.Pie(
				labels = ["Total Revenue", "Total Expense"],
				values = [df_total_revenue, df_total_expense],
				marker = {
					"colors": colors
				},
				hoverinfo = "label+value+percent",
				textinfo = "label+value",
				hole = 0.7,
				rotation = 0,
				insidetextorientation = "radial"
			)
		],
		"layout": go.Layout(
			title = {
				"text": f"Total Revenue vs Expense in company: {w_countries}",
				"y": 0.93,
				"x": 0.5,
				"xanchor": "center",
				"yanchor": "top"
			},
			titlefont = {
				"color": "white",
				"size": 14
			},
			font = {
				"family": "sans-serif",
				"color": "white",
				"size": 12
			},
			hovermode = "closest",
			paper_bgcolor = "#1f2c56",
			plot_bgcolor = "#1f2c56",
			legend = {
				"orientation": "h",
				"bgcolor": "#1f2c56",
				"xanchor": "center",
				"x": 0.5,
				"y": -0.7
			}
		)
	}
	# Return the figure

	return fig


# Line and bars chart
@app.callback(
	Output(
		component_id = "line_chart",
		component_property = "figure"
	),
	Input(
		component_id = "w_countries",
		component_property = "value"
	)
)
def update_line_chart(w_countries):
	# Filter the data
	
	df1=df.copy()
	df2= df1[df1["Company"]== w_countries]
	df3 = df2.groupby('Date').Amount.sum().reset_index()

	# df3['Max'] = max(df3['Amount'])

	# df3['Mean'] = df3["Amount"].mean()


	# Build the figure
	fig = {
		"data": [

			go.Scatter(
				x = df3["Date"],
				y = df3["Amount"],
				# name = "Rolling avg. of the last 7 days - daily confirmed cases",
				mode = "lines",
				line = {
					"width": 3,
					"color": "#ff00ff"
				},
				hoverinfo = "text",
				hovertemplate = "<b>Date</b>: %{x} <br><b>Transaction Amount</b>: %{y:,.0f}<extra></extra>"
			)
		],
		"layout": go.Layout(
			title = {
				"text": f"Total Transaction Amount Timeline in compnay: {w_countries}",
				"y": 0.93,
				"x": 0.5,
				"xanchor": "center",
				"yanchor": "top"
			},
			titlefont = {
				"color": "white",
				"size": 14
			},
			xaxis = {
				"title": "<b>Date</b>",
				"color": "white",
				"showline": True,
				"showgrid": True,
				"showticklabels": True,
				"linecolor": "white",
				"linewidth": 1,
				"ticks": "outside",
				"tickfont": {
					"family": "Aerial",
					"color": "white",
					"size": 12
				}
			},
			yaxis = {
				"title": "<b>Total Amount</b>",
				"color": "white",
				"showline": True,
				"showgrid": True,
				"showticklabels": True,
				"linecolor": "white",
				"linewidth": 1,
				"ticks": "outside",
				"tickfont": {
					"family": "Aerial",
					"color": "white",
					"size": 12
				}
			},
			font = {
				"family": "sans-serif",
				"color": "white",
				"size": 12
			},
			hovermode = "closest",
			paper_bgcolor = "#1f2c56",
			plot_bgcolor = "#1f2c56",
			legend = {
				"orientation": "h",
				"bgcolor": "#1f2c56",
				"xanchor": "center",
				"x": 0.5,
				"y": -0.7
			}
		)
	}
	# Return the figure
	return fig


@app.callback(
	Output(
		component_id = "line_chart_2",
		component_property = "figure"
	),
	Input(
		component_id = "w_countries",
		component_property = "value"
	)
)
def update_line_chart(w_countries):
	# Filter the data
	
	df1=df.copy()
	df2= df1[df1["Company"]== w_countries]
	

	df_revenue= df2.groupby("Category")["Revenue By Category"].first().reset_index()
	df_revenue_sort= df_revenue.sort_values(['Revenue By Category'], ascending=False)

	df_revenue_sort_20= df_revenue_sort.head(20)


	# Build the figure
	fig = {
		"data": [

			go.Bar(
				x = df_revenue_sort_20["Category"],
				y = df_revenue_sort_20["Revenue By Category"],
			
				marker=dict(color='orange'),
				# mode = "lines",
				# line = {
				# 	"width": 3,
				# 	"color": "#ff00ff"
				# },
				hoverinfo = "text",
				hovertemplate = "<b>Category</b>: %{x} <br><b>Revenue Generated</b>: %{y:,.0f}<extra></extra>"
			)
		],
		"layout": go.Layout(
			title = {
				"text": f"Top 20 Categories by Revenue in company: {w_countries}",
				"y": 0.93,
				"x": 0.5,
				"xanchor": "center",
				"yanchor": "top"
			},
			titlefont = {
				"color": "white",
				"size": 14
			},
			xaxis = {
				
				"color": "white",
				"showline": True,
				"showgrid": True,
				"showticklabels": True,
				"linecolor": "white",
				"linewidth": 1,
				"ticks": "outside",
				"tickfont": {
					"family": "Aerial",
					"color": "white",
					"size": 9
				}
			},
			yaxis = {
				"title": "<b>Revenue Generated</b>",
				"color": "white",
				"showline": True,
				"showgrid": True,
				"showticklabels": True,
				"linecolor": "white",
				"linewidth": 1,
				"ticks": "outside",
				"tickfont": {
					"family": "Aerial",
					"color": "white",
					"size": 9
				}
			},
			font = {
				"family": "sans-serif",
				"color": "white",
				"size": 11
			},
			hovermode = "closest",
			paper_bgcolor = "#1f2c56",
			plot_bgcolor = "#1f2c56",
			legend = {
				"orientation": "h",
				"bgcolor": "#1f2c56",
				"xanchor": "center",
				"x": 0.5,
				"y": -0.7
			}
		)
	}
	# Return the figure
	
	return fig



@app.callback(
	Output(
		component_id = "pie_chart_2",
		component_property = "figure"
	),
	Input(
		component_id = "w_countries",
		component_property = "value"
	)
)

def update_line_chart(w_countries):
	# Filter the data
	
	df1=df.copy()
	df2= df1[df1["Company"]== w_countries]
	
	df_expense= df.groupby("Category")["Expense By Category"].first().reset_index()
	df_expense_sort= df_expense.sort_values(['Expense By Category'], ascending=True)

	df_expense_sort_20= df_expense_sort.head(20)


	# Build the figure
	fig = {
		"data": [

			go.Bar(
				x = df_expense_sort_20["Category"],
				y = df_expense_sort_20["Expense By Category"],
				# name = "Rolling avg. of the last 7 days - daily confirmed cases",
				marker=dict(color='orange'),
				# mode = "lines",
				# line = {
				# 	"width": 3,
				# 	"color": "#ff00ff"
				# },
				hoverinfo = "text",
				hovertemplate = "<b>Category</b>: %{x} <br><b>Expense</b>: %{y:,.0f}<extra></extra>"
			)
		],
		"layout": go.Layout(
			title = {
				"text": f"Top 20 Categories by Expenses in company: {w_countries}",
				"y": 0.93,
				"x": 0.5,
				"xanchor": "center",
				"yanchor": "top"
			},
			titlefont = {
				"color": "white",
				"size": 14
			},
			xaxis = {
				
				"color": "white",
				"showline": True,
				"showgrid": True,
				"showticklabels": True,
				"linecolor": "white",
				"linewidth": 1,
				"ticks": "outside",
				"tickfont": {
					"family": "Aerial",
					"color": "white",
					"size": 9
				}
			},
			yaxis = {
				"title": "<b>Expenses</b>",
				"color": "white",
				"showline": True,
				"showgrid": True,
				"showticklabels": True,
				"linecolor": "white",
				"linewidth": 1,
				"ticks": "outside",
				"tickfont": {
					"family": "Aerial",
					"color": "white",
					"size": 9
				}
			},
			font = {
				"family": "sans-serif",
				"color": "white",
				"size": 11
			},
			hovermode = "closest",
			paper_bgcolor = "#1f2c56",
			plot_bgcolor = "#1f2c56",
			legend = {
				"orientation": "h",
				"bgcolor": "#1f2c56",
				"xanchor": "center",
				"x": 0.5,
				"y": -0.7
			}
		)
	}
	# Return the figure
	return fig



# Run the app
if __name__ == "__main__":
  app.run_server(debug = True)
