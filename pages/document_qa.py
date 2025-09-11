import streamlit as st
import streamlit.components.v1 as components
import libs as glib 
import base

# Modern CSS styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #ffecd2 0%, #fcb69f 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: #333;
    }
    .qa-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .document-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #fcb69f;
    }
    .question-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border: 1px solid #e9ecef;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .question-card:hover {
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    .answer-section {
        background: #e8f5e8;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #28a745;
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
    <h1>❓ Document Q&A</h1>
    <p>Ask questions about your documents and get AI-powered answers</p>
</div>
""", unsafe_allow_html=True)

base.init_slidebar()

# Initialize session state for document content
if 'document_content' not in st.session_state:
    st.session_state.document_content = ""
if 'qa_history' not in st.session_state:
    st.session_state.qa_history = []

# Document upload section
st.markdown("### 📤 Upload Document")
uploaded_file = st.file_uploader(
    "Choose a document to analyze",
    type=['txt', 'pdf', 'docx', 'md', 'py', 'js', 'html', 'css', 'json'],
    help="Upload a document to ask questions about its content"
)

# Process uploaded document
if uploaded_file is not None:
    try:
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
                    if paragraph.text:
                        content += paragraph.text + "\n"
            except ImportError:
                st.warning("DOCX processing requires python-docx. Please install it or use text files.")
                content = None
        else:
            # Try to read as text anyway
            try:
                content = str(uploaded_file.read(), "utf-8")
            except:
                st.error("Unsupported file type. Please use text files (.txt), PDF, or DOCX files.")
                content = None
        
        if content and content.strip():
            st.session_state.document_content = content
            st.success(f"✅ Document loaded: {uploaded_file.name}")
        else:
            st.error("❌ Could not extract text from the document. Please try a different file.")
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")

# Sample document option
if not st.session_state.document_content:
    st.markdown("### 📚 Or Try a Sample Document")
    
    sample_doc = st.selectbox("Choose a sample document:", [
        "Select a sample...",
        "Financial Report",
        "Market Analysis", 
        "Business Strategy",
        "Technical Documentation"
    ])
    
    sample_contents = {
        "Financial Report": """
        Q3 2024 Financial Results Summary
        
        Revenue Performance:
        - Total revenue: $2.8 billion (15% YoY growth)
        - Cloud services revenue: $1.2 billion (25% YoY growth)
        - AI products revenue: $450 million (40% YoY growth)
        - Traditional software: $1.15 billion (5% YoY growth)
        
        Profitability:
        - Gross margin: 68% (up from 65% last year)
        - Operating income: $840 million (20% YoY growth)
        - Net income: $680 million (22% YoY growth)
        - Earnings per share: $2.45 (vs $2.01 last year)
        
        Key Metrics:
        - Customer acquisition cost decreased 12%
        - Customer lifetime value increased 18%
        - Monthly recurring revenue: $95 million
        - Churn rate: 3.2% (industry average: 5.1%)
        
        Strategic Initiatives:
        - Launched 3 new AI-powered solutions
        - Expanded into European markets
        - Acquired two complementary startups
        - Increased R&D spending by 15%
        
        Outlook:
        - Q4 revenue guidance: $3.0-3.2 billion
        - Full year 2024 revenue expected: $11.5-12.0 billion
        - Planning to hire 500 additional engineers
        - $500 million share buyback program approved
        """,
        
        "Market Analysis": """
        Technology Sector Analysis - October 2024
        
        Market Overview:
        The technology sector experienced mixed performance in October 2024, with significant divergence between subsectors. Overall, the tech-heavy NASDAQ gained 3.2% for the month, outperforming the broader S&P 500.
        
        Subsector Performance:
        - Artificial Intelligence: +12.5% (driven by breakthrough announcements)
        - Cloud Computing: +8.7% (strong enterprise adoption)
        - Semiconductors: -5.2% (supply chain concerns)
        - Cybersecurity: +6.1% (increased enterprise spending)
        - Social Media: -2.3% (regulatory pressures)
        
        Key Drivers:
        1. AI Revolution: Major tech companies reported significant AI revenue growth
        2. Interest Rates: Fed signals of potential rate cuts boosted growth stocks
        3. Earnings Season: 78% of tech companies beat earnings expectations
        4. Geopolitical Tensions: Trade concerns affected semiconductor stocks
        
        Investment Themes:
        - Focus on companies with strong recurring revenue models
        - AI-enabled businesses showing pricing power
        - Cloud infrastructure providers benefiting from digital transformation
        - Cybersecurity firms with government contracts
        
        Risk Factors:
        - Regulatory scrutiny of big tech companies
        - Potential economic slowdown affecting enterprise spending
        - Currency headwinds for multinational corporations
        - Talent acquisition costs rising in competitive markets
        
        Outlook:
        Analysts remain cautiously optimistic about the tech sector heading into 2025, with particular strength expected in AI, cloud services, and cybersecurity segments.
        """,
        
        "Business Strategy": """
        Digital Transformation Strategy 2024-2026
        
        Executive Summary:
        Our organization is embarking on a comprehensive digital transformation initiative to modernize operations, enhance customer experience, and maintain competitive advantage in an increasingly digital marketplace.
        
        Strategic Objectives:
        1. Operational Excellence
           - Automate 60% of manual processes
           - Reduce operational costs by 25%
           - Improve process efficiency by 40%
        
        2. Customer Experience
           - Launch mobile-first customer portal
           - Implement AI-powered customer service
           - Achieve 90% customer satisfaction score
        
        3. Data-Driven Decision Making
           - Establish centralized data platform
           - Deploy advanced analytics capabilities
           - Train 200+ employees in data literacy
        
        Implementation Roadmap:
        
        Phase 1 (Months 1-6): Foundation
        - Cloud infrastructure migration
        - Core system modernization
        - Employee training programs
        - Budget: $2.5 million
        
        Phase 2 (Months 7-12): Enhancement
        - Customer portal development
        - Process automation deployment
        - Analytics platform implementation
        - Budget: $1.8 million
        
        Phase 3 (Months 13-18): Optimization
        - AI/ML model deployment
        - Advanced reporting systems
        - Performance optimization
        - Budget: $700,000
        
        Expected Benefits:
        - 30% reduction in customer service response time
        - 25% improvement in operational efficiency
        - $3.2 million annual cost savings by year 3
        - 15% increase in customer retention
        
        Risk Mitigation:
        - Cybersecurity framework enhancement
        - Change management program
        - Vendor diversification strategy
        - Continuous monitoring and adjustment protocols
        
        Success Metrics:
        - System uptime: 99.9%
        - User adoption rate: 85%
        - ROI achievement: 18 months
        - Employee satisfaction: 80%+
        """
    }
    
    if sample_doc != "Select a sample..." and sample_doc in sample_contents:
        st.session_state.document_content = sample_contents[sample_doc]
        st.success(f"✅ Sample document loaded: {sample_doc}")

# Q&A Interface
if st.session_state.document_content:
    st.markdown("### 💬 Ask Questions About Your Document")
    
    # Display document preview
    with st.expander("📄 Document Preview", expanded=False):
        st.markdown('<div class="document-section">', unsafe_allow_html=True)
        st.text_area("Document Content", st.session_state.document_content, height=200, disabled=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Suggested questions
    st.markdown("### 💡 Suggested Questions")
    suggested_questions = [
        "What are the main points of this document?",
        "What are the key financial metrics mentioned?",
        "What are the biggest risks or challenges identified?",
        "What are the next steps or recommendations?",
        "Can you explain the most important findings?",
        "What timeline or deadlines are mentioned?"
    ]
    
    cols = st.columns(3)
    for i, question in enumerate(suggested_questions):
        with cols[i % 3]:
            if st.button(question, key=f"suggested_{i}"):
                # Add to Q&A history and process
                st.session_state.qa_history.append({
                    "question": question,
                    "answer": "Processing..."
                })
                st.rerun()
    
    # Custom question input
    st.markdown('<div class="qa-container">', unsafe_allow_html=True)
    
    question = st.text_input(
        "Ask your question:",
        placeholder="What would you like to know about this document?",
        key="question_input"
    )
    
    if st.button("🔍 Get Answer", use_container_width=True) and question:
        # Process the question
        prompt = f"""
        Based on the following document, please answer this question: "{question}"
        
        Document:
        {st.session_state.document_content}
        
        Please provide a clear, accurate answer based only on the information in the document. 
        If the information is not available in the document, please say so.
        """
        
        with st.spinner("🤔 Analyzing document and generating answer..."):
            try:
                response = glib.call_claude_sonet_stream(prompt)
                
                # Collect the full response
                full_answer = ""
                answer_placeholder = st.empty()
                
                for chunk in response:
                    full_answer += chunk
                    answer_placeholder.markdown(f"**Answer:** {full_answer}")
                
                # Add to history
                st.session_state.qa_history.append({
                    "question": question,
                    "answer": full_answer
                })
                
            except Exception as e:
                st.error(f"Error generating answer: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display Q&A History
    if st.session_state.qa_history:
        st.markdown("### 📝 Q&A History")
        
        for i, qa in enumerate(reversed(st.session_state.qa_history)):
            with st.expander(f"Q: {qa['question']}", expanded=(i == 0)):
                st.markdown('<div class="answer-section">', unsafe_allow_html=True)
                st.markdown(f"**A:** {qa['answer']}")
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Clear history button
        if st.button("🗑️ Clear Q&A History"):
            st.session_state.qa_history = []
            st.rerun()

else:
    # No document loaded
    st.markdown("""
    <div class="document-section">
        <h3>📋 How to Use Document Q&A</h3>
        <ol>
            <li><strong>Upload a document</strong> or select a sample document</li>
            <li><strong>Ask questions</strong> about the content using natural language</li>
            <li><strong>Get AI-powered answers</strong> based on the document content</li>
            <li><strong>Explore further</strong> with follow-up questions</li>
        </ol>
        
        <h4>💡 Example Questions You Can Ask:</h4>
        <ul>
            <li>"What are the main conclusions?"</li>
            <li>"What numbers or statistics are mentioned?"</li>
            <li>"What are the key recommendations?"</li>
            <li>"Can you summarize the risks mentioned?"</li>
            <li>"What timeline is discussed?"</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("🔧 **Tip:** Ask specific questions to get more detailed and accurate answers from your documents!")
