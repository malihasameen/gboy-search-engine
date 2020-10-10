import os
import json
import sys

def sorting(input_dir):
	word_dirs = next(os.walk(input_dir))[1]

	for word in word_dirs:
		with open(input_dir + '/' + word + "/info.json") as infile:
			info = json.load(infile)

		info_sorted = dict(sorted(info.items(), key=lambda k: k[1]['pagerank'], reverse=True))

		with open(input_dir + '/' + word + "/info.json", 'w') as outfile:
			json.dump(info_sorted, outfile)

		print(word)

if __name__ == '__main__':
	# Usage: python sorting.py -i path/to/processed_dir
	if sys.argv != 3:
		print("Usage: python sorting.py -i path/to/processed_dir")
		exit()

	input_dir = sys.argv[2]
	print("Sorting........")
	sorting(input_dir)
	print("Sorting Complete!!!")