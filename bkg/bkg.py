"""# submit

# List of all the backgrounds by name
bkgs = [
    # TTJet
    'Autumn18.TTJets_TuneCP5_13TeV-madgraphMLM-pythia8',
    'Autumn18.TTJets_SingleLeptFromTbar_TuneCP5_13TeV-madgraphMLM-pythia8',
    'Autumn18.TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8',
    'Autumn18.TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8',
    'Autumn18.TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8',
    'Autumn18.TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8',
    'Autumn18.TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8',
    'Autumn18.TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8',
    'Autumn18.TTJets_SingleLeptFromTbar_genMET-80_TuneCP5_13TeV-madgraphMLM-pythia8',
    'Autumn18.TTJets_SingleLeptFromT_genMET-80_TuneCP5_13TeV-madgraphMLM-pythia8',
    'Autumn18.TTJets_DiLept_genMET-80_TuneCP5_13TeV-madgraphMLM-pythia8',
    # QCD Pt
    'Autumn18.QCD_Pt_80to120_TuneCP5_13TeV_pythia8',
    'Autumn18.QCD_Pt_120to170_TuneCP5_13TeV_pythia8',
    'Autumn18.QCD_Pt_170to300_TuneCP5_13TeV_pythia8',
    'Autumn18.QCD_Pt_300to470_TuneCP5_13TeV_pythia8',
    'Autumn18.QCD_Pt_470to600_TuneCP5_13TeV_pythia8',
    'Autumn18.QCD_Pt_600to800_TuneCP5_13TeV_pythia8',
    'Autumn18.QCD_Pt_800to1000_TuneCP5_13TeV_pythia8_ext1',
    'Autumn18.QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8',
    'Autumn18.QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8',
    'Autumn18.QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8',
    'Autumn18.QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8',
    'Autumn18.QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8',
    # WJetsToLNu
    'Autumn18.WJetsToLNu_HT-70To100_TuneCP5_13TeV-madgraphMLM-pythia8',
    'Autumn18.WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8',
    'Autumn18.WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8',
    'Autumn18.WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8',
    'Autumn18.WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8',
    'Autumn18.WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8',
    'Autumn18.WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8',
    'Autumn18.WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8',
    # ZJetsToNuNu
    'Autumn18.ZJetsToNuNu_HT-100To200_13TeV-madgraph',
    'Autumn18.ZJetsToNuNu_HT-1200To2500_13TeV-madgraph',
    'Autumn18.ZJetsToNuNu_HT-200To400_13TeV-madgraph',
    'Autumn18.ZJetsToNuNu_HT-400To600_13TeV-madgraph',
    'Autumn18.ZJetsToNuNu_HT-600To800_13TeV-madgraph',
    'Autumn18.ZJetsToNuNu_HT-800To1200_13TeV-madgraph',
    'Autumn18.ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph',
    ]

# Add htcondor option to avoid some sites (these jobs often fail)
htcondor(
    'cmsconnect_blacklist',
    ['*_RU_*', '*FNAL*', '*IFCA*', '*KIPT*', 'T3_IT_Trieste', 'T2_TR_METU', 'T2_US_Vanderbilt', 'T2_PK_NCP']
    )

# For each background, submit 50 jobs
for bkg in bkgs:
    # Skip anything except qcd (for Sara), remove this line if you want to do all bkgs
    if not 'qcd' in bkg.lower(): continue
    for i in range(50):
        submit(bkg=bkg, i_file=i, transfer_files=['~/CMSSW_10_2_21_latest_el7_treemaker.tar.gz'])
"""# endsubmit

import qondor, seutils, os.path as osp

# Download the TreeMaker tarball and extract it
cmssw = qondor.init_cmssw(
    'root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/svjproduction-tarballs/CMSSW_10_2_21_latest_el7_treemaker.tar.gz',
    outdir='.'
    )

bkg = qondor.scope.bkg
i_file = qondor.scope.i_file
scenario = bkg.split('.',1)[0]
year = 2000 + int(scenario[-2:])

# Run the TreeMaker ntupler
cmssw.run_commands([
    'cd TreeMaker/Production/test',
    'cmsRun runMakeTreeFromMiniAOD_cfg.py'
    ' nstart={}'
    ' nfiles=1'
    ' outfile=outfile'
    ' scenario={}'
    ' inputFilesConfig={}'
    ' lostlepton=0'
    ' doZinv=0'
    ' systematics=0'
    ' deepAK8=0'
    ' deepDoubleB=0'
    ' doPDFs=0'
    ' nestedVectors=False'
    ' splitLevel=99'
    ' numevents=5' # ONLY FOR TESTING, remove this option if you're really producing something
    .format(i_file, scenario, bkg)
    ])

# Copy the output root file to a storage element
expected_outfile = osp.join(cmssw.cmssw_src, 'TreeMaker/Production/test', 'outfile_RA2AnalysisTree.root')
seutils.cp(
    expected_outfile,
    'gsiftp://hepcms-gridftp.umd.edu//mnt/hadoop/cms/store/user/thomas.klijnsma/qcdtest3/'
    'bkg_{date}_year{year}/{bkg}/{part}.root'
    .format(date=qondor.get_submission_timestr(), year=year, bkg=bkg, part=i_file),
    env=qondor.BARE_ENV, implementation='gfal'
    )
