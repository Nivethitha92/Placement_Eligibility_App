import random
from faker import Faker
import mysql.connector

class StudentDB:
    def __init__(self, host="localhost", user="root", password="", port=3307, database="students_db"):
        self.fake = Faker('en_IN')
        self.used_ids = set()
        self.used_programming_ids = set()
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            database=database
        )
        self.cursor = self.connection.cursor(buffered=True)
        print("✅ Connected to database:", database)
        self.create_table()
        self.create_programming_table()
        self.create_soft_skills_table()
        self.create_placements_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                Student_ID INT PRIMARY KEY,
                Name VARCHAR(100),
                Gender VARCHAR(10),
                Age INT,
                Email VARCHAR(100),
                Mobile VARCHAR(20),
                Course_Batch VARCHAR(20),
                City VARCHAR(100),
                Graduation_Year INT
            )
        ''')
        print("🧱 students table ready.")

    def generate_student_data(self, count):
        cities = [
            "Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem", 
            "Tirunelveli", "Erode", "Vellore", "Thoothukudi", "Dindigul"
        ]
        graduation_years = list(range(2009, 2017))
        course_batches = ["DS-MDT31", "DS-MDT40", "DS-MDT41", "DS-MDT32", "DS-MDT33", "DS-MDT34", "DS-MDT35", "DS-MDT36"]
        genders = ['Male', 'Female', 'Other']
        
        students = []

        for _ in range(count):
            if len(self.used_ids) >= 500:
                raise Exception("❌ All 500 unique student IDs have been used.")

            while True:
                student_id = random.randint(1, 500)
                if student_id not in self.used_ids:
                    self.used_ids.add(student_id)
                    break

            gender = random.choice(genders)
            name = self.fake.name_male() if gender == 'Male' else self.fake.name_female() if gender == 'Female' else self.fake.name()

            student = (
                student_id,
                name,
                gender,
                random.randint(17, 25),
                self.fake.email(),
                self.fake.phone_number(),
                random.choice(course_batches),
                random.choice(cities),
                random.choice(graduation_years)
            )
            students.append(student)
        
        return students

    def insert_students(self, students):
        self.cursor.executemany('''
            INSERT INTO students (Student_ID, Name, Gender, Age, Email, Mobile, Course_Batch, City, Graduation_Year)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', students)
        self.connection.commit()
        print(f"✅ Successfully inserted {len(students)} student records.")

    def create_programming_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS programming_performance (
                programming_id INT PRIMARY KEY,
                student_id INT,
                language VARCHAR(50),
                codekata INT,
                assessment_score INT,
                assessments_completed INT,
                mini_project INT,
	            latest_project_score INT,
                FOREIGN KEY (student_id) REFERENCES students(Student_ID)
                    ON DELETE CASCADE ON UPDATE CASCADE
            )
        ''')
        print("🧱 programming_performance table created.")

    def generate_performance_data(self, count):
        languages = ['Python', 'Java', 'C++', 'JavaScript', 'R', 'Go']
        
        records = []
        for i in range(1, count + 1):
            if i in self.used_programming_ids:
                continue  # Ensure unique primary key
            self.used_programming_ids.add(i)

            student_id = i  # Foreign key from 1 to 500
            programming_id = i
            language = random.choice(languages)
            codekata = random.randint(100, 800)
            assessment_score = random.randint(100, 500)
            assessments_completed = random.randint(20, 50)  # WPM
            mini_project = random.randint(1, 10)  
            latest_project_score = random.randint(50, 100)


            record = (
                programming_id,
                student_id,
                language,
                codekata,
                assessment_score,
	            assessments_completed,
                mini_project,
                latest_project_score
            )
            records.append(record)

        return records

    def insert_performance_data(self, records):
        self.cursor.executemany('''
            INSERT INTO programming_performance (
                programming_id, student_id, language, codekata, 
                assessment_score, assessments_completed, mini_project, latest_project_score
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', records)
        self.connection.commit()
        print(f"✅ Inserted {len(records)} programming performance records.")

    def create_soft_skills_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS soft_skills (
                soft_skill_id INT PRIMARY KEY,
                student_id INT,
                communication INT,
                teamwork INT,
                presentation INT,
                leadership INT,
                critical_thinking INT,
                interpersonal_skills INT,
                FOREIGN KEY (student_id) REFERENCES students(Student_ID)
                    ON DELETE CASCADE ON UPDATE CASCADE
            )
        ''')
        print("🧠 soft_skills table created.")

    def create_placements_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS placements (
                placement_id INT PRIMARY KEY,
                student_id INT,
                mock_interview_score INT,
                internships_completed INT,
                placement_status VARCHAR(20),
                company_name VARCHAR(100),
                placement_package FLOAT,
                interview_rounds_cleared INT,
                placement_date DATE,
                FOREIGN KEY (student_id) REFERENCES students(Student_ID)
                    ON DELETE CASCADE ON UPDATE CASCADE
            )
        ''')
        print("💼 placements table created.")

    def generate_soft_skills_data(self, count=500):
        records = []
        for i in range(1, count + 1):
            record = (
                i,  # soft_skill_id
                i,  # student_id
                random.randint(50, 100),  # communication
                random.randint(50, 100),  # teamwork
                random.randint(50, 100),  # presentation
                random.randint(50, 100),  # leadership
                random.randint(50, 100),  # critical_thinking
                random.randint(50, 100),  # interpersonal_skills
            )
            records.append(record)
        return records

    def generate_placements_data(self, count=500):
        placement_status_options = ['Not_Placed', 'Placed']
        companies = ['TCS', 'Infosys', 'Wipro', 'Zoho', 'Google', 'Amazon', 'HCL', 'Cognizant', 'None']
        records = []
        for i in range(1, count + 1):
            status = random.choices(['Placed', 'Not_Placed'], weights=[0.4, 0.6])[0]
            company = random.choice(companies) if status == 'Placed' else ''
            package = round(random.uniform(3.5, 12.0), 2) if status == 'Placed' else 0.0
            placement_date = self.fake.date_between(start_date='-2y', end_date='today') if status == 'Placed' else None
            
            record = (
                i,  # placement_id
                i,  # student_id
                random.randint(40, 100),  # mock_interview_score
                random.randint(0, 3),     # internships_completed
                status,
                company,
                package,
                random.randint(1, 5) if status == 'Placed' else 0,
                placement_date
            )
            records.append(record)
        return records

    def insert_soft_skills_data(self, records):
        self.cursor.executemany('''
            INSERT INTO soft_skills (
                soft_skill_id, student_id, communication, teamwork, presentation,
                leadership, critical_thinking, interpersonal_skills
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', records)
        self.connection.commit()
        print(f"✅ Inserted {len(records)} soft skills records.")

    def insert_placements_data(self, records):
        self.cursor.executemany('''
            INSERT INTO placements (
                placement_id, student_id, mock_interview_score, internships_completed,
                placement_status, company_name, placement_package,
                interview_rounds_cleared, placement_date
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', records)
        self.connection.commit()
        print(f"✅ Inserted {len(records)} placement records.")

    def close(self):
        self.cursor.close()
        self.connection.close()
        print("🔒 Connection closed.")


# Usage
if __name__ == "__main__":
    db = StudentDB()
    students_data = db.generate_student_data(500)
    performance_data = db.generate_performance_data(500)
    softskills_data = db.generate_soft_skills_data()
    placement_data = db.generate_placements_data()
    db.insert_students(students_data)
    db.insert_performance_data(performance_data)
    db.insert_soft_skills_data(softskills_data)
    db.insert_placements_data(placement_data)
    db.close()

