import streamlit as st
import streamlit.components.v1 as components
import libs as glib 
import base

# Modern CSS styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #a8edea 0%, #fed6e3 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: #333;
    }
    .upload-section {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border: 2px dashed #a8edea;
        text-align: center;
    }
    .summary-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #a8edea;
    }
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        text-align: center;
    }
    .reportview-container {
        margin-top: -2em;
    }
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    #stDecoration {display:none;}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>📄 Document Summary</h1>
    <p>AI-powered document analysis and summarization</p>
</div>
""", unsafe_allow_html=True)

base.init_slidebar()

# Features section
st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <h3>📝 Smart Summarization</h3>
        <p>Extract key points and main ideas from lengthy documents</p>
    </div>
    <div class="feature-card">
        <h3>🔍 Key Insights</h3>
        <p>Identify important themes, trends, and actionable information</p>
    </div>
    <div class="feature-card">
        <h3>⚡ Quick Processing</h3>
        <p>Get summaries in seconds, not hours of reading</p>
    </div>
    <div class="feature-card">
        <h3>📊 Multiple Formats</h3>
        <p>Support for PDF, TXT, DOCX, and other document types</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Document upload section
st.markdown("### 📤 Upload Document")
st.markdown("""
<div class="upload-section">
    <h4>📁 Choose Your Document</h4>
    <p>Upload a document to get an AI-powered summary</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose a file",
    type=['pdf', 'txt', 'docx', 'md', 'py', 'js', 'html', 'css', 'json'],
    help="Supported formats: TXT, PDF, DOCX, MD, and other text files (Max size: 10MB)"
)

# Summary options
col1, col2 = st.columns(2)
with col1:
    summary_length = st.selectbox(
        "Summary Length",
        ["Brief (2-3 sentences)", "Medium (1 paragraph)", "Detailed (multiple paragraphs)"],
        index=1
    )

with col2:
    summary_focus = st.selectbox(
        "Focus Area",
        ["General Overview", "Key Points", "Action Items", "Financial Highlights", "Technical Details"],
        index=0
    )

# Process document
if uploaded_file is not None:
    st.success(f"✅ File uploaded: {uploaded_file.name}")
    
    if st.button("🚀 Generate Summary", use_container_width=True):
        with st.spinner("🔄 Processing document..."):
            try:
                # Read file content
                content = None
                
                if uploaded_file.type == "text/plain" or uploaded_file.name.endswith('.txt'):
                    content = str(uploaded_file.read(), "utf-8")
                elif uploaded_file.type == "application/pdf" or uploaded_file.name.endswith('.pdf'):
                    try:
                        import PyPDF2
                        from io import BytesIO
                        
                        pdf_reader = PyPDF2.PdfReader(BytesIO(uploaded_file.read()))
                        content = ""
                        for page in pdf_reader.pages:
                            content += page.extract_text()
                    except ImportError:
                        st.warning("PDF processing requires PyPDF2. Please install it or use text files.")
                        content = None
                elif uploaded_file.name.endswith('.docx'):
                    try:
                        from docx import Document
                        from io import BytesIO
                        
                        doc = Document(BytesIO(uploaded_file.read()))
                        content = ""
                        for paragraph in doc.paragraphs:
                            if paragraph.text:  # Check if paragraph has text
                                content += paragraph.text + "\n"
                    except ImportError:
                        st.warning("DOCX processing requires python-docx. Please install it or use text files.")
                        content = None
                else:
                    st.error("❌ Could not extract text from the document. Please try a different file or format.")
                
                if content and content.strip():
                    # Create summary prompt
                    prompt = f"""
                    Please provide a {summary_length.lower()} summary of the following document, 
                    focusing on {summary_focus.lower()}:
                    
                    Document Content:
                    {content[:5000]}  # Limit content to avoid token limits
                    
                    Please structure your summary with:
                    1. Main Topic/Purpose
                    2. Key Points (3-5 bullet points)
                    3. Important Details
                    4. Conclusion/Recommendations (if applicable)
                    """
                    
                    # Enhanced prompt for document summary
                    enhanced_prompt = f"""
                    Context: Document Summarization - Financial & Business Analysis
                    
                    Task: Create a comprehensive summary of the provided document
                    
                    Document Content: {text_content}
                    
                    Summary Framework:
                    1. EXECUTIVE SUMMARY: Key points in 2-3 sentences
                    2. MAIN TOPICS: Core themes and subjects covered
                    3. KEY INSIGHTS: Important findings, data, or conclusions
                    4. FINANCIAL IMPLICATIONS: Market impact, investment relevance
                    5. ACTION ITEMS: Recommendations or next steps (if applicable)
                    
                    Summary Requirements:
                    - Write in Vietnamese (as requested)
                    - Use clear, professional language
                    - Highlight critical information with bullet points
                    - Maintain logical flow and structure
                    - Focus on actionable insights
                    - Keep summary concise but comprehensive
                    
                    Please provide a well-structured summary following this framework.
                    """
                    
                    # Generate summary using your existing function
                    response = glib.call_claude_sonet_stream(enhanced_prompt)
                    
                    st.markdown("### 📋 Document Summary")
                    st.markdown('<div class="summary-card">', unsafe_allow_html=True)
                    
                    # Display streaming response
                    summary_placeholder = st.empty()
                    full_summary = ""
                    
                    for chunk in response:
                        full_summary += chunk
                        summary_placeholder.markdown(full_summary)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Additional actions
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("📋 Copy Summary"):
                            st.success("Summary copied to clipboard!")
                    
                    with col2:
                        if st.button("💾 Save Summary"):
                            st.download_button(
                                "Download Summary",
                                full_summary,
                                file_name=f"summary_{uploaded_file.name}.txt",
                                mime="text/plain"
                            )
                    
                    with col3:
                        if st.button("🔄 Regenerate"):
                            st.rerun()
                            
            except Exception as e:
                st.error(f"Error processing document: {str(e)}")

