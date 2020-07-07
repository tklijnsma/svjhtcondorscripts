#$ file cmssw_tarball root://cmseos.fnal.gov//store/user/klijnsma/semivis/treemakerht1000/CMSSW_10_2_21_treemaker.tar.gz

# $ set
# $  mz 150
# $  items n=4 ls(root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/*.root)
# $  endset
# $ set
# $  mz 250
# $  items n=4 ls(root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz250/*.root)
# $  endset
# $ set
# $  mz 450
# $  items n=4 ls(root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz450/*.root)
# $  endset
#$ set
#$  mz 650
#$  items n=4 ls(root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz650/*.root)
#$  endset

# For a debug job:
# $ set
# $  mz 150
# $  items n=4 ls(root://cmseos.fnal.gov//store/user/klijnsma/semivis/miniaodht1000/Jul04_mz150/8*.root)
# $  endset

import argparse, os.path as osp
parser = argparse.ArgumentParser()
parser.add_argument('--dump', action='store_true')
args = parser.parse_args()

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
    ' debugjets=1 '
    + (' dump=1' if args.dump else '')
    + (' inputFiles=' + ','.join(qondor.get_item()))
    ])

expected_outfile = osp.join(cmssw.cmssw_src, 'TreeMaker/Production/test', 'outfile_RA2AnalysisTree.root')

seutils.cp(
    expected_outfile,
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/treemakerht1000/mz{0}_{1}.root'
    .format(qondor.get_var('mz'), qondor.get_proc_id())
    )
