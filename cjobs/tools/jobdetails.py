import datetime
from tools.util import get_basename


class JobDetails():
    def __init__(self, filenames):
        self.filenames = filenames
        self.basenames = [get_basename(s) for s in self.filenames]
        self.numJobs = len(self.filenames)

    def write_joblist(self, filename):
        with open(filename, mode='w') as f:
            for i, file in enumerate(self.filenames,1):
                f.write(f"{i},{file}\n")
