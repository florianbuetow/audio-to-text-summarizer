import os, logging


class FFmpegAudioExtraction:
    """
    The FFmpegWrapper class provides a simple interface for converting files using the ffmpeg command-line tool.
    The convert() method takes a source file and a destination file as input, and uses the ffmpeg tool to
    convert the source file to mp3 format, storing the result in the destination file.

    For now, the conversion settings are hardcoded in the constructor.
    """

    def __init__(self):
        self._conversion_settings = "-vn -acodec libmp3lame -ac 2 -ab 160k -ar 48000"

    def convert_to_audio(self, src_file: str, dst_file: str, overwrite: bool = False) -> bool:
        # get the extension of the destination file
        dst_extension = os.path.splitext(dst_file)[1]
        if dst_extension == '.mp3':
            return self.convert_to_mp3(src_file, dst_file, overwrite)
        else:
            raise Exception(f"Unsupported audio format '{dst_extension.upper()}'.")

    def convert_to_mp3(self, src_file: str, dst_file: str, overwrite: bool = False) -> bool:
        if os.path.exists(dst_file):
            if overwrite:
                os.remove(dst_file)
            else:
                logging.warning(f"File '{dst_file}' already exists. Skipping conversion.")
                return False

        src_file_escaped = self._escape_path(src_file)
        dst_file_escaped = self._escape_path(dst_file)
        cmd = f"ffmpeg -hide_banner -loglevel error -i {src_file_escaped} {self._conversion_settings} {dst_file_escaped}"
        print("Executing command: ", cmd)
        response = os.system(cmd)
        if response != 0:
            logging.error(f"Error converting file '{src_file}' to '{dst_file}'.")
        return True

    def _escape_path(self, path: str) -> str:
        return path.replace('(', '\(').replace(')', '\)').replace(' ', '\ ').replace("'", "\\'")

