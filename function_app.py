import azure.functions as func
import logging
from chatonyourdata import *

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

def get_json_object(chat_history, question, content, citations, file_paths, urls_paths):
    if chat_history is None:
        # remove [] around question and content if this is an issue
        messages.append({"role": "user", "content": [question]})
        messages.append({"role": "system", "content": [content]})
        messages.append({"role": "tool", "content": citations})

    else:
        messages = chat_history
        messages.append({"role": "user", "content": [question]})
        messages.append({"role": "system", "content": [content]})
        messages.append({"role": "tool", "content": citations})

    # links = urls_paths
    # files = file_paths
    

    
    data = {  
        'messages': messages,  
        'response': content,
        'links': urls_paths,
        'files': file_paths,
    }  
    json_object = json.dumps(data)
    return json_object

@app.route(route="http_trigger_gdms_prd1_chat")
def http_trigger_gdms_prd1_chat(req: func.HttpRequest) -> func.HttpResponse:
    try:
        logging.info('Python HTTP trigger function processed a request.')

        chat_history = []
        req_body = req.get_json()
        question = req_body.get('question')
        chat_history = req_body.get('chat_history')

        logging.info(req.get_json())
        logging.info(f"Question: {question}")
        logging.info(f"Chat History Type: {type(chat_history)}")

        chatter = ChatOnYourData(index="good-fish", role="test-role")
        logging.info(f"Created ChatOnYourData object")
        content, citations, file_paths, urls_paths = chatter.make_request(question, chat_history, includeCitationsInResponse=False)

        
        logging.info(f"response: {content}")
    
        

        return func.HttpResponse(get_json_object(chat_history, question, content, citations, file_paths, urls_paths), status_code=200)
    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse(f"Error: {e}", status_code=500)
