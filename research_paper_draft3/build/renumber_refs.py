"""Renumber the references of manuscript_source.txt into order of first citation.

Usage: python -I renumber_refs.py <manuscript_source.txt>
Citations are [n], lists [a], [b] and ranges [a]-[b]; ranges are rebuilt after renumbering.
Fails if a reference is never cited or a citation has no reference."""
import re
import sys

path = sys.argv[1]
text = open(path, encoding='utf-8').read()
head, sep, refs = text.partition('@H1 References\n')
lines = [l for l in refs.split('\n') if l.strip()]
assert all(l.startswith('@REF') for l in lines), 'unexpected line in the reference list'
by_old = {int(re.match(r'@REF \[(\d+)\]', l).group(1)): re.sub(r'^@REF \[\d+\] ', '', l) for l in lines}
group = re.compile(r'\[(\d+)\](?:-\[(\d+)\])?(?:, \[(\d+)\](?:-\[(\d+)\])?)*')
token = re.compile(r'\[(\d+)\](?:-\[(\d+)\])?')
order = []
for line in head.split('\n'):
    for g in group.finditer(line):
        for a, b in token.findall(g.group(0)):
            for n in (range(int(a), int(b) + 1) if b else [int(a)]):
                if n not in order:
                    order.append(n)
assert set(order) == set(by_old), f'uncited {set(by_old) - set(order)}, unknown {set(order) - set(by_old)}'
new = {old: i + 1 for i, old in enumerate(order)}


def fmt(numbers):
    numbers, out, i = sorted(numbers), [], 0
    while i < len(numbers):
        j = i
        while j + 1 < len(numbers) and numbers[j + 1] == numbers[j] + 1:
            j += 1
        out.append(f'[{numbers[i]}]-[{numbers[j]}]' if j - i >= 2 else ', '.join(f'[{n}]' for n in numbers[i:j + 1]))
        i = j + 1
    return ', '.join(out)


def repl(m):
    numbers = []
    for a, b in token.findall(m.group(0)):
        numbers += list(range(int(a), int(b) + 1)) if b else [int(a)]
    return fmt([new[n] for n in numbers])


head = '\n'.join(group.sub(repl, l) for l in head.split('\n'))
open(path, 'w', encoding='utf-8').write(head + sep + '\n'.join(f'@REF [{new[o]}] {by_old[o]}' for o in order) + '\n')
print(f'{len(order)} references renumbered')
