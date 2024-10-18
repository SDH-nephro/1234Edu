import streamlit as st
import google.generativeai as genai
import os
from PyPDF2 import PdfReader

# Streamlit 앱 제목 설정
st.title("AI Research Paper Review Team")

# 팀 구조 및 역할 설명
st.header("Team Structure")
st.markdown("""
1. **Sam (AI PhD)**: Explains paper content in simple terms
2. **Jenny (AI & Education PhD)**: Simplifies and expands on Sam's draft
3. **Will (Team Leader)**: Finalizes the report
""")

# 워크플로우 설명
st.header("Workflow")
st.markdown("""
1. **Sam's Initial Analysis**: Identify key points and create an initial draft
2. **Jenny's Review**: Simplify and expand on Sam's draft
3. **Will's Final Review**: Compile and finalize the report
""")

# 사용자로부터 API 키 입력 받기
api_key = st.text_input("Gemini API 키를 입력하세요:", type="password")

# PDF 파일 업로드
uploaded_file = st.file_uploader("연구 논문 PDF를 업로드하세요", type="pdf")

# API 키가 입력되었을 때만 처리 진행
if api_key and uploaded_file:
    # Gemini API 설정
    genai.configure(api_key=api_key)

    # PDF 파일 읽기
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    # 텍스트 출력 (디버깅 용도)
    st.text("PDF 내용 (처음 500자):")
    st.text(text[:500] + "...")

    # Gemini 모델 설정
    model = genai.GenerativeModel('gemini-pro')

    # Sam의 초기 분석
    st.subheader("1. Sam's Initial Analysis")
    sam_prompt = f"You are Sam, an AI PhD. Analyze the following research paper and provide a simple explanation of its key points, methodologies, and findings:\n\n{text}"
    sam_response = model.generate_content(sam_prompt)
    st.write(sam_response.text)

    # Jenny의 리뷰 및 개선
    st.subheader("2. Jenny's Review and Enhancement")
    jenny_prompt = f"You are Jenny, with PhDs in AI and Education. Review and simplify Sam's analysis, adding educational context and real-world applications:\n\n{sam_response.text}"
    jenny_response = model.generate_content(jenny_prompt)
    st.write(jenny_response.text)

    # Will의 최종 리뷰 및 컴파일
    st.subheader("3. Will's Final Review and Compilation")
    will_prompt = f"""You are Will, the team leader. Review both Sam and Jenny's contributions and create a final report with the following structure:
    1. Executive Summary
    2. Introduction to the Research Topic
    3. Key Findings and Methodologies
    4. Simplified Explanation of Complex Concepts
    5. Real-world Applications and Implications
    6. Conclusion and Future Research Directions

    Sam's analysis: {sam_response.text}
    Jenny's review: {jenny_response.text}
    """
    will_response = model.generate_content(will_prompt)
    st.write(will_response.text)

else:
    st.warning("API 키를 입력하고 PDF 파일을 업로드해주세요.")

# 피드백 루프
st.header("Feedback Loop")
feedback = st.text_area("프로세스 개선을 위한 피드백을 입력해주세요:")
if st.button("피드백 제출"):
    st.success("피드백이 제출되었습니다. 감사합니다!")

try:
    import google.generativeai as genai
    st.write(f"Successfully imported google.generativeai version: {genai.__version__}")
except ImportError as e:
    st.error(f"Failed to import google.generativeai: {e}")
    st.error(f"Installed packages: {', '.join(__import__('pkg_resources').working_set.by_key.keys())}")
    raise
