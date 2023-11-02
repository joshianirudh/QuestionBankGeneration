from pdfminer.high_level import extract_text
import streamlit as st
import pandas as pd
import openai
import os


openai.api_key = os.environ['OPENAI_API_KEY']

prompt = ""
instruction = "\nMake sure the questions are correctly numbered\nAlso when answering question just respond with the answer only below each question.\nHere is the text:\n"
ask = "Return only the answer and nothing else for the following questions, number the responses."

def get_questions_answers(msg):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[{'role': 'assistant', 'content': msg}]
    )

    question_answer = response.choices[0].message.content.split('\n')
    question_answer = [i for i in question_answer if i not in ['']]
    return question_answer

def create_question_bank(data, pdf_file):
    #bank = {}
    q = 1
    questions = []
    numbered = []
    answers = []
    for index, val in enumerate(data):
        if str(q)+'.' in val:
            numbered.append(val)
            question = val.replace(str(q)+'.', '')
            answer = []
            for ans in data[index+1:]:
                if str(q+1)+'.' not in ans:
                    answer.append(ans)
                else:
                    break
            questions.append(question)
            answer = " ".join([str(i) for i in answer])
            answers.append(answer)
            q += 1
    df = pd.DataFrame(columns=["Question", "Answer"])
    df['Question'] = questions
    df['Answer'] = answers
    df.to_csv(f"QuestionBank_{pdf_file}.csv")
    st.write(f"Question Bank saved in: /QuestionBank_{pdf_file}.csv 📝")
    print("Question Bank Saved!")
    return df, numbered



def get(pdf_file, question_count):
    st.write(f"You uploaded a PDF {pdf_file.name} and want to generate {num_questions} questions.")
    data = extract_text(pdf_file)
    print("Extracted PDF")
    st.write(f"PDF converted to text📚")
    global prompt
    msg = prompt + f"\nGenerate {question_count} questions" + instruction + data
    question_answer = get_questions_answers(msg)
    print("Created Q&A's")
    question_bank, numbered = create_question_bank(question_answer, pdf_file.name)
    print("Question Bank created ")
    st.write(f"Question Bank Created with {question_count} questions!🕒")
    


st.set_page_config(page_title="QB Generator", layout='wide', initial_sidebar_state='auto', page_icon="🚀")


st.title("Question-Bank Generator: QA dataset creator🏦")

# Upload the PDF file
pdf_file = st.file_uploader("Upload a PDF", type=["pdf"])

# Input for number of questions
num_questions = st.text_input("Enter the number of questions you want to generate")

# Submit button
if st.button("Submit🔍"):
    # Call the submit function
    get(pdf_file, num_questions)