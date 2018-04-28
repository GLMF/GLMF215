import sys
from os.path import splitext

def file2hex(filename, destfile=None):
    if destfile is None:
        destfile = splitext(filename)[0] + '.hex'
    try:
        with open(filename, 'r') as fic, open(destfile, 'w') as out:
           for line in fic:
                #n = 0
                #for pos in range(len(line) - 1):
                #    n += int(line[pos]) * 2 ** pos
                #    pos += 1
                #out.write(hex(n))
                out.write(hex(int(line, 2)))
    except Exception as e:
        print('Error while trying to open files {} and {} : {}'.format(filename, destfile, e))
        exit(2)
    print('File converted to hex in {}'.format(destfile))


if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print('Syntax: asc2hex <infile> [outfile]')
        exit(1)
    if len(sys.argv) == 2:
        file2hex(sys.argv[1])
    else:
        file2hex(sys.argv[1], sys.argv[2])
