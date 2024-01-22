# -------------------#
# SETUP
import streamlit as st
import pandas as pd
import altair as alt

# -------------------#
# IMPORT DATA

# Pfad zum df angeben
df3_selectedlocations = pd.read_csv("/Users/Lea/Desktop/dst-projekt/df3_selectedlocations.csv")
europe = pd.read_csv("/Users/Lea/Desktop/dst-projekt/europe_forecast.csv")

colors_linechart3 = alt.Scale(
    range=['#ffa600','#ff6361',]
)

#Liste zum Filtern 
LOCATIONS = df3_selectedlocations.groupby('LOCATION')['TIME'].apply(list).to_dict()
LOCATIONS_SELECTED = st.multiselect('Wähle eine Region zur Visualisierung aus:', list(LOCATIONS.keys()))

# Filter
filtered_df3 = df3_selectedlocations[df3_selectedlocations['TIME'].isin(LOCATIONS_SELECTED)]

# Gefilterter Dataframe
if LOCATIONS_SELECTED:
    filtered_df3 = df3_selectedlocations[df3_selectedlocations['LOCATION'].isin(LOCATIONS_SELECTED)]
else:
    filtered_df3 = df3_selectedlocations


# Code Linechart
linechart3 = alt.Chart(filtered_df3).mark_line().encode(
    x=alt.X('TIME:O', title='Jahr').axis(
        titleAnchor='start',
        labelAngle= -0,
        labelColor='black',
        ),
    y=alt.Y('VALUE').scale(domain=(0.85,1.15)).axis(
        title='BIP pro gearbeitete Stunde',
        titleAnchor='end',
        grid= False,
        labelColor='black',
        ),
    strokeWidth=alt.value(3), 
    color=alt.Color('LOCATION', scale=colors_linechart3),
    tooltip=['LOCATION']
).properties(
    title='Labor Productivity Forecast'
)

# *************************************************************

location_list = filtered_df3['LOCATION'].tolist()

linechart3_labels = alt.Chart(filtered_df3).mark_text(align='left', dx=3).encode(
    alt.X('TIME:O', aggregate='max'),
    alt.Y('VALUE:Q', aggregate={'argmax': 'VALUE'}),
    alt.Text('LOCATION'),
    alt.Color('LOCATION:N', legend=None, scale=alt.Scale(domain=location_list,type='ordinal')), 
).properties(
    width=800,
    height=500,    
)

# *************************************************************

europe_linechart = alt.Chart(europe).mark_line(strokeDash=[5, 5]).encode(
    x=alt.X('TIME:O'),
    y=alt.Y('VALUE'),
    color=alt.value('black'),
    strokeWidth=alt.value(3)
)

europe_list = europe['LOCATION'].tolist()

europe_line_labels = alt.Chart(europe).mark_text(align='left', dx=3).encode(
    alt.X('TIME:O', aggregate='max'),
    alt.Y('VALUE:Q', aggregate={'argmax': 'VALUE'}),
    alt.Text('LOCATION:N'),
    color=alt.value('black')
).properties(
    width=800,
    height=500,    
)

# *************************************************************
# Final Viz: linechart 3

linechart3_final = alt.layer(linechart3, linechart3_labels, europe_linechart, europe_line_labels).configure_view(
    strokeWidth=0
).configure_title(
    fontSize=25,
    anchor='middle',
    fontWeight='bold',
).configure_axis(
    labelFontSize = 11,
    titleFontSize = 12,
    titleFontWeight= 'normal',
    titleColor='grey'
).configure_text(
    fontWeight='bold',
    fontSize = 12
)

linechart3_final

# ---------------------------------------------
# Add slider with user input
st.subheader("Slider")
st.write("This is a Slider")
x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)