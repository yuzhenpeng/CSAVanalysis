# CSAV program: Comparative genomics tool to detect convergent amino acid variants
# version 1.00 (20.May.2020)
# written by Chul Lee

print("CSAV analysis: Copyright (c) Seoul Nat. Univ. and Rockefeller Univ."+'\n'+'\n')
 
#from scipy import stats
from datetime import datetime
import os, glob, sys, math, time
startTime = datetime.today()
print("Start time")
print(startTime)
################################ Global variable ############################
try:
    nTargets = sys.argv[1]
except: # default targets = six avian vocal learners in 47 birds
    nTargets = 'TAEGU,GEOFO,CORBR,MELUN,NESNO,CALAN' # Vocal learners
    #nTargets = 'FALPE,CARCR,TYTAL,HALLE,HALAL,CATAU' # BIRDS OF PREY
    #nTargets = 'PELCR,EGRGA,NIPNI,PHACA,FULGL,PYGAD,APTFO,GAVST,PHALE,EURHE,CHAVO,BALRE,PHORU,PODCR,ANAPL' # WATER BIRDS


## setting date
nYear   = str(datetime.today().year)
nMonth  = str(datetime.today().month)
nDay    = str(datetime.today().day)
nHour   = str(datetime.today().hour)
nMin    = str(datetime.today().minute)
if len(nMonth)==1:
    nMonth = "0" + nMonth
if len(nDay)==1:
    nDay = "0" + nDay
if len(nHour)==1:
    nHour = "0" + nHour
if len(nMin)==1:
    nMin = "0" + nMin
nDate   = nYear + nMonth + nDay + "_" + nHour + nMin


### TAAS
sID_LIST = ['TAEGU','GEOFO','CORBR','MELUN','NESNO','CALAN','MANVI','FALPE','CARCR','MERNU','PICPU','BUCRH','APAVI','LEPDI','COLST','TYTAL','HALLE','HALAL','CATAU','PELCR','EGRGA','NIPNI','PHACA','FULGL','PYGAD','APTFO','GAVST','PHALE','EURHE','CHAVO','BALRE','OPHHO','CHAPE','CAPCA','CHLUN','TAUER','CUCCA','MESUN','PTEGU','COLLI','PHORU','PODCR','GALGA','MELGA','ANAPL','TINMA','STRCA','HUMAN','ACACH']
outgroup_LIST = ['HUMAN','ACACH']


seqPATH = "../data/cds/"
#seqPATH = "tmp/test/"
seqFORM = ".sate.default.pep2cds.removed.shortname.fasta"
tmpTargets = nTargets.replace(',','_')
oPATH   = "out/"#tmpTargets + '_' + nDate+'/'
os.system("mkdir "+oPATH)

targetID_LIST = nTargets.split(',')

fNAME_symbol = "symbol_info.txt"
fNAME_SUMMARY = "0." + nTargets + "_codon_TAASresult_" + nDate + ".txt"


### ProOriBL

## TREE
# - Tree from Fig S7 in Erich et al. (2014) Science.
# - have to be bifurcating rooted tree
# - have to contain branch lengths
# - have to remove bootstrap values
nTree = "(((((((((((((TAEGU:0.042,GEOFO:0.0372):0.0245,CORBR:0.0385):0.044,MANVI:0.0693):0.0479,(MELUN:0.0585,NESNO:0.042):0.0528):0.0021,FALPE:0.0762):0.0013,CARCR:0.055):0.0015,(((((((MERNU:0.103,PICPU:0.1434):0.0039,BUCRH:0.0998):0.0025,APAVI:0.1048):0.0012,LEPDI:0.067):0.0014,COLST:0.1205):0.0006,TYTAL:0.0675):0.0006,((HALLE:0.001,HALAL:0.0011):0.0427,CATAU:0.0301):0.002):0.0008):0.0041,((((((PELCR:0.0417,EGRGA:0.0562):0.0013,NIPNI:0.0398):0.001,PHACA:0.0639):0.0016,(FULGL:0.0342,(PYGAD:0.0135,APTFO:0.0109):0.0214):0.0012):0.0019,GAVST:0.0445):0.0021,(PHALE:0.0591,EURHE:0.0947):0.0032):0.0012):0.0011,((CHAVO:0.0602,BALRE:0.0571):0.0015,OPHHO:0.0756):0.0009):0.001,(((CALAN:0.1126,CHAPE:0.0908):0.0204,CAPCA:0.0697):0.0038,((CHLUN:0.0731,TAUER:0.0708):0.0014,CUCCA:0.1115):0.0011):0.0011):0.0011,(((MESUN:0.0871,PTEGU:0.0717):0.0027,COLLI:0.0963):0.0014,(PHORU:0.0312,PODCR:0.0584):0.013):0.0009):0.032,((GALGA:0.0391,MELGA:0.0449):0.1131,ANAPL:0.1003):0.0394):0.0456,(TINMA:0.1471,STRCA:0.0669):0.0456);"


################################ Automatic setting ##########################

### ProOriBL

