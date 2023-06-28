import os
import json
import openai

# Set the OpenAI API key using an environment variable
openai.api_key = os.environ.get("OPEN_API_KEY")
if openai.api_key is None:
    raise ValueError("Missing OpenAI API key. Set it using the OPEN_API_KEY environment variable.")


def call_openai_api(prompt, model="gpt-3.5-turbo", max_tokens=500):
    try:
        response = openai.ChatCompletion.create(
            model=model, messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


def save_response_to_json_file(response):
    file_name = "data.json"
    try:
        with open(file_name, "w") as json_file:
            json.dump(response, json_file)  # save response 
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def read_file_contents(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


def get_user_input():
    user_input = input(
        "type the subject for your cheat sheet? (Type, 'quit' to exit) >"
    )
    return user_input


def post_process_response(response, title):
    try:
        cheat_sheet = json.loads(response)
    except json.JSONDecodeError as e:
        print("The response could not be converted to JSON:", str(e))
        return None

    if not cheat_sheet:
        print("The response is empty.")
        return None

    return {"title": title, "cheat_sheet": cheat_sheet}



if __name__ == "__main__":
    user_prompt = get_user_input()
    if user_prompt.lower() != "quit":
        json_prompt = """ create a cheat sheet with 20 items. JSON response for the
        cheatsheet about following the subject: {}.
        follow this json format:
                [
        {{
            "Command": "command1",
            "Description": "Description of command1",
            "Usage": "Usage of command1"
        }},
        {{
            "Command": "command2",
            "Description": "Description of command2",
            "Usage": "Usage of command2"
        }},
        ...
    ]
    """.format(user_prompt)

    response = call_openai_api(json_prompt)
    print(response) 
    processed_response = post_process_response(response, user_prompt)
    save_response_to_json_file(processed_response)
