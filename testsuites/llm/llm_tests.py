#from .tests.prompt_injection import testlist as prompt_injection_tests
#from .tests.dan import testlist as dan_tests
#
#
#testlist = prompt_injection_tests + dan_tests

def run_test(gen_func, test_cases):

    for test in test_cases:
        print(f"{test.name}", end = '')
        test["model_output"] = gen_func(test["messages"])


    return test_cases