## make info_tree: topology, branch lengths
info_tree = nTree.split(',')

## make tree_sID_list
tree_sID_list = []
part = nTree.replace("(",'').split(',')
for sIDwInfo in part:
    sID = sIDwInfo.split(':')[0]
    tree_sID_list.append(sID)

## make tree_target_list
nTargets = ','.join(targetID_LIST)
if len(sys.argv)== 2:
    tree_target_list = sys.argv[1].strip().split(',')
elif len(sys.argv)== 1:
    tree_target_list = nTargets.strip().split(',')
else:
    print("Input error",sys.argv)
    sys.exit()

## check if targetID in tree_sID_list?
iCNT_target = 0
for targetID in tree_target_list:
    if targetID in tree_sID_list:
        iCNT_target += 1
if not len(tree_target_list)==iCNT_target:
    print("ERROR: targets -"+','.join(tree_target_list))
    sys.exit()

## sort tree_target_list by the order of tree_sID_list
tmp_tree_target_list = []
for sID in tree_sID_list:
    if sID in tree_target_list:
        tmp_tree_target_list.append(sID)
tree_target_list = tmp_tree_target_list

## Output
tree_oNAME = "0." + ','.join(tree_target_list)+"_codon_ProOriBLresult_"+nDate+'.txt'
tree_fpout = open(oPATH + tree_oNAME,'w')
tree_fpout.write("# Targets: "+','.join(tree_target_list)+'\n')


### TAAS
othersID_LIST  = []
for sID in sID_LIST:
 if not sID in targetID_LIST:
  if not sID in outgroup_LIST:
   othersID_LIST.append(sID)
sID_LIST = []
sID_LIST = targetID_LIST + othersID_LIST + outgroup_LIST

CNT_target    = len(targetID_LIST)
CNT_others    = len(othersID_LIST)

AA_SET        = ["A","R","N","D","C","E","Q","G","H","I","L","K","M","F","P","S","T","W","Y","V","U","O","-",'*',"X"] 
CODONTABLE_dic  = {'TTT':'F','TTC':'F','TTA':'L','TTG':'L','CTT':'L','CTC':'L','CTA':'L','CTG':'L','ATT':'I','ATC':'I','ATA':'I','ATG':'M','GTT':'V','GTC':'V','GTA':'V','GTG':'V','TCT':'S','TCC':'S','TCA':'S','TCG':'S','CCT':'P','CCC':'P','CCA':'P','CCG':'P','ACT':'T','ACC':'T','ACA':'T','ACG':'T','GCT':'A','GCC':'A','GCA':'A','GCG':'A','TAT':'Y','TAC':'Y','TAA':'Z','TAG':'Z','CAT':'H','CAC':'H','CAA':'Q','CAG':'Q','AAT':'N','AAC':'N','AAA':'K','AAG':'K','GAT':'D','GAC':'D','GAA':'E','GAG':'E','TGT':'C','TGC':'C','TGA':'Z','TGG':'W','CGT':'R','CGC':'R','CGA':'R','CGG':'R','AGT':'S','AGC':'S','AGA':'R','AGG':'R','GGT':'G','GGC':'G','GGA':'G','GGG':'G',"---":"-",'CTN':'L','GTN':'V','TCN':'S','CCN':'P','ACN':'T','GCN':'A','CGN':'R','GGN':'G'} # Stop codon = 'Z', NNN = 'X'

### must not include '.', because '.' is used as a marker of loss of gene

FPOUT_SUMMARY = open(oPATH + fNAME_SUMMARY,'w')
tmpline = "Gene" + '\t' + "Position_Nuc" + '\t' + "TAAS_Type_CODON" + '\t' + "TargetCODON" + '\t' + "OthersCODON" + '\t' + "Pvalue_CODON" + '\t' + "Adj.pvalue_CODON" + '\t' + "Total_Entropy_CODON" + '\t' + "Target_Entropy_CODON" + '\t' + "Others_Entropy_CODON" + "\t"+ "\t".join(sID_LIST)+'\t' + "Position_AA" + '\t' + "TAAS_Type_AA" + '\t' + "TargetAA" + '\t' + "OthersAA" + '\t' + "Pvalue_AA" + '\t' + "Adj.pvalue_AA" + '\t' + "Total_Entropy_AA" + '\t' + "Target_Entropy_AA" + '\t' + "Others_Entropy_AA" + "\t"+ "\t".join(sID_LIST)+'\n'
FPOUT_SUMMARY.write(tmpline)


################################ Funtions #################################
############
# ProOriBL #
############
def ordering_sID(stree_target_list):
    tmp_stree_target_list = []
    for sID in tree_sID_list:
        if sID in stree_target_list:
            tmp_stree_target_list.append(sID)
    stree_target_list = tmp_stree_target_list
    return stree_target_list


