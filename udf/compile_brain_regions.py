import xml.etree.ElementTree as ET
import os
import sys

output_json = sys.argv[1]
import json

# Function to return dictionary of dict[parent] = [child1,child2,child3]
# Each parent is a brain region term
def extract_xml(xmlfile,parent_id="canonical",child_id="base"):
    source = os.path.split(xmlfile)[-1].replace(".xml","")
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    nodes = dict()
    # Here we are iterating through tokens
    for child in root:
        parent = child.attrib[parent_id].lower()
        children = []
        # Get any child nodes
        for variant in child:
            children.append({"name":variant.attrib[child_id].lower()})
        nodes[child.attrib[parent_id]] = {"name":parent_id,
                                          "variants":children,
                                          "ref_id":child.attrib["ref_id"]}
    result = {"nodes":nodes,"source":source}
    return result

# Extract brain region dictionaries
aba = extract_xml('NER/aba-syn.xml')
bams = extract_xml('NER/bams2004swanson-syn.xml')

def merge_dicts(regions,regiondict):
    for name,others in regiondict["nodes"].iteritems():
        if name in regions:
            holder = regions[name]
            for region in others["variants"]:
                if not region["name"] in holder["variants"]:
                    holder["variants"].append(region["name"])
            holder["ref_id"] = holder["ref_id"].append(others["ref_id"])
            regions[name] = holder
        else:
            variants = []
            for region in others["variants"]:
                variants.append(region["name"])
            regions[name] = {"variants": variants, 
                             "ref_id": [others["ref_id"]]}
    return regions

# Combine them into one
regions = dict()
regions = merge_dicts(regions,aba)
regions = merge_dicts(regions,bams)

# Write to output file
filey = open(output_json,'wb')
filey.write(json.dumps(regions, sort_keys=True,indent=4, separators=(',', ': ')))
filey.close()
