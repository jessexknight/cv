from utils import *

# -------------------------------------------------------------------------------------------------
# pubs

ptmap = dict(
  oral='Oral',post='Poster',comp='Competitor',
  semi='Seminar',glec='Guest Lecture',prop='Proposal',emtg='Meeting',
)

def x2pub(X,T):
  log(X['id'],2)
  if not tint(X['inc']): return ''
  else: nax(X)
  # strings
  X['aus']   = nbib(X['aus'])
  X['eds']   = nbib(X['eds'])
  X['title'] = stex(X['title'])
  X['pubin'] = stex(X['inlong'])+sfmt(' ({})',X['inshrt'])
  X['pubr']  = stex(X['pubr'])
  X['url']   = salt(X['urlfin'],X['urlpre'])
  # nums
  for k in ['year','mo','vol','num','pr']:
    X[k] = tint(X[k])
  # type
  type = X.pop('type')
  if type == 'jart':
    X.update(bibtype='article',infield='journal')
  if type == 'chap':
    X.update(bibtype='inbook',infield='booktitle')
  if type == 'thes':
    X.update(bibtype='thesis',infield='type = {'+X['deg']+'},\n  school')
  if type in ptmap.keys():
    X.update(bibtype='inproceedings',infield='booktitle',pubin=ptmap[type]+': '+X['pubin'])
  # status
  X['sort'] = ''
  done = X['status'] in ['published','accepted','in press']
  if not done:
    X['sort'] = X['year']
    X['year'] = X['status']
  # keywords
  X['kwds'] = type
  X['kwds'] += ',done' if done else ',prep'
  X['kwds'] += ',misc' if type in ptmap.keys() else ''
  X['kwds'] += ',pr' if X['pr'] else ',npr'
  return re.sub('\n.* = {},','',T.format(**X))

# -------------------------------------------------------------------------------------------------
# funds

me    = 'Knight, Jesse'
ssmap = dict(grant='Grants',fellow='Fellowships',schol='Scholarships')

def x2fund(X,T):
  log(X['id'],2)
  if not tint(X['inc']): return ''
  X['title']    = stex(X['title'])
  X['fundlong'] = stex(X['fundlong'])
  X['calllong'] = stex(X['calllong'])
  X['extra']  = 'NPI: '+ntex(X['npi'])+' ' if X['npi'] != me else ''
  X['extra'] += '('+X['status']+')' if X['status'] not in ['in progress','complete'] else ''
  X['datefr'] = datex(X['yrfr'],X['mofr'])
  X['dateto'] = datex(X['yrto'],X['moto'])
  X['role']   = '' if X['ftype'] != 'grant' else \
    'Principal Investigator' if me in X['pi'].split('; ') else \
    'Co-Investigator' if me in X['coi'].split('; ') else \
    'Co-Applicant'
  return T.format(**X)

# -------------------------------------------------------------------------------------------------
# awards

def x2award(X,T):
  log(X['id'],2)
  if not tint(X['inc']): return ''
  else: nax(X)
  X['title'] = stex(X['title'])
  X['inst']  = stex(X['inst'])
  X['descr'] = stex(X['descr'])
  return T.format(**X)

# -------------------------------------------------------------------------------------------------
# main

log('loading',0)
Xs = dict(
  pubs = loadcsv(datapath('csv','pubs.csv')),
  funds = loadcsv(datapath('csv','funds.csv')),
  awards = loadcsv(datapath('csv','awards.csv')))
Ts = dict(
  pub = loadtxt(datapath('tps','pub.bib')),
  grant = loadtxt(datapath('tps','grant.tex')),
  fellow = loadtxt(datapath('tps','fellow.tex')),
  schol = loadtxt(datapath('tps','schol.tex')),
  award = loadtxt(datapath('tps','award.tex')),
  subsec = loadtxt(datapath('tps','subsec.tex')))

log('pubs',0)
pubs = ''.join([x2pub(X,Ts['pub']) for X in Xs['pubs']])
savetxt(datapath('tex','pubs.bib'),pubs)

log('funds + awards',0)
funds = ''.join(Ts['subsec'].format(title=v)+''.join(
    x2fund(X,Ts[k]) for X in Xs['funds'] if X['ftype'] == k)
  for k,v in ssmap.items())
awards = Ts['subsec'].format(title='Awards')+''.join(
  x2award(X,Ts['award']) for X in Xs['awards'])
savetxt(datapath('tex','funds+awards.tex'),funds+'\n'+awards)

