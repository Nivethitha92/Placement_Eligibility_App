import streamlit as st
import pandas as pd
from db_config import get_connection



st.set_page_config(page_title="Student Dashboard", layout="wide")

# Custom CSS for background color and styling
st.markdown("""
    <style>
    body {
        background-color: #f0f8ff;  /* Light Blue Background */
        font-family: Arial, sans-serif;
    }
    .block-container {
        padding: 2rem;
    }
    .stApp {
        background-color: #f0f8ff;
    }
    .header {
        color: #2f4f4f;
    }
    .stButton>button {
        background-color: #4682b4;
        color: white;
    }
    .stTextInput input {
        background-color: #e6f7ff;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Student Performance Dashboard")

# Connect to the database
conn = get_connection()
cursor = conn.cursor(dictionary=True)

def load_data(query):
    cursor.execute(query)
    return pd.DataFrame(cursor.fetchall())


tab1, tab2, tab3 = st.tabs(["🎓 Students", "🧠 Programming and Soft Skills", "💼 Placements"])


with tab1:
    st.header("Student Details")
    

    
    col1, col2 = st.columns(2)

    with col1:
        course_batches = st.selectbox("Course Batch", ["All", "DS-MDT31", "DS-MDT40", "DS-MDT41", "DS-MDT32", "DS-MDT33", "DS-MDT34", "DS-MDT35", "DS-MDT36"])
        gender = st.selectbox("Gender", ['All', 'Male', 'Female', 'Other'])

    with col2:
        city = st.selectbox("City", ['All', 'Chennai', 'Coimbatore', 'Madurai', 'Tiruchirappalli', 'Salem', 'Tirunelveli', 'Erode', 'Vellore', 'Thoothukudi', 'Dindigul'])
        graduation_year = st.selectbox("Graduation Year", ['All'] + list(range(2009, 2017)))


    query = "SELECT * FROM students WHERE 1=1"
    if course_batches != 'All':
        query += f" AND Course_Batch = '{course_batches}'"
    if gender != 'All':
        query += f" AND Gender = '{gender}'"
    if city != 'All':
        query += f" AND City = '{city}'"
    if graduation_year != 'All':
        query += f" AND Graduation_Year = {graduation_year}"

    df_students = load_data(query)
    st.dataframe(df_students, use_container_width=True, hide_index=True)

    

    

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Programming Skills Criteria")
        st.markdown("Select categories to display the number of students who passed the criteria")
        mini_project = st.slider("Mini_Project", 0, 10, 5)
        Assessment_Score = st.slider("Assessment Score", 100, 500, 250)
        Codekata = st.slider("Codekata", 0, 800, 250)

        query = f"SELECT count(student_id) as Eligible_Student_Count FROM programming_performance WHERE mini_project >= {mini_project} AND assessment_score >= {Assessment_Score} and codekata >= {Codekata}"
        df_prog = load_data(query)
        eligible_count = df_prog['Eligible_Student_Count'][0]

        st.text(f"Eligible Student Count: {eligible_count}")



        query_student = f"SELECT a.student_id, b.Name,b.Course_Batch, a.language FROM programming_performance a join students b WHERE a.student_id = b.student_id and mini_project >= {mini_project} AND assessment_score >= {Assessment_Score} and codekata >= {Codekata}"
        df_prog = load_data(query_student)
        st.dataframe(df_prog, use_container_width=True, hide_index=True)

    with col2: 
        st.subheader("Soft Skills Report")
        st.markdown("Soft Skills of Students who have passed Programming Skills")
        communication = st.slider("Communication", 30, 100, 50)
        presentation = st.slider("Presentation Skills", 30, 100, 50)
        interpersonal_skills = st.slider("Interpersonal Skills", 30, 100, 50)
        query = f"""
        SELECT count(p.student_id) as Eligible_Student_Count FROM programming_performance p
        JOIN soft_skills s ON p.student_id = s.student_id
        JOIN students b ON p.student_id = b.student_id
        WHERE p.mini_project >= {mini_project} 
        AND p.assessment_score >= {Assessment_Score} 
        AND p.codekata >= {Codekata}
        AND s.communication >= {communication} 
        AND s.presentation >= {presentation} 
        AND s.interpersonal_skills >= {interpersonal_skills}
        """
        df_prog = load_data(query)
        eligible_count = df_prog['Eligible_Student_Count'][0]
        st.text(f"Eligible Student Count: {eligible_count}")

        query_soft = f"""
        SELECT b.Name, s.Teamwork, s.Critical_Thinking, s.Leadership 
        FROM programming_performance p
        JOIN soft_skills s ON p.student_id = s.student_id
        JOIN students b ON p.student_id = b.student_id
        WHERE p.mini_project >= {mini_project} 
        AND p.assessment_score >= {Assessment_Score} 
        AND p.codekata >= {Codekata}
        AND s.communication >= {communication} 
        AND s.presentation >= {presentation} 
        AND s.interpersonal_skills >= {interpersonal_skills}
        """
        df_soft = load_data(query_soft)
        st.dataframe(df_soft, use_container_width=True, hide_index=True)

with tab3:
    st.title("📈 Placement Analysis Dashboard")

    
    
    placement_status = st.selectbox("Placement Status", ['All', 'Placed', 'Not_Placed'])
    

    
    query = f"""
    SELECT * FROM placements 
    """
    if placement_status != 'All':
        query += f"where placement_status = '{placement_status}'"

    df_place = load_data(query)

  
    st.subheader("📊 Overall Placement Metrics")

    total_students = len(df_place)
    placed_students = df_place[df_place['placement_status'] == 'Placed']
    Not_placed_Students = df_place[df_place['placement_status'] == 'Not_Placed']
    avg_package = placed_students['placement_package'].mean() if not placed_students.empty else 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("👥 Total Students", total_students)
    col2.metric("✅ Placed", len(placed_students))
    col3.metric("⏳ Not_Placed", len(Not_placed_Students))
    col4.metric("💰 Avg Package", f"{avg_package:.2f} LPA")

    st.markdown("---")

    st.subheader("📋 Placed Student Details")
    
    query = f"""
    SELECT b.Name, b.course_batch, p.language, a.placement_status, a.company_name 
    FROM placements a 
    join students b on a.student_id = b.student_id 
    join programming_performance p on a.student_id = p.student_id 
    
    """

    if placement_status != 'All':
        query += f" AND placement_status = '{placement_status}'"

    
    
    df_placements = load_data(query)
    st.dataframe(df_placements, use_container_width=True, hide_index=True)
   
    st.subheader("🎯 Breakdown of Placed Students by Company")
    query_company = f"""
    SELECT company_name as 'Company' , count(*) as 'No.of.Students'
    FROM placements where 
    placement_status = 'Placed'
    group by company_name
    """
    df_placements = load_data(query_company)
    st.dataframe(df_placements, use_container_width=False, hide_index=True)
# Close connection
cursor.close()
conn.close()