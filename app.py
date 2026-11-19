import streamlit as st
from groq import Groq
st.set_page_config(page_title = "AI Interview Assistant", page_icon = "🪷",layout='centered')
st.title("AI Interview Assistant")
st.caption("Practice and Prepare for your Placements here")
st.caption("Launched by Kusuma S")
try:
  client = Groq(api_key = st.secrets["GROQ_API_KEY"])
except (KeyError, FileNotFoundError):
  st.error("API Key is missing. Add it in Advanced settings")
  st.stop()
role = st.selectbox("Job Title",['Machine Learning Engineer','AI Engineer','Senior Software Engineer','DevOps Engineer'])
if role == "Other":
  st.text_input('Enter your Job Title','xxxxxxxxx')
gen_model = st.selectbox('Model',['openai/gpt-oss-120b','openai/gpt-oss-20b'])
level = st.selectbox('Level',['Beginner','intermediate','Advance'])
mode = st.radio('Activity',['Generate Questions','Generate code Questions','Evaluate Answers','Improve Answers'])
if mode == 'Generate Questions':
  count = st.slider("Number of Questions",1,10,5)
elif mode == 'Generate Code Questions':
  topic = st.selectbox('Topics',['SQL','AIML','Python','DSA','DevOps''c/c++'])
  count = st.slider("Number of Questions",1,10,5)
else:
  question = st.text_area('Enter Interview Question here')
  answer = st.text_area('Enter your answer',height =160)

if st.button("Generate AI response", type='primary'):
  if mode == ['Evalute Answer', 'Improve Answers'] and(not question.strip() or not answer.strip()):
    st.warning("Please enter a valid Question and Answer")
    st.stop()
    
  if mode == 'Generate Questions':
    task = "Genarate" + str(count) + " Frequency asked Interview Question 3 theory and 2 scenario questions. Do not give answers, Gits Hints."
  elif mode == 'Genarate Code Questions':
    task = "Genarate" + str(count) + " Frequency asked coding question on topic" + topic + "and give hints to solve them. Be accurate "
  elif mode == 'Evaluate Answers':
    task = "Question : " + question + " My Answer :" +answer +"Evaluate this answer based on concept, relevance, communicationm length of answer. Give each rating out of 5 in a list."
  elif mode == 'Improve Answers':
    task =  "Question : " + question + " My Answer :" +answer + "Improve the answer based on choice of words, key words to include,accurate,concise and clear answer."
  background = "Job role :" + role+ " Difficlut level" + level
  with st.spinner("Genrating your answer..."):
      try:
        req = client.chat.completions.create(
          model = gen_model,
          messages = [{"role":"system",
                     "content":"Act as a Senior interview,both HR and Technical expert"},
                  {"role":"user",
                   "content" : background +task}],
          temperature = 0.7,
          max_tokens = 1800
        )
        output = req.choices[0].message.content
        st.subheader("AI Response")
        st.markdown(output)
        st.download_button("Download Response",output, file_name = "Interview_Response.txt", mime = "text/plain")
      except Exception as e:
       st.error("API connenction was unsuccessful: ",e)
       st.info("Please check your API Key and rate limits") 
  st.caption("Powered by streamlit.io and Github. Using LLM API")

              
