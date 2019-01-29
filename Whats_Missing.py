import numpy as np
import os

path = '/mnt/finkbeinernas/robodata/Sina/Robo3_Images/JAK-JEL22-Plate2/JAK-JEL22-Plate2-T0_1.log'
# input("What's the path location of the log file you like to open? ")

path = str(path)
print("Path is: ",path,'\n')
log_file = open(path, 'r')
temp = log_file.read()
split_log_file = temp.split(' ; \n')
print("log file length is: ", len(split_log_file)-1)

well_plate = 72
#  input("How many well plate did you use? Type 72, 96,or 384? ")
if well_plate ==72:
	plate_rows = ['A','B','C','D','E','F','G','H']
	plate_columns = ['1','2','3','4','5','6','7','8','9']

image_tiles = 4
# input("What's the image template for this dataset? Press 2 for 2x2, 3 for 3x3, 4 for 4x4 and 5 for 5x5: ")
# expected number of images is calculated by multiplying wells in a plate by number of tiles in a well and
# 	adding one for the Fiduciary
template_range = image_tiles**2

expected_number_of_images = well_plate*(template_range)+1
print("The expected number of images are: ", expected_number_of_images,'\n')

well = []
for w_alpha in range(0,len(plate_rows)):
	for w_num in range(0, len(plate_columns)):
		well.append(plate_rows[w_alpha]+plate_columns[w_num])
print("The wells are: ",well, '\n')

# print(split_log_file)
file =1
while file<=(len(split_log_file)-1):
	# print(file)
	if split_log_file[file].find('FIDUCIARY')<=0:

		well_with_missing_tile = ['']
		# print(int(len(plate_rows)))
		current_line = []
		for w in well:
# loop through all expected wells
			# print(well)
			count =0
			for template in range(1,template_range+1):
				if file < len(split_log_file)-1:
					# print("Line number: ",file, "panel number: ", template)
					# loop through the whole split_log_file to find the respective well and tile
					# current_line= split_log_file[file]
					# if len(current_line.split('_'))>=2:
					# 	# print("we are on line: ", template)
					# 	well_actual = current_line.split('_')[4]
					# 	tile_actual = current_line.split('_')[5]
					# 	print("we are on tile: ", tile_actual)

					for cl in range (1,len(split_log_file)-1):
						if split_log_file[cl].split('_')[4].find(str(w))>=0 and split_log_file[cl].split('_')[5].find(str(template))>=0:
							# print(w,', panel ', template, ': ',split_log_file[cl])
							current_line = split_log_file[cl]
							file = file+1
							break
						else:
							current_line = ''
						# need to fix this condtion to only catch missing

					print(w,', panel ', template, ': ',current_line)
					if split_log_file[cl].split('_')[4].find(str(w))<0 or split_log_file[cl].split('_')[5].find(str(template))<0:
						count = count+1
						well_with_missing_tile[len(well_with_missing_tile):] = [w, template]
					# for cl in range (1,len(split_log_file)-1):
					# 	if split_log_file[cl].find(str(w))<0 and split_log_file[cl].find(str(template))<0:
					# 		count = count+1
					# 		print(w,', panel ', template, ':')
					# 		well_with_missing_tile[len(well_with_missing_tile):] = [well, count]
								# template = template-1
								# break
							# print(well,', panel ', template, ': ',current_line)

			# file = file + template_range
				else:
					break
			print('------------------------------------------------------------------')
		if file >= len(split_log_file)-1:
			break

	else:
		continue


print('\n\n')
titles =['Expected Number of files', 'Number of files found', 'wells with their number of missing tiles are']
data = [titles]+list(zip([expected_number_of_images],[len(split_log_file)-1],[well_with_missing_tile]))
for i,d in enumerate(data):
	line = '|'.join(str(x).ljust(25) for x in d)
	print(line)
	if i ==0:
		print('-'*len(line))
	pass

# for file in range(0,len(split_log_file)-1):
# 	file_entry = split_log_file[file]
# 	temp2 = file_entry.split(' -- ')
# 	file_name = temp2[1]
# 	if file_name.find('FIDUCIARY')<=0:
# 		count =0
# 		for template in range(1,template_range+1):
# 			# position = file+template
# 			if file < len(split_log_file)-1:
# 				current_line = split_log_file[template]
# 				if len(current_line.split('_'))>=2:
# 					well = current_line.split('_')[4]
# 					tile = current_line.split('_')[5]
# 					# print("we are on tile: ", tile)
# 					if  tile != template:
# 						np.add(count,1)
# 						print(well,', panel ', template, ':')
# 					else:
# 						print(well,', panel ', template, ': ',current_line)
# 			else:
# 				break
# 			# print(well,', panel ', template, ': ',current_line)
# 		file = file + template

# 	print('------------------------------------------------------------------')


