from src.composer import shift, shift_melodic, reverse, \
    reverse_melodic, reverse_shift, reverse_shift_melodic, inverse_shift, inverse_reverse_shift, \
    inverse_shift_melodic, inverse_reverse_shift_melodic


def testing(name, func):
    print(f'Testing function {name}\n')
    for n in range(8, 17, 2):
        print(f'Testing note number {n}')
        pri, sec = func(n)
        print(pri)
        print(sec)
    print('\n')


if __name__ == '__main__':
    testing('shift', shift)
    testing('shift_melodic', shift_melodic)
    testing('reverse', reverse)
    testing('reverse_melodic', reverse_melodic)
    testing('reverse_shift', reverse_shift)
    testing('reverse_shift_melodic', reverse_shift_melodic)
    testing('inverse_shift', inverse_shift)
    testing('inverse_shift_melodic', inverse_shift_melodic)
    testing('inverse_reverse_shift', inverse_reverse_shift)
    testing('inverse_reverse_shift_melodic', inverse_reverse_shift_melodic)
