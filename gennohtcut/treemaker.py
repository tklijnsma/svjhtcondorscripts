# Latest updates: Flat subjets with offset vector, no longer TLorentzVectors
#$ file cmssw_tarball root://cmseos.fnal.gov//store/user/klijnsma/semivis/treemakerht1000/CMSSW_10_2_21_treemakerJul28.tar.gz
#$ sites_blacklist *_RU_* *FNAL*

#$ set
#$  mz 150
#$  items n=5 ls(root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/miniaod/nohtcut_Aug05_mz150/*.root)
#$  endset
#$ set
#$  mz 250
#$  items n=5 ls(root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/miniaod/nohtcut_Aug05_mz250/*.root)
#$  endset
#$ set
#$  mz 450
#$  items n=5 ls(root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/miniaod/nohtcut_Aug05_mz450/*.root)
#$  endset
#$ set
#$  mz 650
#$  items n=5 ls(root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/miniaod/nohtcut_Aug05_mz650/*.root)
#$  endset

import qondor, seutils, os.path as osp
cmssw = qondor.init_cmssw()
cmssw.run_commands([
    'cd TreeMaker/Production/test',
    'cmsRun runMakeTreeFromMiniAOD_cfg.py'
    ' numevents=-1'
    ' outfile=outfile'
    ' scenario=Autumn18sig'
    ' lostlepton=0'
    ' doZinv=0'
    ' systematics=0'
    ' deepAK8=0'
    ' deepDoubleB=0'
    ' doPDFs=0'
    ' nestedVectors=False'
    ' debugjets=1'
    ' splitLevel=99'
    + (' inputFiles=' + ','.join(qondor.get_item()))
    ])

expected_outfile = osp.join(cmssw.cmssw_src, 'TreeMaker/Production/test', 'outfile_RA2AnalysisTree.root')

seutils.cp(
    expected_outfile,
    'root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/treemaker/nohtcut_nonested_{date}_mz{mz}/{part}.root'
    .format(date=qondor.get_submission_time().strftime('%b%d'), mz=qondor.get_var('mz'), part=qondor.get_proc_id()),
    )