def find_branchlength(monotree_target_list):
    info_tree = nTree.split(',')
    iCNT_R_parenthesis = 0
    iCNT_L_parenthesis = 0
    for sID in monotree_target_list:
        i = tree_sID_list.index(sID)
        iCNT_R_parenthesis += info_tree[i].count(")") 
        iCNT_L_parenthesis += info_tree[i].count("(")
    diff_RminusL = iCNT_R_parenthesis - iCNT_L_parenthesis
    if iCNT_R_parenthesis < iCNT_L_parenthesis:
        iLen_branch = float(info_tree[tree_sID_list.index(monotree_target_list[-1])].split(')')[-1].split(':')[-1])
    elif iCNT_R_parenthesis > iCNT_L_parenthesis:
        iLen_branch = float(info_tree[i].split(")")[-diff_RminusL-1].split(":")[-1])
    else:#iCNT_R_parenthesis == iCNT_L_parenthesis
        iLen_branch = "Most common ancestral branch"
    return iLen_branch


def scan_right_parenthesis(iPos_sTarget, iCNT_L_parenthesis):
    info_tree = nTree.split(',')
    iCNT_L_parenthesis += info_tree[iPos_sTarget+1].count('(')
    iCNT_R_parenthesis = info_tree[iPos_sTarget+1].count(')')
    if iCNT_L_parenthesis <= iCNT_R_parenthesis:
        nInternalBranch = info_tree[iPos_sTarget+1].split(')')[iCNT_L_parenthesis]
        if ":" in nInternalBranch:
            iLen_InternalBranch_target = float(nInternalBranch.split(':')[-1])
        else:
            iLen_InternalBranch_target = "Branch of most common ancestor"
        endTarget = tree_sID_list[iPos_sTarget+1]
        return endTarget, iLen_InternalBranch_target
    else:
        iCNT_L_parenthesis -= iCNT_R_parenthesis
        endTarget, iLen_InternalBranch_target = scan_right_parenthesis(iPos_sTarget+1, iCNT_L_parenthesis)
        return endTarget, iLen_InternalBranch_target


def scan_left_parenthesis(iPos_sTarget, iCNT_R_parenthesis):
    info_tree = nTree.split(',')
    iCNT_R_parenthesis += info_tree[iPos_sTarget-1].count(')')
    iCNT_L_parenthesis = info_tree[iPos_sTarget-1].count('(')
    if iCNT_R_parenthesis <= iCNT_L_parenthesis:
        startTarget = tree_sID_list[iPos_sTarget-1]
        return startTarget
    else:
        iCNT_R_parenthesis -= iCNT_L_parenthesis
        startTarget = scan_left_parenthesis(iPos_sTarget-1, iCNT_R_parenthesis)
        return startTarget


def find_pairedgroup(pairedID, direction_parenthesis):# Right parenthesis
    info_tree = nTree.split(',')
    if direction_parenthesis == ")":
        if info_tree[tree_sID_list.index(pairedID)].count(')')>0:
            pairedID_list = [pairedID]
        else:
            iCNT_R_parenthesis = 0
            iCNT_L_parenthesis = 0
            iRange_list = range(tree_sID_list.index(pairedID),len(tree_sID_list),1)
            for i in iRange_list:
                sID = tree_sID_list[i]
                if i == 0:
                    iCNT_L_parenthesis -= 1
                iCNT_R_parenthesis += info_tree[i].count(")") 
                iCNT_L_parenthesis += info_tree[i].count("(")
                if iCNT_R_parenthesis >= iCNT_L_parenthesis:
                    pairedID_list = tree_sID_list[tree_sID_list.index(pairedID):tree_sID_list.index(sID)+1]
                    break
                else:pass
    else:# direction_parenthesis == "("
        if info_tree[tree_sID_list.index(pairedID)].count('(')>0:
            pairedID_list = [pairedID]
        else:
            iCNT_R_parenthesis = 0
            iCNT_L_parenthesis = 0
            iRange_list = range(tree_sID_list.index(pairedID),-1,-1)
            for i in iRange_list:
                sID = tree_sID_list[i]
                if i == len(tree_sID_list)-1:
                    iCNT_R_parenthesis -= 1
                iCNT_R_parenthesis += info_tree[i].count(")") 
                iCNT_L_parenthesis += info_tree[i].count("(")
                if iCNT_L_parenthesis >= iCNT_R_parenthesis: 
                    pairedID_list = tree_sID_list[tree_sID_list.index(sID):tree_sID_list.index(pairedID)+1]
                    break
                else:pass
    return pairedID_list


