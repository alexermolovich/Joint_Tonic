"""Original deterministic synthetic fixtures; CC0-1.0."""
import copy
import numpy as np

def reject(fn):
    try:fn()
    except ValueError:return
    raise AssertionError('Expected ValueError')
def same(a,b):np.testing.assert_array_equal(a,b)

def sheet():return dict(dataset_id='fr3_set',version='1.0.0',motivation='pick blocks',collection_method='teleoperation',calibration_sha256='1'*64,license='CC0-1.0',maintenance='lab',limitations='one room',embodiments=['fr3'],sensors=['wrist_rgb'],tasks=['pick'],intended_uses=['research'],prohibited_uses=[])
def example1(m):assert m.validate_robot_datasheet(sheet())==[]
def example2(m):
 s=sheet();del s['license'];s['calibration_sha256']='unknown';s['extras']=1
 assert m.validate_robot_datasheet(s)==[('calibration_sha256','unknown'),('extras','unexpected'),('license','missing')]
def edges(m):
 s=sheet();s['license']='unknown';s['dataset_id']=' fr3_set ';s['version']='1.0.0 ';s['calibration_sha256']=' '+('1'*64);s['motivation']='  meaningful text  '
 assert m.validate_robot_datasheet(s)==[('calibration_sha256','invalid'),('dataset_id','invalid'),('license','unknown'),('version','invalid')]
 for value in ['01.0.0','١.0.0','10000.0.0','1x0x0','unknown']:
  s=sheet();s['version']=value;assert m.validate_robot_datasheet(s)==[('version','invalid')]
 assert m.validate_robot_datasheet({})==sorted((key,'missing') for key in sheet())
def oracle_scale(m):
 s=sheet();s['embodiments']=['r'+str(i) for i in range(128)];s['limitations']='x'*1024;before=copy.deepcopy(s);assert m.validate_robot_datasheet(s)==[] and s==before
 # Every required field distinguishes absent from present-but-malformed.
 for key in sheet():
  absent=sheet();del absent[key];assert m.validate_robot_datasheet(absent)==[(key,'missing')]
  malformed=sheet();malformed[key]=None;assert m.validate_robot_datasheet(malformed)==[(key,'invalid')]
 for key in ['embodiments','sensors','tasks','intended_uses']:
  s=sheet();s[key]=[];assert m.validate_robot_datasheet(s)==[(key,'invalid')]
 s=sheet();s['sensors']=[['unhashable']];assert m.validate_robot_datasheet(s)==[('sensors','invalid')]
 s=sheet();s['tasks']=['pick','pick'];assert m.validate_robot_datasheet(s)==[('tasks','invalid')]
def invalid(m):
 for s in [[],None,{1:'x'},{'':'x'},{'x'*65:1},{'k'+str(i):1 for i in range(33)}]:reject(lambda:m.validate_robot_datasheet(s))

TESTS=[('Worked example1','public',example1),('Worked example2','public',example2),('Boundary semantics','hidden',edges),('Independent oracle,scale and preservation','hidden',oracle_scale),('Invalid documented inputs','hidden',invalid)]
