#$ pip module-install svjqondor
#$ file cmssw_tarball root://cmseos.fnal.gov//store/user/klijnsma/semivis/cmssw_tarballs/CMSSW_10_2_18_htfilterprintout.tar.gz
#$ items 150 250 450 650

import qondor, svjqondor, os.path as osp

cmssw = qondor.init_cmssw()

physics = {
    'year' : 2018,
    'mz' : float(qondor.get_item()),
    'mdark' : 20.,
    'rinv' : 0.3,
    'boost' : 1000.,
    }

svjqondor.download_mg_tarball(dst=osp.join(cmssw.cmssw_src, 'SVJ/Production/test'), **physics)

# Aim for 25 events times a factor
max_events = {
    250 : 2000 * 2,
    450 : 150 * 10,
    50  : 15000, # aim for 10 instead of 25
    650 : 85 * 10
    }[int(qondor.get_item())]

expected_outfile = svjqondor.run_step_cmd(
    cmssw,
    inpre='step0_GRIDPACK', outpre='step1_LHE-GEN', part=1, max_events=max_events, **physics
    )

seutils.cp(
    expected_outfile,
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/triggerstudy/{0}.root'
    .format(int(qondor.get_item()))
    )

# No need for stageout, only care about the efficiency for now