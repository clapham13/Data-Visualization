import altair as alt
import pandas as pd
import json
import os

def loadData():
    """
    Load from prof vo's github
    """
    import os
    import urllib.request, json 
    json_data = 'https://raw.githubusercontent.com/hvo/' + \
                'datasets/master/nyc_restaurants_by_cuisine.json'
    with urllib.request.urlopen(json_data) as url:
        data = json.loads(url.read().decode())
        restaurants_df = pd.io.json.json_normalize(data)
    return restaurants_df

data = loadData()

def showViz(data, zip_code):
    color_expression = "(indexof(lower(datum.cuisine),search.term)>=0) \
                         || (highlight._vgsid_==datum._vgsid_)"
    color_condition = alt.ConditionalPredicateValueDef(color_expression, 
                                                       'SteelBlue')
    highlight_selection = alt.selection_single(name='highlight', on='mouseover', 
                                               empty='none')
    search_selection = alt.selection_single(name='search', on='mouseover', 
                                            empty='none', fields=["term"],
                                            bind=alt.VgGenericBinding('input'))

    vizualization = alt.Chart(data) \
        .mark_bar(stroke='Black') \
        .encode(
            alt.X('total:Q', axis=alt.Axis(title='# of Restaurants')),
            alt.Y('cuisine:O', sort=alt.SortField(field='total', op='argmax')),
            alt.ColorValue('LightGrey', condition=color_condition),
            ).properties(
                selection=(highlight_selection + search_selection),
                )
    return vizualization
