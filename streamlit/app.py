# -------------------#
# SETUP
import streamlit as st
import pandas as pd
import altair as alt

# -------------------#
# IMPORT DATA

# Pfad zum df angeben
df_selectedlocations = pd.read_csv("/Users/Lea/Desktop/dst-projekt/df_selectedlocations.csv")


### -------------------###
# START OF OUR APP

# -------------------#
# HEADER

# Title of our app
st.title("Data Storytelling Projekt: Dashboard")

# Add image
st.image('unsplash_header.jpg')

# Add header
st.write("Präsentiert von Lea Frech")


# -------------------#
# SIDEBAR


# -------------------#
# BODY

#Color Scale
colors = alt.Scale(
    range=['#003f5c','#58508d','#bc5090','#ff6361','#ffa600']
)

st.markdown("## Die Arbeitsproduktivität unseres Unternehmens im Vergleich zu anderen Ländern") 
st.markdown("Betrachtet werden interne Daten des Jahres **2022** und reicht zurück bis in das Jahr **2019**.") 

# Map Ansicht, um zu zeigen, woher die Daten kommen -> Neuen df erzeugen mit Längen & Breitengrade für GBR und DEU
st.markdown("#### Geographische Übersicht: Karte")


# Balkendiagramm (paar Fakten ergänzen!) -> Filter pro Jahr, als interaktivität
st.markdown("#### Gearbeitete Stunden gemessen an einer normalen 5-Tage Woche à 40h")

barchart = alt.Chart(df_selectedlocations).mark_bar().encode(
        x=alt.X('LOCATION').axis(
            title='Location',
            titleAnchor='start',
            labelAngle=0,
            grid=False,
            labelColor='black',
            tickColor='black'),
        y=alt.Y('VALUE').axis(
            title='Value',
            titleAnchor='end',
            grid=False,
            labelColor='black',
            tickColor='black'),
        color=alt.Color('TIME', scale=colors, legend=None),
        tooltip=['TIME']
    ).properties(
        width=600,
        height=400
    )

st.altair_chart(barchart, use_container_width=True )


# Boxplot: Hours worked to exit poverty, im Verlauf der Jahre 2019-22
st.markdown("#### Boxplot: Benötigte Arbeitsstunden, um nicht in Armut zu leben innerhalb der letzten Jahre")

# Häufigkeitsverteilung:
st.markdown("#### Histogramm")

# Scatterplot
st.markdown("#### Scatterplot")


# Linechart: Productivity Forecast

df3_selectedlocations = pd.read_csv("/Users/Lea/Desktop/dst-projekt/df3_selectedlocations.csv")
europe = pd.read_csv("/Users/Lea/Desktop/dst-projekt/europe_forecast.csv")

st.markdown("#### Wie sich die Arbeitsproduktivität in Zukunft entwickeln wird")

# Code für Chart 
colors_linechart3 = alt.Scale(
    range=['#ffa600','#ff6361',]
)

# *************************************************************

linechart3 = alt.Chart(df3_selectedlocations).mark_line().encode(
    x=alt.X('TIME:O', title='Jahr').axis(
        titleAnchor='start',
        labelAngle= -0,
        ),
    y=alt.Y('VALUE').scale(domain=(0.85,1.15)).axis(
        title='GDP per hour worked',
        titleAnchor='end',
        grid= False,
        ),
    strokeWidth=alt.value(3), 
    color=alt.Color('LOCATION', scale=colors_linechart3),
    tooltip=['LOCATION']
).properties(
    title='Labor Productivity Forecast'
)

# *************************************************************

location_list = df3_selectedlocations['LOCATION'].tolist()

linechart3_labels = alt.Chart(df3_selectedlocations).mark_text(align='left', dx=3).encode(
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
    fontSize=20,
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

### -------------------###
# END OF APP