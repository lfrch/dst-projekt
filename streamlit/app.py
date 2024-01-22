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


#Datenübersicht
st.sidebar.title("Übersicht zu den genutzen Daten")
st.sidebar.markdown('''
| Variable  | Bedeutung  |
|--------|--------|
| Location  | Land oder Ländergruppe |
| Indicator   | Spezielle Kategorien, in denen der Datensatz aufgeschlüsselt ist, hier: der durchschnittliche Lohn  |
| Subject | Familienstatus der einzelnen Entitäten    |
| Time | Erhebungsjahr der Daten  |
| Value | Durchschnittliche Anzahl an Arbeitsstunden  |''')



#Keypoints
st.sidebar.markdown("\n")
st.sidebar.markdown("### Fakten rund um das Thema Arbeitsproduktivität")
st.sidebar.markdown("*Stichwort1")
st.sidebar.markdown("*Stichwort2")
st.sidebar.markdown("*Stichwort3")
st.sidebar.markdown("*Stichwort4")
st.sidebar.markdown("*Stichwort5")



# -------------------#
# BODY

#Color Scale
colors = alt.Scale(
    range=['#003f5c','#58508d','#bc5090','#ff6361','#ffa600']
)

st.markdown("## Die Arbeitsproduktivität unseres Unternehmens im Vergleich zu anderen Ländern") 
st.markdown('Betrachtet werden interne Daten des Jahres :orange[**2022**] und reicht zurück bis in das Jahr :blue[**2019**].')

st.markdown("### Die Daten")
st.write("ggf. gejointer Dataframe hier anzeigen lassen?") # je nach Filter für Charts, muss auch nicht ausgegeben werden?


# *********************Balkendiagramm *****************************

st.markdown("#### Gearbeitete Stunden gemessen an einer normalen 5-Tage Woche à 40h")

#Liste zum Filtern 
YEARS = df_selectedlocations.groupby('TIME')['LOCATION'].apply(list).to_dict()
YEAR_SELECTED = st.multiselect('Jahr zur Darstellung auswählen:', list(YEARS.keys()))

# Filter
filtered_df = df_selectedlocations[df_selectedlocations['LOCATION'].isin(YEAR_SELECTED)]

# Gefilterter Dataframe
if YEAR_SELECTED:
    filtered_df = df_selectedlocations[df_selectedlocations['TIME'].isin(YEAR_SELECTED)]
else:
    filtered_df = df_selectedlocations

# Code Barchart filtered
barchart_base = alt.Chart(filtered_df).mark_bar().encode(
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

barchart_labels = alt.Chart(filtered_df).mark_text(baseline='middle', color='black').encode(
    x=alt.X('VALUE'),
    y=alt.Y('LOCATION')  
)

barchart_final = alt.layer(barchart_base,barchart_labels).configure_view(
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

# Show filtered Chart
st.altair_chart(barchart_final, use_container_width=True)

# *********** Histplot *******************

st.markdown("#### Histogramm")
st.markdown("""---""")


# ***********Boxplot: Hours worked to exit poverty, im Verlauf der Jahre 2019-22*******************

st.markdown("#### Benötigte Arbeitsstunden, um nicht in Armut zu leben")

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

st.write("Auswertung noch und und farblich hervorheben + Linechart als Erweiterung, Column Darstellung?")

# ***********Histogramm kombinierte Darstellung*******************

selector = alt.selection_point(fields=['SUBJECT'])

color_scale = alt.Scale(domain=['2 CHILDREN', 'NO CHILDREN'],
                        range=['#58508d','#ff6361'])

base = alt.Chart(df2_selectedlocations).properties(
    width=250,
    height=250
).add_params(selector)

points = base.mark_point(filled=True, size=200).encode(
    x=alt.X('TIME:O').axis(
        title="Jahr",
        labelAngle=0),
    y=alt.Y('mean(VALUE):Q', axis=alt.Axis(title='Mean Value', format='.1f'))
        .scale(domain=[8,16]),
    color=alt.condition(
        selector,
        'SUBJECT:N',
        alt.value('lightgray'),
        scale=color_scale),
)

histogram2 = base.mark_bar(opacity=0.7, thickness=100).encode(
    alt.X('VALUE', title="Stundenanzahl")
        .bin(step=5), # step keeps bin size the same
    alt.Y('count()', title="Häufigkeit")
        .stack(None)
        .scale(domain=[0,15])
        ,
    alt.Color('SUBJECT:N').scale(color_scale)
).transform_filter(
    selector
)

points | histogram2
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

st.write("Peak & Low erklären + Ausblick -> farblich hervorheben")
st.markdown("""---""")

### -------------------###
# END OF APP