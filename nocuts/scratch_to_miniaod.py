# SVJ stuff is all compiled under slc6 :(
#$ htcondor +REQUIRED_OS "rhel6"
#$ htcondor +DesiredOS REQUIRED_OS
#$ env gccsetup /cvmfs/sft.cern.ch/lcg/contrib/gcc/7/x86_64-slc6-gcc7-opt/setup.sh
#$ env pipdir /cvmfs/sft.cern.ch/lcg/releases/pip/19.0.3-06476/x86_64-slc6-gcc7-opt
#$ env rootsetup /cvmfs/sft.cern.ch/lcg/releases/LCG_95/ROOT/6.16.00/x86_64-slc6-gcc7-opt/ROOT-env.sh
#$ env SCRAM_ARCH slc6_amd64_gcc700
#$ sites_blacklist *_RU_* *FNAL* *IFCA* *KIPT* T3_IT_Trieste T2_TR_METU T2_US_Vanderbilt

#$ pip module-install svjqondor
#$ file cmssw_tarball root://cmseos.fnal.gov//store/user/klijnsma/semivis/cmssw_tarballs/CMSSW_10_2_18_htfilterprintout.tar.gz
#$ htcondor request_memory 1024MB

#$ njobs 800

# Do the higher masses first
# $ set
# $  mz 650
# $  endset
# $ set
# $  mz 450
# $  endset
# $ set
# $  mz 250
# $  endset
#$ set
#$  mz 150
#$  endset

import qondor, seutils, svjqondor, os.path as osp
cmssw = qondor.init_cmssw()
mz = int(qondor.get_var('mz'))

# Rate is about 40 evts/h
entries_per_file = 640
series = 8000
part_for_svj = qondor.get_proc_id() + series

physics = {
    'year' : 2018,
    'mz' : mz,
    'mdark' : 20.,
    'rinv' : 0.3,
    'boost' : 0.,
    }
svjqondor.download_mg_tarball(dst=osp.join(cmssw.cmssw_src, 'SVJ/Production/test'), **physics)

gen_outfile = svjqondor.run_step_cmd(
    cmssw,
    inpre='step0_GRIDPACK', outpre='step1_LHE-GEN', part=part_for_svj, max_events=entries_per_file, **physics
    )

expected_outfile = svjqondor.run_sim_reco_miniaod(cmssw, part=part_for_svj, rootfile=gen_outfile, **physics)

seutils.cp(
    expected_outfile,
    'root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/miniaod/nohtcutfromscratch_{date}_mz{mz}_epf{epf}_series{series}/{part}.root'
    .format(date=qondor.get_submission_time().strftime('%b%d'), mz=mz, epf=entries_per_file, series=series, part=part_for_svj)
    )
