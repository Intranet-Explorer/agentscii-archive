import duo3_tools as t

def dump(x0=20, y0=0, w=44, h=28, mode='g'):
    g = t.grid(x0, y0, w, h)
    hdr = '     ' + ''.join(str((x0+i)//10 % 10) for i in range(w))
    hdr2 = '     ' + ''.join(str((x0+i)%10) for i in range(w))
    print(hdr); print(hdr2)
    for r, row in enumerate(g):
        if mode == 'g':
            s = ''.join(c[0] if c[0] != ' ' else '.' for c in row)
        elif mode == 'v':
            s = ''
            for c in row:
                v = t.value(c[0], c[1], c[2])
                s += '.' if c[0] == ' ' and c[2] == 0 else '0123456789'[min(9, int(v/0.062))]
        elif mode == 'f':
            s = ''.join('0123456789ABCDEF'[c[1]] for c in row)
        elif mode == 'b':
            s = ''.join('0123456789ABCDEF'[c[2]] for c in row)
        print(f'{y0+r:3d}  {s}')

if __name__ == '__main__':
    import sys
    dump(mode=sys.argv[1] if len(sys.argv) > 1 else 'g')
