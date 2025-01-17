import xml.etree.ElementTree as ET
import json

# Load and parse the XLIFF file
xlf_file = 'C:\\Users\\Ayomide Ogun-Ajala\\Downloads\\Extractor\\Translate_To_hu_HU_4_0607fe82-d9b0-43f3-a657-0dd48dfa8b1d.xml.xlf'
tree = ET.parse(xlf_file)
root = tree.getroot()

# Load and parse the TBX file
tbx_file = 'C:\\Users\\Ayomide Ogun-Ajala\\Downloads\\Extractor\\terminology.tbx'
tbx_tree = ET.parse(tbx_file)
tbx_root = tbx_tree.getroot()

# Define the namespace for xml
namespaces = {'xml': 'http://www.w3.org/XML/1998/namespace'}

# Extract terminology entries from the TBX file
terminologies = []
for term_entry in tbx_root.findall(".//termEntry"):
    en_term = term_entry.find(".//langSet[@xml:lang='en-US']/tig/term", namespaces).text
    hu_term = term_entry.find(".//langSet[@xml:lang='hu-HU']/tig/term", namespaces).text
    definition_elem = term_entry.find(".//langSet[@xml:lang='hu-HU']/tig/descrip[@type='definition']", namespaces)
    definition = definition_elem.text if definition_elem is not None else 'None'
    terminologies.append((en_term, hu_term, definition))

# Load and extract data from control.dat file
control_dat_file = 'C:\\Users\\Ayomide Ogun-Ajala\\Downloads\\Extractor\\control.dat'
control_data = {}
with open(control_dat_file, 'r', encoding='utf-8') as file:
    current_section = None
    for line in file:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' in line:
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            if current_section:
                control_data[current_section][key] = value
            else:
                control_data[key] = value
        elif line.startswith('#BEGIN FILE'):
            current_section = 'FILE'
            control_data[current_section] = {}
        elif line.startswith('#END FILE'):
            current_section = None

# Extract translation units and their data
json_data = []
with open('extracted_info.txt', 'w', encoding='utf-8') as f:
    f.write("Control.dat Information:\n")
    for key, value in control_data.items():
        if isinstance(value, dict):
            f.write(f"\n[{key}]\n")
            for sub_key, sub_value in value.items():
                f.write(f"{sub_key}: {sub_value}\n")
        else:
            f.write(f"{key}: {value}\n")

    f.write("\nTranslation Units Information:\n")

    for trans_unit in root.iter('trans-unit'):
        if trans_unit.attrib.get('translate') == 'no':
            continue

        trans_id = trans_unit.get('id')
        source_elem = trans_unit.find('source')
        source = source_elem.text if source_elem is not None else None
        target_elem = trans_unit.find('target')
        target = target_elem.text if target_elem is not None else 'None'

        if source is None:
            continue

        # Initialize the list of other suggestions
        other_suggestions = []

        # Process each alt-trans element
        for alt_trans in trans_unit.findall('alt-trans'):
            if alt_trans.attrib.get('translate') == 'no':
                continue
            match_quality = alt_trans.attrib.get('match-quality', 'None')
            mt_target_elem = alt_trans.find('target')
            mt_suggestion = mt_target_elem.text if mt_target_elem is not None else 'None'

            # Extract note information
            note_elem = alt_trans.find('note')
            note_content = note_elem.text if note_elem is not None else 'None'

            # Determine the type value
            note_type = 'none'
            if note_elem is not None:
                note_lines = note_content.split('\n')
                for line in note_lines:
                    if line.startswith('type='):
                        note_type = line.split('=')[1]
                        break

            other_suggestions.append({
                "sourceText": source,
                "targetText": mt_suggestion,
                "score": int(float(match_quality.strip('%'))) if match_quality != 'None' else None,
                "type": note_type,
                "note": note_content
            })

        f.write(f"\nID: {trans_id}\n")
        f.write(f"Source: {source}\n")
        f.write(f"Target: {target}\n")
        f.write("Other Suggestions:\n")
        for suggestion in other_suggestions:
            f.write(f"  - Type: {suggestion['type']}\n")
            f.write(f"    Match Quality: {suggestion['score']}\n")
            f.write(f"    Target: {suggestion['targetText']}\n")
            f.write(f"    Note: {suggestion['note']}\n")

        f.write("Terminologies:\n")
        unit_terminologies = []
        for en_term, hu_term, definition in terminologies:
            if en_term in source:
                f.write(f"  - EN: {en_term}\n")
                f.write(f"    HU: {hu_term}\n")
                f.write(f"    Definition: {definition}\n")
                unit_terminologies.append({
                    "en_term": en_term,
                    "hu_term": hu_term,
                    "definition": definition
                })

        f.write("\n")

        # Prepare JSON data
        json_data.append({
            "sourceText": source,
            "targetText": target,
            "other_suggestions": other_suggestions,
            "terminologies": unit_terminologies,
            "properties": {
                "filePath": control_data.get('OriginalName', ''),
                "itemId": trans_id,
                "sourceLang": control_data.get('sourceLanguage', 'en'),
                "targetLang": control_data.get('targetLanguage', 'hu'),
                "domain": control_data.get('Domain', ''),
                "customEngine": control_data.get('tool', '')
            }
        })

# Write JSON data to file
with open('extracted_info.json', 'w', encoding='utf-8') as json_file:
    json.dump(json_data, json_file, indent=4, ensure_ascii=False)

print("Extracted information saved to extracted_info.txt and extracted_info.json")
