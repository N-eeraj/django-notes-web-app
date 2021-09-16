def skip_line(lines):
    data = list()
    for i in range(len(lines)):
        if i % 2 == 0:
            data.append(lines[i].replace('\n', ''))
    return data