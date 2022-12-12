import os, logging

import openai


class GPT3Wrapper:

    def __init__(self, model_name: str, api_key: str):
        openai.api_key = api_key
        self._model_name = model_name

    def summarise_to_file(self, src_file: str, dst_file: str, overwrite: bool = False) -> bool:
        if not overwrite and os.path.exists(dst_file):
            logging.warning(f"File '{dst_file}' already exists. Skipping summarization.")
            return False
        try:
            with open(dst_file, 'w') as fh:
                pass
        except Exception as e:
            logging.error(f"Cannot write to destination '{dst_file}'.")
            logging.error(e)
            return False

        text = self.summarize(src_file)
        with open(dst_file, 'w') as f:
            f.write(text)
        return True

    def summarize(self, text: str) -> str:
        text = f"{text}\n\nTl;dr"  # adding Tl;dr to prompt GPT-3 to create a summary
        response = openai.Completion.create(
            engine=self._model_name,
            prompt=text,
            max_tokens=1024,
            n=1,
            temperature=0.5
        )
        summary = response["choices"][0]["text"]
        if summary.startswith(":"):
            summary = summary[1:]
        summary = summary.strip()
        return summary
