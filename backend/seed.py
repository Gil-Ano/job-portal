from app.database import SessionLocal, engine, Base
from app import models
from app.auth import hash_password

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Skip if data already exists
if db.query(models.User).filter(models.User.email == "employer@seed.com").first():
    print("Seed data already exists. Skipping.")
    db.close()
    exit()

# ----- EMPLOYER 1 -----
emp1_user = models.User(
    email="employer@seed.com",
    password_hash=hash_password("password123"),
    role="employer",
    full_name="TechCorp Zimbabwe",
)
db.add(emp1_user)
db.flush()

emp1 = models.EmployerProfile(
    user_id=emp1_user.id,
    company_name="TechCorp Zimbabwe",
    company_description="Leading tech company in Harare",
    location="Harare",
    website="https://techcorp.co.zw",
)
db.add(emp1)
db.flush()

# ----- EMPLOYER 2 -----
emp2_user = models.User(
    email="employer2@seed.com",
    password_hash=hash_password("password123"),
    role="employer",
    full_name="DataPro Africa",
)
db.add(emp2_user)
db.flush()

emp2 = models.EmployerProfile(
    user_id=emp2_user.id,
    company_name="DataPro Africa",
    company_description="Data analytics and AI solutions",
    location="Remote",
    website="https://datapro.africa",
)
db.add(emp2)
db.flush()

# ----- JOBSEEKER -----
seeker_user = models.User(
    email="seeker@seed.com",
    password_hash=hash_password("password123"),
    role="jobseeker",
    full_name="Tafadzwa Moyo",
)
db.add(seeker_user)
db.flush()

seeker = models.JobseekerProfile(
    user_id=seeker_user.id,
    headline="Aspiring Software Developer",
    skills=["Python", "JavaScript", "React", "FastAPI"],
)
db.add(seeker)
db.flush()

