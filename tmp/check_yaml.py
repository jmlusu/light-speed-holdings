import yaml
data = yaml.safe_load(open('company-registry.yaml'))
for a in data['company']['agents']:
    if a['id'] == 'board_chair':
        rpt = a['reports_to']
        print('board_chair reports_to:', repr(rpt))
        break
else:
    print('board_chair not found')