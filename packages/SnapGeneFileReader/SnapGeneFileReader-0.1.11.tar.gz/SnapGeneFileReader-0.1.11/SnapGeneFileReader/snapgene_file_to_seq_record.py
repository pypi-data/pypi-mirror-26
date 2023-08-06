import sys
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import DNAAlphabet
from Bio.SeqFeature import SeqFeature, FeatureLocation
import html2text

from .SnapGeneFileReader import SnapGeneFileReader

html_parser = html2text.HTML2Text()
html_parser.ignore_emphasis = True
html_parser.ignore_links = True
html_parser.body_width = 0

def parse_qualifiers(qualifiers_list):
    qualifiers_dict = {}
    for q in qualifiers_list:
        name = q['name']
        val = q['value']
        for key in val:
            try:
                qualifiers_dict[name] = html_parser.handle(val[key])[:-2]
            except:
                qualifiers_dict[name] = 'unknown'
            break
    return qualifiers_dict

def snapgene_file_to_seq_record(name, file_object=None):
    """
    name: it can be the file name, or just a string if file_object is provided.
    file_object: it can be an opened file, or io.BytesIO
    """
    if file_object:
        obj_dict = SnapGeneFileReader().read_file(name, file_object=file_object)
    else:
        obj_dict = SnapGeneFileReader().read_file(name)

    record = SeqRecord(Seq(obj_dict['seq'], DNAAlphabet() ))

    strand_dict = {'+':1, '-':-1, '.':0}

    for feature in obj_dict['features']:
        record.features.append(
            SeqFeature(
                FeatureLocation(
                    feature['start'], 
                    feature['end'],
                    strand=strand_dict[feature['strand']],
                    ),
                strand=strand_dict[feature['strand']],
                id=feature['text'],
                type=feature['type'],
                qualifiers=parse_qualifiers(feature['qualifiers'])
                )
        )

    record.name = record.id = obj_dict['name']

    return record

