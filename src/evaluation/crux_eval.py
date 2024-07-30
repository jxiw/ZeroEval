import json 
from collections import defaultdict
import os 
from tabulate import tabulate 
import re
import sys 
from eval_utils import load_model_results, extract_values_from_json, extract_first_complete_json, model_specific_extraction
 

def is_valid_string(value):
    if not isinstance(value, str):
        return False
    
    if any(char in value for char in '({[]})'):
        return False
    
    if value.replace('.', '', 1).isdigit():
        return False
    
    if value.lower() in ['true', 'false']:
        return False
    
    return True

def eval_model(model, filepath):
    global private_solutions
    with open(filepath, "r") as f:
        print(f"Processing {filepath}")
        data = json.load(f)

    solved_examples = 0 
    num_total_examples = len(data) 
    no_answer = 0  
    
    reason_lens = []
    for item in data:  
        # Read and Parse the prediction from model output
        prediction_str = item["output"][0] 
        prediction_json = extract_first_complete_json(prediction_str)
        if prediction_json is None or "answer" not in prediction_json:
            prediction_json = extract_values_from_json(prediction_str, allow_no_quotes=True)
            # print("-")
        if prediction_json is None or "answer" not in prediction_json: 
            try_extracted_answer = model_specific_extraction(model, prediction_str)
            if try_extracted_answer:
                # print(f"Extracted answer from model: {try_extracted_answer}")
                prediction_json["answer"] = try_extracted_answer
            else:
                no_answer += 1 
                if False and  "3.1" in model: # used for debugging the format of the output
                    print("--------------------------")
                    print(f"No answer for {item['id']}")
                    print(prediction_str)
                    print(prediction_json)
                    print(correct_answer)
                continue 
        reason = prediction_json.get("reasoning", "")
        # We use string to compare the answers
        if is_valid_string(prediction_json["answer"]):
            model_answer = '\'' + str(prediction_json["answer"]) + '\''
        else:
            model_answer = str(prediction_json["answer"])
        correct_answer = str(item["answer"])
        
        correct = False 
        if model_answer and correct_answer:
            if model_answer == correct_answer:
                correct = True
                # To debug the correct examples
                if False and "SimPO" in model:
                    if raw_model_answer != correct_answer:
                        print(f"Raw Model Answer: {raw_model_answer}")
                        print(f"Model Answer: {model_answer}, Truth: {correct_answer}")
                        print(f"Extracted from model: {first_number_in_model_answer.group()}, Extracted from truth: {first_number_in_correct_answer.group()}")
                        print("--- correct")
            else:
                # To debug the wrong examples
                if "3.1" in model:
                    print(f"--- incorrect {item['id']} ---")
                    print(f"Model: {model_answer}, Truth: {correct_answer}")
                    print(f"Problem: {item['question']}")
                    print(f"Json: {prediction_json}")
                    print(f"Extracted from model: {model_answer}, Extracted from truth: {correct_answer}")
        if correct:
            solved_examples += 1

        # For Debugging:
        if False and "SimPO" in model:
            if not correct:
                print(item["id"], "incorrect")
        reason_lens.append(len(reason))
 
    result = {}
    result["Model"] = model.split("%")[0]
    result["Mode"] = model.split("%")[1]
    result["Acc"] = f"{solved_examples/num_total_examples*100:.2f}"
    result["No answer"] = f"{no_answer/num_total_examples*100:.2f}"
    result["Total"] = num_total_examples
    result["Reason Lens"] = f"{sum(reason_lens)/len(reason_lens):.2f}"
    return result


def gen_results(run_name_folders): 
    model_results = load_model_results(run_name_folders)

    columns = ["Model", "Mode", "Acc", "No answer", "Total", "Reason Lens"]
    rows = []
    for model_name, filepath in model_results.items(): 
        result = eval_model(model_name, filepath) 
        rows.append(result)

    # sort the rows by puzzle accuracy
    rows = sorted(rows, key=lambda x: -float(x["Acc"]))
    # Convert rows to the expected format for tabulate
    table_data = [[row[col] for col in columns] for row in rows]

    print(tabulate(table_data, headers=columns, tablefmt="fancy_outline", stralign="center", numalign="center"))
    # print(tabulate(rows, headers=columns, tablefmt="github"))

    # write to markdown file
    banner_header = """
<div style="text-align: center;">
  <img src="https://github.com/user-attachments/assets/4666e72d-4202-4283-8e78-e5ce2b030dcf" alt="zebra_banner" style="width: 69%;" />
</div>


"""
    with open(f"result_dirs/{data_name}.summary.md", "w") as f:
        f.write(banner_header+tabulate(table_data, headers=columns, tablefmt="github", stralign="center", numalign="center"))

    # write to json file 
    with open(f"result_dirs/{data_name}.summary.json", "w") as f:
        json.dump(rows, f, indent=2)


if __name__ == "__main__":

    data_name = "crux" # by default if there is no sys.argv[1]
    if len(sys.argv) > 1:
        data_name = sys.argv[1]
    run_name_folders = {
        "greedy": f"result_dirs/{data_name}", 
        "sampling": f"result_dirs/{data_name}/sampling",
        "greedy@no_cot": f"result_dirs/{data_name}/greedy@no_cot",
    }  
    gen_results(run_name_folders)