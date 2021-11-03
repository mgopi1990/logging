#!/usr/bin/env python3

'''
Packs logs into a single file and makes it convinient to copy into excel
eg.
logging_pack.py file1.txt file2.txt file3.txt
file1.txt file2.txt file3.txt will be concat into a.out
'''

import sys
import pprint

def parse_logs(infilelist, outfile='a.out'):
	outfp = open (outfile, 'w')

	for file in infilelist:
		try:
			fp = open (file, 'r')
		except e:
			print (' ERROR: Open failed {}'.format(file))
			fp.close()
			continue

		heading = []
		for line in fp:
			if line == '\n' or line == '':
				break
			heading.append(line)

		brief = []
		tstring = ''
		skip = True 
		for line in fp:
			if line == '\n' or line == '':
				if skip == False:
					brief.append(tstring)
					tstring = ''
				skip = True
			else:
				skip = False
				tstring += line
		else:
			## for the last line
			if skip == False:
				brief.append(tstring)

		#pprint.pprint (heading)
		#pprint.pprint (brief)

		if len(heading) != len(brief):
			print (' ERROR: {}: len mismatch {}/{}'.format(file, len(heading), len(brief)))
			#pprint.pprint (heading)
			#pprint.pprint (brief)
			fp.close()
			continue

		outfp.write('{}\n{}\n'.format('=='*5, file))
		for i in range(0, len(heading)):
			outfp.write(' {}'.format(heading[i]))
		outfp.write('-----\n')

		for i in range(0, len(heading)):
			outfp.write('\n{}\n{}\n{}\n-----\n'.format(file, heading[i], brief[i]))

	outfp.close()
	return

if __name__ == "__main__":
	parse_logs(sys.argv[1:])
			
