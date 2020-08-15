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

# raw rate: ~7500/h (60k for 8h, 75k for 10h)
# Matching eff ~ 0.4, so about 3000/h effective
# About 0.131 MB/evt

# Go for ~4h jobs, 1M total events, do 27 jobs with 37500 events.
# Need about 2000MB disk at minimum, not counting the .lhe
#$ htcondor request_disk 5000MB
#$ max_events 8000
#$ njobs 20

# # For debugging:
# #$ set
# #$  mz 650
# #$  max_events 10000
# #$  njobs 1
# #$  endset

# Do the higher masses first
#$ set
#$  mz 650
#$  endset
#$ set
#$  mz 450
#$  endset
#$ set
#$  mz 250
#$  endset
#$ set
#$  mz 150
#$  endset

import qondor, seutils, svjqondor, os.path as osp
cmssw = qondor.init_cmssw()

mz = int(qondor.get_var('mz'))
max_events = int(qondor.get_var('max_events'))

# CMSSW files with ~18k events are hard to manage
# Run in blocks of 400 max_events, ~200 evts net per output
entries_per_file = 400
n_blocks = int((0.5*max_events) / entries_per_file)

physics = {
    'year' : 2018,
    'mz' : mz,
    'mdark' : 20.,
    'rinv' : 0.3,
    'boost' : 0.,
    }
svjqondor.download_mg_tarball(dst=osp.join(cmssw.cmssw_src, 'SVJ/Production/test'), **physics)
part = qondor.get_proc_id() + 1

for i_block in range(n_blocks):
    part_for_svj = 1000*part + i_block  # Also need to ensure uniqueness per block

    expected_outfile = svjqondor.run_step_cmd(
        cmssw,
        inpre='step0_GRIDPACK', outpre='step1_LHE-GEN', part=part_for_svj, max_events=entries_per_file, **physics
        )

    seutils.cp(
        expected_outfile,
        'root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/gen/nohtcut_{date}_mz{mz}/{part}_{i_block}.root'
        .format(date=qondor.get_submission_time().strftime('%b%d'), mz=mz, part=part, i_block=i_block)
        )
