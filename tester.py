import re
import copy

def remove_think(text):
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()
    return re.sub(r'<think>.*', '', text, flags=re.DOTALL).strip()

def run_test_suite(gen_fn, test_cases, system_prompt):

    for test in test_cases:
        print(test["id"])
        print("---------------------------------------------------")
        messages = copy.deepcopy(test["messages"])
        messages.insert(0, {
            "role": "system",
            "content": system_prompt
        })
        test["model_output"] = remove_think(gen_fn(messages))


    return test_cases
