import pdfplumber


def flatten(xss):
    return [x for xs in xss for x in xs]


def remove_all(x, ele):
    return list(filter(lambda a: a != ele, x))


def join_all(subjects):
    condition = all(s[0].isupper() for s in subjects)
    if condition:
        return subjects
    else:
        cleaned_subjects = []
        for i, v in enumerate(subjects):
            if v.islower():
                cleaned_subjects.pop()
                cleaned_subjects.append(" ".join((subjects[i - 1], v)))
            else:
                cleaned_subjects.append(v)
        return join_all(cleaned_subjects)


def extract_bold_text(pages):
    all_text = []
    for page in pages:
        clean_text = page.filter(
            lambda obj: obj["object_type"] == "char" and "Bold" in obj["fontname"]
        )
        text = clean_text.extract_text()
        if text:
            split_text = text.split("\n")
            all_text.append(split_text)
    return all_text


def extract_topics_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        page_start_index, page_end_index = 0, 0

        # Get Start/End Topic List
        all_text = extract_bold_text(pdf.pages)
        for page in all_text:
            if page_start_index == page_end_index:
                for i, s in enumerate(page):
                    if "SUBJECT CONTENT" in s:
                        page_start_index = int(s.split()[-1]) - 1
                        page_end_index = int(page[i + 1].split()[-1]) - 1
        subjects = remove_all(
            flatten(extract_bold_text(pdf.pages[page_start_index:page_end_index])),
            "Topic/Sub-topics Content",
        )
        cleaned_subjects = join_all(subjects)
        return cleaned_subjects[1:]


# Extract SEAB Syllabus topics with `extract_topics_from_pdf(pdf_path)`
# pdf_path = "olevel4048mathsyllabus.pdf"  # Replace with your PDF file path
# topics = extract_topics_from_pdf(pdf_path)
# print(topics)