def find_upper_clade(stree_target_list,iLen_OriginBranch):#stree_target_list = target species in a monophyletic clade 
    info_tree = nTree.split(',')
    startID = stree_target_list[0]
    endID = stree_target_list[-1]
    info_tree_of_stree_target_list = info_tree[tree_sID_list.index(startID):tree_sID_list.index(endID)+1]
    iCNT_L_parenthesis = 0 # (
    iCNT_R_parenthesis = 0 # )
    for info_tree_sTarget in info_tree_of_stree_target_list:
        iCNT_L_parenthesis += info_tree_sTarget.count('(')
        iCNT_R_parenthesis += info_tree_sTarget.count(')')
        
    if iCNT_L_parenthesis > iCNT_R_parenthesis:
        pairedID              = tree_sID_list[tree_sID_list.index(endID)+1]
        direction_parenthesis = ")"
        pairedID_list         = find_pairedgroup(pairedID, direction_parenthesis )
        iCNT_target = 0
        for pairedID in pairedID_list:
            if pairedID in tree_target_list:
                iCNT_target +=1
        if iCNT_target == len(pairedID_list):
            ORIGIN_stree_target_list = stree_target_list + pairedID_list
            ORIGIN_stree_target_list = ordering_sID(ORIGIN_stree_target_list)
            ORIGIN_iLen_OriginBranch = find_branchlength(ORIGIN_stree_target_list)
        else:
            ORIGIN_stree_target_list, ORIGIN_iLen_OriginBranch = stree_target_list, iLen_OriginBranch
            
    elif iCNT_L_parenthesis < iCNT_R_parenthesis:
        pairedID              = tree_sID_list[tree_sID_list.index(startID)-1]
        direction_parenthesis = "("
        pairedID_list         = find_pairedgroup(pairedID, direction_parenthesis)
        iCNT_target = 0
        for pairedID in pairedID_list:
            if pairedID in tree_target_list:
                iCNT_target +=1
        if iCNT_target == len(pairedID_list):
            ORIGIN_stree_target_list = stree_target_list + pairedID_list
            ORIGIN_stree_target_list = ordering_sID(ORIGIN_stree_target_list)
            ORIGIN_iLen_OriginBranch = find_branchlength(ORIGIN_stree_target_list)
        else:
            ORIGIN_stree_target_list, ORIGIN_iLen_OriginBranch = stree_target_list, iLen_OriginBranch
            
    else:#iCNT_L_parenthesis == iCNT_R_parenthesis
        ORIGIN_stree_target_list = stree_target_list
        ORIGIN_iLen_OriginBranch = iLen_OriginBranch
    
    return ORIGIN_stree_target_list, ORIGIN_iLen_OriginBranch 
    

def scan_outer_internalbranch(stree_target_list,iLen_OriginBranch):
    ORIGIN_stree_target_list, ORIGIN_iLen_OriginBranch = find_upper_clade(stree_target_list,iLen_OriginBranch)
    if not ORIGIN_stree_target_list == stree_target_list:
        stree_target_list = ORIGIN_stree_target_list
        iLen_OriginBranch = ORIGIN_iLen_OriginBranch
        ORIGIN_stree_target_list, ORIGIN_iLen_OriginBranch = scan_outer_internalbranch(stree_target_list,iLen_OriginBranch)
    return ORIGIN_stree_target_list, ORIGIN_iLen_OriginBranch

    
def trim_unselected_tree_target_list(stree_target_list,unselected_tree_target_list):
    ntree_target_list = []
    for nTarget in unselected_tree_target_list:
        if not nTarget in stree_target_list:
            ntree_target_list.append(nTarget)
    unselected_tree_target_list = ntree_target_list
    return unselected_tree_target_list


def scan_OriBranch(sTarget,unselected_tree_target_list):
    info_tree = nTree.split(',')
    stree_target_list = [sTarget]
    
    # 1. Set Origin branch length = terminal branch length
    iLen_TerminalBranch_target = find_branchlength(stree_target_list)
    iLen_OriginBranch = iLen_TerminalBranch_target

    # 2.find ancestral branch
    iPos_sTarget = tree_sID_list.index(sTarget)
    sID_in_clade_list = [sTarget]
    if '(' in info_tree[iPos_sTarget]:
        iCNT_L_parenthesis = 1
        endTarget, iLen_InternalBranch_target = scan_right_parenthesis(iPos_sTarget, iCNT_L_parenthesis)
        sID_inInternalBranch_list = tree_sID_list[iPos_sTarget:tree_sID_list.index(endTarget)+1]
        
    else:
        info_tree = nTree.split(',')
        nInternalBranch = info_tree[iPos_sTarget].split(')')[1]
        if ":" in nInternalBranch:
            iLen_InternalBranch_target = float(nInternalBranch.split(':')[-1])
        else:
            iLen_InternalBranch_target = "Branch of most common ancestor"

        iCNT_R_parenthesis = 1
        startTarget = scan_left_parenthesis(iPos_sTarget, iCNT_R_parenthesis)
        sID_inInternalBranch_list = tree_sID_list[tree_sID_list.index(startTarget):iPos_sTarget+1]

    sID_AncestralBranch_list    = sID_inInternalBranch_list
    iLen_AncestralBranch        = iLen_InternalBranch_target
    
    ###
    # targets == species under ancestral branch?
    # Yes: iFlag = 1 / No: iFlag = 0
    iFlag = 0
    iCNT_eqID = 0
    for sID in sID_AncestralBranch_list:
        if sID in tree_target_list:
            iCNT_eqID +=1
    if iCNT_eqID == len(sID_AncestralBranch_list):
        stree_target_list = sID_AncestralBranch_list
        iLen_OriginBranch = iLen_AncestralBranch
        iFlag = 1

    ###
    #
    if iFlag == 0:
        unselected_tree_target_list = trim_unselected_tree_target_list(stree_target_list,unselected_tree_target_list)
        print_line = "# Target group: "+','.join(stree_target_list)+' / OriBL: '+str(iLen_OriginBranch)
        print(print_line)
        tree_fpout.write(print_line+'\n')
        return iLen_OriginBranch, unselected_tree_target_list

    else:#iFlag == 1
        stree_target_list, iLen_OriginBranch = scan_outer_internalbranch(stree_target_list, iLen_OriginBranch)
        unselected_tree_target_list = trim_unselected_tree_target_list(stree_target_list,unselected_tree_target_list)
        print_line = "# Target group: "+','.join(stree_target_list)+' / OriBL: '+str(iLen_OriginBranch)
        print(print_line)
        tree_fpout.write(print_line+'\n')
        return iLen_OriginBranch, unselected_tree_target_list

    
