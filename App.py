from dash import Dash
from dash import dcc
from dash import html
from dash import Input
from dash import Output
import dash_daq as daq 
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('Instagram_Acc_Data.csv',header = 0)
X = df.drop(columns='fake')
y = df['fake']
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.20,random_state=0,stratify=y)
clf = RandomForestClassifier(random_state=1)
clf.fit(X_train,y_train)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = Dash(__name__, external_stylesheets=external_stylesheets,suppress_callback_exceptions=True)
server = app.server
app.title = "Instagram Account Detector"
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🎭" ,className="header-emoji"),
                html.H1(
                    children="Instagram Account Detector", className="header-title"
                ),
                html.P(
                    children="Input the value of each variables"
                    " to generate the authenticity of the account" 
                    " from Instagram  " ,
            className="header-description",
        ),
        ],
            className="header",
        ),

        # input each feature (profile pic, url, num/length username, posts, follows, followers)
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Existence of Profile Picture 🖼️", className="menu-title"),
                        dcc.Dropdown(
                            id="profile",
                            options=[
                                {'label': 'Yes😊', 'value': 1},
                                {'label': 'No😨', 'value': 0},
                            ],
                            placeholder="Choose an option",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Existence of External URL 🔗", className="menu-title"),
                        dcc.Dropdown(
                            id="url",
                            options=[
                                {'label': 'Yes😊', 'value': 1},
                                {'label': 'No😨', 'value': 0},
                            ],
                            placeholder="Choose an option",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Numbers/Username Length 📏", className="menu-title"),
                        html.Div(
                            dcc.Input(id="nlu", type="number",
                            style={'height': '42px', 'width': '200px','font-size': '15px'}, placeholder="0.00~1.00",min=0.00, max=1.00,step=0.01,),
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Numbers of Posts 📮", className="menu-title"),
                        html.Div(
                            dcc.Input(id="po", type="number",
                            style={'height': '42px', 'width': '200px','font-size': '15px'}, placeholder="0~1000",min=0, max=1000,step=1,),
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Number of Follows 👣", className="menu-title"),
                        html.Div(
                            dcc.Input(id="flw", type="number",
                            style={'height': '42px', 'width': '200px','font-size': '15px'}, placeholder="0~7500",min=0, max=7500,step=1,),
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Number of Followers 👪", className="menu-title"),
                        html.Div(
                            dcc.Input(id="flwer", type="number",
                            style={'height': '42px', 'width': '200px','font-size': '15px'}, placeholder="0~10000",min=0, max=10000,step=1,),
                            className="dropdown",
                        ),
                    ]
                ),            
            ],
            className="menu",
        ),

        # input description length
        html.Div(
            children=[
                html.Div(children="Description Length (Characters) 🤔", className="dl-title"),
                html.H5(".", style={'color': 'white'}),
                html.Div([
                    daq.Slider(
                    id = 'dl',
                    min=0,
                    max=150,
                    value=0,
                    handleLabel={"showCurrentValue": True,"label": " "},
                    step=1,
                    size=1000,
                ),
                    html.Div(id='slider-output-container')
                ])
            ],
            className="slider-class",
        ),

        # output
        html.Div(
            children=[
                html.Div(children="Result: ", className="result-title"),
                html.Div([
                html.Div(id='result')
                ])
            ],
            className="wrapper",
        ),
    ],
)

@app.callback(
    Output('slider-output-container', 'children'),
    Input('dl', 'value')
    )
    
def update_output(value):
    return html.Div(['The Description Length in characters of the account is "{}"'.format(value)],style={'font-size': '18px', 'color': 'grey', 'text-align': 'left'})

@app.callback(
    Output('result', 'children'),
    [Input(component_id='profile', component_property='value'),
    Input('nlu', 'value'),
    Input('dl', 'value'),
    Input('url', 'value'),
    Input('po', 'value'),
    Input('flw', 'value'),
    Input('flwer', 'value'),
    ])

