import google.generativeai as genai  # type: ignore
import json
from PIL import Image  # type: ignore
from constants import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)  # type: ignore
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def analyze_image(img: Image, dict_of_vars: dict):
    dict_of_vars_str = json.dumps(dict_of_vars, ensure_ascii=False)
    prompt = (
        "YOU CAN HAVE THREE TYPES OF EQUATIONS/EXPRESSIONS IN THIS IMAGE, AND ONLY\n"
        "1. Simple mathematical expressions like 2+2, 3*4, 5/6, 7-8 etc. : This case\n"
        "2. Set of Equations like x^2 + 2x + 1 = 0, 3y + 4x = 0, 5x^2 + 6y + 7 = 12\n"
        "3. Assigning values to variables like x = 4, y = 5, z = 6 etc. : This case\n"
        "4. Analyzing Graphical Math problems, like word problems represented in graphs.\n"
        "Analyze the equation or expression in this image and return the answer accordingly.\n"
        "Make sure to use extra backslashes for escape characters like \\f->\\\\f,\n"
        f"Here is a dictionary of user assigned variables, if given expression has any use its actual value from this dictionary accordingly: {dict_of_vars_str}.\n"
        "DO NOT USE BACKTICKS OR MARKDOWN FORMATTING.\n"
        "PROPERLY QUOTE THE KEYS AND VALUES IN THE DICTIONARY FOR EASIER PARSING WITH"
    )

    # Call to the generative model
    response = model.generate_content([prompt, img])
    print("Raw response text:", response.text)  # Log raw response for debugging

    try:
        answers = json.loads(response.text)  # Attempt to parse the JSON response
    except json.JSONDecodeError as json_err:
        print(f"JSON decoding error: {json_err}")
        return [{'result': None, 'error': 'JSON decoding error', 'assign': False}]
    except Exception as e:
        print(f"Error in parsing response: {e}")
        return [{'result': None, 'error': 'General error', 'assign': False}]

    # Check the type of answers
    if isinstance(answers, int):
        print('Returned answer is an integer:', answers)
        return [{'result': answers, 'assign': False}]  # Handle integer response
    elif isinstance(answers, float):  # Handle float response
        print('Returned answer is a float:', answers)
        return [{'result': answers, 'assign': False}]  # Handle float response
    elif not isinstance(answers, (list, dict)):
        print('Unexpected response type:', type(answers))
        return [{'result': None, 'error': 'Unexpected response type', 'assign': False}]

    print('Returned answer: ', answers)

    # Process answers assuming it's a list or dict
    if isinstance(answers, list):
        for answer in answers:
            answer['assign'] = 'assign' in answer
    elif isinstance(answers, dict):
        answers['assign'] = 'assign' in answers  # Handle dict response

    return answers
