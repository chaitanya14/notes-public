import re
import emoji

def clean_teams_chat_file(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as f:
        chat_text = f.read()

    cleaned_messages = []
    lines = chat_text.split('\n')

    # Pattern: [9:05 AM] John Smith: Hello there!
    message_pattern = re.compile(r'^\[\d{1,2}:\d{2} [APMapm]{2}\] [^:]+: (.*)$')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        match = message_pattern.match(line)
        if match:
            # Extract and clean the message
            message = emoji.replace_emoji(match.group(1), replace='').strip()
            if message:
                cleaned_messages.append(message)
        else:
            # Handle message continuation or malformed lines
            cleaned_line = emoji.replace_emoji(line, replace='').strip()
            if cleaned_line:
                cleaned_messages.append(cleaned_line)

    # Save cleaned output
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(cleaned_messages))

    print(f"✅ Cleaned chat saved to: {output_file_path}")

# Example usage
input_path = "teams_chat_history.txt"
output_path = "cleaned_chat.txt"

clean_teams_chat_file(input_path, output_path)