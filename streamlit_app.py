# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# st.text(fruityvice_response.json())

# Write directly to the app
st.title(":cup_with_straw: Custom smoothie form Streamlit App :cup_with_straw:")
st.write(
    """Choose the fruit you want in the custom smoothie.\n
    """
)

# opt = st.selectbox(
#     'what is your fav fruit',
#     ('Banana','Strawberries','Peaches')
#     )
# st.write(
#     f"""you selected: {opt}"""
# )

name_on_order = st.text_input('Name on the smoothie:')
st.write('The name on the smoothie will be:',name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredient_list= st.multiselect(
    'select only 5 fruits from the table',
    my_dataframe,
    max_selections=5
)
if ingredient_list:

    ingredients_string=""
    for ingredient in ingredient_list:
        ingredients_string+=ingredient + ' '
        fv_df= st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order) values ('""" + ingredients_string + """','"""+ name_on_order + """')"""
    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")



