import xml.etree.ElementTree as ET

for level in range(-1, 4):
    tree = ET.parse('map.xml')
    root = tree.getroot()

    for c in root.findall('way'):
        hasLevel = False
        for i in c.findall('tag'):
            if i.attrib['k'] == 'min_level' or i.attrib['k'] == 'max_level':
                hasLevel = True
                break
            if i.attrib['k'] == 'level':
                hasLevel = True
                # print(i.attrib['v'])
                if not(len(i.attrib['v']) >= 3 or i.attrib['v'] == str(level)):
                    # print('removed')
                    root.remove(c)
        if not hasLevel:
            root.remove(c)
    for c in root.findall('relation'):
        root.remove(c)

    tree.write(str(level) + '_only.xml')

# for level in range(-1, 4):
#     tree = ET.parse(str(level) + '_only.xml')
#     root = tree.getroot()
#     for i in root:
#         print(i)
