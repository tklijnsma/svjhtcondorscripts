#$ pip module-install svjqondor
#$ file cmssw_tarball root://cmseos.fnal.gov//store/user/klijnsma/semivis/cmssw_tarballs/CMSSW_10_2_18_htfilterprintout.tar.gz
#$ htcondor request_memory 3000MB
#$ htcondor request_disk 3000MB

# Aim for the following events per job:
# 150 : 400000, # ~105 evts/file,  110 jobs
# 250 : 100000, # ~110 evts/file,  110 jobs
# 450 : 50000,  # ~400 evts/file,  30 jobs
# 650 : 50000,  # ~550 evts/file,  30 jobs

# For debugging:
# $ htcondor hold True
# $ set
# $  mz 650
# $  max_events 300
# $  njobs 1
# $  endset

# Do the higher masses first
#$ set
#$  mz 450
#$  max_events 50000
#$  njobs 30
#$  endset
#$ set
#$  mz 650
#$  max_events 50000
#$  njobs 30
#$  endset
#$ set
#$  mz 150
#$  max_events 400000
#$  njobs 110
#$  endset
#$ set
#$  mz 250
#$  max_events 100000
#$  njobs 110
#$  endset

import qondor, seutils, svjqondor, os.path as osp
cmssw = qondor.init_cmssw()

mz = int(qondor.get_var('mz'))
max_events = int(qondor.get_var('max_events'))
part = qondor.get_proc_id() + 1 # proc_id starts at 0, runSVJ expects starting at 1

physics = {
    'year' : 2018,
    'mz' : mz,
    'mdark' : 20.,
    'rinv' : 0.3,
    'boost' : 1000.,
    }

svjqondor.download_mg_tarball(dst=osp.join(cmssw.cmssw_src, 'SVJ/Production/test'), **physics)

expected_outfile = svjqondor.run_step_cmd(
    cmssw,
    inpre='step0_GRIDPACK', outpre='step1_LHE-GEN', part=1, max_events=max_events, **physics
    )

seutils.cp(
    expected_outfile,
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/genht1000/Jun29_mz{mz}/{part}.root'
    .format(mz=mz, part=part)
    )
