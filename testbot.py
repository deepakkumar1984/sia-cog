from bot import chatbot

#chatbot.create("bdk1")
#chatbot.train("bdk1", [   'How can I help you?',    'I want to create a chat bot',    'Have you read the documentation?',    'No, I have not',    'This should help get you started: http://chatterbot.rtfd.org/en/latest/quickstart.html'])
#chatbot.corpustrain("bdk1", ["greetings"])
print(chatbot.predict("bdk1", "  "))

