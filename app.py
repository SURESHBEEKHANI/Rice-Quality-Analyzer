import streamlit as st
from PIL import Image
import os
import base64
import io
from dotenv import load_dotenv
from groq import Groq
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ======================
# CONFIGURATION SETTINGS
# ======================
PAGE_CONFIG = {
    "page_title": "Rice Quality Analyzer",
    "page_icon": "🌾",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

ALLOWED_FILE_TYPES = ['png', 'jpg', 'jpeg']

CSS_STYLES = """
<style>
    .main { background-color: #f4f9f9; color: #000000; }
    .sidebar .sidebar-content { background-color: #d1e7dd; }
    .stTextInput textarea { color: #000000 !important; }
    .stButton>button { 
        background-color: #21eeef; 
        color: white; 
        font-size: 16px; 
        border-radius: 5px; 
    }
    .report-container {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #21eeef;
    }
    .report-text {
        font-family: 'Arial', sans-serif;
        font-size: 14px;
        line-height: 1.6;
        color: #2c3e50;
    }
</style>
"""

# ======================
# CORE FUNCTIONS
# ======================
def configure_application():
    """Initialize application settings and styling"""
    st.set_page_config(**PAGE_CONFIG)
    st.markdown(CSS_STYLES, unsafe_allow_html=True)

def initialize_api_client():
    """Create and validate Groq API client"""
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        st.error("API key not found. Please verify .env configuration.")
        st.stop()
    
    return Groq(api_key=api_key)

def process_image_data(uploaded_file):
    """Convert image to base64 encoded string"""
    try:
        image = Image.open(uploaded_file)
        buffer = io.BytesIO()
        image.save(buffer, format=image.format)
        return base64.b64encode(buffer.getvalue()).decode('utf-8'), image.format
    except Exception as e:
        st.error(f"Image processing error: {str(e)}")
        return None, None

def generate_pdf_report(report_text):
    """Generate PDF document from report text"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    title = Paragraph("<b>Rice Quality Report</b>", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    content = Paragraph(report_text.replace('\n', '<br/>'), styles['BodyText'])
    story.append(content)
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def generate_rice_report(uploaded_file, client):
    """Generate AI-powered rice quality analysis"""
    base64_image, img_format = process_image_data(uploaded_file)
    
    if not base64_image:
        return None

    image_url = f"data:image/{img_format.lower()};base64,{base64_image}"

    try:
        response = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": (
                        "Analyze the rice grain image and provide a detailed report including:\n"
                        "1. Rice type classification\n2. Quality assessment (broken grains %, discoloration %, impurities %)\n"
                        "3. Foreign object detection\n4. Size and shape consistency\n5. Recommendations for processing or improvement"
                    )},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ]
            }],
            temperature=0.2,
            max_tokens=400,
            top_p=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"API communication error: {str(e)}")
        return None

# ======================
# UI COMPONENTS
# ======================
def display_main_interface():
    """Render primary application interface"""
    st.title("🌾 Rice Quality Analyzer")
    st.subheader("AI-Powered Rice Grain Inspection")
    st.markdown("---")

    # Display analysis results
    if st.session_state.get('analysis_result'):
        st.markdown("### 📋 Analysis Report")
        st.markdown(
            f'<div class="report-container"><div class="report-text">{st.session_state.analysis_result}</div></div>', 
            unsafe_allow_html=True
        )
        pdf_report = generate_pdf_report(st.session_state.analysis_result)
        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_report,
            file_name="rice_quality_report.pdf",
            mime="application/pdf"
        )

    if st.button("Clear Analysis 🗑️"):
        st.session_state.pop('analysis_result', None)
        st.rerun()

def render_sidebar(client):
    """Create sidebar interface elements"""
    with st.sidebar:
        st.markdown("### Features")
        st.markdown("""
        - **Rice Type Classification** (e.g., Basmati, Jasmine, Indica)
        - **Quality Check** (Broken grains %, impurities %, discoloration %)
        - **Foreign Object Detection** (Husks, stones, debris)
        - **Grain Size & Shape Analysis**
        - **Processing Recommendations**
        """)
        st.markdown("---")
        
        st.subheader("Upload Rice Image")
        uploaded_file = st.file_uploader(
            "Select an image of rice grains", 
            type=ALLOWED_FILE_TYPES
        )
        
        if uploaded_file:
            st.image(Image.open(uploaded_file), caption="Uploaded Image", use_column_width=True)
            if st.button("Analyze Rice Quality 🔍"):
                with st.spinner("Processing image... This may take a few seconds."):
                    report = generate_rice_report(uploaded_file, client)
                    st.session_state.analysis_result = report
                    st.rerun()

# ======================
# APPLICATION ENTRYPOINT
# ======================
def main():
    """Primary application controller"""
    configure_application()
    groq_client = initialize_api_client()
    
    display_main_interface()
    render_sidebar(groq_client)

if __name__ == "__main__":
    main()
