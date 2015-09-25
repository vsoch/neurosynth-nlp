import xml.etree.ElementTree as ET
import numpy
import os
import json
import sys

output_json = sys.argv[1]
input_files = sys.argv[2]

input_files = input_files.split(",")
input_files =  [os.path.abspath(input_file) for input_file in input_files]
output_json = os.path.abspath(output_json)

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
        nodes[parent] = {"name":parent_id,
                        "variants":children,
                        "ref_id":child.attrib["ref_id"]}
    result = {"nodes":nodes,"source":source}
    return result

# Extract brain region dictionaries
xmls = []
for input_file in input_files:
    xmls.append(extract_xml(input_file))

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
for x in xmls:
    regions = merge_dicts(regions,x)

# Now make it proper json!
result = []
for region,info in regions.iteritems():
    result.append({"name":region,
                   "ref_id":info["ref_id"],
                   "variants":numpy.unique(info["variants"]).tolist()})

# Write to output file
filey = open(output_json,'wb')
filey.write(json.dumps(result, sort_keys=True,indent=4, separators=(',', ': ')))
filey.close()
