import streamlit as st
import pypdf
import json
from io import BytesIO
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="AI HR Recruitment Agent",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Groq API
def initialize_groq():
    """Initialize Groq API with user's API key"""
    api_key = st.secrets.get("GROQ_API_KEY")
    if not api_key:
        st.warning("⚠️ Groq API key not found in secrets. Please add GROQ_API_KEY to your Streamlit secrets.")
        return None
    return Groq(api_key=api_key)

# Evaluation function using Groq
def evaluate_candidate(resume_text, job_description):
    """
    Use Groq with Llama 3.3 70B to evaluate candidate match
    Returns structured JSON with evaluation metrics
    """
    try:
        client = initialize_groq()
        if not client:
            return None
        
        prompt = f"""
        You are an expert HR recruiter. Analyze the following resume against the job description and provide a structured JSON response.
        
        RESUME:
        {resume_text}
        
        JOB DESCRIPTION:
        {job_description}
        
        Please provide a JSON response with exactly these fields:
        {{
            "candidate_name": "extracted candidate name or 'Not Found'",
            "match_percentage": <integer between 0-100>,
            "missing_skills": ["skill1", "skill2", "skill3"],
            "hiring_status": "Strong Hire" | "Hire" | "Consider" | "Pass",
            "feedback": "Brief professional feedback about the candidate's fit"
        }}
        
        Respond ONLY with valid JSON, no other text.
        """
        
        message = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1024,
        )
        
        response_text = message.choices[0].message.content.strip()
        
        # Parse JSON response
        evaluation_data = json.loads(response_text)
        return evaluation_data
        
    except json.JSONDecodeError as e:
        st.error(f"❌ Error parsing Groq response: {str(e)}")
        return None
    except Exception as e:
        st.error(f"❌ Error calling Groq API: {str(e)}")
        return None

# Render evaluation cards
def render_evaluation_cards(evaluation_data):
    """Render evaluation results as visual cards"""
    if not evaluation_data:
        return
    
    st.markdown("---")
    st.header("📊 Evaluation Results")
    
    # Main metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Candidate Name",
            evaluation_data.get("candidate_name", "N/A")
        )
    
    with col2:
        match_pct = evaluation_data.get("match_percentage", 0)
        # Color code based on match percentage
        if match_pct >= 80:
            color = "🟢"
        elif match_pct >= 60:
            color = "🟡"
        else:
            color = "🔴"
        
        st.metric(
            "Match Percentage",
            f"{color} {match_pct}%"
        )
    
    with col3:
        hiring_status = evaluation_data.get("hiring_status", "N/A")
        st.metric(
            "Hiring Status",
            hiring_status
        )
    
    with col4:
        missing_skills = evaluation_data.get("missing_skills", [])
        st.metric(
            "Missing Skills Count",
            len(missing_skills)
        )
    
    # Detailed information
    st.markdown("---")
    
    col_details1, col_details2 = st.columns(2)
    
    with col_details1:
        st.subheader("💬 Feedback")
        feedback = evaluation_data.get("feedback", "No feedback available")
        st.info(feedback)
    
    with col_details2:
        st.subheader("🔧 Missing Skills")
        missing_skills = evaluation_data.get("missing_skills", [])
        if missing_skills:
            for i, skill in enumerate(missing_skills, 1):
                st.write(f"{i}. {skill}")
        else:
            st.success("✅ No missing skills identified!")

# Title
st.title("👔 AI HR Recruitment Agent")
st.markdown("Powered by Groq AI")
st.markdown("---")

# Main layout with columns
col1, col2 = st.columns(2)

