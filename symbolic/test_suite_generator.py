from datetime import datetime
import os, errno

def test_suite_generator(filename, allEntries, allGeneratedInputs, allReturnVals):
    # jteoh: need to ensure that the pyexz3 path is present - the following is copied from
    # pyexz3.py and adapted for this file. (2 dirnames because it's in a nested directory).
    # This is required in case the input file contains an import for symbolic types.
    pyexz3_base_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__))))
    directory = os.path.dirname(filename)
    suite_directory = "generated_test_suites"
    make_dir_if_not_exist(suite_directory)

    filename = os.path.basename(filename)[:-3] # also exclude .py
    test_filename = os.path.join(suite_directory, filename+"_test_suite.py")
    file = open(test_filename,"w+")
    file.write("import unittest\n")
    file.write("import sys\n")

    # Add folders to sys path so the file can be imported.
    file.write("sys.path.append(\"" + pyexz3_base_dir + "\")\n") # for symbolic decorators
    file.write("sys.path.append(\"" + directory + "\")\n") # for the actual input program/module

    for entry in allEntries:
        file.write("from " + filename + " import " + entry +"\n\n")

    file.write("class Test_" + filename + "(unittest.TestCase):\n\n")

    index = 0
    for entry, generatedInputs, returnVals in zip(allEntries, allGeneratedInputs, allReturnVals):
        for i, r in zip(generatedInputs, returnVals):
            file.write("\tdef test" + str(index) + "(self):\n")
            file.write("\t\tself.assertEqual(" + entry + "(")
            write_comma = False
            for arg in i:
                if write_comma:
                    file.write(",")
                write_comma = True
                file.write(wrap(arg[1])) #  arg = (variable, value)
            file.write("), " + wrap(r) + ")\n\n")
            index+=1

    file.write("if __name__ == '__main__':\n")
    file.write("\tunittest.main()\n")

    file.close()

    print("Created test suite file " + test_filename)

def make_dir_if_not_exist(directory):
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def wrap(obj):
    """
    Wrap a data object to a string that python can evaluate. Currently this only explicitly supports strings.
    Any other data type is treated as-is via the str() operator.
    """
    if isinstance(obj, str):
        return "\"%s\"" % obj
    else:
        return str(obj)