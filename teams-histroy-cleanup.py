import re
import emoji

def clean_teams_channel_chat(input_text: str) -> str:
    cleaned_lines = []
    lines = input_text.split('\n')
    in_code_block = False

    for line in lines:
        original_line = line
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Skip Teams UI garbage
        if any([
            re.match(r'^\d+ Like reaction(s)?\.?$', line, re.IGNORECASE),
            re.match(r'^Reply$', line, re.IGNORECASE),
            re.match(r'^See more$', line, re.IGNORECASE),
            re.match(r'^Open \d+ repl(y|ies) from', line, re.IGNORECASE),
            re.match(r'^CC\b.*', line, re.IGNORECASE),
            emoji.replace_emoji(line, replace='').strip() == ''
        ]):
            continue

        # Skip lines that are likely just a name or timestamp
        if re.match(r'^[A-Za-z ,.\'-]+$', line):
            continue
        if re.match(r'^\w+day \d{1,2}:\d{2} [APMapm]{2}$', line):
            continue

        # Handle code block start
        if '{' in line and not in_code_block:
            in_code_block = True

        # Remove emojis from the message
        line = emoji.replace_emoji(line, replace='')

        cleaned_lines.append(line)

        # Handle code block end
        if '}' in line and in_code_block:
            in_code_block = False

    return '\n'.join(cleaned_lines)