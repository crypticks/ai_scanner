def run_test_suite(name, comm_fn, test_cases):

    if name == "llm":
        from .llm.llm_tests import run_test
        return run_test(comm_fn, test_cases)

    raise ValueError(f"Unknown suite {name}")
