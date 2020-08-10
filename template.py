from os import walk

import pybars

templates = {}
compiler = pybars.Compiler()


def load_templates():

    for (dir, path, names) in walk("template"):

        for n in names:
            fp = dir+"/"+n
            if n in templates:
                exit("Duplicated template name. "+fp)
            f = open(fp)
            templates[n] = compiler.compile(f.read())



