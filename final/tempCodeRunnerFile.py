def extract_headings_and_sentences(text):
    headings = []
    sentences = []
    current_heading = ''
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if is_heading(line):
            current_heading = line
        else:
            if current_heading:
                headings.append(current_heading)
                sentences.append(line)
            else:
                sentences[-1] += ' ' + line if len(sentences) > 0 else line

    return headings, sentences