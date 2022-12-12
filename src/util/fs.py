import os
from abc import ABC, abstractmethod


class FSUtil(ABC):

    @abstractmethod
    def list_files(self, directory: str, extension: str = "") -> list[str]:
        pass

    @abstractmethod
    def get_size_mb(self, file: str) -> int:
        pass

    @abstractmethod
    def exists(self, file: str) -> bool:
        pass

    @abstractmethod
    def ensure_path_exists(self, path: str):
        pass

    @abstractmethod
    def load_text(self, src_file: str) -> str:
        pass

    @abstractmethod
    def save_text(self, dst_file: str, text: str, overwrite: bool = False) -> bool:
        pass

    @abstractmethod
    def source_to_target(self, srcFile: str, dstPath: str, dstExtension: str) -> str:
        pass

    @abstractmethod
    def is_absolute_path(self, path: str) -> bool:
        pass

    @abstractmethod
    def normalise_path(self, path: str) -> str:
        pass


class LocalFSUtil(FSUtil):

    def list_files(self, directory: str, extension: str = "") -> list[str]:
        if extension and not extension.startswith('.'):
            extension = '.' + extension
        file_list = []
        for file_name in os.listdir(directory):
            if not extension or file_name.endswith(extension):
                file = os.path.join(directory, file_name)
                if os.path.isfile(file):
                    file_list.append(file)
        return file_list

    def delete_file_if_empty(self, path: str):
        if os.path.isfile(path) and os.path.getsize(path) == 0:
            os.remove(path)
            return True
        return False

    def get_size_str(self, file: str) -> str:
        size = self.get_size_bytes(file)
        if size < 1024:
            return f"{size} bytes"
        elif size < 1024 * 1024:
            return f"{self.get_size_kb(file)} KB"
        else:
            return f"{self.get_size_mb(file)} MB"

    def get_size_mb(self, file: str) -> int:
        return int(self.get_size_bytes(file) / (1024 * 1024))

    def get_size_kb(self, file: str) -> int:
        return int(self.get_size_bytes(file) / 1024)

    def get_size_bytes(self, file: str) -> int:
        return int(os.path.getsize(file))

    def exists(self, file: str) -> bool:
        return os.path.exists(file)

    def ensure_path_exists(self, path: str) -> bool:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            return True

    def load_text(self, src_file: str) -> str:
        with open(src_file, 'rt') as f:
            return f.read()

    def save_text(self, dst_file: str, text: str, overwrite: bool = False) -> bool:
        if not overwrite and os.path.exists(dst_file):
            return False
        with open(dst_file, 'wt') as f:
            f.write(text)
        return True

    def source_to_target(self, srcFile: str, dstPath: str, dstExtension: str) -> str:
        baseName = os.path.basename(srcFile)
        baseName = os.path.splitext(baseName)[0]
        return os.path.join(dstPath, baseName + dstExtension)

    def is_absolute_path(self, path: str) -> bool:
        return os.path.isabs(path)

    def normalise_path(self, path: str) -> str:
        return os.path.normpath(path)

    def escape_path(self, path: str) -> str:
        return path.replace('(', '\(').replace(')', '\)').replace(' ', '\ ').replace("'", "\\'")
