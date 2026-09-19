from docx import Document

sections = ['summary', 'experience', 'education', 'skills', 'awards']

keyword_dict = ['Python', 'cucumber', 'gherkin', 'Cypress', 'Java', 'Jenkins', 'etl validation', 'pytest', 'git', 'bs', 'bachelor of science',
                'C#', 'QA', 'test engineer', 'senior', 'Sr', 'qa engineer', 'B2B', 'Saas', 'jquery', 'jmeter', 'C++', 'AI', 'Claude']

keyword_lookup_set = {k.casefold() for k in keyword_dict}

def get_file_text(filepath):
    document = Document(filepath)
    full_text = []

    for para in document.paragraphs:
        if para.text.strip():
            full_text.append(para.text)

    keywords_found = [
        k for k in keyword_dict
        if any(k.casefold() in t.casefold() for t in full_text)
    ]
    skills_missing = [
        k for k in keyword_dict
        if not any(k.casefold() in t.casefold() for t in full_text)
    ]

    print(f'Keywords found: {keywords_found}\n Skills missing: {skills_missing}')


    return "\n".join(full_text)

print(get_file_text("C:/Users/Jose/Downloads/Camacho_Jose-resume_QA-Engineer--Siftwell.docx"))