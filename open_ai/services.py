import json
import os

from openai import OpenAI

from open_ai.structures import ReceiptData
from open_ai.decorators import handle_openai_errors
from open_ai.managers import TmpFileManager, TmpThreadManager


class BaseOpenAIMethods:

    @handle_openai_errors
    def __init__(self, **kwargs):
        self.client = OpenAI()

    @handle_openai_errors
    def _get_response(self, thread_id):
        messages = self.client.beta.threads.messages.list(thread_id=thread_id)
        message_content = messages.data[0].content
        if message_content:
            message_content = message_content[0].text

            annotations = message_content.annotations
            for annotation in annotations:
                message_content.value = message_content.value.replace(annotation.text, '')

            response_message = message_content.value
            return response_message
        return None


class OpenAIService(BaseOpenAIMethods):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.analyze_receipt_assistant = self.client.beta.assistants.retrieve(os.getenv('OPENAI_ANALYZE_RECEIPT_ASSISTANT_ID'))
        self.usage = []

    @handle_openai_errors
    def analyze_receipt(self, image_path: str, prompt: str = '', poll_interval_ms=1000) -> ReceiptData:
        with open(image_path, mode='rb') as file:
            with TmpFileManager(self.client, create_kwargs={'file': file, 'purpose': 'vision'}) as tmp_file:
                content = [{'type': 'image_file', 'image_file': {'file_id': tmp_file.id}}]

                if prompt:
                    content.append({'type': 'text', 'text': prompt})

                with TmpThreadManager(self.client) as tmp_thread:
                    run = self.client.beta.threads.runs.create_and_poll(
                        thread_id=tmp_thread.id,
                        assistant_id=self.analyze_receipt_assistant.id,
                        poll_interval_ms=poll_interval_ms,
                        additional_messages=[{'content': content, 'role': 'user'}]
                    )
                    self.usage.append(run.usage)

                    response_message = self._get_response(run.thread_id)
                    response_json = json.loads(response_message)
                    return ReceiptData(**response_json)
