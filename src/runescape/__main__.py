import math

from .file_models import read_file


def find_amounts(mat):
    exp = input('Wanted Smithing EXP: ')
    reqs, exps = mat.make_from([])
    smith_exp = next(e for e in exps if e.item == 'Smithing')
    amount_needed = math.ceil(int(exp) / smith_exp.amount)
    reqs *= amount_needed
    print('You need:')
    for req in reqs:
        print(f'{req.amount} {req.item.name}')

    print('You get:')
    exps *= amount_needed
    for exp in exps:
        print(f'{exp.amount} {exp.item} exp')
    print(f'{amount_needed} {mat.item.name}')


if __name__ == '__main__':
    mats = read_file('./runescape/mats.json')
    find_amounts(mats['Necronium Platebody+4'])