def Run_ProOriBL():
    print("### Result")
    ordered_tree_target_list = tree_target_list
    ordered_tree_target_list = ordering_sID(ordered_tree_target_list)
    unselected_tree_target_list = ordered_tree_target_list
    iLen_OriginBranch_list = []
    target_clade_list      = []
    for sTarget in ordered_tree_target_list:
        if sTarget in unselected_tree_target_list:
            iLen_OriginBranch, tmp_unselected_tree_target_list = scan_OriBranch(sTarget, unselected_tree_target_list)
            iLen_OriginBranch_list.append(iLen_OriginBranch)

            selected_tree_target_list = []
            for target_ID in unselected_tree_target_list:
                if not target_ID in tmp_unselected_tree_target_list:
                    selected_tree_target_list.append(target_ID)
            target_clade_list.append(selected_tree_target_list)
            unselected_tree_target_list = tmp_unselected_tree_target_list
        
            if len(unselected_tree_target_list)==0:
                break
        
    ProOriBL = 1
    for iLen_OriginBranch in iLen_OriginBranch_list:
        ProOriBL *= iLen_OriginBranch
    print("#")
    print("### Summary")
    print("# Number of independent origins: " + str(len(iLen_OriginBranch_list)))
    print("# Product of Origin branch lengths: " + str(ProOriBL))
    print("#")
    print(str(ProOriBL)+'\n')
    
    tree_fpout.write("# Number of independent origins: " + str(len(iLen_OriginBranch_list))+'\n')
    tree_fpout.write("# Product of Origin branch lengths: " + str(ProOriBL)+'\n')
    tree_fpout.write(str(ProOriBL)+'\n')
    tree_fpout.close()
    return ProOriBL, target_clade_list
    


########
# TAAS #
########

def EnrichmentTEST(targetAA_list, othersAA_list):
    targetAA_set = list(set(targetAA_list))
    targetAA_set.sort()
    othersAA_set = list(set(othersAA_list))
    othersAA_set.sort()
    CNT_target_targetAA     = 0
    CNT_target_othersAA     = 0
    CNT_others_targetAA     = 0
    CNT_others_othersAA     = 0
    for nAA in AA_SET:
        if nAA in targetAA_set:
            targetAA = nAA
            CNT_target_targetAA += targetAA_list.count(targetAA)  
            CNT_others_targetAA += othersAA_list.count(targetAA)
        else:
            othersAA = nAA
            CNT_target_othersAA += targetAA_list.count(othersAA)
            CNT_others_othersAA += othersAA_list.count(othersAA)
    a = CNT_target_targetAA
    b = CNT_target_othersAA
    c = CNT_others_targetAA
    d = CNT_others_othersAA
    contingency_table = [[a,b],[c,d]]
    # Fisher Exact
    oddsratio, pvalue = "#N/A","#N/A" #stats.fisher_exact(contingency_table)
    return ''.join(targetAA_set),''.join(othersAA_set), oddsratio, pvalue

def EnrichmentTEST_CODON(targetCODON_list, othersCODON_list):
    targetCODON_set = []
    for targetCODON in targetCODON_list:
        if not targetCODON == "...":
            targetCODON_set.append(targetCODON)
    othersCODON_set = []
    for othersCODON in othersCODON_list:
        if not othersCODON == "...":
            othersCODON_set.append(othersCODON)
    targetCODON_set = list(set(targetCODON_set))
    targetCODON_set.sort()
    othersCODON_set = list(set(othersCODON_set))
    othersCODON_set.sort()
    CNT_target_targetCODON     = 0
    CNT_target_othersCODON     = 0
    CNT_others_targetCODON     = 0
    CNT_others_othersCODON     = 0
    for nCODON in CODONTABLE_dic.keys():
        if nCODON in targetCODON_set:
            targetCODON = nCODON
            CNT_target_targetCODON += targetCODON_list.count(targetCODON)  
            CNT_others_targetCODON += othersCODON_list.count(targetCODON)
        else:
            othersCODON = nCODON
            CNT_target_othersCODON += targetCODON_list.count(othersCODON)
            CNT_others_othersCODON += othersCODON_list.count(othersCODON)
    a = CNT_target_targetCODON
    b = CNT_target_othersCODON
    c = CNT_others_targetCODON
    d = CNT_others_othersCODON
    contingency_table = [[a,b],[c,d]]
    # Fisher Exact
    oddsratio, pvalue = "#N/A","#N/A" #stats.fisher_exact(contingency_table)
    return ','.join(targetCODON_set),','.join(othersCODON_set), oddsratio, pvalue


