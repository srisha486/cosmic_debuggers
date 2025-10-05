import plotly.graph_objects as go
import pandas as pd
import random

# Load NASA ocean dataset
df = pd.read_csv('nasa_ocean_data.csv')

# Sea animal facts per ocean region (images removed)
region_animals = {
    'Atlantic': [
        {
            'animal': "Blue Whale",
            'fact': "The blue whale is the largest animal ever known to have lived on Earth."
        },
        {
            'animal': "Atlantic Puffin",
            'fact': "Atlantic puffins are known for their colorful beaks and can dive up to 60m."
        }
    ],
    'Pacific': [
        {
            'animal': "Green Sea Turtle",
            'fact': "Green sea turtles are herbivores and can live up to 80 years."
        },
        {
            'animal': "Giant Pacific Octopus",
            'fact': "The giant Pacific octopus is the largest octopus species and can change color rapidly."
        }
    ],
    'Indian': [
        {
            'animal': "Dugong",
            'fact': "Dugongs are related to manatees and are sometimes called 'sea cows'."
        },
        {
            'animal': "Whale Shark",
            'fact': "The whale shark is the largest fish in the sea, found in the warm waters of the Indian Ocean."
        }
    ]
}

# Assign a region label for storytelling (customize as needed)
def assign_region(lat, lon):
    if -70 < lon < 20:
        return 'Atlantic'
    elif 100 < lon < 180 or -180 < lon < -100:
        return 'Pacific'
    else:
        return 'Indian'

df['region'] = [assign_region(lat, lon) for lat, lon in zip(df['latitude'], df['longitude'])]

# Shuffle animal facts so every run is different
for region in region_animals:
    random.shuffle(region_animals[region])

# Assign an animal fact per row, cycling through each region's animal list
animal_idx = {'Atlantic': 0, 'Pacific': 0, 'Indian': 0}
animal_list_len = {k: len(v) for k, v in region_animals.items()}

def get_animal_info(region):
    idx = animal_idx[region]
    animal_info = region_animals[region][idx % animal_list_len[region]]
    animal_idx[region] += 1
    return animal_info

df['animal_info'] = [get_animal_info(region) for region in df['region']]

# Build hover text with fun fact (no image)
def build_hover(region, temp, lat, lon, animal_info):
    return (
        f"<b>{region} Ocean</b><br>"
        f"Temperature: {temp}°C<br>"
        f"Location: {lat:.2f}, {lon:.2f}<br><br>"
        f"<b>Sea Animal: {animal_info['animal']}</b><br>"
        f"<i>{animal_info['fact']}</i>"
    )

df['hover'] = [
    build_hover(region, temp, lat, lon, animal_info)
    for region, temp, lat, lon, animal_info in zip(
        df['region'], df['temperature'], df['latitude'], df['longitude'], df['animal_info']
    )
]

# Build interactive globe
fig = go.Figure(go.Scattergeo(
    lon = df['longitude'],
    lat = df['latitude'],
    text = df['hover'],
    marker = dict(
        size = 6,
        color = df['temperature'],
        colorscale = 'Reds',  # Different shades of red for temperature
        colorbar_title = 'Sea Temp (°C)',
        opacity = 0.9,
        line_color = 'deepskyblue'
    ),
    hoverinfo = 'text',
    mode = 'markers',
    name = 'Ocean Data'
))

fig.update_layout(
    title = "🌏 Dive Into Earth's Oceans: Meet the Sea Animals",
    geo = dict(
        projection_type = 'orthographic',
        showland = False,
        showocean = True,
        oceancolor = 'deepskyblue',
        bgcolor = 'black'
    ),
    template = 'plotly_dark',
    margin = dict(l=0, r=0, t=50, b=0)
)

fig.show()
