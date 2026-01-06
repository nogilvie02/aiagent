import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    load_dotenv()
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
    except RuntimeError as e:
        print("Error encountered: {e}")
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output") 
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions],
                                            system_instruction=system_prompt, 
                                            temperature=0),
        )
    except errors.ClientError as e:
        msg = str(e)
        if "429" in msg or "RESOURCE_EXHAUSTED" in msg or "quota" in msg.lower():
            print("Error: API quota exceeded. Please wait and try again later.")
        else:
            print(f"Error from Gemini API: {msg}")
        return
    if response.usage_metadata is None:
        raise RuntimeError("Response Usage Metadata is None (does not exist).")
    
    if args.verbose is True:
        print("User prompt: ",args.user_prompt)
        print("Prompt tokens: ", response.usage_metadata.prompt_token_count)
        print("Response tokens: ", response.usage_metadata.candidates_token_count)
    if response.function_calls:
        function_results = []
        for function_call in response.function_calls:
            #print(f"Calling function: {function_call.name}({function_call.args})")
            function_call_result = call_function(function_call, args.verbose)
            if not function_call_result.parts:
                raise Exception("Error: function_call_result has empty .parts list")
            elif not function_call_result.parts[0].function_response:
                raise Exception("Error: function_repsonse property is empty")
            elif not function_call_result.parts[0].function_response.response:
                raise Exception("Error: function_response result is empty")
            else:
                function_results.append(function_call_result.parts[0])
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print("RESPONSE: ", response.text)


if __name__ == "__main__":
    main()
