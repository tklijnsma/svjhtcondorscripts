# Latest updates: Subjet counts rather than offsets
#$ file cmssw_tarball root://cmseos.fnal.gov//store/user/klijnsma/semivis/treemaker-tarballs/CMSSW_10_2_21_sjcountsAug18.tar.gz
#$ sites_blacklist *_RU_* *FNAL* *IFCA* *KIPT* T3_IT_Trieste T2_TR_METU

#$ set
#$  mz 150
#$  items b=50 ls(root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/miniaod/nohtcutfromscratch_Sep01_mz150_epf640_series8000/8*.root)
# $  items b=50 ls(root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/miniaod/nohtcutfromscratch_Aug31_mz150_*series7000/7*.root)
# $ items n=5 ls(root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/miniaod/nohtcut_Aug05_mz150/*.root)
# $ items b=20 ls(root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/miniaod/nohtcutfromscratch_Aug25_mz150/4*.root)
# $ items b=20 ls(root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/miniaod/nohtcutfromscratch_Aug25_mz150/5*.root)
# $ items b=50 ls(root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/miniaod/nohtcutfromscratch_Aug31_mz150/6*.root)
#$  endset
# #$ set
# #$  mz 250
# #$  items b=50 ls(root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/miniaod/nohtcutfromscratch_Aug31_mz250_*series7000/7*.root)
# # $ items n=5 ls(root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/miniaod/nohtcut_Aug05_mz250/*.root)
# # $ items b=20 ls(root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/miniaod/nohtcutfromscratch_Aug25_mz250/4*.root)
# # $ items b=20 ls(root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/miniaod/nohtcutfromscratch_Aug25_mz250/5*.root)
# #$  endset
# #$ set
# #$  mz 450
# # $ items n=5 ls(root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/miniaod/nohtcut_Aug05_mz450/*.root)
# # $ items b=20 ls(root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/miniaod/nohtcutfromscratch_Aug25_mz450/4*.root)
# # $ items b=20 ls(root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/miniaod/nohtcutfromscratch_Aug25_mz450/5*.root)
# #$  endset
# #$ set
# #$  mz 650
# # $ items n=5 ls(root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/miniaod/nohtcut_Aug05_mz650/*.root)
# # $ items b=20 ls(root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/miniaod/nohtcutfromscratch_Aug25_mz650/4*.root)
# # $ items b=20 ls(root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/miniaod/nohtcutfromscratch_Aug25_mz650/5*.root)
# #$  endset

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
    'root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/treemaker/nohtcutfromscratch_{date}_mz{mz}_epf640_series8000/{part}.root'
    .format(date=qondor.get_submission_time().strftime('%b%d'), mz=qondor.get_var('mz'), part=qondor.get_proc_id()),
    )
