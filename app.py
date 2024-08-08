import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc
from dash import html
from dash import Dash, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

df = pd.read_csv("Dininghall_r.csv")

#initial stuff

external_stylesheets = ['dbc.themes.BOOTSTRAP']
app = Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])
server = app.server 

#APP!!!!!

first_card = dbc.Card(
                dbc.CardBody(
                    html.Div([
                        html.H4(id = 'potential_freq'),
                        "weekly takeouts",
                    ]
                    ),
                ),
            )

second_card = dbc.Card(
                dbc.CardBody(
                    html.Div([
                        html.H4(id = 'potential_price'),
                        "willingness to pay",
                    ]
                    ),                
                ),
            )


app.layout = html.Div(
    [
        #nav bar
        dbc.Col([
            #Filter By
            dbc.Row(
                [
                    dbc.Col(
                        [
                        html.H2("Filter By:"),
                        html.Div(
                            [
                            html.H4("Dining Hall:"),
                            dbc.Checklist(
                                id="filter_hall",
                                options=[
                                    {"label": "RVC", "value": "RVC"},
                                    {"label": "BMH", "value": "BMH"},
                                    {"label": "New", "value": "New"},
                                    {"label": "C4", "value": "C4"},
                                ],
                                inline=True,
                                value=["RVC","BMH","New","C4"]
                            ),
                            ],
                        ),
                        html.Div(
                            [
                            html.H4("Mealplan Status:"),
                            dbc.Checklist(
                                id="filter_mealplan",
                                options=[
                                    {"label": "Mealplan", "value": "Yes"},
                                    {"label": "No Mealplan", "value": "No"},
                                ],
                                inline=True,
                                value=["Yes","No", "Missing"]
                            ),
                            ]
                        ),
                        html.Div(
                            [
                            html.H4("Frequency of eating at dining halls (daily basis):"),
                            dbc.Checklist(
                                id="filter_freq",
                                options=[
                                    {"label": "3x", "value": '3'},
                                    {"label": "2x", "value": '2'},
                                    {"label": "1x", "value": '1'},
                                    {"label": "0x", "value": '0'},
                                ],
                                inline=True,
                                value=['3','2','1','0', "Missing"] #Not recognizing 3 2 1 0 for some reason
                            ),
                            ],
                        ),
                        ],
                    ),
                ],
                justify="center",
                ),
            #Key Takeaways
            dbc.Row([
                dbc.Col(
                        [
                        dbc.Row(
                            html.H2("Key Takeaways:"
                                ),
                            ),
                        dbc.Row(
                            [
                            dbc.Card(
                                dbc.CardBody(
                                    html.Div(
                                        [html.H2(id="bringbackid"),
                                        "of students want takeout back"
                                        ]
                                    ),
                                ),
                                ),
                            ],
                            style={
                                "margin-bottom": "5%",
                            },
                            ),
                        dbc.Row(
                            [
                            dbc.Card(
                                dbc.CardBody(
                                    html.Div(
                                        [html.H2(id="numrespondentsid"),
                                        "Student respondents"
                                        ]
                                    ),
                                ),
                                ),
                            ],
                            ),
                        dbc.Row(
                            [
                            dbc.Card(
                                dbc.CardBody(
                                    html.Div(
                                        [html.H2(id="mostfactorid"),
                                        "was the most important takeout factor"     
                                        ]            
                                   ),                                                                                                        ),
                                ),
                            ],
                            style={
                                "margin-top": "5%",
                            },                            
                            ),                                                        
                        ],
                        ),
                ],
                justify="center",
                style={
                    "margin-top": "8%",
                }
            ),
            #opp cost
            dbc.Row([
                    html.Div(
                            [
                                html.H2("Potential takeout revenue:"),
                                dbc.Card(
                                    dbc.CardBody(
                                        html.H2(id = 'potential_rev'),
                                    ),
                                    style={
                                        "margin-bottom": "3%",
                                    }
                                ),
                                "With students potentially averaging",
                                dbc.Row(
                                    [
                                    dbc.Col(first_card, width = 6),
                                    dbc.Col(second_card, width = 6),
                                    ],
                                    style={
                                        "margin-bottom": "3%",
                                        "margin-top": "3%",
                                    }
                                ),
                                html.Small(
                                    "*3000 students, 40 weeks in residence",
                                    className="card-text text-muted",
                                )
                            ]
                        ),
            ],
                justify="center",
                style={
                    "margin-top": "8%",
                }
            )
        ],
        width = {"size": 3},
        style={
            "backgroundColor": "#f1f1f2",
            "position": "fixed",
            "top": 0,
            "left": 0,
            "right": 0,
            "padding": "1.5%",
            "padding-left": "2%",
            "padding-right": "2%",
            "height": "100%"
            },
        ),
        #stuff
        dbc.Col(
            [
            #Header
            dbc.Row(
                dbc.Col(
                    html.Div(
                        html.H1("Dining Hall Takeout Survey")
                            ),
                    width={"size": 12},
                    style={"backgroundColor": "ffffff",
                            "text-align": "center",
                            "padding-bottom": "1.5%",
                            "padding-top": "1.5%",
                            },
                ),
                className="g-0",
                justify="center",
                style={"box-shadow": "0 0 20px 3px #e9e9ee",
                    "textAlign": "center"
                        },
            ),

            #Element row
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            dcc.Graph(
                                id = 'Bring_Back_graph',
                                style={
                                    "height": "25vh",
                                }
                            )
                        ),
                        style={"width": "30%",
                            "box-shadow": "0 0 20px 3px #e9e9ee",
                            "margin-right": "2%",
                            "backgroundColor": "ffffff",
                            "padding": "2%",
                            },
                    ),                    
                    dbc.Col(
                        html.Div(
                            dcc.Graph(
                                id = 'Takeout_Freq_graph',
                                style={
                                    "height": "25vh",
                                }
                            )
                    ),
                        style={"width": "30%",
                            "box-shadow": "0 0 20px 3px #e9e9ee",
                            "backgroundColor": "ffffff",
                            "border-radius": "4%",
                            },
                    ),
                    dbc.Col(
                        html.Div(
                            [dcc.Graph(
                                id = 'Max_Pay_graph',
                                style={
                                    "height": "25vh",
                                }
                            ),
                            html.Div(
                            "Note: No respondents chose the >$15 option",
                            className='text-center',
                            )
                        ]
                    ),
                        style={"width": "30%",
                            "box-shadow": "0 0 20px 3px #e9e9ee",
                            "margin-left": "2%",
                            "backgroundColor": "ffffff",
                            "border-radius": "4%",
                            }, 
                    ),
                ],
            justify="center",
            style={"padding-left": "5%",
                "padding-right": "5%",
                "margin-top": "2%",
                },
            className="h-25",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            dcc.Graph(
                                id = 'Main_Factor_graph',
                                style={
                                    "height": "25vh",
                                }
                            )
                    ),
                        style={"width": "30%",
                            "box-shadow": "0 0 20px 3px #e9e9ee",
                            "margin-right": "2%",
                            "backgroundColor": "ffffff",
                            "border-radius": "4%",
                            },
                    ),
                    dbc.Col(
                        html.Div(
                            dcc.Graph(
                                id = 'Scales_graph',
                                style={
                                    "height": "25vh",
                                }                            
                            )
                    ),
                        style={"width": "30%",
                            "box-shadow": "0 0 20px 3px #e9e9ee",
                            "backgroundColor": "ffffff",
                            "border-radius": "4%",
                            }, 
                    ),
                    dbc.Col(
                        html.Div(
                            dcc.Graph(
                                id = 'Food_Thievery_graph',
                                style={
                                    "height": "25vh",
                                }                            
                            )
                        ),
                        style={"width": "30%",
                            "box-shadow": "0 0 20px 3px #e9e9ee",
                            "margin-left": "2%",
                            "backgroundColor": "ffffff",
                            },
                    ),
                ],
            justify="center",
            style={"padding-left": "5%",
                "padding-right": "5%",
                "margin-top": "2%"
                }
            ),
            dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id = 'Bought_Takeout_graph',
                            style={
                                "height": "25vh",
                            }
                        )
                ),
                    style={"width": "30%",
                           "box-shadow": "0 0 20px 3px #e9e9ee",
                           "margin-right": "2%",
                           "backgroundColor": "ffffff",
                           "border-radius": "4%",
                           },
                ),
                dbc.Col(
                    html.Div(
                        [
                        html.B("Common Grab n Go concerns expressed by respondents who did not want to buy Grab n Go included:"),
                        html.Br(),
                        html.Br(),
                        html.Div(id='num_avail'),
                        html.Div(id='num_price'),
                        html.Div(id='num_qual'),
                        html.Div(id='num_var'),
                        html.Div(id='num_access')
                        ],
                    ),
                    style={"width": "30%",
                           "box-shadow": "0 0 20px 3px #e9e9ee",
                           "backgroundColor": "ffffff",
                           "padding": "2%",
                           },
                ),
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id = 'Delivery_Freq_graph',
                            style={
                                "height": "25vh",
                            }                            
                        )
                ),
                    style={"width": "30%",
                           "box-shadow": "0 0 20px 3px #e9e9ee",
                           "margin-left": "2%",
                           "backgroundColor": "ffffff",
                           "border-radius": "4%",
                           }, 
                ),
            ],
        justify="center",
        style={"padding-left": "5%",
               "padding-right": "5%",
               "margin-top": "2%"
               }
        ),
            ],
        width = {"size": 9,
                 "offset": 3},
        ),
    ],
    style={
        "height": "relative",
    }
)

