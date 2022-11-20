import pandas as pd
import numpy as np
#from jinja2.utils import markupsafe 
#markupsafe.Markup()
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import SelectField

# Read in the data as "df"
df = pd.read_csv("test1-2021.csv")
print("hi")

###frontend
application = app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'
app.static_folder = 'static'

# A Form class for the user to select a player.
class Form(FlaskForm):
    #player = SelectField('Player', choices=["Paolo Banchero", "Chet Holmgren", "Jabari Smith", "Keegan Murray","Jaden Ivey",
                                     #"Bennedict Mathurin","Jonathan Davis", "Tari Eason","Dalen Tery","Jake LaRavia","TyTy Washington Jr.", "Keon Ellis"])
    player = SelectField('Player', list(df['Player']))
    


# Ima be honest, idk what this next line means, I copy and pasted it.
# but you should ready the documentation.
@app.route('/', methods=['GET', 'POST'])
def index():
    form = Form()

    # If the user is making a POST HTTP request (submitting data to be processed)
    if request.method == "POST":
        # Get the player's name
        player = form.player.data
        # Get the player's image
        picture = "static/img/" + player.lower().replace(" ", "").replace(".", "").replace("'", "") + ".png"

        # Get that player's row of stats from the dataframe
        player_row = df[df["player"].str.lower().str.replace(" ", "").str.replace(".", "").str.replace("'", "") == player.lower().replace(" ", "").replace(".", "").replace("'", "")]
        name = player.upper()
        role = df.iloc[0]["role"]

        # Get the 5 stats
        t1 = round(player_row.iloc[0]["onball freq"] * 100, 0) 
        t2 = round(player_row.iloc[0]["score vs pass out"] * 100, 0)
        t3 = round(player_row.iloc[0]["rim prop"] * 100, 0)
        t4 = round(player_row.iloc[0]["%2 ast"], 0)
        t5 = round(player_row.iloc[0]["offcatchdrive freq"] * 100, 0)

        # If the player's stat is less than 20 (on a scale of 1-100), hide the label since it won't
        # fit on the bar chart.
        label1 = "" if t1 <= 20 else t1
        label2 = "" if t2 <= 20 else t2
        label3 = "" if t3 <= 20 else t3
        label4 = "" if t4 <= 20 else t4
        label5 = "" if t5 <= 20 else t5

        # If the player's stat is greater than 80 (on a scale of 1-100), hide the label since it won't
        # fit on the bar chart. 
        label6 = "" if t1 >= 80 else 100-t1
        label7 = "" if t2 >= 80 else 100-t2
        label8 = "" if t3 >= 80 else 100-t3
        label9 = "" if t4 >= 80 else 100-t4
        label10 = "" if t5 >= 80 else 100-t5

        # Send that data to the template. 
        template = open("templates/graphic_template.html").read().format(picture, name, role, 
                                                                        t1 - 1.5, label1,100 - t1  - 1.5, label6,
                                                                        t2 - 1.5, label2,100 - t2  - 1.5, label7,
                                                                        t3 - 1.5, label3,100 - t3  - 1.5, label8,
                                                                        t4 - 1.5, label4,100 - t4  - 1.5, label9,
                                                                        t5 - 1.5, label5,100 - t5  - 1.5, label10

                                                                 )
        return(template)

    return render_template('index_template.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)