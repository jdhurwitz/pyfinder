# This needs to be run with CVC
# Technically pyexz3 has been modified to start with "" for seed values on CVC. However, CVC exits (rather than throwing
# a catchable exception) when two types do not match, eg Int and String. The only way around this would be to
# modify pyexz3 to explicitly spawn new threads in case CVC exits due to these errors.
def string_no_annotation(inp):
    if inp == "Hello World":
        return 1
    elif inp == "foobar":
        return 2
    else:
        return 0


def expected_result():
    return [0, 1, 2]