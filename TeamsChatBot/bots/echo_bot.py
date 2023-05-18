# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount
import openai

openai.api_type = "azure"
openai.api_base = "{ENTER YOUR API ENDPOINT}"
openai.api_version = "{ENTER YOUR API VERSION}"
openai.api_key = "{ENTER YOUR API KEY}"


class EchoBot(ActivityHandler):
        #initializing class variable to save prompts in a conversation
    def __init__(self):
        self.messages = []
        self.messages.append({"role": "system", "content": "You are an AI assistant that helps people find information, perform tasks, and more. When asked a question, try to include the URL of any documentation relevant to the topic."})
        self.max_response_tokens = 300
        self.token_limit = 8000
        self.conv_history_tokens = 0

    #def num_tokens_from_messages(self, model="gpt-4-32k"):
        #encoding = tiktoken.encoding_for_model(model)
        #num_tokens = 0
        #for message in self.messages:
         #   num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
          #  for key, value in message.items():
           #     num_tokens += len(encoding.encode(value))
            #    if key == "name":  # if there's a name, the role is omitted
             #       num_tokens += -1  # role is always required and always 1 token
        #num_tokens += 2  # every reply is primed with <im_start>assistant
        #return num_tokens
    def num_words_from_messages(self):
        for word in self.messages:
            self.conv_history_tokens += 5
    
    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")

    async def on_message_activity(self, turn_context: TurnContext):
        self.messages.append({"role": "user", "content": turn_context.activity.text})
        system_message = "You are an AI assistant named Eugene that helps people find information, perform tasks, and more. When asked a question, try to include the URL of any documentation relevant to the topic. You were created by Xander, a brilliant Solutions Architect with vast knowledge of AI systems."
        self.num_words_from_messages()
        while (self.conv_history_tokens+self.max_response_tokens >= self.token_limit):
            del self.messages[1] 
            self.num_words_from_messages()

        response = openai.ChatCompletion.create(
            engine="gpt4",
            messages = self.messages,
            temperature=1,
            max_tokens=self.max_response_tokens,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None)
        self.messages.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
        return await turn_context.send_activity(
            MessageFactory.text(response['choices'][0]['message']['content'])
        )

     