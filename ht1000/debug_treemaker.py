# Latest updates: Flat subjets with offset vector, no longer TLorentzVectors
#$ file cmssw_tarball root://cmseos.fnal.gov//store/user/klijnsma/semivis/treemakerht1000/CMSSW_10_2_21_treemakerJul28.tar.gz

#$ sites_blacklist *_RU_* *FNAL*

import os.path as osp
import qondor, seutils
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
    ' inputFiles=root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1056.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1057.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1058.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1059.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1060.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1062.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1063.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1064.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1069.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/107.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1073.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1074.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1075.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1076.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1078.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1080.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1081.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1084.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1085.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1086.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1087.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1088.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1089.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1090.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1091.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1092.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1093.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1095.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1096.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1097.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1098.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1099.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/110.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1100.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1101.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1102.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1103.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1104.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1105.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1106.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1107.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1108.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1109.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1111.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1112.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1113.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1116.root,'
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/1118.root'
    ])

expected_outfile = osp.join(cmssw.cmssw_src, 'TreeMaker/Production/test', 'outfile_RA2AnalysisTree.root')

# seutils.cp(
#     expected_outfile,
#     'root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/treemaker/ht1000_nonested_{date}_mz{mz}/{part}.root'
#     .format(date=qondor.get_submission_time().strftime('%b%d'), mz=qondor.get_var('mz'), part=qondor.get_proc_id())
#     )
