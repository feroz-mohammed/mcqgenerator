import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgen.utils import read_file,get_table_data
from mcqgen.logger import logging

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

load_dotenv()

KEY=os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(openai_api_key=KEY,model_name = "gpt-3.5-turbo")

TEMPLATE="""Text:{text}
    You are an MCQ maker. Given the above text, it is your job to \
    create a quiz of {number} multiple choice questions for {subject} studenrs is {tone} tone.
    make sure the question are not repeated and check all the questions to be conforming the text as well.
    Make sure tto format your response like RESPONSE_JSON below nd use it as a guide. \
    Ensure to make {number} MCQs
    ### RESPONSE_JSON
    {response_json}
    
    """


quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=TEMPLATE
)

quiz_chain=LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)


TEMPLATE2="""
    You are an expert English grammarian and writer given at multiple choice quiz per {subject} students. \
    You need to evaluate the complexity of the question and give a complete analysis of the quiz.
    Only use at maximum of 50 words per quiz. 
    The quiz is not per with the cognitive and analytical abilities of the student,\
    Compare to quiz, questions which need to be changed and change the tool such that it perfectly fits the student abilities. 
    Quiz_MCQ:
    {quiz}
    
    
check for an expert English writer of the above quiz:
"""

quiz_evaluation_prompt=PromptTemplate(input_variables=["subject", "quiz"], template=TEMPLATE)

review_chain=LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)


generate_evaluate_chain=SequentialChain(chains=[quiz_chain, review_chain], input_variables=["text","number", "subject","tone", "response_json"], 
                                        output_variables=["quiz", "review"], verbose=True,)

