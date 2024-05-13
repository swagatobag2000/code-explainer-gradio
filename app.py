import gradio as gr
import os
import google.generativeai as palm
from dotenv import load_dotenv, dotenv_values 

# load model
# PaLM API Key here
load_dotenv()
api_key = os.environ["HUGGING_FACE_API_KEY"]
palm.configure(api_key=api_key)

models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name
print("Using Model:", model)

# define the completion function
def get_completion(code_snippet):

  python_code_examples = f"""
  ---------------------
  Example 1: Code Snippet
  x = 10
  def foo():
      global x
      x = 5
  foo()
  print(x)
  Correct output: 5
  Code Explanation: Inside the foo function, the global keyword is used to modify the global variable x to be 5.
  So, print(x) outside the function prints the modified value, which is 5.
  ---------------------
  Example 2: Code Snippet
  def modify_list(input_list):
      input_list.append(4)
      input_list = [1, 2, 3]
  my_list = [0]
  modify_list(my_list)
  print(my_list)
  Correct output: [0, 4]
  Code Explanation: Inside the modify_list function, element 4 is appended to input_list.
  Then, input_list is reassigned to a new list [1, 2, 3], but this change doesn't affect the original list.
  So, print(my_list) outputs [0, 4].
  ---------------------
  """

  prompt = f"""
  Your task is to act as a Python Code Explainer and Reviewer.
  I'll give you a Code Snippet. Your job is to explain the Code Snippet step-by-step.
  Break down the code into as many steps as possible. Mention the DSA used inside the code. Share intermediate checkpoints & steps along with results.
  A few good examples of Python code output between #### separator:
  ####
  {python_code_examples}
  ####
  Code Snippet is shared below, delimited with triple backticks:
  ```
  {code_snippet}
  ```
  """

  completion = palm.generate_text(
      model=model,
      prompt=prompt,
      temperature=0.5,
      # The maximum length of the response
      max_output_tokens=1000,
      )
  response = completion.result
  return response

# define app UI
iface = gr.Interface(fn=get_completion, inputs=[gr.Textbox(label="Insert Code Snippet",lines=5)],
                    outputs=[gr.Textbox(label="Explanation Here",lines=5)],
                    title="Python Code Explainer"
                    )

iface.launch(share=True)