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
# no ht cut samples: ~18k evts/h
# --> 18k / 40 = 450 hour... Need to split files per job
#     40 * 8 = 320 evts for ~8h jobs, 16k/320 = 50 jobs

# For debugging
# $ set
# $     mz 150
# $     items b=1 nmax=1 \ 
# $       ls(root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/gen/nohtcut_Aug04_mz150/*.root)
# $     endset

#$ set
#$     mz 150
#$     items b=2 \ 
#$       ls(root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/gen/nohtcut_Aug04_mz150/*.root)
#$     endset
#$ set
#$     mz 250
#$     items b=2 \ 
#$       ls(root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/gen/nohtcut_Aug04_mz250/*.root)
#$     endset
#$ set
#$     mz 450
#$     items b=2 \ 
#$       ls(root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/gen/nohtcut_Aug04_mz450/*.root)
#$     endset
#$ set
#$     mz 650
#$     items b=2 \ 
#$       ls(root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/gen/nohtcut_Aug04_mz650/*.root)
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
    'boost' : 0.,
    }
part = qondor.get_proc_id() + 1

for i_rootfile, rootfile in enumerate(qondor.get_item()):
    # Ensure unique part name per rootfile across jobs; Not sure if necessary for SIM>MINIAOD
    svjpart = 1000 * part + i_rootfile

    qondor.logger.info('Job %s: Processing %s', qondor.get_proc_id(), rootfile)
    extended_physics = dict(physics, part=svjpart, max_events=max_events)

    expected_infile = osp.join(
        cmssw.cmssw_src, 'SVJ/Production/test',
        svjqondor.formatted_filename('step1_LHE-GEN', **extended_physics)
        )

    seutils.cp(rootfile, expected_infile)

    svjqondor.run_step_cmd(
        cmssw,
        inpre='step1_LHE-GEN', outpre='step1_SIM', **extended_physics
        )

    # Try the reco step a few times, since it can often break because of intermittent network
    # problems
    i_attempt = 0
    while(True):
        try:
            svjqondor.run_step_cmd(
                cmssw,
                inpre='step1_SIM', outpre='step3_DIGI-RECO', **extended_physics
                )
            break
        except:
            if i_attempt == 5:
                qondor.logger('RECO step permanently failed')
                raise
            else:
                qondor.logger('Caught exception on RECO step')
                qondor.logger('This was attempt %s; Sleeping 60s and retrying', i_attempt)
                from time import sleep
                sleep(60)
                i_attempt += 1

    expected_outfile = svjqondor.run_step_cmd(
        cmssw,
        inpre='step3_DIGI-RECO', outpre='step4_MINIAOD', **extended_physics
        )

    seutils.cp(
        expected_outfile,
        'root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/miniaod/nohtcut_{date}_mz{mz}/{part}_{i_rootfile}.root'
        .format(date=qondor.get_submission_time().strftime('%b%d'), mz=mz, part=part, i_rootfile=i_rootfile)
        )
