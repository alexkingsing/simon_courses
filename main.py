import streamlit as st
import pandas as pd

st.title("Hi!")

## Obtaining master CSV file in one instantiation
@st.experimental_singleton
def get_courses(file) -> pd.DataFrame:
    courses = pd.read_csv(file)
    return courses

all_courses = get_courses("courses.csv")

st.sidebar.write("Main Menu")
concentration = st.sidebar.radio("Choose your concentration",["Consulting","Finance","Marketing"])

match concentration:
    case "Consulting":
        
        # Catchy title space...
        st.subheader("Consulting!")

        ### PART 1 -> CREATE ALL RELEVANT TABLES AND LISTS FOR FUTURE ITERATION ###

        # Extract and  all possible specializations to facilitate future iterations
        consulting_spe = all_courses["Specialization"].unique()
        consulting_courses = all_courses["course"].unique() 

        # Create a unique dataframe where only the relevant concentration is being observed
        @st.experimental_memo
        def concentration_courses(dataframe, concentration) -> pd.DataFrame:
            concentration_df = dataframe[dataframe["Concentration"] == concentration]
            # drop unnecessary column
            concentration_df.drop("Concentration", axis = 1, inplace = True)

            return concentration_df
        
        consulting_df = concentration_courses(all_courses, "Consulting")

        # create a selection of all potential courses for the person to iterate
        personal_courses = st.multiselect("Please select the courses you've taken or are planning to take", consulting_courses)
        
        ### PART 2 -> PERFORM ALL RELEVANT SEGMENTATIONS TO CALCULATE COMPLETION ###

        #### INITIAL TEST
        st.write(consulting_df)

        # creating binary mask with selected courses to facilitate filtering
        mask = consulting_df["course"].isin(personal_courses)

        st.write(consulting_df[consulting_df["course"].isin(personal_courses)])

    case "Finance":
        st.subheader("Under construction...")




    case "Marketing":
        st.subheader("Under construction...")