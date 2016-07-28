import re

p = re.compile(r'(\w+) (\w+)')
s = 'i say miss, hello world good!, i say miss'
parse=p.sub(r'\2 \1', s)
print(parse,"parse")

def func(m):
    print("func:",m)
    return m.group(1).title() + ' ' + m.group(2).title
print(p.sub(func, s))