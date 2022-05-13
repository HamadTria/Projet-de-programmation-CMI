
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

a = {'A': 1, 'B': 2}
print(a['A'])

a = 'Je suis {0} {0} !'.format('1', '2')
print(a)

a = 'Okiland'
b = f'O-{a}'
print(b)