import pathlib

class JobDetails():
    def __init__(self, jobFilenames):
        self.jobFilenames = jobFilenames
        self.jobBasenames = [pathlib.Path(s).stem for s in self.jobFilenames]
        self.numJobs = len(self.jobFilenames)
        self.jobNumber = 0
        self.cjobsID = None
        
        self.scheduler = None
        self.software = None
        self.containerFile = None
        self.singularityVersion = None
        self.GID = None
        
        self.mode = 'single'
        self.isArray = False
        self.isMassive = False
        
        self.cpu = None
        self.ram = None
        self.time = None
        
        self.options = None
        self.standalone = False
        
        self.localDir = None
        self.scrDir = None
        self.usrScrDir = None
        self.exeDir = None
        self.ctDirRemote = None
        self.ctDirLocal = None
        self.bashJobname = '$(get_csv_element cjobs_joblist.csv "$job_number" 2)'
        self.bashBasename = fr"$(echo $job | rev | cut -f 2- -d '.' | rev)"
        
        self.sendAdditionalFiles = False
        self.additionalFiles = []

    def write_joblist(self, filename):
        with open(filename, mode='w') as f:
            for i, file in enumerate(self.jobFilenames,1):
                f.write(f"{i},{file}\n")
    
    def include_additional_file(self, file, rename=''):
        self.additionalFiles.append((file, rename))
