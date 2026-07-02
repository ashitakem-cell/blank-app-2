import streamlit as st
import pypdf
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="AI HR Recruitment Agent",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("👔 AI HR Recruitment Agent")
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

# Analysis button
st.markdown("---")
if st.button("🚀 Analyze Candidate Match", use_container_width=True):
    if resume_text and job_description:
        st.info("✨ Analysis feature coming soon! Your resume and job description are ready for processing.")
    else:
        st.error("❌ Please upload a resume and enter a job description before analyzing.")

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
    st.info(
        "💡 **About this tool:**\n\n"
        "This AI HR Recruitment Agent helps match candidates to job descriptions by:\n"
        "- Extracting resume content from PDF files\n"
        "- Analyzing key skills and experience\n"
        "- Comparing with job requirements\n"
        "- Generating a match score"
    )
