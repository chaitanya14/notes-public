import re
import emoji

def clean_teams_chat_file_scrub_names(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as f:
        chat_text = f.read()

    cleaned_messages = []
    lines = chat_text.split('\n')

    # Matches: [9:05 AM] John Smith: Message
    full_line_pattern = re.compile(r'^\[\d{1,2}:\d{2} [APMapm]{2}\] [^:]+: (.*)$')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        match = full_line_pattern.match(line)
        if match:
            message = match.group(1).strip()
        else:
            message = line  # Possibly a continuation or unstructured line

        # Remove emojis
        message = emoji.replace_emoji(message, replace='')

        # Remove leading dashes, bullets, or extra formatting artifacts
        message = re.sub(r'^[-•\*\s]+', '', message)

        # Skip empty lines after cleaning
        if message:
            cleaned_messages.append(message)

    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(cleaned_messages))

    print(f"✅ Cleaned and anonymized chat saved to: {output_file_path}")

# Example usage
input_path = "teams_chat_history.txt"
output_path = "cleaned_chat.txt"

clean_teams_chat_file_scrub_names(input_path, output_path)