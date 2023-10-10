import plotly.graph_objects as go
import pymongo
import pandas as pd
from PIL import Image

img = Image.open('/home/ec2-user/image.png')
myclient=pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["po_db"]
mycol = mydb["player_count"]

data = []

for x in mycol.find():
    obj={"date":x['date'],"player_count":x['player_count']}
    data.append(obj)

df = pd.DataFrame(data)
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df['date'],
    y=df['player_count'],
    mode='lines',
    name='PO Player Count'))
fig.update_layout(title='PO Player Count',
                  xaxis_title='Dates',
                  yaxis_title='Online Players',
                  xaxis_tickangle=45,
                  showlegend=True,
                  xaxis_tickformat = '%d %M %Y',)
fig.add_layout_image(
    dict(
        source=img,
        xref="x",
        yref="y",
        x=0,
        y=0,
        sizex=2,
        sizey=2,
        sizing="stretch",
        opacity=0.5,
        layer="below")
)

fig.write_html('/home/ec2-user/player-count.html')