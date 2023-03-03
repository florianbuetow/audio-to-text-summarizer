class NLPUtil:

    def __init__(self):
        pass

    def split_text_by_punctuation(text: str) -> list:
        """
        Split the text into chunks by punctuation. To avoid splitting up sentences, we only split at periods
        if the chunk is less than 32 characters or the total length of the chunk is less than 128 characters.
        :return:
        """
        result = []
        text = text.strip()

        # find all the positions of punctuation in text
        positions, curr_pos = [0], 0
        while curr_pos >= 0:
            curr_pos = text.find('.', curr_pos)
            if curr_pos >= 0:
                positions.append(curr_pos)
                curr_pos += 1

        if len(positions) > 1 and positions[1] == positions[0]: positions = positions[1:]
        if positions[-1] != len(text) - 1: positions.append(len(text))

        # split the text by punctuation
        tmp = []
        tmp_len = 0
        prev_pos = 0
        countdown = 0
        for pos in positions:
            length = pos - prev_pos
            part = text[prev_pos:pos + 1]
            if countdown == 0 and length >= 32 and tmp_len >= 64:
                result.append("".join(tmp))
                tmp, tmp_len = [], 0
            elif length < 32:
                countdown = 2  # prevent splitting at the next two punctuation marks
            tmp.append(part)
            tmp_len += len(part)
            prev_pos = pos + 1
            if countdown: countdown -= 1
        if tmp:
            result.append("".join(tmp))
        return result
