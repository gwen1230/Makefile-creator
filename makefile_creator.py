#!/bin/python

import sys
import glob
import os

def empty_src(content):
    i = 0
    while (i < len(content) and content[i][:3] != "SRC"):
        i = i + 1
    if (len(content[i]) < 7):
        return (1)
    return (0)

def list_files(ndir):
    files = []
    if (os.path.isdir(ndir) == True):
        d = glob.glob(ndir + '/*')
        for f in d:
            if (os.path.isdir(f)):
                files.extend(list_files(f))
            else:
                files.append(f)
    else:
        print ("Warning : " + ndir + " is not a directory!")
    return (files)

def search_line(content):
    i = 0
    while (i < len(content) and content[i][:3] != "SRC"):
        i = i + 1
    while (i < len(content) and content[i] != "" and content[i][:4] != "NAME"):
        i = i + 1
    return (i)

def write_list_in_files(content):
    f = open("Makefile", "w")
    i = 0
    while (i < len(content)):
        f.writelines(content[i] + '\n')
        i = i + 1
    f.close()

def add_src(ndir, f):
    i = 0
    l_files = []
    while (i < len(ndir)):
        l_files.extend(list_files(ndir[i]))
        i = i + 1
    f.writelines("SRC\t=\t")
    if (len(l_files) > 0):
        f.writelines(l_files[0] + ' \\\n')
    else:
        f.writelines('\n')
    i = 1;
    while (i < len(l_files)):
        f.writelines('\t\t' + l_files[i] + ' \\\n')
        i = i + 1
    f.writelines('\n')

def add_name(f):
    name = input("Exec name ?\n")
    f.writelines("NAME\t=\t" + name + '\n\n')

def create_makefile(ndir):
    f = open("Makefile", "w")
    f.writelines("CC\t=\tcc\n\n")
    f.writelines("RM\t=\trm -f\n\n")
    add_src(ndir, f)
    add_name(f)
    f.writelines("OBJ\t=\t$(SRC:.c=.o)\n\n")
    f.writelines("CFLAGS\t=\t-Wall -Wextra\n\n")
    f.writelines("all:\t\t$(NAME)\n\n")
    f.writelines("test:\t\tall clean\n\n")
    f.writelines("$(NAME):\t$(OBJ)\n")
    f.writelines("\t\t$(CC) -o $(NAME) $(OBJ)\n\n")
    f.writelines("clean:\n")
    f.writelines("\t\t$(RM) $(OBJ)\n\n")
    f.writelines("fclean:\t\tclean\n")
    f.writelines("\t\t$(RM) $(NAME)\n\n")
    f.writelines("re:\t\tfclean all\n\n")
    f.close()

def add_dir(ndir):
    if (os.path.exists("./Makefile") == False):
        print ("Makefile does not exist!")
        exit()
    f = open("Makefile", "r")
    content = f.read().split('\n')
    f.close()
    l_files = []
    i = 0
    while (i < len(ndir)):
        l_files.extend(list_files(ndir[i]))
        i = i + 1
    i = search_line(content)
    if (i == len(content)):
        print ("SRC not found!")
        exit()
    j = 0
    while (j < len(l_files)):
        if (empty_src(content) == 1):
            content.remove("SRC\t=\t")
            i = i - 1
            content.insert(i, 'SRC\t=\t' + l_files[j] + ' \\')
        else:
            content.insert(i, '\t\t' + l_files[j] + ' \\')
        i = i + 1
        j = j + 1
    write_list_in_files(content)

def add_file(files):
    if (os.path.exists("./Makefile") == False):
        print ("Makefile does not exist!")
        exit()
    f = open("Makefile", "r")
    content = f.read().split('\n')
    f.close()
    i = search_line(content)
    if (i == len(content)):
        print ("SRC not found!")
        exit()
    j = 0
    while (j < len(files)):
        if (empty_src(content) == 1):
            content.remove("SRC\t=\t")
            i = i - 1
            if (os.path.exists("./" + files[j]) == True and os.path.isfile(files[j]) == True):
                content.insert(i, 'SRC\t=\t' + files[j] + ' \\')
            else:
                print ("Warning : " + files[j] + " is not a file")
        else:
            if (os.path.exists("./" + files[j]) == True and os.path.isfile(files[j]) == True):
                content.insert(i, '\t\t' + files[j] + ' \\')
            else:
                print ("Warning : " + files[j] + " is not a file")
        i = i + 1
        j = j + 1
    write_list_in_files(content)

def del_dir(ndir):
    if (os.path.exists("./Makefile") == False):
        print ("Makefile does not exist!")
        exit()
    f = open("Makefile", "r")
    content = f.read().split('\n')
    f.close()
    j = 0
    while (j < len(ndir)):
        if (os.path.isdir(ndir[j]) == True):
            i = 0
            while (i < len(content) and content[i][:3] != "SRC"):
                i = i + 1
            if (ndir[j] == content[i][6:len(ndir[j]) + 6] and content[i][len(ndir[j]) + 6] == '/'):
                content.remove(content[i])
                content.insert(i, "SRC\t=\t")
            while (i < len(content) and content[i] != "" and content[i][:4] != "NAME"):
                if (ndir[j] == content[i][2:len(ndir[j]) + 2] and content[i][len(ndir[j]) + 2] == '/'):
                    content.remove(content[i])
                else:
                    i = i + 1
        else:
            print ("Warning : " + str(ndir[j] + " is not a directory!"))
        j = j + 1
    write_list_in_files(content)

def del_file(files):
    if (os.path.exists("./Makefile") == False):
        print ("Makefile does not exist!")
        exit()
    f = open("Makefile", "r")
    content = f.read().split('\n')
    f.close()
    j = 0
    while (j < len(files)):
        if (os.path.isfile(files[j]) == True):
            i = 0
            while (i < len(content) and content[i][:3] != "SRC"):
                i = i + 1
            if (files[j] == content[i][6:-2]):
                content.remove(content[i])
                content.insert(i, "SRC\t=\t")
            while (i < len(content) and content[i] != "" and content[i][:4] != "NAME"):
                if (files[j] == content[i][2:-2]):
                    content.remove(content[i])
                else:
                    i = i + 1
        else:
            print ("Warning : " + str(files[j] + " is not a file!"))
        j = j + 1
    write_list_in_files(content)

def maj_dir(ndir):
    del_dir(ndir)
    add_dir(ndir)

def print_help():
    print ("-c  <dir> ...\tcreate Makefile with dir")
    print ("-d  <dir> ...\tAdd dir to Makefile")
    print ("-f  <file> ...\tAdd file to Makefile")
    print ("-rd <dir> ...\tRemove dir to Makefile")
    print ("-rf <file> ...\tRemove file to Makefile")
    print ("-m  <dir> ...\tUpdate dir in Makefile")
    print ("-h\t\tHelp")

if __name__=='__main__':
    if (len(sys.argv) == 2 and sys.argv[1] == '-h'):
        print_help()
        exit()
    if (len(sys.argv) < 3):
        print ("Usage : " + sys.argv[0] + " <opt> <files/dir> ...")
        exit()
    if (sys.argv[1] == '-c'):
        create_makefile(sys.argv[2:])
    elif (sys.argv[1] == '-d'):
        add_dir(sys.argv[2:])
    elif (sys.argv[1] == '-f'):
        add_file(sys.argv[2:])
    elif (sys.argv[1] == '-rd'):
        del_dir(sys.argv[2:])
    elif (sys.argv[1] == '-rf'):
        del_file(sys.argv[2:])
    elif (sys.argv[1] == '-m'):
        maj_dir(sys.argv[2:])
    else:
        print ("bad option!")
