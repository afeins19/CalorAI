# formatting timestamps to work with JSON (NEEDED FOR MFP)

def datacleanup(data):
  res = []
  for d in data:
    if 'date' in d:
      d['date'] = str(d['date'])
    if type(d)==list:
      if 'day' in d[0]:
        d[0]['day'] = str(d[0]['day'])
      if 'date' in d[0]:
        d[0]['date'] = str(d[0]['date'])
    res.append(d)
  return res