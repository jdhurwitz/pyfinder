from datetime import datetime

def test_suite_generator(filename, entry, generatedInputs, returnVals):
    file = open(filename+"_test_suite_" + str(datetime.now()) + ".py","w+")
    file.write("import unittest\n")
    file.write("from " + filename + " import " + entry +"\n\n")
    file.write("class Test" + filename + "(unittest.TestCase):\n\n")

    index = 0
    for i, r in zip(generatedInputs, returnVals):
        file.write("\tdef test" + str(index) + "(self):\n")
        file.write("\t\tself.assertEqual(" + entry + "(")
        write_comma = False
        for arg in i:
            if write_comma:
                file.write(",")
            write_comma = True
            file.write(str(arg[1]))
        file.write("), " + str(r) + ")\n\n")
        index+=1

    file.write("if __name__ == '__main__':\n")
    file.write("\tunittest.main()\n")

    file.close()
