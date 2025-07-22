import re
import emoji

def clean_teams_chat_fully_scrubbed(input_text: str) -> str:
    cleaned_lines = []
    lines = input_text.split('\n')
    in_code_block = False

    # Match lines like: Friday 8:22 AM or Monday 11:45 PM
    day_time_pattern = re.compile(r'^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s+\d{1,2}:\d{2}\s+[APMapm]{2}$', re.IGNORECASE)

    for line in lines:
        line = line.strip()

        # Skip empty lines or emoji-only lines
        if not line or emoji.replace_emoji(line, replace='').strip() == '':
            continue

        # Skip junk metadata
        if any([
            re.match(r'^\d+ Like reaction(s)?\.?$', line, re.IGNORECASE),
            re.match(r'^Reply$', line, re.IGNORECASE),
            re.match(r'^See more$', line, re.IGNORECASE),
            re.match(r'^Open \d+ repl(y|ies) from', line, re.IGNORECASE),
            re.match(r'^CC\b.*', line, re.IGNORECASE),
            re.match(r'^[A-Za-z ,.\'-]+$', line),  # Likely a name line like "Johnson, Jeff M"
            day_time_pattern.match(line)           # Skip lines like "Friday 8:12 AM"
        ]):
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