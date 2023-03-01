import os
import yt_dlp
from abc import ABC, abstractmethod


class VideoDownloader(ABC):

    @abstractmethod
    def download(self, video_url: str, dst_path: str, dst_format: str) -> str:
        """Downloads the given video and returns the path to the downloaded file"""
        pass


class YouTubeDownloader(VideoDownloader):

    def download(self, video_url: str, dst_path: str) -> str:
        """Downloads the given video with audio and returns the path to the downloaded file"""
        cmd = f"yt-dlp --paths '{dst_path}' '{video_url}'"
        return self._download(cmd)

    def _download(self, cmd: str) -> str:

        cmd_output = os.popen(cmd).read()
        lines = [line for line in cmd_output.splitlines() if line.count('|') != -1]

        downloaded_file = None
        for line in lines:
            find_str = '[Merger] Merging formats into "'
            find_pos = line.find(find_str)
            if find_pos > -1:
                line = line[find_pos + len(find_str):-1]
                downloaded_file = line.strip()
                continue

            # get the full path of the downloaded file from the output
            find_str = '[download] Destination:'
            find_pos = line.find(find_str)
            if find_pos > -1:
                line = line[find_pos + len(find_str):]
                downloaded_file = line.strip()
                continue

            # get the full path of a previously downloaded file from the output
            find_str = '[download]'
            find_pos = line.find(find_str)
            if find_pos > -1:
                line = line[find_pos + len(find_str):]
                find_str = 'has already been downloaded'
                find_pos = line.find(find_str)
                if find_pos > -1:
                    line = line[:find_pos]
                    downloaded_file = line.strip()
                    break

        if not downloaded_file:
            raise Exception("Download failed")
        return downloaded_file
