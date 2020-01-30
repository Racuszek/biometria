from math import sqrt

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
                # print(name)
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
def count_mean_tuple(tup1, tup2):
    long_list=[]
    for c, d in zip(tup1, tup2):
        mean_list=[(a+b)/2 for a, b in zip(c, d)]
        long_list.append(tuple(mean_list))
    return tuple(long_list)

# a=((1, 2), (3, 4))
# b=((3, 4), (5, 6))
# test_dict1={'key1': a, 'key2': b}
# test_dict2={'key1': b, 'key2': a}
# print(count_mean_tuple(a, b))

def count_mean_dict(dict1, dict2):
    mean_dict={}
    for key in dict1.keys():
        tup1=dict1[key]
        tup2=dict2[key]
        tup3=count_mean_tuple(tup1, tup2)
        mean_dict[key]=tup3
    return mean_dict

model_kciuk=count_mean_dict(parse('kciuk1.txt'), parse('kciuk2.txt'))
model_wskazujacy=count_mean_dict(parse('wskazujacy1.txt'), parse('wskazujacy2.txt'))
model_srodkowy=count_mean_dict(parse('srodkowy1.txt'), parse('srodkowy2.txt'))
model_serdeczny=count_mean_dict(parse('serdeczny1.txt'), parse('serdeczny2.txt'))

def points_distance(tup1, tup2):
    if len(tup1)==3:
        return sqrt((tup1[0]-tup2[0])**2+(tup1[1]-tup2[1])**2+(tup1[2]-tup2[2])**2)
    elif len(tup1)==2:
        return sqrt((tup1[0]-tup2[0])**2+(tup1[1]-tup2[1])**2)

def sum_distances(dict1, dict2):
    sum=0.
    for key in dict1.keys():
        for f, g in zip(dict1[key], dict2[key]):
            sum+=points_distance(f, g)
            return sum
# sum_distances(test_dict1, test_dict2)
model_kciuk=(count_mean_dict(parse('kciuk2.txt'), parse('kciuk3.txt')))
print(sum_distances(parse('srodkowy1.txt'), model_kciuk))