# ----- JOBS -----
jobs_data = [
    {
        "employer_id": emp1.id,
        "title": "Junior Python Developer",
        "company": "TechCorp Zimbabwe",
        "location": "Harare",
        "salary_min": 800,
        "salary_max": 1500,
        "description": "We are looking for a passionate Junior Python Developer to join our growing team. You will work on backend systems using FastAPI and PostgreSQL. Perfect for recent graduates eager to learn.",
        "requirements": "Python, FastAPI, PostgreSQL, Git, Basic understanding of REST APIs",
        "type": "full-time",
        "category": "software-engineering",
    },
    {
        "employer_id": emp1.id,
        "title": "React Frontend Developer",
        "company": "TechCorp Zimbabwe",
        "location": "Harare",
        "salary_min": 900,
        "salary_max": 1800,
        "description": "Build beautiful, responsive user interfaces for our SaaS products. You'll work closely with designers and backend developers.",
        "requirements": "React, JavaScript, Tailwind CSS, TypeScript, 1+ years experience",
        "type": "full-time",
        "category": "software-engineering",
    },
    {
        "employer_id": emp1.id,
        "title": "DevOps Intern",
        "company": "TechCorp Zimbabwe",
        "location": "Bulawayo",
        "salary_min": 500,
        "salary_max": 800,
        "description": "Learn DevOps practices in a real production environment. Work with Docker, CI/CD pipelines, and cloud deployment.",
        "requirements": "Basic Linux, Git, Willingness to learn Docker and AWS",
        "type": "internship",
        "category": "devops",
    },
    {
        "employer_id": emp2.id,
        "title": "Data Analyst",
        "company": "DataPro Africa",
        "location": "Remote",
        "salary_min": 1200,
        "salary_max": 2500,
        "description": "Analyze large datasets to extract business insights. Build dashboards and reports for clients across Africa.",
        "requirements": "Python, SQL, Pandas, Power BI or Tableau, 2+ years experience",
        "type": "full-time",
        "category": "data-science",
    },
    {
        "employer_id": emp2.id,
        "title": "Machine Learning Engineer",
        "company": "DataPro Africa",
        "location": "Remote",
        "salary_min": 2500,
        "salary_max": 4500,
        "description": "Design and deploy ML models for our clients in finance and healthcare. Work with cutting-edge AI technologies.",
        "requirements": "Python, TensorFlow or PyTorch, MLOps, 3+ years experience",
        "type": "full-time",
        "category": "data-science",
    },
    {
        "employer_id": emp1.id,
        "title": "Mobile App Developer",
        "company": "TechCorp Zimbabwe",
        "location": "Harare",
        "salary_min": 1000,
        "salary_max": 2000,
        "description": "Develop cross-platform mobile applications using React Native. Join a team building the next big fintech app.",
        "requirements": "React Native, JavaScript, REST APIs, 1+ years mobile development",
        "type": "full-time",
        "category": "mobile-development",
    },
    {
        "employer_id": emp2.id,
        "title": "Cybersecurity Analyst",
        "company": "DataPro Africa",
        "location": "Remote",
        "salary_min": 1800,
        "salary_max": 3000,
        "description": "Protect our systems and client data. Conduct security audits, vulnerability assessments, and implement security best practices.",
        "requirements": "Network security, SIEM tools, CEH or similar certification, 2+ years experience",
        "type": "contract",
        "category": "cybersecurity",
    },
    {
        "employer_id": emp1.id,
        "title": "UI/UX Designer",
        "company": "TechCorp Zimbabwe",
        "location": "Harare",
        "salary_min": 700,
        "salary_max": 1400,
        "description": "Design intuitive and beautiful user experiences for web and mobile applications. Create wireframes, prototypes, and design systems.",
        "requirements": "Figma, Adobe XD, User research, Portfolio of design work",
        "type": "full-time",
        "category": "design",
    },
    {
        "employer_id": emp2.id,
        "title": "Cloud Solutions Architect",
        "company": "DataPro Africa",
        "location": "Remote",
        "salary_min": 3000,
        "salary_max": 5500,
        "description": "Design cloud infrastructure for enterprise clients. Lead migration projects and optimize cloud costs.",
        "requirements": "AWS or Azure, Terraform, Kubernetes, 5+ years experience",
        "type": "full-time",
        "category": "cloud",
    },
    {
        "employer_id": emp1.id,
        "title": "Part-Time Content Writer (Tech)",
        "company": "TechCorp Zimbabwe",
        "location": "Remote",
        "salary_min": 400,
        "salary_max": 700,
        "description": "Write technical blog posts, documentation, and marketing content about our products and industry trends.",
        "requirements": "Excellent English writing, Basic tech knowledge, Writing samples required",
        "type": "part-time",
        "category": "content",
    },
    {
        "employer_id": emp2.id,
        "title": "Backend Developer (Node.js)",
        "company": "DataPro Africa",
        "location": "Remote",
        "salary_min": 1500,
        "salary_max": 2800,
        "description": "Build scalable backend services for our data platform. Work with microservices architecture and message queues.",
        "requirements": "Node.js, Express, MongoDB, Redis, Docker, 2+ years experience",
        "type": "full-time",
        "category": "software-engineering",
    },
    {
        "employer_id": emp1.id,
        "title": "IT Support Technician",
        "company": "TechCorp Zimbabwe",
        "location": "Harare",
        "salary_min": 600,
        "salary_max": 1000,
        "description": "Provide technical support to staff and clients. Manage hardware, software installations, and network troubleshooting.",
        "requirements": "Windows/Linux, Networking basics, Customer service skills",
        "type": "full-time",
        "category": "it-support",
    },
    {
        "employer_id": emp2.id,
        "title": "Database Administrator",
        "company": "DataPro Africa",
        "location": "Remote",
        "salary_min": 1800,
        "salary_max": 3200,
        "description": "Manage and optimize our PostgreSQL and MongoDB databases. Ensure data integrity, backup strategies, and performance tuning.",
        "requirements": "PostgreSQL, MongoDB, Query optimization, 3+ years DBA experience",
        "type": "full-time",
        "category": "database",
    },
    {
        "employer_id": emp1.id,
        "title": "Graduate Trainee - Software Engineering",
        "company": "TechCorp Zimbabwe",
        "location": "Harare",
        "salary_min": 500,
        "salary_max": 900,
        "description": "Rotational program for recent graduates. Spend 3 months each in frontend, backend, and DevOps teams. Training provided.",
        "requirements": "Computer Science degree, Basic programming knowledge, Eager to learn",
        "type": "full-time",
        "category": "software-engineering",
    },
    {
        "employer_id": emp2.id,
        "title": "Product Manager",
        "company": "DataPro Africa",
        "location": "Remote",
        "salary_min": 2000,
        "salary_max": 4000,
        "description": "Lead product development from ideation to launch. Work with engineering, design, and business teams to deliver value.",
        "requirements": "Agile/Scrum, Product roadmap experience, Technical background preferred, 3+ years experience",
        "type": "full-time",
        "category": "product",
    },
]

for job_data in jobs_data:
    job = models.Job(**job_data)
    db.add(job)

db.commit()
db.close()

print("✅ Seed data created successfully!")
print("  - 2 employers (employer@seed.com, employer2@seed.com)")
print("  - 1 jobseeker (seeker@seed.com)")
print("  - 15 jobs across multiple categories")
print("  - Password for all accounts: password123")