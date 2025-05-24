import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgen.utils import read_file,get_table_data
import streamlit as st
from langchain .callbacks import get_openai_callback
from src.mcqgen.MCQ_Generator import generate_evaluate_chain
from src.mcqgen.logger import logging

with open('C:\Users\MOHAMMED FEROZ\mcqgenerator\Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)

st.title("mcq creator application langchain")

with st.form("user_inputs"):
    uploaded_file=st.file_uploader("upload a pdf or text file")

    mcq_count=st.number_input("no. of MCWs", min_value=3, max_value=50)

    subject=st.text_input("insert subkect", max_chars=20)
    tone=st.text_input("complexity level of questions", max_chars=20, placeholder="simple")
    button=st.form_submit_button("create mcqs")


    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text=read_file(uploaded_file)
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain({
                        "text": TEXTS,
                        "number": NUMBER,
                        "subject": SUBJECT,
                        "tone": TONE,
                        "response_json": json.dumps(RESPONSE_JSON)

                            }
                    )
            except Exception as e:
                traceback.print_exception(type(e), e, e.__trackback__)
                st.error("Error")

            else:
                print(f"Total Tokens:{cb.total_tokens}")
                print(f"Ptompt Tokens:{cb.prompt_tokens}")
                print(f"Completion Tokens:{cb.completion_tokens}")
                print(f"Total Cost:{cb.total_cost}")
                if instances(response, dict):
                    quiz=response.get("quiz", None)
                    if quiz is not None:
                        table_data=get_table_data(quiz)
                        if table_data is not None:
                            df=pd.DataFrame(table_data)
                            df.index=df.index+1
                            st.table(df)
                            st.text_area(label="Review", value=response["review"])
                        else:
                            st.error("error in the table data")
                
                else:
                    st.write(response)
