import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.header("Simon Business School, MBA course specialization tool")

## Obtaining master CSV file in one instantiation
@st.experimental_memo
def get_courses(file) -> pd.DataFrame:
    courses = pd.read_csv(file)
    return courses

all_courses = get_courses("courses.csv")

st.sidebar.write("Main Menu")
concentration = st.sidebar.radio("Choose your concentration",["Main page", "Consulting","Finance","Marketing"])

if concentration == "Main page":
    st.write('''
            Welcome!

            The purpose of this tool is to help you plan your specializations based on your course selection. A few notes:
            \n
            - Core courses are NOT included in this tool since everyone has to take them.
            - Credit calculation is not included as part of this tool.
            - Minor(s) analysis is currently not in scope of this tool...

            ''')

elif "Consulting":
    
    # Specialization requirements
    strategy = {"required":0, "top":4, "bottom":3}
    pricing = {"required":0, "top":2, "bottom":2}
    technology = {"required":3, "top":3}
    operations = {"required":4, "top":2}

    # Catchy title space...
    st.subheader("Consulting Specializations!")

    ########## PART 1 -> CREATE ALL RELEVANT TABLES AND LISTS FOR FUTURE ITERATION ##########

    # Extract array of courses for future selection
    consulting_specializations = all_courses["Specialization"].unique()
    consulting_courses = all_courses["course"].unique() 

    # Create a unique dataframe where only the relevant concentration is being observed
    @st.experimental_memo
    def concentration_courses(dataframe, concentration) -> pd.DataFrame:
        concentration_df = dataframe[dataframe["Concentration"] == concentration]
        # drop unnecessary column
        concentration_df.drop("Concentration", axis = 1, inplace = True)
        return concentration_df
    
    consulting_df = concentration_courses(all_courses, "Consulting")

    # create a selection of all potential courses for the person to iterate as a FORM
    personal_courses = st.multiselect("Please select the courses you've taken or are planning to take", consulting_courses)
    
    ########## PART 2 -> PERFORM ALL RELEVANT SEGMENTATIONS TO CALCULATE COMPLETION ##########

    # creating binary mask with selected courses to facilitate filtering
    mask = consulting_df["course"].isin(personal_courses)

    # creating a segmented dataframe to hold filtered results
    consulting_segmented_df = consulting_df[mask]

    ########## PART 3 -> CREATE VISUAL SEGMENTATION ##########
    
    # tab quantity hard-coded, because why not...
    tab1, tab2, tab3, tab4 = st.tabs(consulting_specializations.tolist())

    with tab1:
        st.write("**Strategy completion**")
        
        ##Creating small dataframes with the individual top and down segmentations for future use
        # dataframe if course is for Strategy AND is needed as 'top'
        top_strategy = consulting_df[(consulting_df["top"]>0) & (consulting_df["Specialization"]=="Strategy")]
        # dataframe if course is for Strategy AND is needed as 'bottom'
        bottom_strategy = consulting_df[(consulting_df["bottom"]>0) & (consulting_df["Specialization"]=="Strategy")]

        ## Obtaining counts of how many courses the person has from each list
        top_count_strat = consulting_segmented_df[consulting_segmented_df["Specialization"]=="Strategy"]["top"].sum()
        bottom_count_strat = consulting_segmented_df[consulting_segmented_df["Specialization"]=="Strategy"]["bottom"].sum()

        y0 = [top_count_strat, bottom_count_strat]

        ### @@@@@@@@@@@@ ADD LOGIC FOR WHEN THE NUMBERS WOULD BE NEGATIVE...
        y1 = [strategy["top"] - top_count_strat, strategy["bottom"] - bottom_count_strat]

        # Create stacked bar chart to show total courses selected vs needed for specialization
        fig1 = go.Figure(data=[
            go.Bar(name="Completed courses", x=["Top list", "Bottom list"], y=y0, marker_color="dodgerblue"),
            go.Bar(name="Pending courses",x=["Top list", "Bottom list"], y=y1, marker_color="crimson")]
            )
        fig1.update_layout(barmode='stack')
        st.plotly_chart(fig1)

        ########## PART 4 -> CREATE TABLE DETAILING PENDINGS ##########

        col1, col2 = st.columns(2)
        top_pending = top_strategy[~top_strategy["course"].isin(consulting_segmented_df[consulting_segmented_df["top"]==1]["course"])]
        bottom_pending = bottom_strategy[~bottom_strategy["course"].isin(consulting_segmented_df[consulting_segmented_df["bottom"]==1]["course"])]

        with col1:
            st.write(f"You have taken **{top_count_strat} courses** from the top list. You need **{strategy['top']} in total**.")
            st.dataframe(top_pending.drop(["required?","top","bottom"], axis=1))

        with col2:
            st.write(f"You have taken **{bottom_count_strat} courses** from the bottom list. You need **{strategy['bottom']} in total**.")
            st.dataframe(bottom_pending.drop(["required?","top","bottom"], axis=1))

    with tab2:
        st.write("**Pricing completion**")

    with tab3:
        st.write("**Technology completion**")
        

    with tab4:
        st.write("**Operations completion**")
        

elif "Finance":
    st.subheader("Under construction...")


elif "Marketing":
    st.subheader("Under construction...")