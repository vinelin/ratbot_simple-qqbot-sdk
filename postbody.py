def send_text(text:str):
    return  {
                "type": "text",
                "data": {"text": text}
            }

def send_at(qq_id:str):
    return  {
                "type": "at",
                "data": {"qq": qq_id}
            }

def send_emoji(face_id:str):
    return  {
                "type": "face",
                "data": {"id": face_id}
            }
def send_image(url:str):
    return {
                "type": "image",
                "data": {"file": url}
            }

def post_content(*args):
    message_dict = {'message': []}
    message_dict['message'][:] = args
    return message_dict