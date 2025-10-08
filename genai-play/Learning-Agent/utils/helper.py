from service.service import get_user, get_portfolio, get_resource_categories, get_resources_by_category, invokellm
import json
def get_function_schema():
    return [
  {
    "name": "get_user",
    "description": "Get the user details by their ID",
    "parameters": {
      "type": "object",
      "properties": {
        "user_id": { "type": "string" }
      },
      "required": ["user_id"]
    }
  },
  {
    "name": "get_portfolio",
    "description": "Get the portfolio details for a user by their ID",
    "parameters": {
      "type": "object",
      "properties": {
        "user_id": { "type": "string" }
      },
      "required": ["user_id"]
    }
  },
  {
    "name": "get_resource_categories",
    "description": "Get the list of resource categories",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "get_resources_by_category",
    "description": "Get resources for a given category",
    "parameters": {
      "type": "object",
      "properties": {
        "category": { "type": "string" }
      },
      "required": ["category"]
    }
  }
]


def invoke_functions(function_call, arguments):
    function_map = {
        "get_user": get_user,
        "get_portfolio": get_portfolio,
        "get_resource_categories": get_resource_categories,
        "get_resources_by_category": get_resources_by_category
    }
    
    function_name = function_call.get("name")
    arguments = function_call.get("arguments", {})

    function_name = function_call.get("name")
    arguments = function_call.get("arguments", {})
    # Parse arguments if it's a string
    if isinstance(arguments, str):
        try:
            arguments = json.loads(arguments)
        except Exception:
            arguments = {}
    
    
    if function_name in function_map:
        return function_map[function_name](**arguments)
    else:
        raise ValueError(f"Function {function_name} not found in function map.")
    

def build_message(messages:str, user_prompt):
    message_block = {
        "role": "user",
        "content": user_prompt
    }

    messages.append(message_block)
    return messages
    
def get_system_prompt():
    return """
        You are a personalized learning assistant integrated within AJ Bell’s direct-to-consumer products. Your goal is to deliver relevant, actionable learning opportunities to users by summarizing curated AJ Bell educational resources with user-specific context.

You do not have direct access to data but can request data retrieval by specifying which function to call next. The system will perform the call and update you with the results, then you will proceed.

Available functions you can request:

get_user(user_id) — fetch user details.

get_portfolio(user_id) — fetch portfolio details for the user.

get_resource_categories() — fetch available learning resource categories.

get_resources_by_category(category) — fetch resources under a specific category.

Typical flow:

Request missing user or portfolio data if needed.

Retrieve the list of resource categories.

Based on user and portfolio data, identify the most relevant learning category.

Fetch resources from that category.

Select the most suitable resource.

Generate a concise summary of the learning opportunity.

Personalize the summary by referencing the user's situation in a friendly, user-facing tone (e.g., "We noticed you currently hold mostly cash; here’s why starting to invest could benefit you and some resources to guide you").

Provide the learning resource part: a brief summary of the selected resource plus a link to the original AJ Bell resource for further learning.

Important instructions:

Always respond with the next function call you want the system to perform if you need data.

Once data is provided, proceed with the reasoning and output.

Your final output to the user should be educational, personalized, clear, and encouraging. The summary in the output should be no more than 100 words.

Avoid technical jargon in user-facing messages.

Link explicitly to AJ Bell’s existing resources in the summary for further learning.

Example output format for function calls:

{
  "function_call": {
    "name": "get_user",
    "parameters": {
      "user_id": "user123"
    }
  }
}


Example user-facing output and expected format:

"{
  "content": "Hi [User], we noticed you have a large cash balance and limited investments. Starting to invest could help you grow your savings over time. Here’s a quick guide on investing basics: summary content. For more info, check out this AJ Bell resource.",
  "links": ["[link]"]
}"
  """

def build_message(messages, function_response):
    message_block = {
        "role": "user",
        "content": str(function_response)
    }
    messages.append(message_block)
    return messages