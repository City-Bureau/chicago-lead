import re

def open_file(file_name, skiprows=1):
    with open(file_name) as f:
        for i in range(0, skiprows):
            next(f)
        return f.read()

def strip_nl(x):
    base = x.group(0).split('\n')[0]
    if ',' in base:
        return '%s,' % base
    return '%s,' % base.strip('"')

def detect_start(x):
    return '\n' if '\n' in x.group(0) else ''

def strip_flags(x):
    return re.sub(',(-|BA|AA|ND)\n', '\n', x)

def convert_none(x):
    return re.sub('(ND|<[0-9].[0-9]+|None Detected)', '0', x)

def prepend_school_name(x, school_name):
    x = re.sub('^', '%s,' % school_name, x)
    return re.sub('\n', '\n%s,' % school_name, x)

def append_file_name(x, filename):
    pdf = re.sub('.csv', '.pdf', filename.split('-')[-1])
    return re.sub('\n', ',%s\n' % pdf, x)

def process(x, school_name, file_name, droprows=1):
    x = strip_flags(x)
    x = convert_none(x)
    x = prepend_school_name(x, school_name)
    x = append_file_name(x, file_name)
    return '\n'.join(x.split('\n')[:-droprows])

files = {
    'Sabin': 'tabula/tabula-individualschool_sabin_610342.csv', 
    'Powell': 'tabula/tabula-IndividualSchool_Powell_610281.csv', 
    'Falconer': 'tabula/tabula-Individualschool_Falconer_609910.csv', 
    'Skinnernorth': 'tabula/tabula-individualschool_skinnernorth_610534.csv', 
    'Tanner': 'tabula/tabula-Individualschool_Tanner_610279.csv', 
    'Younghs': 'tabula/tabula-IndividualSchool_YoungHS_ 609755.csv', 
    'Juarezhs': 'tabula/tabula-IndividualSchool_JuarezHS_ 609764.csv', 
    'Garvy': 'tabula/tabula-individualschool_garvy_609937.csv', 
    'Cassell': 'tabula/tabula-individualschool_cassell_609849.csv', 
    'Collinshs': 'tabula/tabula-IndividualSchool_CollinsHS_610499.csv', 
    'Lasalle': 'tabula/tabula-individualschool_lasalle_610033.csv'
}

# special cases
collinshs = open_file(files['Collinshs'], skiprows=3)
collinshs = re.sub('(\n|^)"",Collins,[0-9]{5},', detect_start, collinshs)
collinshs = re.sub('\n9561', '\n59561', collinshs)
collinshs = re.sub('59561-1-HAL-WC01-003,"P', '59651-1-HAL-WC01-003,"P', collinshs)
collinshs = re.sub('\n"",.*\n', '\n', collinshs)
collinshs = re.sub(',{1,}\n', '\n', collinshs)
collinshs = process(collinshs, 'Collinshs', files['Collinshs'])

juarezhs = open_file(files['Juarezhs'])
juarezhs = re.sub('(^|\n)[^0-9]*,[0-9]{5},', detect_start, juarezhs)
juarezhs = re.sub('".*\n.*",', strip_nl, juarezhs)
juarezhs = re.sub('(ND,){2}.*\n', 'ND,ND\n', juarezhs)
juarezhs = re.sub('\n[0-9]+[^0-9]{2}.*\n', '\n', juarezhs)
juarezhs = process(juarezhs, 'Juarezhs', files['Juarezhs'])

tanner = open_file(files['Tanner'], skiprows=2)
tanner = re.sub('".*\n.*",', strip_nl, tanner)
tanner = re.sub('51484-2-N-F02-,', '51484-2-N-F02-10,', tanner)
tanner = re.sub('"Chicago Public Schools\nDepartment of Facility\nOperations"', '51484-1-N-F01-11', tanner)
tanner = process(tanner, 'Tanner', files['Tanner'], droprows=2)

younghs = open_file(files['Younghs'])
younghs = re.sub('".*\n.*",', strip_nl, younghs)
younghs = re.sub('(^|\n)[^0-9]*,[0-9]{5},', detect_start, younghs)
younghs = process(younghs, 'Younghs', files['Younghs'], droprows=2)

falconer = open_file(files['Falconer'], skiprows=2)
falconer = process(falconer, 'Falconer', files['Falconer'], droprows=2)

# standard
sabin = open_file(files['Sabin'])
sabin = process(sabin, 'Sabin', files['Sabin'])

powell = open_file(files['Powell'])
powell = process(powell, 'Powell', files['Powell'])

skinnernorth = open_file(files['Skinnernorth'])
skinnernorth = process(skinnernorth, 'Skinnernorth', files['Skinnernorth'])

garvy = open_file(files['Garvy'])
garvy = process(garvy, 'Garvy', files['Garvy'])

cassell = open_file(files['Cassell'])
cassell = process(cassell, 'Cassell', files['Cassell'])

lasalle = open_file(files['Lasalle'])
lasalle = process(lasalle, 'Lasalle', files['Lasalle'])

data = ('\n'.join([
    'school,sample,location,date,result,filename',
    collinshs, juarezhs, tanner, younghs, falconer, 
    sabin, powell, skinnernorth, garvy, cassell, lasalle
]))

data = re.sub(',,', ',', data)

print(data)