def TAASanalysis(targetAA_list, othersAA_list):
    targetAA_set = list(set(targetAA_list))
    othersAA_set = list(set(othersAA_list))
    TAAS  = ""
    iFlag = 0
    CNT_targetETC = 0
    for targetAA in targetAA_set:
        if targetAA in AA_SET:
            if targetAA in othersAA_set:
                iFlag = 1
        else:
            CNT_targetETC += 1
    if iFlag == 0:
        TAAS = "MutuallyExclusive"
    return TAAS


def EntropyTEST(AA_list):
    CNT_AAs = float(0)
    for nAA in AA_list:
        if nAA in AA_SET:
            CNT_AAs += 1
            
    Entropy = 0
    tmpAA_set = list(set(AA_list))
    for nAA in tmpAA_set:
        if nAA in AA_SET:
            freqAA = AA_list.count(nAA)/CNT_AAs
            if freqAA == 0:
                entropyAA = 0
            else:
                entropyAA = -freqAA * math.log(freqAA,2)
            
            Entropy += entropyAA
    return Entropy

def TAASanalysis_CODON(nGene, iPos, targetCODON_list, othersCODON_list):
    targetCODON_set = list(set(targetCODON_list))
    othersCODON_set = list(set(othersCODON_list))
    TAAS_CODON  = ""
    iFlag = 0
    CNT_targetETC = 0
    for targetCODON in targetCODON_set:
        if targetCODON in CODONTABLE_dic.keys():
            if not targetCODON == "...": 
                if targetCODON in othersCODON_set:
                    iFlag = 1
            else:
                CNT_targetETC += 1
                
    if iFlag == 0:
        TAAS_CODON = "MutuallyExclusive"
    return TAAS_CODON

def EntropyTEST_CODON(CODON_list):
    CNT_CODONs = float(0)
    for nCODON in CODON_list:
        if nCODON in CODONTABLE_dic.keys():
            CNT_CODONs += 1
            
    Entropy = 0
    tmpCODON_set = list(set(CODON_list))
    for nCODON in tmpCODON_set:
        if nCODON in CODONTABLE_dic.keys():
            freqCODON = CODON_list.count(nCODON)/CNT_CODONs
            if freqCODON == 0:
                entropyCODON = 0
            else:
                entropyCODON = -freqCODON * math.log(freqCODON,2)
            
            Entropy += entropyCODON
    return Entropy


def MAKE_SEQ_DB(fNAME):
    sID_list = []
    sID_nSeq_dic = {}
    fpin = open(fNAME,'r')
    for line in fpin:
        if line[0] == ">":
            sID = line[1:].strip()
            sID_nSeq_dic.setdefault(sID,'')
            sID_list.append(sID)
        else:
            sID_nSeq_dic[sID]+= line.strip().replace(' ','')
    fpin.close()
    seq_len = len(sID_nSeq_dic[sID])
    tmpline = ''
    for i in range(seq_len):
        tmpline += "."
    sID_nSeq_matrix = []
    for sID in sID_LIST:
        try:
            sID_nSeq_matrix.append(sID_nSeq_dic[sID])
        except:
            sID_nSeq_matrix.append(tmpline)
    return sID_list, sID_nSeq_matrix

