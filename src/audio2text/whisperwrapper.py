import os, logging, whisper


class WhisperWrapper:

    def __init__(self, model_name: str, lazy_loading: bool = True):
        self._model_name = model_name
        self._model = None
        if not lazy_loading: self._get_model()

    def _get_model(self):
        if self._model is None:
            self._model = whisper.load_model(self._model_name)
        return self._model

    def __str__(self):
        return f"WhisperWrapper(model_name={self._model_name}, loaded={self._model is not None})"

    def transcribe(self, srcFile: str) -> str:
        model = self._get_model()
        result = model.transcribe(srcFile)
        return result['text']

    def transcribe_to_file(self, src_file: str, dst_file: str, overwrite: bool = False) -> bool:
        if not overwrite and os.path.exists(dst_file):
            logging.warning(f"File '{dst_file}' already exists. Skipping transcription.")
            return False
        try:
            with open(dst_file, 'w') as fh:
                pass
        except Exception as e:
            logging.error(f"Cannot write to destination '{dst_file}'.")
            logging.error(e)
            return False

        text = self.transcribe(src_file)
        with open(dst_file, 'w') as f:
            f.write(text)
        return True
