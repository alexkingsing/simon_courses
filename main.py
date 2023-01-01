import streamlit as st
import pandas as pd

st.title("Hi!")

## Obtaining master CSV file in one instantiation
@st.experimental_singleton
def get_courses(file) ->pd.DataFrame:
    courses = pd.read_csv(file)
    return courses

all_courses = get_courses("courses.csv")

st.sidebar.write("Main Menu")
concentration = st.sidebar.radio("Choose your concentration",["Consulting","Finance","Marketing"])

match concentration:
    case "Consulting":
        st.subheader("Consulting!")
        st.table(all_courses)




    case "Finance":
        st.subheader("Under construction...")




    case "Marketing":
        st.subheader("Under construction...")