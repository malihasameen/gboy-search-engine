import os
import json
import xml.etree.ElementTree as ET
from stemmer import PorterStemmer
import re

def cleaning(text):
	text = text.strip().lower()
	text = re.sub('[^0-9a-zA-Z]+', ' ', text)
	text = text.strip().split()
	prep_file = open('preposition.dat', 'r').read().split('\n')
	text = [x for x in text if x not in prep_file]
	return text

def inverted_index(xmlfile, output_dir):
	tree = ET.parse(xml_path)
	root = tree.getroot()
	print("Started Indexing.......")

	for page in root.iter('page'):
	    # Cleaning title and text words
	    title = cleaning(page[0].text)
	    id = page[2].text
	    text = cleaning(page[-1][-2].text)
	    
	    # Indexing title words
	    for i, word in enumerate(title):
	    	# Word already exists
	        if os.path.exists(output_dir + '/'  + word):
	            with open(output_dir + '/'  + word + "/info.json") as infile:
	                info = json.load(infile)
	            if id in info:
	                count_title = info[id]['count_title'] + 1
	                count_text = info[id]['count_text']
	                pagerank = info[id]['pagerank'] + (1/((i+10)+10))
	            else:
	                count_title = 1
	                count_text = 0
	                pagerank = 0.0 + (1/((i+10)+10))
	            
	            info[id] = {'count_title': count_title, 'count_text':count_text, 'pagerank': pagerank}
	        
	            with open(output_dir + '/'  + word + "/info.json", 'w') as outfile:
	                json.dump(info, outfile, indent=4)
	        
	        # Word doesnot exists
	        else:
	            os.mkdir(output_dir + '/'  + word)
	            
	            info = {}
	            count_title = 1
	            count_text = 0
	            pagerank = 0.0 + (1/((i+10)+10))
	            
	            info[id] = {'count_title': count_title, 'count_text':count_text, 'pagerank': pagerank}
	            
	            with open(output_dir + '/'  + word + "/info.json", 'w') as outfile:
	                json.dump(info, outfile)
	    
	    # Indexing text words            
	    for i, word in enumerate(text):
	    	# Word already exists
	        if os.path.exists(output_dir + '/'  + word):
	            with open(output_dir + '/'  + word + "/info.json") as infile:
	                info = json.load(infile)
	            if id in info:
	                count_title = info[id]['count_title']
	                count_text = info[id]['count_text'] + 1
	                pagerank = info[id]['pagerank'] + (0.3/((i+100)+100))
	            else:
	                count_title = 0
	                count_text = 1
	                pagerank = 0.0 + (0.3/((i+100)+100))
	            
	            info[id] = {'count_title': count_title, 'count_text':count_text, 'pagerank': pagerank}
	        
	            with open(output_dir + '/'  + word + "/info.json", 'w') as outfile:
	                json.dump(info, outfile, indent=4)
	        
	        # Word doesnot exists
	        else:
	            os.mkdir(output_dir + '/'  + word)
	            
	            info = {}
	            count_title = 0
	            count_text = 1
	            pagerank = 0.0 + (0.3/((i+100)+100))
	            
	            info[id] = {'count_title': count_title, 'count_text':count_text, 'pagerank': pagerank}
	            
	            with open(output_dir + '/'  + word + "/info.json", 'w') as outfile:
	                json.dump(info, outfile, indent=4)
    	print(id)

if __name__ == '__main__':
	# Usage: python inverted_index.py -i path/to/input_file.xml -o path/to/processed_dir
	if sys.argv != 5:
		print("Usage: python inverted_index.py -i path/to/input_file.xml -o path/to/output_dir")
		exit()

	xml_path = sys.argv[2]
	output_dir = sys.argv[4]

	inverted_index(xml_path, output_dir)