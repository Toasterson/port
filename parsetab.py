
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.5'

_lr_method = 'LALR'

_lr_signature = '8EF373ACBAE3EF79FD4F837CD7B1616E'
    
_lr_action_items = {'VERSION':([0,],[2,]),'$end':([1,7,],[0,-1,]),'EQUALS':([2,],[3,]),'DOUBLEQUOTE':([3,5,11,],[4,7,-2,]),'NUMBER':([4,8,10,],[6,9,11,]),'PERIOD':([6,9,],[8,10,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'version':([0,],[1,]),'versionstring':([4,],[5,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> version","S'",1,None,None,None),
  ('version -> VERSION EQUALS DOUBLEQUOTE versionstring DOUBLEQUOTE','version',5,'p_version','plytest.py',90),
  ('versionstring -> NUMBER PERIOD NUMBER PERIOD NUMBER','versionstring',5,'p_versionstring','plytest.py',96),
  ('makro -> MAKRO','makro',1,'p_makro','plytest.py',102),
]