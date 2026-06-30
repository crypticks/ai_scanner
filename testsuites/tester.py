def run_test_suite(name, comm_fn):

    if name == "llm-garak":
        from .llm.garak.garak_tests import run_test_suite as run_garak
        return run_garak(comm_fn, ["probes.promptinject.HijackHateHumans"], [])

    raise ValueError(f"Unknown suite {name}")
