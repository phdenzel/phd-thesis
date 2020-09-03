import sys
import os
import numpy as np

repo_root = os.getcwd()
submod_dir = "papers"
tex_dir = "tex"

if len(sys.argv) > 1:
    submodules = sys.argv[1:]
else:
    submodules = os.listdir(os.path.join(repo_root, submod_dir))


def fullpath(d, root=repo_root, subdir=None):
    if subdir is not None:
        path = os.path.join(root, subdir)
    else:
        path = root
    return os.path.join(path, d)

def extract_abstract(path, verbose=False):
    if verbose:
        print(path)
    abstract = []
    with open(path, 'rb') as f:
        text = f.readlines()
    readmode = False
    for line in text:
        if 'begin' in line and 'abstract' in line:
            readmode = True
            continue
        elif 'end' in line and 'abstract' in line:
            readmode = False
            continue
        if readmode:
            abstract.append(line)
    if verbose:
        print("".join(abstract))
    return abstract

def text2file(path, text, postkey='\section*{Abstract}',
              write=True, verbose=False):
    if verbose:
        print(path)
    with open(path, 'rb') as f:
        contents = f.readlines()
    linum = [i+1 for i, line in enumerate(contents) if postkey in line]
    if linum: linum = linum[0]
    if '%' in contents[linum]:
        return
    contents = contents[:linum] + text + contents[linum:]
    contents = "".join(contents)
    if verbose:
        print(contents)
    if write:
        with open(path, "wb") as f:
            f.write(contents)


if __name__ == "__main__":
    for subm in submodules:
        # search for main.tex in submodules
        submpath = fullpath(subm, subdir=submod_dir)
        files = os.listdir(submpath)
        if not "main.tex" in files:
            continue
        else:
            main = os.path.join(submpath, "main.tex")
        # get abstract from main
        abstr = extract_abstract(main)
        # search for corresponding tex file
        subtexpath = fullpath('', subdir=tex_dir)
        files = os.listdir(subtexpath)
        if not '{}.tex'.format(subm) in files:
            continue
        else:
            subtex = fullpath('{}.tex'.format(subm), subdir=tex_dir)
        # insert abstract
        print(subtex)
        text2file(subtex, abstr, postkey='\section*{Abstract}', verbose=True)





