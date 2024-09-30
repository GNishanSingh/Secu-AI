from mistralai import Mistral

api_key = "16pbJ0TeemXrN7Dl2aP5GZouFcn2Tv1E"
client = Mistral(api_key=api_key)

model = "codestral-latest"
message = [{"role": "user", "content": "Write a windows event filter for checking process spawned by c:\\windows\\explorer.exe and sysmon is installed"}]
chat_response = client.chat.complete(
    model = model,
    messages = message
)
print(chat_response.choices[0].message.content)