import textwrap


def format_time_srt(seconds: float) -> str:
    """Converts seconds to SRT time format HH:MM:SS,mmm"""
    if seconds is None:
        return "00:00:00,000"
    total_seconds = int(seconds)
    milliseconds = int((seconds - total_seconds) * 1000)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def split_text_lines(text, max_line_length=40, max_lines=2):
    """
    Split text into lines with max_line_length, up to max_lines.
    Returns a list of lines.
    """
    wrapper = textwrap.TextWrapper(width=max_line_length, break_long_words=False, replace_whitespace=False)
    lines = wrapper.wrap(text)
    return lines


def split_lines_balanced(text, max_line_length=40, max_lines=2):
    """
    Split text into balanced lines with max_line_length and max_lines.
    Tries to avoid breaking words and keeps lines of similar length.
    """
    if not text:
        return []

    # First pass: naive wrapping
    lines = split_text_lines(text, max_line_length, max_lines)

    # If we have more than one line, try to balance
    if len(lines) > 1:
        # Measure current balance
        lengths = [len(line) for line in lines]
        avg_length = sum(lengths) / len(lengths)

        # If the variance is high, we try to balance
        if max(lengths) - min(lengths) > avg_length * 0.3:
            # Join all lines and re-wrap with a new strategy
            joined = ' '.join(lines)
            lines = split_text_lines(joined, max_line_length // 2, max_lines * 2)

    return lines


def split_segment_by_time_and_lines(
    segment, max_line_length=40, max_lines=2,
    min_ms_per_char=0.03, ideal_ms_per_char=0.05, max_ms_per_char=0.185,
    min_duration=0.7, max_duration=5.0
):
    """
    Split a segment into multiple SRT blocks if needed, balancing time by character count.
    Returns a list of dicts with 'start', 'end', 'lines'.
    """
    text = segment.get('text', '').strip()
    if not text:
        return []
    start = float(segment.get('start', 0.0))
    end = float(segment.get('end', start + 1.0))
    total_duration = end - start

    # Split text into lines
    lines = split_lines_balanced(text, max_line_length)
    # Split lines into blocks of max_lines
    blocks = [lines[i:i+max_lines] for i in range(0, len(lines), max_lines)]

    # Calculate total chars for all blocks
    block_char_counts = [sum(len(line) for line in block) for block in blocks]
    total_chars = sum(block_char_counts)

    # Calculate ideal durations for each block
    block_durations = []
    for chars in block_char_counts:
        # Ideal duration for this block
        ideal = max(min_duration, min(max_duration, chars * ideal_ms_per_char))
        # But also proportional to total segment duration
        prop = total_duration * (chars / total_chars) if total_chars > 0 else ideal
        # Use the max between ideal and proportional, but clamp to min/max
        duration = max(min_duration, min(max_duration, max(ideal, prop)))
        # Clamp by min/max per char
        duration = max(duration, chars * min_ms_per_char)
        duration = min(duration, chars * max_ms_per_char)
        block_durations.append(duration)

    # Adjust durations to fit exactly in total_duration
    duration_sum = sum(block_durations)
    if duration_sum > 0:
        scale = total_duration / duration_sum
        block_durations = [d * scale for d in block_durations]

    # Build SRT blocks with balanced timings
    srt_blocks = []
    current_start = start
    for block_lines, duration in zip(blocks, block_durations):
        block_end = current_start + duration
        srt_blocks.append({
            'start': current_start,
            'end': block_end,
            'lines': block_lines
        })
        current_start = block_end
    return srt_blocks


def get_word_groups(words, max_chars=40, max_lines=2):
    """
    Group words respecting character and line limits,
    keeping original timings for each group
    """
    groups = []
    current_group = []
    current_chars = 0
    current_lines = 1

    for word in words:
        word_text = word['word'].strip()
        word_len = len(word_text)
        
        # Check if adding this word exceeds the character limit for the line
        if current_chars + word_len + 1 > max_chars:  # +1 for the space
            # If we are already on the second line, start a new group
            if current_lines == max_lines:
                groups.append({
                    'words': current_group,
                    'start': current_group[0]['start'],
                    'end': current_group[-1]['end']
                })
                current_group = [word]
                current_chars = word_len
                current_lines = 1
            else:
                # Add a new line
                current_lines += 1
                current_chars = word_len
                current_group.append(word)
        else:
            current_chars += word_len + (1 if current_group else 0)
            current_group.append(word)

    # Add the last group if it exists
    if current_group:
        groups.append({
            'words': current_group,
            'start': current_group[0]['start'],
            'end': current_group[-1]['end']
        })

    return groups

def balance_group_timing(groups, min_duration=0.7, max_duration=5.0):
    """
    Adjust group timings to avoid overlap and 
    respect minimum/maximum durations
    """
    for i, group in enumerate(groups):
        duration = group['end'] - group['start']
        
        # Adjust minimum/maximum duration
        if duration < min_duration:
            extra = (min_duration - duration) / 2
            group['start'] = max(group['start'] - extra, 0)
            group['end'] += extra
        elif duration > max_duration:
            mid_point = (group['start'] + group['end']) / 2
            group['start'] = mid_point - (max_duration / 2)
            group['end'] = mid_point + (max_duration / 2)

        # Avoid overlap with previous group
        if i > 0:
            prev_group = groups[i-1]
            if group['start'] <= prev_group['end']:
                gap = (prev_group['end'] - group['start']) / 2
                prev_group['end'] -= gap
                group['start'] += gap

def format_srt_block(lines):
    """Format text lines balancing them"""
    if not lines:
        return []
    
    total_chars = sum(len(line) for line in lines)
    if total_chars <= 40:
        return [' '.join(lines)]
        
    # Try to balance into two lines
    mid_point = total_chars // 2
    current_chars = 0
    split_idx = 0
    
    words = ' '.join(lines).split()
    line1 = []
    
    for i, word in enumerate(words):
        if current_chars < mid_point:
            line1.append(word)
            current_chars += len(word) + 1
        else:
            split_idx = i
            break
            
    line2 = words[split_idx:]
    
    return [' '.join(line1), ' '.join(line2)]

def convert_segment_to_srt(segment):
    """Convert a segment into SRT blocks"""
    if 'words' not in segment:
        return []
        
    # Group words respecting limits
    groups = get_word_groups(segment['words'])
    
    # Adjust group timings
    balance_group_timing(groups)
    
    srt_blocks = []
    for group in groups:
        words_text = [w['word'].strip() for w in group['words']]
        formatted_lines = format_srt_block(words_text)
        
        if formatted_lines:
            srt_blocks.append({
                'start': group['start'],
                'end': group['end'],
                'lines': formatted_lines
            })
    
    return srt_blocks

def get_balanced_word_blocks(words, max_chars=40, max_lines=2):
    """
    Group words into balanced blocks, keeping original timings
    and respecting character/line limits
    """
    # First join hyphenated words
    words = join_hyphenated_words(words)
    
    blocks = []
    current_block = []
    current_line = []
    current_chars = 0
    lines_count = 1
    
    for word in words:
        word_text = word['word'].strip()
        word_len = len(word_text)
        
        # Check if adding this word exceeds current line limit
        if current_chars + word_len + 1 > max_chars:
            if lines_count == max_lines:
                # Finish current block
                if current_line:
                    current_block.extend(current_line)
                if current_block:
                    blocks.append({
                        'words': current_block,
                        'start': current_block[0]['start'],
                        'end': current_block[-1]['end'],
                        'text': ' '.join(w['word'].strip() for w in current_block)
                    })
                # Start new block with current word
                current_block = [word]
                current_line = []
                current_chars = word_len
                lines_count = 1
            else:
                # Add current line to block and start new line
                if current_line:
                    current_block.extend(current_line)
                current_line = [word]
                current_chars = word_len
                lines_count += 1
        else:
            current_line.append(word)
            current_chars += word_len + (1 if current_line else 0)
    
    # Add remaining words if any
    if current_line:
        current_block.extend(current_line)
    if current_block:
        blocks.append({
            'words': current_block,
            'start': current_block[0]['start'],
            'end': current_block[-1]['end'],
            'text': ' '.join(w['word'].strip() for w in current_block)
        })
    
    return blocks

def format_block_lines(block, max_chars=40):
    """
    Format block text into up to two balanced lines
    """
    words = block['text'].split()
    total_chars = len(block['text'])
    
    if total_chars <= max_chars:
        return [block['text']]
        
    # Try to find the most balanced split point
    best_diff = float('inf')
    best_split = None
    
    for i in range(1, len(words)):
        line1 = ' '.join(words[:i])
        line2 = ' '.join(words[i:])
        
        if len(line1) <= max_chars and len(line2) <= max_chars:
            diff = abs(len(line1) - len(line2))
            if diff < best_diff:
                best_diff = diff
                best_split = (line1, line2)
    
    return list(best_split) if best_split else [block['text']]

def adjust_block_timing(blocks, min_gap=0.01):
    """
    Adjust block timings to avoid overlap and respect min/max durations
    """
    for i in range(len(blocks)):
        current = blocks[i]
        
        # Get exact word timings
        start_time = current['words'][0]['start']
        end_time = current['words'][-1]['end']
        
        # Set exact timings from words
        current['start'] = float(start_time)
        current['end'] = float(end_time)
        
        # Add small gap between blocks if needed
        if i > 0:
            prev = blocks[i-1]
            if current['start'] < prev['end'] + min_gap:
                current['start'] = prev['end'] + min_gap

def segments2srt(segments, text_type='words'):
    """
    Generate SRT file from Whisper segments
    """
    srt_content = []
    sequence_number = 1

    for segment in segments:
        if text_type not in segment:
            continue
            
        # Group words into balanced blocks
        blocks = get_balanced_word_blocks(segment['words'])
        
        # Adjust block timings
        adjust_block_timing(blocks)
        
        # Generate SRT blocks
        for block in blocks:
            formatted_lines = format_block_lines(block)
            if formatted_lines:
                srt_block = (
                    f"{sequence_number}\n"
                    f"{format_time_srt(block['start'])} --> {format_time_srt(block['end'])}\n"
                    f"{chr(10).join(formatted_lines)}\n"
                )
                srt_content.append(srt_block)
                sequence_number += 1

    return '\n'.join(srt_content)

def join_hyphenated_words(words):
    """
    Join words that should be hyphenated.
    Example: "post" and "-catrina" become "post-catrina"
    """
    result = []
    i = 0
    while i < len(words):
        word = words[i]
        word_text = word['word'].strip()
        
        # Check if next word starts with hyphen
        if i < len(words) - 1 and words[i + 1]['word'].strip().startswith('-'):
            next_word = words[i + 1]
            # Join the words with hyphen
            joined_word = {
                'word': word_text + next_word['word'].strip(),
                'start': word['start'],
                'end': next_word['end']
            }
            result.append(joined_word)
            i += 2
        else:
            result.append(word)
            i += 1
    return result