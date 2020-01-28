def parse(filename):
    with open(filename) as file:
        lines=file.read().split('\n')
    # print(lines)
    for line in lines:
        if line=='':
            continue
        else:
            if line[0].isalpha():
                name=line.split(' ')[0]
            else:
                print('* ')

parse("kciuk_p_01.txt")
print(rozwidlenia)
