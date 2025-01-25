from pathlib import Path
# Append project to python search path in order to resolve local packages.
import sys
sys.path.append(Path('./').absolute().name)

from utils.io_helper import IOHelper
from pathlib import Path
example_file = Path('./test.txt')
example_file.touch(exist_ok=True)


io_helper = IOHelper(output_dir=Path('app/work_dir/output').absolute())

io_helper.init_work_dir([example_file.absolute().name])

file_inside_temp = Path(f'{io_helper.work_dir.name}/tester.txt')
file_inside_temp.touch()

io_helper.create_zipped_output('tester.zip')

io_helper.cleanup()