def run_test_suite(gen_fn, test_cases):

    for test in test_cases:
        #print(f"{test.id}", end = '')
        print("---------------------------------------------------") 
        print(test["id"])
        print("---------------------------------------------------")
        test["model_output"] = gen_fn(test["messages"])


    return test_cases
