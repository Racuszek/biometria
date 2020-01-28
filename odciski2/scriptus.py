def parse(filename):
    # Given a file with feature vectors, it returns a dictionary, where key is the minutia name
    # and value is list of its feature vectors as tuples. We assume the file contains no double spaces.
    dict_of_minutiae={}
    with open(filename) as file:
        lines=file.read().split('\n')
    # print(lines)
    for line in lines:
        if line=='':
            continue
        else:
            if line[0].isalpha():
                name=line.split()[0]
                print(name)
                globals()[name]=[]
            else:
                vector_as_list=[float(item) for item in line[1:].split(' ')]
                vector_as_tuple=tuple(vector_as_list)
                globals()[name].append(vector_as_tuple)
    dict_of_minutiae['rozwidlenia']=rozwidlenia
    dict_of_minutiae['zakonczenia']=zakonczenia
    dict_of_minutiae['rdzen_delta']=rdzen_delta

    return dict_of_minutiae

# print(parse('kciuk_p_01.txt'))

