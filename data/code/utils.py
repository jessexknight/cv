import os,re,csv

verb = 3

def datapath(*args):
  return os.path.join('data',*args)

def log(msg,lvl):
  if verb >= lvl:
    print(['-'*50+'\n{}','> {}','  + {}'][lvl].format(msg))

def loadcsv(fname):
  log('loading: '+fname,1)
  with open(fname,'r') as f:
    return [row for row in csv.DictReader(f)]

def loadtxt(fname):
  log('loading: '+fname,1)
  with open(fname,'r') as f:
    return f.read()

def savetxt(fname,txt):
  log('saving: '+fname,1)
  with open(fname,'w') as f:
    return f.write(txt)

def nax(X):
  X.update(**{k:'' for k in X.keys() if X[k] in ('','NA')})

def salt(s1,s2):
  return s1 if s1 else s2

def sfmt(fmt,s):
  return fmt.format(s) if s else ''

def tint(s):
  try: return int(s)
  except: return s

def stex(s):
  return s.replace('&','\&').replace(' - ',' -- ')

def nbib(s):
  return s.replace('; ',', and ')

def ntex(s):
  return ', '.join(' '.join(name.split(', ')[::-1]) for name in s.split('; '))

def datex(yr,mo,alt=''):
  if mo: return '{}.{:02d}'.format(yr,tint(mo))
  if yr: return yr
  return alt