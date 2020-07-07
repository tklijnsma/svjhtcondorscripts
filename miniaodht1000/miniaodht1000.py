#$ pip install svjqondor
#$ file cmssw_tarball root://cmseos.fnal.gov//store/user/klijnsma/semivis/cmssw_tarballs/CMSSW_10_2_18_htfilterprintout.tar.gz
#$ htcondor request_memory 4096MB
#$ htcondor request_disk 1800MB

# Number of evts per mass:
# 650: total: 8869  (28 files, 316.75 evts/file)
# 450: total: 2916  (28 files, 104.14 evts/file)
# 250: total: 4979  (121 files, 41.15 evts/file)
# 150: total: 2732  (210 files, 13.01 evts/file)

# $ set
# $     mz 150
# $     items b=15 \ 
# $      ls(root://cmseos.fnal.gov//store/user/klijnsma/semivis/genht1000/Jun30_mz150/*.root) \
# $      ls(root://cmseos.fnal.gov//store/user/klijnsma/semivis/genht1000/Jul02_mz150/*.root)
# $     endset
# $ set
# $     mz 250
# $     items b=5 \ 
# $      ls(root://cmseos.fnal.gov//store/user/klijnsma/semivis/genht1000/Jun30_mz250/*.root) \
# $      ls(root://cmseos.fnal.gov//store/user/klijnsma/semivis/genht1000/Jul02_mz250/*.root)
# $     endset
# $ set
# $     mz 450
# $     items b=2 \ 
# $      ls(root://cmseos.fnal.gov//store/user/klijnsma/semivis/genht1000/Jun30_mz450/*.root) \
# $      ls(root://cmseos.fnal.gov//store/user/klijnsma/semivis/genht1000/Jul02_mz450/*.root)
# $     endset
#$ set
#$     mz 650
#$     items b=1 \ 
#$      ls(root://cmseos.fnal.gov//store/user/klijnsma/semivis/genht1000/Jun30_mz650/*.root) \
#$      ls(root://cmseos.fnal.gov//store/user/klijnsma/semivis/genht1000/Jul02_mz650/*.root)
#$     endset

import os.path as osp, argparse, re
import qondor, seutils, svjqondor

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

rootfiles = qondor.get_item()
qondor.logger.info('Job %s: Processing %s', qondor.get_proc_id(), rootfiles)
for rootfile in rootfiles:
    part = int(osp.basename(rootfile).replace('.root', '')) # Get part from the gen step
    extended_physics = dict(physics, part=part, max_events=max_events)
    
    expected_infile = osp.join(
        cmssw.cmssw_src, 'SVJ/Production/test',
        svjqondor.formatted_filename('step1_LHE-GEN', **extended_physics)
        )
    if not osp.isfile(expected_infile): seutils.cp(rootfile, expected_infile)

    svjqondor.run_step_cmd(
        cmssw,
        inpre='step1_LHE-GEN', outpre='step1_SIM', **extended_physics
        )

    svjqondor.run_step_cmd(
        cmssw,
        inpre='step1_SIM', outpre='step3_DIGI-RECO', **extended_physics
        )

    expected_outfile = svjqondor.run_step_cmd(
        cmssw,
        inpre='step3_DIGI-RECO', outpre='step4_MINIAOD', **extended_physics
        )

    seutils.cp(
        expected_outfile,
        'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz{mz}/{part}.root'
        .format(mz=mz, part=part)
        )
