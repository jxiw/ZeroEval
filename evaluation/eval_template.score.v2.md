# Instruction 

You are an expert evaluator. Your task is to evaluate the quality of the responses generated by AI models. 
We will provide you with the user query and an AI-generated responses.
You should first read the user query and the conversation history carefully for analyzing the task, and then evaluate the quality of the responses based on and rules provided below.

# Conversation between User and AI

## History
<|begin_of_history|>

{$history}

<|end_of_history|> 

## Current User Query
<|begin_of_query|>

{$user_query}

<|end_of_query|>

## AI Response
<|begin_of_response|>

{$model_output}

<|end_of_response|>
 

# Evaluation   

## Checklist 

<|begin_of_checklist|>

{$checklist}

<|end_of_checklist|>

Please use this checklist to guide your evaluation, but do not limit your assessment to the checklist.

## Rules 

You should compare the above response based on your analysis of the user queries and the conversation history.
You should first write down your analysis and the checklist that you used for the evaluation, and then provide your assessment according to the checklist.
The scores are in the range of 1~10, where 1 means the response is very poor and 10 means the response is perfect.
Here are more detailed criteria for the scores:

- Score 1~2: The response is very poor and does not make sense at all.
- Score 3~4: The response is poor and does help user solve the problem in a meaningful way.
- Score 5~6: The response is fair but has some issues (e.g., factual errors, hallucinations, missing key information).
- Score 7~8: The response is good enough but could be improved in some ways.
- Score 9~10: The response is perfect and provides helpful information that can help user solve the problem.

## Output Format 
First, please output your analysis for each model response, and then summarize your assessment to three aspects: "reason A=B", "reason A>B", and "reason B>A", and finally make your choice for the final assessment.

Please provide your evaluation results in the following json format by filling in the placeholders in []:
```
{
    "strengths": "[analysis for the strengths of the response]",
    "weaknesses": "[analysis for the weaknesses of the response]",
    "score": "[1~10]"
}
```