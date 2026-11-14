"""Original deterministic synthetic fixtures; CC0-1.0."""
import copy
import numpy as np

def reject(fn):
    try:fn()
    except ValueError:return
    raise AssertionError('Expected ValueError')
def same(a,b):np.testing.assert_array_equal(a,b)

def cal(k='k',lo=0,hi=10):return dict(calibration_id=k,session_id='s',robot_id='r',sha256='1'*64,valid_from_ns=lo,valid_until_ns=hi)
def episode(k='a',lo=0,hi=10):return dict(episode_id=k,session_id='s',robot_id='r',calibration_id='k',calibration_sha256='1'*64,start_ns=lo,end_ns=hi)
def example1(m):assert m.audit_calibration_lineage([episode()],[cal()])==[]
def example2(m):
 e=episode('b',9,11);e['session_id']='other';e['calibration_sha256']='2'*64
 assert m.audit_calibration_lineage([e],[cal()])==[('b','digest_mismatch'),('b','session_mismatch'),('b','validity_gap')]
def edges(m):
 high=2**63-1;assert m.audit_calibration_lineage([episode('a',high-2,high)],[cal(lo=high-2,hi=high)])==[]
 assert m.audit_calibration_lineage([episode('a',high-3,high)],[cal(lo=high-2,hi=high)])==[('a','validity_gap')]
 e=episode();e['calibration_id']='absent';e['robot_id']='other';assert m.audit_calibration_lineage([e],[])==[('a','unknown_calibration')]
 assert m.audit_calibration_lineage([],[])==[]
def oracle_scale(m):
 records=[];expected=[]
 for i in range(5000):
  e=episode('e'+str(i),0,10)
  if i%2:e['robot_id']='other';expected.append((e['episode_id'],'robot_mismatch'))
  if i%3==0:e['calibration_sha256']='2'*64;expected.append((e['episode_id'],'digest_mismatch'))
  if i%5==0:e['end_ns']=11;expected.append((e['episode_id'],'validity_gap'))
  records.append(e)
 before=copy.deepcopy(records);assert m.audit_calibration_lineage(records[::-1],[cal()])==sorted(expected);assert records==before

def invalid(m):
 for field,value in [('sha256','bad'),('valid_from_ns',True),('valid_until_ns',0)]:
  c=cal();c[field]=value;reject(lambda:m.audit_calibration_lineage([], [c]))
 reject(lambda:m.audit_calibration_lineage([episode()]*2,[cal()]));reject(lambda:m.audit_calibration_lineage([],[cal()]*2));reject(lambda:m.audit_calibration_lineage([episode(lo=1,hi=1)],[cal()]))

TESTS=[('Worked example1','public',example1),('Worked example2','public',example2),('Boundary semantics','hidden',edges),('Independent oracle,scale and preservation','hidden',oracle_scale),('Invalid documented inputs','hidden',invalid)]
