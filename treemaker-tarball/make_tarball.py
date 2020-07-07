import qondor
cmssw = qondor.CMSSW('CMSSW_10_2_21/src')
cmssw.make_tarball(tag='treemaker')