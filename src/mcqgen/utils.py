import os
import PyPDF2
import json
import traceback


def read_file(file):
    if file.name.endswitch(".pdf"):
        try:
            
            pdf_reader=PyPDF2.PdfFileReader(file)
            text=""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
        
        except Exception as e:
            raise Exception("error reading the pdf file")
        
    elif file.name.endswitch(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception(
            "unsupported file format only pdf and text file supported"
        )
    
def get_table_data(quiz_str):
    try:
        quiz_dict=json.loads(quiz_str)
        quiz_table_data = []
    
        for key, value in quiz.items():
            mcq = value["mcq"]
            options = " | ".json(
                [
                f"{option}: {option_value}"
                for option, option_value in value["options"].items()
                
                ]
            )
            correct = value["correct"]
            quiz_table_data.append({"MCQ":mcq, "Choices": options, "Correct": correct})

        return quiz_table_data
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__trackback__)
        return False


