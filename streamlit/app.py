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


# Liniendiagramm: Hours worked to exit poverty, im Verlauf der Jahre 2019-22
st.markdown("#### Benötigte Arbeitsstunden, um nicht in Armut zu leben innerhalb der letzten Jahre")

# Häufigkeitsverteilung:
st.markdown("#### Histogramm")

# Scatterplot
st.markdown("#### Scatterplot")



### -------------------###
# END OF APP