with col1:
    st.header("📄 Resume Upload")
    st.markdown("Upload a PDF resume to extract text and analyze candidate information.")
    
    # PDF upload
    uploaded_file = st.file_uploader(
        "Choose a PDF resume",
        type="pdf",
        help="Upload a PDF file containing the candidate's resume"
    )
    
    resume_text = ""
    if uploaded_file is not None:
        try:
            # Read and extract text from PDF
            pdf_reader = pypdf.PdfReader(BytesIO(uploaded_file.read()))
            resume_text = ""
            
            for page in pdf_reader.pages:
                resume_text += page.extract_text()
            
            st.success(f"✅ Successfully extracted text from {len(pdf_reader.pages)} page(s)")
            
            # Display extracted resume text
            with st.expander("📋 View Extracted Resume Text"):
                st.text_area(
                    "Extracted Resume Content",
                    value=resume_text,
                    height=300,
                    disabled=True
                )
        except Exception as e:
            st.error(f"❌ Error processing PDF: {str(e)}")

with col2:
    st.header("💼 Job Description")
    st.markdown("Paste the job description to match against the candidate's resume.")
    
    # Job description text area
    job_description = st.text_area(
        "Enter Job Description",
        placeholder="Paste the job description here...",
        height=300,
        help="Enter the complete job description to analyze against the resume"
    )

# Bottom section for analysis
st.markdown("---")
st.header("🤖 Analysis Section")

col_analysis1, col_analysis2 = st.columns(2)

with col_analysis1:
    st.subheader("Resume Summary")
    if resume_text:
        resume_preview = resume_text[:500] + "..." if len(resume_text) > 500 else resume_text
        st.info(f"📌 Resume extracted with {len(resume_text)} characters")
        st.text_area(
            "Resume Preview",
            value=resume_preview,
            height=150,
            disabled=True
        )
    else:
        st.warning("⚠️ Upload a resume to see the summary")

with col_analysis2:
    st.subheader("Job Description Summary")
    if job_description:
        jd_preview = job_description[:500] + "..." if len(job_description) > 500 else job_description
        st.info(f"📌 Job description contains {len(job_description)} characters")
        st.text_area(
            "Job Description Preview",
            value=jd_preview,
            height=150,
            disabled=True
        )
    else:
        st.warning("⚠️ Enter a job description to see the summary")

# Evaluation button
st.markdown("---")
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])

with col_btn2:
    if st.button("🚀 Evaluate Candidate", use_container_width=True, type="primary"):
        if resume_text and job_description:
            # Check if Groq API is initialized
            if initialize_groq():
                with st.spinner("🔄 Analyzing candidate with AI..."):
                    evaluation_result = evaluate_candidate(resume_text, job_description)
                    if evaluation_result:
                        st.session_state.evaluation_result = evaluation_result
                        st.success("✨ Evaluation complete!")
            else:
                st.error("❌ Groq API is not configured. Please set up your API key.")
        else:
            st.error("❌ Please upload a resume and enter a job description before evaluating.")

# Display evaluation results if available
if "evaluation_result" in st.session_state:
    render_evaluation_cards(st.session_state.evaluation_result)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    st.markdown("---")
    
    similarity_threshold = st.slider(
        "Match Similarity Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.6,
        step=0.05,
        help="Set the minimum similarity score for a match"
    )
    
    st.markdown("---")
    st.subheader("📊 Statistics")
    if resume_text:
        st.metric("Resume Length", f"{len(resume_text):,} characters")
    if job_description:
        st.metric("Job Description Length", f"{len(job_description):,} characters")
    
    st.markdown("---")
    st.subheader("🔑 API Configuration")
    api_key_status = "✅ Configured" if st.secrets.get("GROQ_API_KEY") else "❌ Not Configured"
    st.write(f"Groq API: {api_key_status}")
    
    st.markdown("---")
    st.info(
        "💡 **About this tool:**\n\n"
        "This AI HR Recruitment Agent helps match candidates to job descriptions by:\n"
        "- Extracting resume content from PDF files\n"
        "- Using Groq AI with Llama 3.3 70B for analysis\n"
        "- Comparing with job requirements\n"
        "- Generating a detailed match score and feedback\n\n"
        "**Powered by:** Groq API with Llama 3.3 70B Versatile"
    )
