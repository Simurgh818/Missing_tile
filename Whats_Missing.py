import numpy as np
import os
import csv

csv_file = []
csv_file_tile = []
template_range = 0

with open('/mnt/finkbeinernas/robodata/Sina/Robo3_Images/JAK-MPA2-1-DR/JAK_MPA2_1_DR.csv', newline='') as f:
	reader = csv.reader(f)
	for row in reader:
		# print(row)
		csv_file[len(csv_file):] = [row[0]]
		csv_file_tile[len(csv_file_tile):]= [row[2]]

print(len(csv_file))
# print(csv_file,'\n')
if 'Well' in csv_file:
	well_index = csv_file.index('Well')+1
	# print("the well element is on: ",well_index)
	print("the wells are: ", csv_file[well_index:],'\n')
	well_plate = len(csv_file[well_index:])
	print("We got ", well_plate, "wells in the plate.",'\n')

print(csv_file_tile,'\n')
if 'Timepoint' in csv_file_tile:
	timepoint_index = csv_file_tile.index('Timepoint')+1
	timepoints = csv_file_tile[timepoint_index:csv_file_tile.index('Array')-1]
	print("The timepoints are: ", timepoints)

if 'Array' in csv_file_tile:
	tile_index=csv_file_tile.index('Array')+1
	image_tiles = csv_file_tile[tile_index]
	template_range = int(csv_file_tile[tile_index])**2
	print("The number of tiles are ", template_range, '\n')


# well_plate = 96
#  input("How many well plate did you use? Type 72, 96,or 384? ")
if well_plate ==72:
	plate_rows = ['A','B','C','D','E','F','G','H']
	plate_columns = ['1','2','3','4','5','6','7','8','9']
elif well_plate ==96:
	plate_rows = ['A','B','C','D','E','F','G','H']
	plate_columns = ['1','2','3','4','5','6','7','8','9','10','11','12']

number_of_channels = 3
# image_tiles = 4
# input("What's the image template for this dataset? Press 2 for 2x2, 3 for 3x3, 4 for 4x4 and 5 for 5x5: ")
# expected number of images is calculated by multiplying wells in a plate by number of tiles in a well and
# 	adding one for the Fiduciary
# template_range = image_tiles**2

expected_number_of_images = well_plate*(template_range)*number_of_channels
print("The expected number of images are: ", expected_number_of_images,'\n')

well = []


for w_alpha in range(0,len(plate_rows)):
	for w_num in range(0, len(plate_columns)):
		well.append(plate_rows[w_alpha]+plate_columns[w_num])
print("The wells are: ",well, '\n')

plate_dir = '/mnt/finkbeinernas/robodata/Sina/Robo3_Images/JAK-MPA2-1-DR/'
for lf in os.listdir(plate_dir):
	print(lf)
	if lf.endswith('.log') and lf.find('JAK-MPA2-1-DR-T10.log')>=0:
		print('\n',lf)
		well_with_missing_tile = []
		current_line = []

		path = plate_dir + lf
		# path = '/mnt/finkbeinernas/robodata/Sina/Robo3_Images/JAK-JEL22-Plate2/JAK-JEL22-Plate2-T0_1.log'
		# input("What's the path location of the log file you like to open? ")

		path = str(path)
		print("Path is: ",path,'\n')
		log_file = open(path, 'r')
		temp = log_file.read()
		split_log_file = temp.split(' ; \n')
		# print(split_log_file)
		# if split_log_file.find('FIDUCIARY')>0:
		length_split_log_file = len(split_log_file)

		print("log file length is: ", length_split_log_file)
		for file in range(1, len(split_log_file)-1):
			if split_log_file[file].find('FIDUCIARY')>=0 or split_log_file[file].find('ROTFID')>=0:
				length_split_log_file = length_split_log_file-1


		# print(split_log_file)
		file =1
		count_img = 0
		while file<(len(split_log_file)):
			# print(file)
			# if split_log_file[file].find('FIDUCIARY')>0:
			# 	length_split_log_file = length_split_log_file-1
			if split_log_file[file].find('FIDUCIARY')<=0 and split_log_file[file].find('ROTFID')<=0:

				# loop through all expected wells
				for w in well:
					# print(well)
					count =0
					for template in range(1,template_range+1):
						if file < length_split_log_file:

							for cl in range (1,len(split_log_file)):
								if split_log_file[cl].split('_')[4].find(str(w))>=0 and split_log_file[cl].split('_')[5].find(str(template))>=0:
									current_line = split_log_file[cl]
									time_stamp = split_log_file[cl].split('--')[0]
									count_img = count_img+1
									file = file+1
									break
								else:
									current_line = ''


							# print(w,', panel ', template, ': ',current_line)
							if current_line == '':
								count = count+1
								well_with_missing_tile[len(well_with_missing_tile):] = [(w, template, time_stamp)]

						else:
							break
					# print('------------------------------------------------------------------')
				if file >= length_split_log_file:
					break

			else:
				file = file+1
				continue


		print('\n\n')
		titles =['Expected Number of images', 'Number of images found', 'wells with their number of missing tiles are']
		data = [titles]+list(zip([expected_number_of_images],[count_img],[well_with_missing_tile]))
		for i,d in enumerate(data):
			line = '|'.join(str(x).ljust(25) for x in d)
			print(line)
			if i ==0:
				print('-'*len(line))
			pass
		print('------------------------------------------------------------------')

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


