import re
import emoji

def clean_teams_channel_chat(chat_text):
    cleaned_messages = []

    # Match [Time] Name: Message
    lines = chat_text.split('\n')
    message_pattern = re.compile(r'^\[\d{1,2}:\d{2} [APMapm]{2}\] ([^:]+): (.*)$')

    for line in lines:
        match = message_pattern.match(line)
        if match:
            message = match.group(2).strip()
            message = emoji.replace_emoji(message, replace='')
            if message:
                cleaned_messages.append(message)
        else:
            # Handle continuation of a previous message
            message = emoji.replace_emoji(line.strip(), replace='')
            if message:
                cleaned_messages.append(message)

    return '\n'.join(cleaned_messages)