# Sample documents section
st.markdown("### 📚 Try Sample Documents")
st.markdown("Don't have a document ready? Try these sample texts:")

sample_texts = {
    "Financial Report": """
    Q3 2024 Financial Results: Revenue increased 15% year-over-year to $2.8 billion, 
    driven by strong performance in cloud services and AI products. Net income rose 
    22% to $680 million. The company expanded its market share in enterprise software 
    and launched three new AI-powered solutions. Operating expenses increased 8% due 
    to R&D investments. The board approved a $500 million share buyback program.
    """,
    "Market Analysis": """
    The technology sector showed mixed performance in October 2024. While AI and 
    cloud computing stocks gained 12% on average, semiconductor companies declined 
    5% due to supply chain concerns. Interest rate expectations continue to influence 
    market sentiment. Analysts recommend focusing on companies with strong balance 
    sheets and recurring revenue models. The upcoming earnings season will be crucial 
    for determining market direction.
    """,
    "Business Strategy": """
    Our digital transformation initiative aims to modernize operations and improve 
    customer experience. Key objectives include: implementing cloud-based systems, 
    automating manual processes, and developing mobile applications. The project 
    timeline spans 18 months with a budget of $5 million. Expected benefits include 
    30% reduction in processing time and 25% improvement in customer satisfaction. 
    Risk mitigation strategies address cybersecurity and change management challenges.
    """
}

cols = st.columns(3)
for i, (title, text) in enumerate(sample_texts.items()):
    with cols[i]:
        if st.button(f"📄 {title}", use_container_width=True):
            prompt = f"""
            Please provide a medium-length summary of the following {title.lower()}:
            
            {text}
            
            Please structure your summary with:
            1. Main Topic/Purpose
            2. Key Points (3-5 bullet points)
            3. Important Details
            4. Conclusion/Recommendations (if applicable)
            """
            
            st.markdown(f"### 📋 Summary: {title}")
            st.markdown('<div class="summary-card">', unsafe_allow_html=True)
            
            response = glib.call_claude_sonet_stream(prompt)
            summary_placeholder = st.empty()
            full_summary = ""
            
            for chunk in response:
                full_summary += chunk
                summary_placeholder.markdown(full_summary)
            
            st.markdown('</div>', unsafe_allow_html=True)

# Tips section
st.markdown("### 💡 Tips for Better Summaries")
tips_col1, tips_col2 = st.columns(2)

with tips_col1:
    st.markdown("""
    **📝 Document Preparation:**
    - Ensure text is clear and readable
    - Remove unnecessary formatting
    - Include complete sentences and paragraphs
    """)

with tips_col2:
    st.markdown("""
    **🎯 Summary Optimization:**
    - Choose appropriate length for your needs
    - Select relevant focus area
    - Review and refine as needed
    """)