@app.callback(
    [
     Output('potential_freq', 'children'),
     Output('potential_price', 'children'),
     Output('potential_rev', 'children'),
     Output('bringbackid', 'children'),
     Output('numrespondentsid', 'children'),
     Output('mostfactorid', 'children'),
     Output('Bring_Back_graph', 'figure'),
     Output('Takeout_Freq_graph', 'figure'),
     Output('Max_Pay_graph', 'figure'),
     Output('Main_Factor_graph', 'figure'),
     Output('Scales_graph', 'figure'),
     Output('Food_Thievery_graph', 'figure'),
     Output('Bought_Takeout_graph', 'figure'),
     Output('Delivery_Freq_graph', 'figure'),
     Output('num_avail', 'children'),
     Output('num_price', 'children'),
     Output('num_qual', 'children'),
     Output('num_var', 'children'),
     Output('num_access', 'children'),
     ],
    [
    Input('filter_freq', 'value'),
    Input('filter_mealplan', 'value'),
    Input('filter_hall', 'value'),

    ]
)

def update_charts(filter_freq, filter_mealplan, filter_hall):
    filtered_df = df[df['Eating_Freq'].isin(filter_freq)] #Mealplan filter working fine
    filtered_df = filtered_df[filtered_df['Mealplan'].isin(filter_mealplan)] #Mealplan filter working fine
    filtered_df[['RVC', 'BMH', 'New', 'C4']] = filtered_df[['RVC', 'BMH', 'New', 'C4']].astype(int)
    filtered_df = filtered_df[filtered_df[filter_hall].sum(axis=1) > 0] 
   #filtered_df = df[df['Hall'].str.contains('|'.join(filter_hall))]
    #filtered_df = filtered_df[(filtered_df[filter_hall] == 1).any(axis=1)]

    #Key takeaways
    response_count = len(filtered_df)
    numrespondentsid = filtered_df['Mealplan'].mode().values[0] if not filtered_df.empty else None
    bringbackid = round(filtered_df["Bring_Back"].value_counts()["Yes"]/filtered_df["Bring_Back"].count()*100,3)
    most_factorid = filtered_df["Main_Factor"].value_counts().idxmax()

    #Opp cost
    potential_freq = round(filtered_df["Takeout_Freq"].mean(),2)
    def transform_pay(x):
        if x == 4:
            x = 3
        elif x == 5:
            x = 7.5
        elif x == 10:
            x = 12.5
        return x
    filtered_df["Max_Pay_Edit"] = filtered_df["Max_Pay"].transform(transform_pay)
    potential_price = round(filtered_df["Max_Pay_Edit"].mean(),2)
    potential_rev = int(potential_price * potential_freq * 3000 * 40)

    #Qualitative no takeout
    num_avail = sum(filtered_df["Why_Not_Qualitative"].str.contains("Availability")==True)
    num_qual = sum(filtered_df["Why_Not_Qualitative"].str.contains("Quality")==True)
    num_var = sum(filtered_df["Why_Not_Qualitative"].str.contains("Variety")==True)
    num_access = sum(filtered_df["Why_Not_Qualitative"].str.contains("Accessibility")==True)
    num_price = sum(filtered_df["Why_Not_Qualitative"].str.contains("Price")==True)


    #n = 
    num_bringback = filtered_df["Bring_Back"].count()
    num_takeoutfreq = filtered_df["Takeout_Freq"].count()
    num_maxpay = filtered_df["Max_Pay"].count()
    num_mainfactor = filtered_df["Main_Factor"].count()
    num_scales = (int(filtered_df["Cost_Factor"].count() +
                filtered_df["Speed_Factor"].count() +
                filtered_df["Quality_Factor"].count() +
                filtered_df["Variety_Factor"].count())/4)
    num_foodthievery = filtered_df["Food_Thievery"].count()
    num_boughttakeout = filtered_df["Bought_Takeout"].count()
    num_deliveryfreq = filtered_df["Delivery_Freq"].count()

    #Chart fixes
    labels_takeoutfreq = {0: "0x a week",
                        1: "0-1x a week",
                        2: "2-3x a week",
                        4: "4+x a week"}
    filtered_df["Takeout_Freq"] = filtered_df["Takeout_Freq"].map(labels_takeoutfreq)

    labels_maxpay = {   0: "$0",
                        4: "<$5",
                        5: "$5-$10",
                        10: "$10-$15",
                        15: ">$15"}
    filtered_df["Max_Pay"] = filtered_df["Max_Pay"].map(labels_maxpay)

    filtered_df["Delivery_Freq"] = filtered_df["Delivery_Freq"].map(labels_takeoutfreq) #works dw about it

    labels_mainfactor = {"Schedule": "Eating at convenient times",
                        "Place": "Ability to eat elsewhere",
                        "Speed": "Getting food quickly",
                        "Waste": "Reducing food waste",
    }
    filtered_df["Main_Factor"] = filtered_df["Main_Factor"].map(labels_mainfactor)

    #First row graphs
    Bring_Back_graph = px.pie(
                filtered_df,
                    names = filtered_df["Bring_Back"].value_counts().index,
                    values = filtered_df["Bring_Back"].value_counts().values,
                    labels = filtered_df["Bring_Back"].value_counts().index,
                    title = "Do you think McGill dining halls <br> should offer takeout again?<br>(n=" + str(num_bringback) +")",
                )
    Takeout_Freq_graph = px.pie(
                            filtered_df,
                                names = filtered_df["Takeout_Freq"].value_counts().index,
                                values = filtered_df["Takeout_Freq"].value_counts().values,
                                labels = filtered_df["Takeout_Freq"].value_counts().index, #make lbels work
                                title = "How often would you get takeout <br> if McGill dining halls offered it?<br>(n=" + str(num_takeoutfreq) +")",
                            )
    Max_Pay_graph = px.bar(
        filtered_df,
        x=filtered_df["Max_Pay"].value_counts().index,
        y=filtered_df["Max_Pay"].value_counts().values,
        color = filtered_df["Max_Pay"].value_counts().index.astype(str),
        title = "What's the maximum you'd <br> pay for McGill takeout?<br>(n=" + str(num_maxpay) +")",
        labels = dict(x="Max Price",
                      y = "Count (n)")
        )
    Max_Pay_graph.update_layout(showlegend=False)


    #Second row graphs
    # Main factor
    Main_Factor_graph = px.bar(
    filtered_df,
    x=filtered_df["Main_Factor"].value_counts().index,
    y=filtered_df["Main_Factor"].value_counts().values,
    color = filtered_df["Main_Factor"].value_counts().index,
    title = "Why takeout over dine in?<br>(n=" + str(num_mainfactor)+")",
    labels = dict(x="Main Factor",
                  y = "Count (n)")
    )
    # Likert scales
    filtered_df = filtered_df.rename(
    columns={"Cost_Factor": "Price",
             "Speed_Factor": "Speed",
             "Quality_Factor": "Quality",
             "Variety_Factor": "Variety"}
    )
    vars = ["Price", "Speed", "Quality", "Variety"]
    Scales_graph = make_subplots(rows=1, cols=len(vars))
    for i, var in enumerate(vars):
        Scales_graph.add_trace(
            go.Box(y=filtered_df[var],
            name=var),
            row=1, col=i+1
        )
    Scales_graph.update_traces(
        boxpoints='all',
        jitter=.3,
    )
    Scales_graph.update_layout(
        title = ("How important is each of these <br> takeout factors? <br>(n=" 
                + str(num_takeoutfreq)
                +")")
    )
    #Food thievery
    dff = (filtered_df.groupby(
        ['Food_Thievery_YN', 'Food_Thievery']).size().reset_index(name='Count'))

    Food_Thievery_graph = px.bar(
        dff,
        x = "Food_Thievery_YN",
        y = "Count",
        color = "Food_Thievery",
        barmode = "relative",
        title = "Have you ever taken out food <br> from the dining halls before?<br>(n=" + str(num_foodthievery) +")",
    )

    #Third row
    Bought_Takeout_graph = px.pie(
                            filtered_df,
                                names = filtered_df["Bought_Takeout"].value_counts().index,
                                values = filtered_df["Bought_Takeout"].value_counts().values,
                                labels = filtered_df["Bought_Takeout"].value_counts().index, #make lbels work
                                title = "Have you ever bought <br> current Grab n Go takeout?<br>(n=" + str(num_boughttakeout) +")",
                            )
    Delivery_Freq_graph = px.bar(
        filtered_df,
        x=filtered_df["Delivery_Freq"].value_counts().index,
        y=filtered_df["Delivery_Freq"].value_counts().values,
        color = filtered_df["Delivery_Freq"].value_counts().index.astype(str),
        title = "How many times in a week do you<br>buy takeout from delivery apps?<br>(n=" + str(num_deliveryfreq) +")",
        labels = dict(x="Frequency",
                    y = "Count (n)")
        )
    Delivery_Freq_graph.update_layout(xaxis_type='category') #legend is a little fucky


    return (
        potential_freq,
        potential_price,
        potential_rev,
        f'{bringbackid}%',
        f'{response_count}',
        most_factorid,
        Bring_Back_graph,
        Takeout_Freq_graph,
        Max_Pay_graph,
        Main_Factor_graph,
        Scales_graph,
        Food_Thievery_graph,
        Bought_Takeout_graph,
        Delivery_Freq_graph,
        f'Lack of availability: {num_avail}',
        f'Poor quality: {num_qual}',
        f'Lack of variety: {num_var}',
        f'Poor accessibility: {num_access}',
        f'High price: {num_price}'
        )

if __name__ == '__main__':
    app.run(debug=True)
