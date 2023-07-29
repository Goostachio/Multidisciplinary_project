#complete version, implemented to main.py
import dash
from dash import html, dcc, Input, Output
import pandas as pd
from datetime import datetime, timezone
import dateutil.parser
import requests
import plotly.express as px
import csv
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

def changeFormat(date):
    return dateutil.parser.isoparse(date).astimezone()

def acPaymentCalc(watt): #from 4/5/2023
    if watt >=401:
        return watt*3015
    elif watt>=301:
        return watt*2919
    elif watt>=201:
        return watt*2612
    elif watt>=101:
        return watt*2074
    elif watt>=51:
        return watt*1786
    else:
        return watt*1728

def actualW(humidity):  #hudmidity may change ac's power input
    if (humidity>=40) & (humidity<=60):
        return 40
    elif (humidity>=20) | (humidity<=80):
        return 40*1.25
    else:
        return 40*1.75

def addToday(morning, afternoon, evening):
    tracking = [datetime.today().date(), morning, afternoon, evening]
    with open("/data/usage_tracking.csv", 'a') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the data rows
        csvwriter.writerow(tracking)

        # close file
        csvfile.close()

def update_today(today, morning, afternoon, evening):
    with open("/data/usage_tracking.csv", 'r') as file:
        reader = csv.reader(file)
        time = list(reader)

    # Update the values in the last row
    time[-1] = [today, morning, afternoon, evening]

    # Open the CSV file in write mode and write the updated rows
    with open(today, morning, afternoon, evening, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(time)
        file.close()

def run_Dash():
    #initiate app
    app = dash.Dash(__name__,external_stylesheets=[dbc.themes.CYBORG])
    load_figure_template('Cyborg')

    #used for later
    tick = 0 #live track time in sec
    power_used = 0
    morning = 0  # from 00:00 to 10:59
    afternoon = 0  # from 11:00 to 17:59
    evening = 0  # from 18:00 to 23:59

    # Layout
    app.layout = html.Div(
        style={
            "background-image": "url('/assets/for_ac.jpg')",
            "background-size": "cover",
            "background-repeat": "no-repeat",
            "display": "flex",
            "flex-direction": "column",
            "align-items": "center",
            "height": "100vh",
        },
        children=[
            html.H1("Your AC Statistics", style={"color": "white"}),
            dcc.Interval(id="interval", interval=2000),
            html.Div(
                style={
                    "display": "flex",
                    "flex-direction": "row",
                    "justify-content": "center",
                    "width": "100%",
                },
                children=[
                    html.Div(
                        style={"flex": "1", "margin": "10px"},
                        children=[
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H3(
                                            "Power Used in This Session (kWh)",
                                            className="card-title",
                                            style={"text-align": "center",
                                                   "color": "white"},
                                        ),
                                        html.Div(
                                            id="power-used",
                                            children="0",
                                            className="card-text",
                                            style={"font-size": "36px"},
                                        ),
                                    ]
                                ),
                                color="primary",
                                outline=True,
                            ),
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H3(
                                            "Current Payment This Session (VND)",
                                            className="card-title",
                                            style={"text-align": "center",
                                                   "color": "white"},
                                        ),
                                        html.Div(
                                            id="current-pay",
                                            children="0",
                                            className="card-text",
                                            style={"font-size": "36px"},
                                        ),
                                    ]
                                ),
                                color="success",
                                outline=True,
                            ),
                        ],
                    ),
                    html.Div(
                        style={"flex": "1", "margin": "10px"},
                        children=[
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            "Usage in the Day",
                                            className="card-title",
                                            style={
                                                "font-size": "24px",
                                                "color": "white",
                                                "text-align": "center",
                                            },
                                        ),
                                        dcc.Graph(
                                            id="pie-chart",
                                            figure={},
                                            style={"height": "400px"},
                                        ),
                                    ]
                                ),
                                color="info",
                                outline=True,
                            )
                        ],
                    ),
                ],
            ),
        ],
    )



    # Callback for power used in session
    @app.callback(
        Output('power-used', 'children'),
        Input('interval', 'n_intervals')
    )

    def update_power_used(n_intervals):
        #fetch api from button
        # define API endpoint and key
        url = "	https://io.adafruit.com/api/v2/Multidisciplinary_Project/feeds/button1"
        headers = {"X-AIO-Key": "aio_zdIq64LiUqWjsdEG0yWBsIJY73hS"}
        timeFrame = requests.get(url, headers=headers).json()

        #fetch api of humidity
        url = "https://io.adafruit.com/api/v2/Multidisciplinary_Project/feeds/sensor2"
        headers = {"X-AIO-Key": "aio_zdIq64LiUqWjsdEG0yWBsIJY73hS"}
        response = requests.get(url, headers=headers).json()
        humidity = int(float(response['last_value']))

        global power_used
        if int(timeFrame['last_value']) == 1:
            #track in second, this way will not reset the tick
            global tick
            tick +=1
        else:
            #when end, save payment in a .csv file
            payment = [changeFormat(timeFrame["created_at"]),power_used,acPaymentCalc(power_used)]

            #should be in a seperate func to save in a .csv file but don't work. pls help
            with open("/data/pay.csv", 'a') as csvfile:
                # creating a csv writer object
                csvwriter = csv.writer(csvfile)

                # writing the data rows
                csvwriter.writerow(payment)

                # close file
                csvfile.close()

            tick=0


        power_used += (tick/3600)*(actualW(humidity)/1000)
        return html.H2(f"{power_used:.2f} (kWh)") #in kWs


    # Callback for current pay this month
    @app.callback(
        Output('current-pay', 'children'),
        Input('power-used', 'children')
    )


    def update_current_pay(power_used):
        # fetch api of humidity
        url = "https://io.adafruit.com/api/v2/Multidisciplinary_Project/feeds/sensor2"
        headers = {"X-AIO-Key": "aio_zdIq64LiUqWjsdEG0yWBsIJY73hS"}
        response = requests.get(url, headers=headers).json()
        humidity = int(float(response['last_value']))

        global current_pay
        current_pay = 0
        if power_used:
            power_used = (tick/3600)*(actualW(humidity)/1000)
            current_pay += acPaymentCalc(power_used)

            return html.H2(f"{current_pay:.2f} (VND) ")

        return html.H2("0 (VND)")


    # Callback for pie chart
    @app.callback(
        Output('pie-chart', 'figure'),
        Input('interval', 'n_intervals')
    )

    def update_pie_chart(n_intervals):
        # fetch api from button
        # define API endpoint and key
        url = "	https://io.adafruit.com/api/v2/Multidisciplinary_Project/feeds/button1"
        headers = {"X-AIO-Key": "aio_zdIq64LiUqWjsdEG0yWBsIJY73hS"}
        timeFrame = requests.get(url, headers=headers).json()
        record = changeFormat(timeFrame['created_at'])

        global morning
        global afternoon
        global evening

        data = pd.DataFrame("/data/usage_tracking.csv")

        if timeFrame['last_value'] == "1": #is turned on
            if record != datetime.today().date(): #the date is not today, means has come to the next day
                if record in data['dates'].unique(): #update value if there is already the same date, or make a new one if it don't
                    if (record.hour >= 0) & (record.hour <= 10):
                        morning += 1
                    elif (record.hour >= 11) & (record.hour <= 17):
                        afternoon += 1
                    else:
                        evening += 1

                    update_today(record,morning,afternoon,evening)
                else:
                        # evaluation
                    if (record.hour >= 0) & (record.hour <= 10):
                        morning += 1
                    elif (record.hour >= 11) & (record.hour <= 17):
                        afternoon += 1
                    else:
                        evening += 1
                    addToday(morning,afternoon,evening)
        elif record in data['date'].unique():
            #pull, eval, update
            morning = data.iloc[-1].morning
            afternoon = data.iloc[-1].afternoon
            evening = data.iloc[-1].evening

            if (record.hour >= 0) & (record.hour <= 10):
                morning += 1
            elif (record.hour >= 11) & (record.hour <= 17):
                afternoon += 1
            else:
                evening += 1

            update_today(record, morning, afternoon, evening)
        else:
            if (record.hour >= 0) & (record.hour <= 10):
                    morning += 1
            elif (record.hour >= 11) & (record.hour <= 17):
                afternoon += 1
            else:
                evening += 1

            addToday(morning,afternoon,evening)

        df = pd.DataFrame(data=[["morning",morning],["afternoon",afternoon],["evening",evening]],columns=["Time of the day",'Duration'])
        fig = px.pie(df,values="Duration",names="Time of the day", title="Usage of today")
        return fig

    if __name__ == '__main__':
        app.run_server(debug=True)