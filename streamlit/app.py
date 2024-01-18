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

st.sidebar.title("Übersicht zu relevanten Fakten rund um die Arbeitsproduktivität")


# -------------------#
# BODY

#Color Scale
colors = alt.Scale(
    range=['#003f5c','#58508d','#bc5090','#ff6361','#ffa600']
)

st.markdown("## Die Arbeitsproduktivität unseres Unternehmens im Vergleich zu anderen Ländern") 
st.markdown('Betrachtet werden interne Daten des Jahres :orange[**2022**] und reicht zurück bis in das Jahr :blue[**2019**].')

# Map Ansicht, um zu zeigen, woher die Daten kommen -> Neuen df erzeugen mit Längen & Breitengrade für GBR und DEU
st.markdown("#### Geographische Übersicht: Karte")


# *********************Balkendiagramm *****************************
#paar Fakten ergänzen! -> Filter pro Jahr, als interaktivität

st.markdown("#### Gearbeitete Stunden gemessen an einer normalen 5-Tage Woche à 40h")

#Code für Balkendiagramm
barchart1 = alt.Chart(df_selectedlocations).mark_bar().encode(
    x=alt.X('VALUE', scale=alt.Scale(bins=[0,1000,2000,3000,4000,5000,6000,7000])).axis(
        title='Anzahl Stunden',
        titleAnchor='start',
        grid=False,
        labelColor='black',
        tickColor='grey'),
    y=alt.Y('LOCATION').axis(
        title='Standort',
        titleAnchor='middle',
        titleAngle=-90,
        labelAngle= 0,
        grid=False,
        labelColor='black',
        tickColor='black'),
    color=alt.Color('TIME:O', scale=colors),
    #column=alt.Column('day:N', sort=['Thur','Fri','Sat','Sun'], header=alt.Header(orient='bottom'))  
).properties(
    width=800,
    height=500,
    title=alt.Title(
        "Hours worked",
    )
)

barchart1_labels = alt.Chart(df_selectedlocations).mark_text(baseline='middle', color='black').encode(
    x=alt.X('VALUE'),
    y=alt.Y('LOCATION')  
)

barchart1_final = alt.layer(barchart1,barchart1_labels).configure_view(
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

barchart1_final

st.write('Hier Filter einbauen?')
st.markdown("""---""")


# ***********Boxplot: Hours worked to exit poverty, im Verlauf der Jahre 2019-22*******************

st.markdown("#### Boxplot: Benötigte Arbeitsstunden, um nicht in Armut zu leben innerhalb der letzten Jahre")
st.markdown("""---""")

df2_selectedlocations = pd.read_csv("/Users/Lea/Desktop/dst-projekt/df2_selectedlocations.csv")

colors2 = alt.Scale(
    range=['#58508d','#ff6361','#ffa600']
)

#Code Boxplot
boxplot = alt.Chart(df2_selectedlocations).mark_boxplot(size=80, extent=0.5).encode(
    x=alt.X('SUBJECT').axis(
        title=None,
        labelAngle=0,
        grid=False,
        labelColor='black',
        tickColor='grey'),
    y=alt.Y('VALUE:Q', scale=alt.Scale(bins=[0,2,4,6,8,10,12,14,16,18],domain=(0,20))).axis(
        titleAnchor='start',
        grid=False,
        labelColor='black',
        tickColor='black'),
    color=alt.Color('SUBJECT', scale=colors2, legend=None),
).properties(
    width=800,
    height=500,
    title=alt.Title(
        "Hours needed to exit poverty",
        subtitle="in relation to family status at average wage",
    )
)

boxplot_final = alt.layer(boxplot).configure_view(
    strokeWidth=0
).configure_title(
    fontSize=25,
    anchor='middle',
    fontWeight='bold',
).configure_axis(
    labelFontSize = 11,
    labelFontWeight='bold',
    titleFontSize = 12,
    titleFontWeight= 'normal',
    titleColor='grey'
).configure_text(
    fontWeight='bold',
    fontSize = 12
)

boxplot_final

st.markdown("""---""")

# *********** Histplot *******************

st.markdown("#### Histogramm")
st.markdown("""---""")


# *********** Scatterplot *******************
st.markdown("#### Scatterplot")
st.write("Hier Zusammenhang der gearbeiteten Stunden Wöchentlich und Jährlich zeigen")
st.markdown("""---""")


# ***********Linechart: Productivity Forecast*******************

df3_selectedlocations = pd.read_csv("/Users/Lea/Desktop/dst-projekt/df3_selectedlocations.csv")
europe = pd.read_csv("/Users/Lea/Desktop/dst-projekt/europe_forecast.csv")

st.markdown("#### Wie sich die Arbeitsproduktivität in Zukunft entwickeln wird")

# Code für Chart 
colors_linechart3 = alt.Scale(
    range=['#ffa600','#ff6361',]
)

linechart3 = alt.Chart(df3_selectedlocations).mark_line().encode(
    x=alt.X('TIME:O', title='Jahr').axis(
        titleAnchor='start',
        labelAngle= -0,
        labelColor='black',
        ),
    y=alt.Y('VALUE').scale(domain=(0.85,1.15)).axis(
        title='GDP per hour worked',
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

st.markdown("""---""")

### -------------------###
# END OF APP