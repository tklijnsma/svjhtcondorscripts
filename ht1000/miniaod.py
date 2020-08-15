# SVJ stuff is all compiled under slc6 :(
#$ htcondor +REQUIRED_OS "rhel6"
#$ htcondor +DesiredOS REQUIRED_OS
#$ env gccsetup /cvmfs/sft.cern.ch/lcg/contrib/gcc/7/x86_64-slc6-gcc7-opt/setup.sh
#$ env pipdir /cvmfs/sft.cern.ch/lcg/releases/pip/19.0.3-06476/x86_64-slc6-gcc7-opt
#$ env rootsetup /cvmfs/sft.cern.ch/lcg/releases/LCG_95/ROOT/6.16.00/x86_64-slc6-gcc7-opt/ROOT-env.sh
#$ env SCRAM_ARCH slc6_amd64_gcc700

#$ pip install svjqondor
#$ file cmssw_tarball root://cmseos.fnal.gov//store/user/klijnsma/semivis/cmssw_tarballs/CMSSW_10_2_18_htfilterprintout.tar.gz
#$ htcondor request_memory 4096MB
#$ htcondor request_disk 5000MB

# SIM+RECO+MINIAOD: ~40 evts/h
# evts/file: mz150: 13, mz250: 45, mz450: 110, mz650: 300
# files per job (based on 8h jobs, i.e. 320 evts):
# mz150: 25, mz250: 8, mz450: 3, mz650: 1
# Limit mz650 to 20 jobs max, really don't need this many events

# $ set
# $     mz 150
# $     items b=1 nmax=1 \ 
# $       ls(root://cmseos.fnal.gov//store/user/klijnsma/semivis/genht1000/*mz150*/*.root)
# $     endset

#$ set
#$     mz 150
#$     items b=25 \ 
#$       ls(root://cmseos.fnal.gov//store/user/klijnsma/semivis/genht1000/*mz150*/*.root)
#$     endset
#$ set
#$     mz 250
#$     items b=8 \ 
#$       ls(root://cmseos.fnal.gov//store/user/klijnsma/semivis/genht1000/*mz250*/*.root)
#$     endset
#$ set
#$     mz 450
#$     items b=3 \ 
#$       ls(root://cmseos.fnal.gov//store/user/klijnsma/semivis/genht1000/*mz450*/*.root)
#$     endset
#$ set
#$     mz 650
#$     items b=1 nmax=20 \ 
#$       ls(root://cmseos.fnal.gov//store/user/klijnsma/semivis/genht1000/*mz650*/*.root)
#$     endset

import os.path as osp, argparse, re
import qondor, seutils, svjqondor, uuid
seutils.debug()

cmssw = qondor.init_cmssw()

mz = int(qondor.get_var('mz'))
max_events = 10000 # runSVJ wants maxEvents to be passed, just set it large enough
physics = {
    'year' : 2018,
    'mz' : mz,
    'mdark' : 20.,
    'rinv' : 0.3,
    'boost' : 1000.,
    }
part = qondor.get_proc_id() + 1

for i_rootfile, rootfile in enumerate(qondor.get_item()):
    # Ensure unique part name per rootfile across jobs; Not sure if necessary for SIM>MINIAOD
    svjpart = 1000 * part + i_rootfile
    qondor.logger.info('Job %s: Processing %s', qondor.get_proc_id(), rootfile)
    expected_outfile = svjqondor.run_sim_reco_miniaod(cmssw, part=svjpart, rootfile=rootfile, **physics)
    seutils.cp(
        expected_outfile,
        'root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/miniaod/ht1000_{date}_mz{mz}/{part}_{i_rootfile}.root'
        .format(date=qondor.get_submission_time().strftime('%b%d'), mz=mz, part=part, i_rootfile=i_rootfile)
        )