def RUN_TAAS_analysis(sID_list, sID_nSeq_matrix, oNAME, nGene_iCNT_TAAS_dic, target_clade_list):
    tmp_nGene_iCNT_TAAS_dic = nGene_iCNT_TAAS_dic

    print_geneNAME = os.path.basename(oNAME).split(seqFORM)[0]
    
    print_Seq_Len  = 0
    print_Entropy  = 0
    print_Num_TAAS = 0
    
    seq_len 		= len(sID_nSeq_matrix[0])
    print_Seq_Len 	= seq_len
    BonferroniALPHA     = 0.05/seq_len
	
    #fpout = open(oNAME,'w')                                    # Write result of each gene
    #fpout.write(str(len(sID_list))+'\t'+str(seq_len)+'\n')     # Write result of each gene
    nGene = os.path.basename(oNAME).split("_")[0]
    iPos_AA = 0
    for iColumn in range(0,seq_len,3):
        
        iPos = str(iColumn + 1)
        iPos_AA = int(iPos_AA)
        iPos_AA +=1  

        # Target
        targetCODON_list = []
        targetAA_list = []
        for iRow in range(CNT_target):
            targetCODON = sID_nSeq_matrix[iRow][iColumn:(iColumn+3)]
            targetCODON_list.append(targetCODON)
            try:
                targetAA = CODONTABLE_dic[targetCODON]
                
            except:
                if targetCODON == "...":
                    targetAA = "."
                else:
                    targetAA = "X"
            targetAA_list.append(targetAA)
            

        # Others
        othersCODON_list = []
        othersAA_list = []
        for iRow in range(CNT_target,CNT_target+CNT_others):
            othersCODON = sID_nSeq_matrix[iRow][iColumn:(iColumn+3)]
            othersCODON_list.append(othersCODON)
            try:
                othersAA = CODONTABLE_dic[othersCODON]    
            except:
                if othersCODON == "...":
                    othersAA = "."
                else:
                    othersAA = "X"
            othersAA_list.append(othersAA)
            

        # Outgroup
        outgroupCODON_list = []
        outgroupAA_list = []
        for iRow in range(len(sID_LIST)-len(outgroup_LIST),len(sID_LIST)):
            outgroupCODON = sID_nSeq_matrix[iRow][iColumn:(iColumn+3)]
            outgroupCODON_list.append(outgroupCODON)
            try:
                outgroupAA = CODONTABLE_dic[outgroupCODON]
            except:
                if outgroupCODON == "...":
                    outgroupAA = "."
                else:
                    outgroupAA = "X"
            outgroupAA_list.append(outgroupAA)

        # Codon-wide TAAS analysis    
        #############################################
        # STEP1. Fisher's exact test at codon level #
        #############################################
        targetCODONs, othersCODONs, oddsratio_CODON, pvalue_CODON = EnrichmentTEST_CODON(targetCODON_list, othersCODON_list)
        adj_pvalue_CODON = "#N/A"# pvalue_CODON*seq_len
        
        #######################################
        # STEP2. TAAS analysis at codon level #
        #######################################
        TAAS_CODON = TAASanalysis_CODON(nGene, iPos, targetCODON_list, othersCODON_list)
        
        #####################################
        # STEP3. EntropyTest at codon level #
        #####################################
        Total_Entropy_CODON  = EntropyTEST_CODON(targetCODON_list + othersCODON_list)
        Target_Entropy_CODON = EntropyTEST_CODON(targetCODON_list)
        Others_Entropy_CODON = EntropyTEST_CODON(othersCODON_list)
        if not TAAS_CODON == "":
            if Target_Entropy_CODON == 0:
                if Others_Entropy_CODON == 0:
                    TAAS_CODON = "1"
                else: # Others_Entropy_CODON > 0
                    TAAS_CODON = "2"
            else: # Target_Entropy_CODON > 0:
                if Others_Entropy_CODON == 0:
                    TAAS_CODON = "3"
                else: # Others_Entropy > 0
                    TAAS_CODON = "4"


        # AminoAcid-wide TAAS analysis

        ##############################
        # STEP1. Fisher's exact test #
        ##############################
        targetAAs, othersAAs, oddsratio, pvalue = EnrichmentTEST(targetAA_list, othersAA_list)
        adj_pvalue = "#N/A"# pvalue*seq_len

        ########################
        # STEP2. TAAS analysis #
        ########################
        TAAS = TAASanalysis(targetAA_list, othersAA_list)
        
        ######################
        # STEP3. EntropyTest #
        ######################
        Total_Entropy  = EntropyTEST(targetAA_list + othersAA_list)
        Target_Entropy = EntropyTEST(targetAA_list)
        Others_Entropy = EntropyTEST(othersAA_list)
        targetAAs = targetAAs.replace('.','')
        othersAAs = othersAAs.replace('.','')
        if not TAAS == "":
            if Target_Entropy == 0:
                if Others_Entropy == 0:
                    TAAS = "1"
                else: # Others_Entropy > 0
                    TAAS = "2"
            else: # Target_Entropy > 0:
                if Others_Entropy == 0:
                    TAAS = "3"
                else: # Others_Entropy > 0
                    TAAS = "4"
                    
        iPos = str(iPos)
        iPos_AA = str(iPos_AA)
        #Result_position = nGene + '\t' + iPos + '\t' + TAAS + '\t' + targetAAs+'\t' + othersAAs + '\t'+str(pvalue)+'\t'+str(adj_pvalue)+ '\t' + str(Total_Entropy)+ '\t' + str(Target_Entropy)+ '\t' + str(Others_Entropy)
        Result_position = nGene + '\t' + iPos + '\t' + TAAS_CODON + '\t' + targetCODONs+'\t' + othersCODONs + '\t'+str(pvalue_CODON)+'\t'+str(adj_pvalue_CODON)+ '\t' + str(Total_Entropy_CODON)+ '\t' + str(Target_Entropy_CODON)+ '\t' + str(Others_Entropy_CODON)
        
        #fpout.write(Result_position + '\n')                    # Write result of each gene
        print_Entropy += Total_Entropy
        if not TAAS_CODON == "":
            ## filtered by number of speceis in each origin ##
            iFlag_allclades = 0
            iCNT_gain_allclades = 0
            for clade_list in target_clade_list:
                iCNT_loss_eachclade = 0
                for targetID in clade_list:
                    i = targetID_LIST.index(targetID)
                    targetCODON = targetCODON_list[i]
                    if targetCODON == '...':
                        iCNT_loss_eachclade += 1
                    else:
                        iCNT_gain_allclades += 1
                if len(clade_list)==iCNT_loss_eachclade:
                    iFlag_allclades += 1
            if float(len(targetAA_list))/2 > iCNT_gain_allclades:
                iFlag_allclades += 1
            ## ############################################ ##
        
            if iFlag_allclades == 0:
                print_Num_TAAS += 1
                totalCODON_list = targetCODON_list + othersCODON_list + outgroupCODON_list
                for nCODON in totalCODON_list:
                    if nCODON == "...":
                        Result_position += '\t' +""
                    else:
                        Result_position += '\t' +nCODON
                Result_position += '\t' + iPos_AA + '\t' + TAAS + '\t' + targetAAs+'\t' + othersAAs + '\t'+str(pvalue)+'\t'+str(adj_pvalue)+ '\t' + str(Total_Entropy)+ '\t' + str(Target_Entropy)+ '\t' + str(Others_Entropy)
                totalAA_list = targetAA_list + othersAA_list + outgroupAA_list
                for nAA in totalAA_list:
                    if nAA == ".":
                        Result_position += '\t' +""
                    else:
                        Result_position += '\t' +nAA
                FPOUT_SUMMARY.write(Result_position+'\n')
                tmp_nGene_iCNT_TAAS_dic.setdefault(nGene,[0,0,0,0])
                if TAAS_CODON == "1":
                    tmp_nGene_iCNT_TAAS_dic[nGene][0] += 1
                elif TAAS_CODON == "2":
                    tmp_nGene_iCNT_TAAS_dic[nGene][1] += 1
                elif TAAS_CODON == "3":
                    tmp_nGene_iCNT_TAAS_dic[nGene][2] += 1
                elif TAAS_CODON == "4":
                    tmp_nGene_iCNT_TAAS_dic[nGene][3] += 1
                else:
                    print("Error: type of TAAS")
    #fpout.close()                                                              # Write result of each gene
    return tmp_nGene_iCNT_TAAS_dic
    
