from typing import List
from pathlib import Path
from zipfile import ZipFile
from tempfile import TemporaryDirectory

class IOHelper():
    def __init__(self,
                 output_dir: Path,
                 user_input_dir_name: str = 'user_input'
    ):
        self.output_dir = output_dir
        self.user_input_dir_name = user_input_dir_name
        self.work_dir = None
    
    def init_work_dir(self, file_pathes: List[str]) -> None:
        self.work_dir = TemporaryDirectory()
        user_input_dir = Path(self.work_dir.name) / self.user_input_dir_name
        user_input_dir.mkdir(exist_ok=True)
        
        for file_path in file_pathes:
            file = Path(file_path)
            file_name = file_path.split('/')[-1]
            file.rename(user_input_dir / file_name)

    def create_zipped_output(self, output_name: str) -> str:
        zip_path = self.output_dir / output_name
        work_dir_path = Path(self.work_dir.name)
        with ZipFile(zip_path, 'w') as zipf:
            for file in work_dir_path.iterdir():
                if file.is_file():
                    arcname = file.relative_to(work_dir_path)
                    zipf.write(file, arcname=arcname)
        return str(zip_path.absolute())

    def cleanup(self) -> None:
        if self.work_dir:
            self.work_dir.cleanup()