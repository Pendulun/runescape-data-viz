import streamlit as st
import requests

st.set_page_config(page_title="Runescape items visualizer")

st.title("Runescape item's prices visualizer")
st.write("This is a personal project intended to practice to create an API,"\
         " develop an user interface for the API and apply machine learning"\
            " forecast models to predict future item's prices.")
github_url = "https://github.com/Pendulun"
linkedin_url = "https://www.linkedin.com/in/souzacamposdaniel/"
st.write(
    f"Created by Daniel Souza de Campos. Reach me on [LinkedIn]({linkedin_url}) and see other projects on my [Github]({github_url})"
)

st.header("Context", divider=True)
runescape_url = "https://www.runescape.com/l=3/splash"
guinnes_url = "https://www.guinnessworldrecords.com/world-records/105537-most-users-of-an-mmo-videogame"
st.write(f"[Runescape]({runescape_url}) is a 20+ years old MMORPG game that was"\
         f" considered in 2017 to have [the most users of an MMO videogame]({guinnes_url})."\
        " Besides all the quests you can do and fun you can have with it, there is a"\
        " very important place in it called Grand Exchange Market. As players can"\
        " craft items inside the game, they can sell it as well in the market." \
        " Then, other players might buy it for many reasons. It really resembles"\
        " a real market where prices are defined/suggested based on supply and demand.")
ge_official_url="https://secure.runescape.com/m=itemdb_rs/"
st.write("As this is a very common way, if not the main, to make ingame money,"\
         " it is likely that one should watch the prices for items it want to buy or"\
        f" sell. Althougt there is already a [official website]({ge_official_url}) "\
            "for the Grand Exchange Market, I wanted to give it a go and add "\
                "a price forecast model to it. For fun. And as a portifolio project.")

st.header("About the API", divider=True)
st.subheader("Which API?")
grand_exchange_api = "https://runescape.wiki/w/Application_programming_interface#Grand_Exchange_Database_API"
st.write(
    "The API that this app uses is a wrapper of the [Grand Exchange Database API](%s)(GEDA)"
    % grand_exchange_api)
st.subheader("Why a wrapper?")
st.markdown(
    "I felt that the GEDA has some non user friendly routes. For example, if we" \
    " wanted to get all items for one category, we would have to:"\
    "\n1. Know the category ID (which is harder to know than the category name)" \
    "\n2. For a character, request the first 12 items that start with that character in the category" \
    "\n3. Repeat step 2 until there are no items left for the category starting with the letter" \
    "\n4. Repeat step 2 and 3 for every character."
)
st.write("The wrapper API does all of this in one route. Another example would "\
         "be getting an item summary info and historical prices. You would have to"\
        " know the item's ID. Using this app, you can find the item searching for its"\
        " category without having to remember its ID.")