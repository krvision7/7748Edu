import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import io

# PDF 파일 읽기 함수
def read_pdf(uploaded_file):
    pdf_reader = PdfReader(io.BytesIO(uploaded_file.getvalue()))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Streamlit 앱 설정
st.title("AI 연구 논문 리뷰 팀")

# 팀 구조 및 역할 설명
st.header("팀 구조 및 역할")
st.markdown("""
1. Sam (AI PhD): 
   - 논문 내용을 주의 깊게 읽고 핵심 포인트, 방법론, 발견 사항을 파악합니다.
   - 논문의 내용을 간단한 용어로 설명하는 초기 초안을 작성합니다.
   - 정확성에 중점을 두면서 명확성을 목표로 합니다.

2. Jenny (AI & 교육 PhD): 
   - Sam의 초기 초안을 검토합니다.
   - 더 나은 이해를 위해 언어를 더욱 단순화합니다.
   - 관련된 교육적 맥락과 실제 응용 사례를 추가합니다.
   - 추가 설명이 필요한 영역을 확장합니다.
   - 내용이 더 넓은 청중에게 접근 가능하도록 합니다.

3. Will (팀 리더): 
   - Sam과 Jenny의 기여를 검토합니다.
   - 원본 논문의 모든 핵심 포인트가 다루어졌는지 확인합니다.
   - 단순화된 설명의 정확성을 검증합니다.
   - 보고서 전체에 걸쳐 일관된 톤과 스타일을 유지합니다.
   - 누락된 중요 정보를 추가합니다.
   - 최적의 가독성을 위해 최종 보고서를 구조화합니다.
""")

st.header("최종 보고서 구조")
st.markdown("""
1. 요약
2. 연구 주제 소개
3. 주요 발견 및 방법론
4. 복잡한 개념의 간단한 설명
5. 실제 응용 및 영향
6. 결론 및 향후 연구 방향
""")

# API 키 입력 받기
api_key = st.text_input("Gemini API 키를 입력하세요:", type="password")

if api_key:
    # Gemini API 키 설정
    genai.configure(api_key=api_key)

    # PDF 파일 업로드 기능 추가
    uploaded_file = st.file_uploader("AI 연구 논문 PDF 파일을 업로드하세요", type="pdf")

    if uploaded_file is not None:
        pdf_content = read_pdf(uploaded_file)
        
        # 각 팀원의 분석 결과를 저장할 변수
        sam_analysis = ""
        jenny_review = ""
        will_final_report = ""
        
        # Sam의 초기 분석
        if st.button("Sam의 초기 분석 시작"):
            try:
                model = genai.GenerativeModel('gemini-pro')
                prompt = f"""당신은 Sam입니다. AI PhD 졸업생으로 복잡한 AI 개념을 분석하는 전문가입니다. 
                다음 AI 연구 논문의 내용을 주의 깊게 읽고, 핵심 포인트, 방법론, 발견 사항을 파악하여 
                간단한 용어로 설명해주세요. 정확성에 중점을 두면서 명확성을 목표로 하세요:\n\n{pdf_content}"""
                response = model.generate_content(prompt)
                sam_analysis = response.text
                st.write("Sam의 분석:")
                st.write(sam_analysis)
            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}")
        
        # Jenny의 리뷰 및 개선
        if sam_analysis and st.button("Jenny의 리뷰 시작"):
            try:
                model = genai.GenerativeModel('gemini-pro')
                prompt = f"""당신은 Jenny입니다. AI와 교육 분야의 PhD를 보유하고 있습니다. 
                Sam의 초기 분석을 검토하고 더 단순화하세요. 교육적 맥락과 실제 응용 사례를 추가하고, 
                필요한 영역을 확장하여 더 넓은 청중이 이해할 수 있도록 만드세요:\n\n{sam_analysis}"""
                response = model.generate_content(prompt)
                jenny_review = response.text
                st.write("Jenny의 리뷰:")
                st.write(jenny_review)
            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}")
        
        # Will의 최종 리뷰 및 컴파일
        if jenny_review and st.button("Will의 최종 보고서 작성"):
            try:
                model = genai.GenerativeModel('gemini-pro')
                prompt = f"""당신은 Will입니다. 팀 리더로서 최종 보고서를 작성해야 합니다. 
                Sam과 Jenny의 기여를 검토하고, 원본 논문의 모든 핵심 포인트가 다루어졌는지 확인하세요. 
                단순화된 설명의 정확성을 검증하고, 일관된 톤과 스타일을 유지하며, 누락된 중요 정보를 추가하세요. 
                다음 구조를 따라 최종 보고서를 작성해주세요:

                1. 요약
                2. 연구 주제 소개
                3. 주요 발견 및 방법론
                4. 복잡한 개념의 간단한 설명
                5. 실제 응용 및 영향
                6. 결론 및 향후 연구 방향

                Sam의 분석: {sam_analysis}

                Jenny의 리뷰: {jenny_review}"""
                response = model.generate_content(prompt)
                will_final_report = response.text
                st.write("Will의 최종 보고서:")
                st.write(will_final_report)
            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}")
    else:
        st.warning("PDF 파일을 업로드해주세요.")
else:
    st.warning("API 키를 입력해주세요.")