def cond(profile,nlu,dl,url,po,flw,flwer):
    if not any(pd.isnull(np.array([profile,nlu,dl,url,po,flw,flwer]))):
        if (clf.predict(np.array([[profile,nlu,dl,url,po,flw,flwer]]))==1):
            return html.Div([html.Div("Hah! It is Fake 🚫",style={'font-size': '25px', 'color': 'grey', 'text-align': 'left'}),html.Img(src='data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxISEhISEBIWEhAQEBUPEA8SEhAPDw8PFRUWFhUSFRUYHSggGBolGxUVITEhJSkrLi4uFx8zODMtNygtLisBCgoKDg0OGhAQGi0dHR0tLS0rLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLTcrNystNy0rLf/AABEIAOEA4QMBIgACEQEDEQH/xAAcAAABBQEBAQAAAAAAAAAAAAAAAQIEBQYDBwj/xAAwEAACAQMDAwIFBAMAAwAAAAAAAQIDBBEFITEGEkFRYRMiMkJxFIGRoRVSwRax8P/EABoBAAIDAQEAAAAAAAAAAAAAAAECAAMEBQb/xAAfEQEBAAMAAwEBAQEAAAAAAAAAAQIDERIhMQQTQVH/2gAMAwEAAhEDEQA/ANQGRAOutNlIIyFcRYIiHJEO+1GFJbvcjaxqypLC5MNqGozqvnbJVnvmMPjj1O1PXpVG1HOCsUG3vl/kKFAlKJyd/wCny+L8NTl8JD1FCsEYMtlyaZhIMCNDxJCez3GI1aCH6Rd/DmvRsKqIsluvyadGfKo2YTj06yrd0U16EjJTdP1s01+C1hI72nLsYMsXZANQqZphZSgCYAMB8ZDACFdO4O45jg9ocdEKc0PQ/U6UEJgUW0egBcABEYGAFYhFfqeoqlF+pKua3bFv0MB1FqDk2u7YTPKTEUS/vZVZt529BKFPBFpVYxWWxktUiuDifozytaNcWyF7ijlqTlsgSqP7v7Md61SrmUjnO4iuWVStJvmR2hp3+zyCQOpbvo+o136GxsY/kfCzivAZE65yv0yHWutye6MPREK4hHKLMJ7LnfTa9M1G4L8Gjpme6WpYgvwaCJ2/zfHOz+uqmx8GM29R8Tb0h4CRY7IOnIAuAwMgwKhQwQAPQ1SHJj/4E+lFiGASFhunAJgBgRW0Rq19CPLMhqvU/dlU1+5QzuKlTeTa/c52z9Enxdjha0nU2v8AyuNPcwNxXqzfBc06Hq8/k7qlgwbf1Xi2aWbVnVkdKOnT8miwKjDlt6vx18UcNMqLg7qzq+pboVMW5G8aqf01b1EkqyLlMRvPAPIfDqjnUrIjyuK3uaRL1BwXoGZjMGVqXFQj06snJZZrpUY+iI89Pg/BZjnJS54LLQ/idqUZf2XEKFx4aZj1QnB5hJ4RMtdarU8Zy0dHTukjFnrsahq5jvyOp6hXjzHP8nHT+qoyWJ7MvrXUKc1s0bcN0yU3Gqpa5OP1Q/ok0OoYv6k0WXw4y8JjJabSf2o0Y2F5SUtUpy849iXCtF8MrKmhU3xlHGpo8o/RN7DeSLyLOmCgpyrw91/6J1O/eykseoLeosUh+CNTrJ8EgMtNw4BEKMAAAIDyOnRSOqgh3aOcTyX9LXXmuQxIVxHdoNi+VPMZDO0d2i4FEQ1oaOqDR8RAIBQ+KScLFi9w0QniJQyIBPEOBobKmmPQMaWxXcUOraLwNhWqU90ThOwabcsaS65UzTOqHHCqGt03WadVbPcwVW1T5RGpVZ0XmLeDZp/XZ9UZ6HrQqRlen+oI1MRk9/c1NKomsrg6erdMme48dYJegjoxf2gqg7uZf0CKglwh+w3uYqYYBchkawH6HDsgNAiceWbnVHLtZ1ieNdqFGtDhGBOBAgQIImzGD5ITtGhSIEAkiBSgRK95GPuRVqLk9uA8pfJagc6dRY3F+Ig+6broDG9wuSdEAIgDBKMqQydAwDv/AAqBUTptTjthm36c1qM4qLe5ib+WzK6x1GVJ5S/g1fn23Gsm7D/j2mEs8D4yMVoXU6liM3j22NbSrKSyjr6tvYyWcSxUNTOkUaYAwIxWJ2hoDIBsAEeXvgIA+BUeRdsojFEYEIKIAUJgRodgSSD0vDGyBqF52rC5Jdw3jYo50m22/A04TKiEHL5pcDalyuIoS4rZXaiXp2n8N/wWelXtDoqrN+UduypDltl4oJcIbKmpcgth8ZUezrOS35JSQkaeOB0RMp6WiLHCZFJELjYTI5PYbgMgVxrUclVeUlHhF1JEavb5B3lV3H0oKUpxmpLbD/B6d07fucUjAajDEeDRdFV28ZZ0Pz7PcYtuHK9FpM7RI1GRIR2td7FJ4khUwaHK5gP7RQeh68tfAqGsU8g7PfZRRoAG+i4DAg4gRzkILIbkZBNFPqU+1beS4yQbu07xoFiBp9n37v8AYu6cO0ZbUe1YOwbkHiRoIxHCA6PAGAAnRILgAQyAEAC9QNgAA6HEe5oqSY3RZunUST8neSIs9pp+5bqy5kz7cex6dZ1e5JliUOg1MwT/AAXx3/z5djFZwvcKMbENPVdrp3gMwIHlR5kAC4PHu6QAAidgDIYFwRPRrQjQq5H5GhXPAYH5Q3O5C01gKAZfSd9GiiDarwgcDyPyGSDTr5eCZFk4nkcAIA0wAARLEAAwyAvS4I1ySe0hajUwhsfqvO9anpK4bSRtMnnnRtXdG7lVS5fJ3PyX0wbHdiI50p54OjNyl0wvUDlgUbyR5oGRi2HJe55DjudKxAEbAU4MnGdbAx3cfUg9dznWzjY5/rIeGdo1U1yWQOoEbuSe5LpVMkW+oZ45IVncuMsMlL1dobVeBKdTKz6hMkiW+kD9a+/tfHqd72tiJWapLteUV07mTW72HmKu5LSwl3NtlxS4M/pVZJ7l7TmsbE8aMyjugGKYqYqyWHMRAhQUTZ8EW5uOxZwSZsjVsPxlhkV5ZIj1nHKI1xfKZx1VtL6Hj1IFspPhF2OtRlnGr6cvexpLk21tUnUxkxPSmn9805ePB6XZ2ySWEdT8zHnfaRb0sI6gIkb1ZwgYAgvNMAhvcOyeUdzpGJMdgSUUTgdcJUU+TjOyiyUh2Cew7FZLTPRkb4dSOyexeYGuKHhMlL+snHlZIcqycs8F/XjDBnbumpS+XwHGey9XtpUTjsyRkobeNSCO6v5L6lsxgtddSod5Ahpbk0osn1L6GOS10G6ox+aWMrdfksxnVGVQY9KThHvnLC5x5IyvFGXYsPDxkb1brlWrPtg2oLbCMzThPOd+eS7LD0rmVlbiEtjqmVGm3EnFdxZRqryzLlONGFd0xGxnx4+onx4+pXzq2Zn1Gd9DjCVT5/pIFassbMq6l1NZ7Xgu1zlVbL/xper9UtIx7I47vYzNjWi1lFdLT51Jd0pclrZWEYrCe5ouUZb1rOkMNm8gsHkNndzoPMXwWVv1nNZ7vO3Jdo3cvCZYvS51EuXsQrnVoR2juzL6Xc1LnLbaWfXwX9lpcVhvc6WGfVfOOf8AlZ/6gWv6aPov4FLR68ooX+eSZCuvUuNI0qlVguO7+zrU6TTe0meXmPXW6pVP3FciZU6UqJ/LLYjz6frrgb+Y+TnkXIlTRbhLhlTqdKvRXzJg/mHVq6i9SNdalCCznPsZapqE35I9Sq5csaYcC1paFwq8lGOzZotN6Wi3lvf9zB6Nc9lRM9R0S+jNLD38/wAB8QNu9Aio7eDNXlrHdYzg9DlR71zj/pwWjQzl7jeKcjyi70qcvoi8HKlpFzH7Xg9mpWUEvpX8I6qhDzFfwNzhLr68VrVHHaUN17Dad5F7Y3PS+odMpSz2xWX7GNXTk4y71HZPjA/2K8sJHKxsalT6VhGksumMrMyToVzH6XDDWxo1NJC3DpscVB/4tBo4VelqSX1f2R+qOrVSbjB5aMLc9UVpPOXj0yGaoTPPjd0+m6Od5FhDp6gvR+5idJ6hi8KpJlzdavSSzCpv+Rpr4r/pF3eaBRUG1z7GJ1mg6TfY3nJd6Jr/AMSTg3tnHJoHolOfzPfyS4jLK8ztu+b+bJPdhHGfQv8AXdMjSy48FWp5gyv3KNx9LfpCu1JR8HoFBHnXScH3r8npFulg6P5slWc4fkB+AOh5K+PP+mLhcZ4NjE8306r2VF4PQrKt3QX4PNYR1Hc6RRzHRHQ9xXoZbra3Tp+6RqkV2t2anTlnfZh4eYvDJRGtE3V6HZUklxnYggoUiZpOltXcJpN7GcyEJtPK5IV7jp+oQkst8k2V9TXMkjxrTdaqpqOTX6fbuthup+VkaB1r5axRX3ESfUFJeThR6ep/c8k2lotFLjI8HqHPXqL5X9HWlqtCSxwT/wDD0v8AVHKehU34x/AxbOudvGg3mOMsl3NDMGlz4ONLSYQ3RY04LG4OjMXjHVuj1Y1JTcW02ZSosH0Tf6dCrFqSMD1D0It508+uFgMZ9uHXmDYqk/8A7Jbz0Ct3dvY+ecF7o3RFSck5pqP7DdZf5ZOfR2nzbUsPnJ6Iqk6ccpZ9jppeiRoxSXKO97XUE2yfV2GNjFdS6vUeU4bGZo3s2+3D3NDrFedebjTjn3wXvT3TWEnUW/4QJrtPlk5dLVYwx37e7NjRvKb4kn+5yqaNTlFLGMehBn0/h5ptr9zfpw4z5Xq774+q/kCi/wAXV/2Yps6TrC3DxujWdP6inFJvcyEayktjvZXTpvPg8zjXVvp6VGWUORW6Veqced8cFkh0hykNrTjhp+UEuCuu7ac+GPFjzTrG3SqZXlmd+E/Q9P17p9yh3PlGbs6UY7SjxsJkknWTdN+UMaNveaVGcdlj8GdudLks7ZwL5w903nYqUy10rV5U5Ld4INa1lHlYOShkeVnuNj0/SuqYywpS/k1tlcxmsp5PGtK0qUns2jQq+nQ2TzgaUlvHp6mhcmGserFsp/yXVDqWi/uQbejMl7IdFlTHWKL+9fyc7jW6cV8r7mHHG1LskW1S4jHliQuoP7kY25q17jKhmKZ0tNJuY/dkvx1KstrVOhT5xH1GyuacPuSwUy0m4fMsDqHTkm/mkNNVVXY63+uxSxB5fsVMLatcSXdntyaG10CEXl7ltChFLZFuH5/ZbtqrsdFhT3wslkonYQ2Y6pFFytNQ5IAG8YHSgIBOROvG5WT+14INZ1IPfg0fwX6HKrRzyjy0ydjKImia58N4kbzTtYhNLc8+raan7DrelVpfRIfyJ8epKeeBYyxuefUuoasNpZeOSwp9W5xlP32LZnDdaW8vov5X59jIaxpkoy74r5XuLqGtxlutiXpmtUprsqPPga8qeXFRbXv2yRJ7UyVe6LCTbpP3RWysq0PGSnLBq1bpPVF5YRlF7Gao6e/iJcLJpmquy7Sbp+iOT75LHkXDGyn354WehKmqVJSSWcGc/Vqcnnfc0PUs4xh25G9M6PRlu3ls0YTrlbclTSsJVfojyXeldIN7zybOz06nBfKkS0scG3Xo77ZrtZyl0nSXqWFvoFKPjJaiZNWOmQtzptG2gvpSR2whgpdMIHlTxrQJh3E4HeljFjsMb3gphDp2AFbEGNIAAAksABkA+NBg6pX1v+igeSdzL4izHIADVV+ONQjVAAaFR7jg4Wf1gBdgFbnSOEWVbwADwP8AXNEz7f2YAL/q3L5GG6j8/kldJ/8ARQLNf1i2vRKH0r8D5cgB1dfxjv0IcwAtP/hUCEAsiFGsUCq/UhAQoACuo0ALMTwAwAeFy+kAAGB//9k=')])
        else:
            return html.Div([html.Div("Congrats! It is Reallllllll ✔️",style={'font-size': '25px', 'color': 'grey', 'text-align': 'left'}),html.Img(src='https://media.tenor.com/5fJmkcdVPgYAAAAC/tom-and-jerry-jerry.gif')])

if __name__=="__main__":
    app.run_server(debug=True)