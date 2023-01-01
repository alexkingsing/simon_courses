import streamlit as st
import pandas as pd

st.header("Simon Business School, MBA course specialization tool")

## Obtaining master CSV file in one instantiation
@st.experimental_memo
def get_courses(file) -> pd.DataFrame:
    courses = pd.read_csv(file)
    return courses

all_courses = get_courses("courses.csv")

st.sidebar.write("Main Menu")
concentration = st.sidebar.radio("Choose your concentration",["Main page", "Consulting","Finance","Marketing"])

match concentration:

    case "Main page":
        st.write('''
                Welcome!

                The purpose of this tool is to help you plan your specializations based on your course selection. A few notes:
                \n
                - Core courses are NOT included in this tool since everyone has to take them.
                - Credit calculation is not included as part of this tool.
                - Minor(s) analysis is currently not in scope of this tool...

                ''')

    case "Consulting":
        
        # Specialization requirements
        strategy = {"required":0, "selective":7}
        pricing = {"required":0, "selective":5}
        technology = {"required":3, "selective":3}
        operations = {"required":4, "selective":2}

        # Catchy title space...
        st.subheader("Consulting Specializations!")

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

        # creating a segmented dataframe to hold filtered results
        segmented_df = consulting_df[consulting_df["course"].isin(personal_courses)]

        st.write(segmented_df)



    case "Finance":
        st.subheader("Under construction...")




    case "Marketing":
        st.subheader("Under construction...")