################################# Main ####################################

# Calculate product of origin branch lengths
ProOriBL, target_clade_list = Run_ProOriBL()

# TAAS analysis
CNT_TEST = 0
flist = glob.glob(seqPATH+"*"+seqFORM)
iCNT_ortho = len(flist)
print("Number of processes : " + str(iCNT_ortho))
print("")
print("Running TAAS")
iProcess = 0
iPercent = 10
nGene_iCNT_TAAS_dic = {}
for fNAME in flist:
    iProcess += 1
    if iCNT_ortho >= 10:
        if iProcess in range(int(iCNT_ortho/10),int(iCNT_ortho),int(iCNT_ortho/10)):
            print("Processing",iPercent,"%")
            iPercent += 10
    sID_list, sID_nSeq_matrix = MAKE_SEQ_DB(fNAME)
    oNAME = oPATH + os.path.basename(fNAME)
    nGene_iCNT_TAAS_dic = RUN_TAAS_analysis(sID_list, sID_nSeq_matrix, oNAME,nGene_iCNT_TAAS_dic, target_clade_list)
FPOUT_SUMMARY.close()



# Read symbol info
ortho_symbol_dic = {}
try:
    fpin = open("data/" + fNAME_symbol,'r')
    for line in fpin:
        part = line.strip().split('\t')
        nOrtho = part[0]
        nSymbol = part[1]
        ortho_symbol_dic.setdefault(nOrtho,nSymbol)
    fpin.close()
except:
    pass


# Write summary
fpout = open("0."+nTargets+"_codon_summary_"+nDate+'.txt','w')
nGene_list = []
for nGene in nGene_iCNT_TAAS_dic.keys():
    nGene_list.append(nGene)
nGene_list.sort()
iCNT_Gene = len(nGene_list)
iCNT_TAAS_list = [0,0,0,0,0] #[all, type1, type2, type3, type4]
for nGene in nGene_list:
    for i in range(4):
        iCNT_TAAS_list[0] += nGene_iCNT_TAAS_dic[nGene][i]
        iCNT_TAAS_list[i+1] += nGene_iCNT_TAAS_dic[nGene][i]
nHeader = "#"+nTargets + '\t'+str(ProOriBL)+'\t'+str(iCNT_Gene)
for iCNT_TAAS in iCNT_TAAS_list:
    nHeader += '\t'+str(iCNT_TAAS)
fpout.write(nHeader+'\n')

for nGene in nGene_list:
    try:# if symbol file is present
        nOrtho = nGene.split('.')[0]
        nSymbol = ortho_symbol_dic[nOrtho]
        fpout.write(nSymbol+'\n')
    except: # if symbol file is absent
        fpout.write(nGene+'\n')
fpout.close()


endTime = datetime.today()
print("Running time")
print(endTime - startTime)
print(".........................................Finish CSAV analysis")