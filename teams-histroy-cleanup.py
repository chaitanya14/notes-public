import re
import emoji

def clean_teams_chat_with_code_blocks(input_text):
    cleaned_lines = []
    lines = input_text.split('\n')
    in_code_block = False

    for line in lines:
        line = line.strip()

        # Skip empty lines and UI junk
        if not line or line.lower() in ['reply', '1 like reaction.', '👍'] or 'Open' in line:
            continue

        # Toggle code block mode
        if '{' in line and '}' not in line:
            in_code_block = True

        # Remove emojis
        line = emoji.replace_emoji(line, replace='')

        # Remove names and timestamps like "Johnson, Jeff M\nFriday 8:22 AM"
        if re.match(r'^[A-Za-z ,]+$', line):
            continue
        if re.match(r'^\w+day \d{1,2}:\d{2} [APMapm]{2}$', line):
            continue

        # Keep code block content
        if in_code_block:
            cleaned_lines.append(line)
            if '}' in line:
                in_code_block = False
            continue

        cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)

# Example: run this on your pasted file content
# with open("teams_chat.txt", "r") as f:
#     raw = f.read()
# clean = clean_teams_chat_with_code_blocks(raw)
# with open("cleaned_output.txt", "w") as f:
#     f.write(clean)