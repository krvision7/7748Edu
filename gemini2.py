import streamlit as st
import google.generativeai as genai
import PyPDF2
import os

# Streamlit 페이지 설정
st.set_page_config(page_title="Gemini PDF Assistant")
st.title("AI 연구 논문 분석기")
st.markdown("""
### 🤖 AI Research Paper Review Team
1. **Sam (AI PhD)**: 논문 내용을 간단한 용어로 설명
2. **Jenny (AI & Education PhD)**: Sam의 분석을 더 쉽게 설명하고 보완
3. **Will (팀 리더)**: 최종 보고서 완성
""")

# API 키 입력 섹션
api_key = st.text_input("Google API 키를 입력하세요:", type="password")

if api_key:
    # Gemini API 설정
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    # PDF 파일 경로 입력
    pdf_path = st.text_input("PDF 파일의 경로를 입력하세요:", 
                            placeholder="예: C:/Users/Documents/example.pdf")

    if pdf_path and os.path.exists(pdf_path):
        try:
            # PDF 파일 읽기
            pdf_reader = PyPDF2.PdfReader(pdf_path)
            text_content = ""
            
            # PDF의 모든 페이지 텍스트 추출
            for page in pdf_reader.pages:
                text_content += page.extract_text()

            # 텍스트 내용 표시
            st.write("PDF 내용:")
            st.write(text_content[:1000] + "...") # 처음 1000자만 표시

            # 사용자 질문 입력
            user_question = st.text_input("PDF에 대해 질문하세요:")

            # 분석 단계 선택
            analysis_stage = st.radio(
                "분석 단계를 선택하세요:",
                ["Sam의 초기 분석", "Jenny의 검토 및 보완", "Will의 최종 보고서"]
            )

            if user_question:
                # 각 역할에 맞는 프롬프트 생성
                prompts = {
                    "Sam의 초기 분석": f"""
                    당신은 AI PhD 출신 Sam입니다. 다음 논문을 읽고 핵심 내용을 간단히 설명해주세요:
                    문서 내용: {text_content}
                    질문: {user_question}
                    
                    주요 포인트와 방법론, 연구 결과를 명확하게 설명해주세요.
                    """,
                    
                    "Jenny의 검토 및 보완": f"""
                    당신은 AI와 교육 분야 PhD를 가진 Jenny입니다. Sam의 분석을 검토하고 더 쉽게 설명해주세요:
                    문서 내용: {text_content}
                    질문: {user_question}
                    
                    실제 응용 사례를 포함하고 더 넓은 독자층이 이해할 수 있도록 설명해주세요.
                    """,
                    
                    "Will의 최종 보고서": f"""
                    당신은 팀 리더 Will입니다. 다음 내용을 종합적으로 분석하여 최종 보고서를 작성해주세요:
                    문서 내용: {text_content}
                    질문: {user_question}
                    
                    다음 구조로 보고서를 작성해주세요:
                    1. 핵심 요약
                    2. 연구 주제 소개
                    3. 주요 발견 및 방법론
                    4. 복잡한 개념의 쉬운 설명
                    5. 실제 응용 및 시사점
                    6. 결론 및 향후 연구 방향
                    """
                }
                
                response = model.generate_content(prompts[analysis_stage])
                
                st.write(f"### {analysis_stage} 결과:")
                st.write(response.text)

        except Exception as e:
            st.error(f"PDF 파일을 처리하는 중 오류가 발생했습니다: {str(e)}")
    
    elif pdf_path:
        st.error("입력한 경로에 PDF 파일이 존재하지 않습니다.")

else:
    st.warning("API 키를 입력해주세요.")
