import os, logging


class FFmpegAudioExtraction:
    """
    The FFmpegWrapper class provides a simple interface for converting files using the ffmpeg command-line tool.
    The convert() method takes a source file and a destination file as input, and uses the ffmpeg tool to
    convert the source file to mp3 format, storing the result in the destination file.

    The supported target audio formats and their ffmpeg conversion settings are hardcoded in the constructor.

    Note: The specified wav format is the only format that can be read by whisper without any further pre-processing.
    If whisper is given another audio format such as an MP3, it will use ffmpeg to convert the MP3 into this PCM wav format before transcribing.
    """

    def __init__(self):
        # List of supported target formats and their ffmpeg conversion settings
        self._conversion_settings = {
            '.mp3': '-vn -acodec libmp3lame -ac 2 -ab 160k -ar 48000',
            '.wav': '-vn -ar 16000 -ac 1 -c:a pcm_s16le'
        }

    def convert_to_audio(self, src_file: str, dst_file: str, overwrite: bool = False) -> bool:
        print("Converting file '{}' to '{}'.".format(src_file, dst_file))
        # get the extension of the destination file
        dst_extension = os.path.splitext(dst_file)[1].lower()
        print("dst_extension: {}".format(dst_extension))
        if dst_extension in self._conversion_settings:
            return self._convert_with_ffmpeg(src_file, dst_file, self._conversion_settings[dst_extension], overwrite)
        else:
            raise Exception(f"Unsupported audio format '{dst_extension.upper()}'.")


    def _convert_with_ffmpeg(self, src_file: str, dst_file: str, conversion_settings: str, overwrite: bool = False) -> bool:
        if os.path.exists(dst_file):
            if overwrite:
                os.remove(dst_file)
            else:
                logging.warning(f"File '{dst_file}' already exists. Skipping conversion.")
                return False

        src_file_escaped = self._escape_path(src_file)
        dst_file_escaped = self._escape_path(dst_file)
        cmd = f"ffmpeg -hide_banner -loglevel error -i {src_file_escaped} {conversion_settings} {dst_file_escaped}"
        response = os.system(cmd)
        if response != 0:
            logging.error(f"Error converting file '{src_file}' to '{dst_file}'.")
        return True

    def _escape_path(self, path: str) -> str:
        return path.replace('(', '\(').replace(')', '\)').replace(' ', '\ ').replace("'", "\\'")

