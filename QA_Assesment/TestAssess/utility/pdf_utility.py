from PyPDF2 import PdfReader
import re

def fetch_substring(input_string, start_char, end_char):
    start_index = input_string.find(start_char)
    if not end_char == -1:
        end_index = input_string.find(end_char, start_index + 1)
    else:
        end_index = -1
    
    if start_index != -1 and end_index != -1:
        result_substring = input_string[start_index + len(start_char):end_index]
        return result_substring.strip()  # Remove leading and trailing whitespaces
    elif start_index != -1 and end_index == -1:
        result_substring = input_string[start_index + len(start_char):]
        return result_substring.strip()
    else:
        return None
    

def extract_pdf_text(filepath,typ):
    with open(filepath,'rb') as pdf:
        reader = PdfReader(pdf)
        results = []
        for i in range(len(reader.pages)):
            page = reader.pages[i]
            text = page.extract_text()
            results.append(text)
        result = ' '.join(results)
        result = result.replace('\n', ' ')

    QA = re.split(r'Question \d+\.\d+', result)[1:]
    sections = re.findall(r'Question \d+\.\d+', result)

    for i in range(len(QA)):
        QA[i] = sections[i] + QA[i]

    if typ == 'Teacher':
        answer = 'Instructions to marker:'
    else:
        answer = 'Answer:'

    final_QA = []
    for i in range(len(QA)):
        qa_dict = {}
        qa_dict['section'] = sections[i].split()[1].split('.')[0]
        qa_dict['question_no'] = sections[i].split()[1].split('.')[1]
        qa_dict['question'] = fetch_substring(QA[i],'Question:','(')
        qa_dict['marks'] = fetch_substring(QA[i],'(',')')
        qa_dict['answer'] = fetch_substring(QA[i],answer,-1)
        final_QA.append(qa_dict)

    return QA,final_QA



def evaluate_pdf(QA,typ):
    errors =[]
    q = None
    cur_que_no = None
    cur_section_no = None
    if typ == 'Teacher':
        answer = 'Instructions to marker:'
    else:
        answer = 'Answer:'
    for i in QA:
        # print(i)
        if not re.search(r'Question \d+\.\d+',i):
            print("checking section")
            if q is not None:
                errors.append(f"There is a problem with Section and Question number after {q}")
            else:
                errors.append("There is a problem with Section and Question number in first question")
        else:
            q = re.findall(r'Question \d+\.\d+',i)[0]
            # print(q)
            cur_section_no = q.split()[1].split('.')[0]
            cur_que_no = section_no = q.split()[1].split('.')[1]
            if not re.search(r'Question:',i):
                print("checking Question")
                errors.append(f"There is a problem with Question: in {q}, also please check spelling of question or : is missing")
            else:
                if not re.search(r'Instructions to marker:',i):
                    print('checking Instruction')
                    errors.append(f"There is a problem with Instructions to marker: in {q}, also please check spelling of Instructions to marker:")
                else:
                    print("checking marks")
                    check_marks_string = fetch_substring(i,'Question:',answer)
                    # print(check_marks_string)
                    if not re.search(r'.*\(\d+ mark(s)?\)$',check_marks_string):
                        errors.append(f"There is a problem with Marks in {q}, also please check spelling of Marks or check if ( or ) is missing.")
    return errors



def evaluate_student_pdf(QA):
    errors =[]
    q = None
    cur_que_no = None
    cur_section_no = None
    for i in QA:
        # print(i)
        if not re.search(r'Question \d+\.\d+',i):
            if q is not None:
                errors.append(f"There is a problem with Section and Question number after {q}")
            else:
                errors.append("There is a problem with Section and Question number in first question")
        else:
            q = re.findall(r'Question \d+\.\d+',i)[0]
            # print(q)
            section_no = q.split()[1].split('.')[0]
            que_no = section_no = q.split()[1].split('.')[1]
            if not re.search(r'Question:',i):
                print("checking Question")
                errors.append(f"There is a problem with Question: in {q}, also please check spelling of question or : is missing")
            else:
                if not re.search(r'Answer:',i):
                    print('checking Instruction')
                    errors.append(f"There is a problem with Instructions to marker: in {q}, also please check spelling of Instructions to marker:")
                else:
                    print("checking marks")
                    check_marks_string = fetch_substring(i,'Question:','Answer:')
                    # print(check_marks_string)
                    if not re.search(r'.*\(\d+ mark(s)?\)$',check_marks_string):
                        errors.append(f"There is a problem with Marks in {q}, also please check spelling of Marks or check if ( or ) is missing.")
    return errors