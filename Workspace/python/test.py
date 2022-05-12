
a = [1, 2, 3]
print(a[:-1])

b = '5'
print(int(b))

c = 'Je suis ddtoi'
c = c[:-4]
print(c)

d = [1]
if d:
    print('a')

e = ['1', '2', '3', '4', '5', '6']
e = list(map(lambda x: x.replace('1', '10'), e))
print(e)

f = 'AA '.join(['5', '55'])
print(f)