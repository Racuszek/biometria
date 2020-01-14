arr=[]
# names=['kciuk_p_0', 'srodkowy_p_0', 'serdeczny_l_0', 'wskazujacy_p_0']
names=['kciuk_p_0']
for name in names:
#     for i in range(1, 4):
    for i in range(1, 2):
        file=open(name+str(i)+'.txt')
        all_lines=file.read().split('\n')
        for line in all_lines:
            if len(line)==0:
                continue;
            if line[0].isalpha():
                print(line)
            else:
                arr.append((line.split()[0], line.split()[1], line.split()[2]))
print(arr)
