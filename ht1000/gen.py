# SVJ stuff is all compiled under slc6 :(
#$ htcondor +REQUIRED_OS "rhel6"
#$ htcondor +DesiredOS REQUIRED_OS
#$ env gccsetup /cvmfs/sft.cern.ch/lcg/contrib/gcc/7/x86_64-slc6-gcc7-opt/setup.sh
#$ env pipdir /cvmfs/sft.cern.ch/lcg/releases/pip/19.0.3-06476/x86_64-slc6-gcc7-opt
#$ env rootsetup /cvmfs/sft.cern.ch/lcg/releases/LCG_95/ROOT/6.16.00/x86_64-slc6-gcc7-opt/ROOT-env.sh
#$ env SCRAM_ARCH slc6_amd64_gcc700

#$ pip module-install svjqondor
#$ file cmssw_tarball root://cmseos.fnal.gov//store/user/klijnsma/semivis/cmssw_tarballs/CMSSW_10_2_18_htfilterprintout.tar.gz
#$ htcondor request_memory 1024MB
#$ htcondor request_disk 1800MB

# raw rate: ~7500/h (60k for 8h, 75k for 10h)
# effective evts
#      1h  10h
# 650  50  500
# 450  15  150
# 250  4   40
# 150  1   10

# For debugging:
# $ htcondor hold True
# $ set
# $  mz 650
# $  max_events 300
# $  njobs 1
# $  endset

# Do the higher masses first
# $ set
# $  mz 650
# $  max_events 75000
# $  njobs 10
# $  endset
# $ set
# $  mz 450
# $  max_events 75000
# $  njobs 30
# $  endset
#$ set
#$  mz 250
#$  max_events 75000
#$  njobs 200
#$  endset
#$ set
#$  mz 150
#$  max_events 75000
#$  njobs 600
#$  endset

import qondor, seutils, svjqondor, os.path as osp
cmssw = qondor.init_cmssw()

mz = int(qondor.get_var('mz'))
max_events = int(qondor.get_var('max_events'))

offset = 3000 # apply an offset to the part to generate new events
part = qondor.get_proc_id() + 1 + offset # proc_id starts at 0, runSVJ expects starting at 1

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
    inpre='step0_GRIDPACK', outpre='step1_LHE-GEN', part=part, max_events=max_events, **physics
    )

seutils.cp(
    expected_outfile,
    'root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/gen/ht1000_{date}_mz{mz}/{part}.root'
    .format(date=qondor.get_submission_time().strftime('%b%d'), mz=mz, part=part)
    )
