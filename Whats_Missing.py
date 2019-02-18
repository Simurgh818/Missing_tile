import numpy as np
import os
import csv

csv_file = []
csv_file_tile = []
csv_file_channel = []
template_range = 0
well_plate = 0

with open('/mnt/finkbeinernas/robodata/Sina/Robo3_Images/JAK-MPA1-TL-2/JAK-MPA1-TL-2-RowAB/JAK-MPA1-TL-2-RowAB.csv', \
	newline='\n') as f:
	reader = csv.reader(f, delimiter=',')
# , delimiter=';'
	# print(next(reader))

	for row in reader:
		# row = row[0]
		# next(reader)
		# print("length of row is: ",len(row),"tile", row[4:5])

		csv_file[len(csv_file):] = row[0:1]
		csv_file_tile[len(csv_file_tile):]= row[2:3]
		csv_file_channel[len(csv_file_channel):]= row[4:5]

# print(csv_file,'\n\n',csv_file_tile,'\n\n',csv_file_channel)

if 'Well' in csv_file:
	well_index = csv_file.index('Well')+1
	# print("the well element is on: ",well_index)
	# print("the wells are: ", csv_file[well_index:],'\n')
	well_plate = len(csv_file[well_index:])
	print("We got ", well_plate, "wells in the plate.",'\n')

# print(csv_file_tile,'\n')
if 'Timepoint' in csv_file_tile:
	timepoint_index = csv_file_tile.index('Timepoint')+1
	timepoints = csv_file_tile[timepoint_index:csv_file_tile.index('Array')]
	print("The timepoints are: ", timepoints)

if 'Array' in csv_file_tile:
	tile_index=csv_file_tile.index('Array')+1
	image_tiles = csv_file_tile[tile_index]
	template_range = int(csv_file_tile[tile_index])**2
	print("The number of tiles are ", template_range, '\n')

if 'Channels' in csv_file_channel:
	channels_index = csv_file_channel.index('Channels')+1
	channels = csv_file_channel[channels_index]
	channels_array = channels.split(';')
	print(channels_array)
	number_of_channels = len(channels_array)
	print("number of channels are ", number_of_channels, '\n')

# print(csv_file_channel,'\n')

# well = []

plate_dir = '/mnt/finkbeinernas/robodata/Sina/Robo3_Images/JAK-MPA1-TL-2/JAK-MPA1-TL-2-RowAB/'
for lf in os.listdir(plate_dir):
	print(lf)
	if lf.endswith('.log') and lf.find('JAK-MPA1-TL-2-RowAB-T17.log')>=0:
		# and lf.find('JAK-MPA1-TL-2-RowAB-T8.log')>=0
		if lf.find('T0')>=0:
			expected_number_of_images = well_plate*(template_range)*number_of_channels
			print("The expected number of images are: ", expected_number_of_images,'\n')
		else:
			expected_number_of_images = well_plate*(template_range)
			print("The expected number of images are: ", expected_number_of_images,'\n')
			channels_array = channels_array[1:]

		# print('\n',lf)


		path = os.path.join(plate_dir,lf)
		# path = '/mnt/finkbeinernas/robodata/Sina/Robo3_Images/JAK-JEL22-Plate2/JAK-JEL22-Plate2-T0_1.log'
		# input("What's the path location of the log file you like to open? ")

		path = str(path)
		print("Path is: ",path,'\n')
		log_file = open(path, 'r')
		temp = log_file.read()
		split_log_file = temp.split('\n\n')
		# (' ; \n')
		# ### The split log file is:
		# print("The Split log file is: ", split_log_file)
		# if split_log_file.find('FIDUCIARY')>0:
		length_split_log_file = len(split_log_file)-1

		print("log file length is: ", length_split_log_file)
		for file in range(0, len(split_log_file)):
			if split_log_file[file].find('FIDUCIARY_MONTAGE')>=0 or \
				split_log_file[file].find('ROTFID_STACK')>=0 or \
				split_log_file[file].find('ROTFID_MONTAGE')>=0:

				length_split_log_file = length_split_log_file-1
				# print("found one at ", file, length_split_log_file)
		well_with_missing_tile = []
		current_line = [' ']*len(split_log_file)
		# print("current_line: ", len(current_line), '\n')
		print("log file length after subtracting FIDUCIARY and ROTFID is: ", length_split_log_file,'\n')
		# print(split_log_file)
		file =1
		count_img = 0
		count = 0
		while file<len(split_log_file):
			# print(file)

			if split_log_file[file].find('FIDUCIARY')<=0 or split_log_file[file].find('ROTFID')<=0 \
				or split_log_file[file].find('\n')<=0:

				# loop through all expected wells
				for w in csv_file[well_index:]:
					# print(w)
					count =0
					for template in range(1,template_range+1):
					# loop through expected tiles
						for ch in channels_array:
							# loop through expected channels
							# print("we are on channel: ", ch)
							time_stamp = [' ']*len(split_log_file)
							for cl in range (0,len(split_log_file)-1):
								# check the whole log for the specific file entry
								current_well = str(split_log_file[cl].split('_')[4])
								current_tile = str(split_log_file[cl].split('_')[5])
								current_channel = str(split_log_file[cl].split('_')[6].split('.')[0])
								time_stamp[cl] = split_log_file[cl].split(' ')[3]
								# print("current_well is: ", current_well, "current_tile is: ", current_tile \
									# , "current_channel is :", current_channel)
								# print(current_well == str(w), current_tile == str(template),\
										# current_channel == str(ch))
								# split_log_file[cl].find('.tif')>=0  and \
								if (current_well == str(w) and \
										current_tile == str(template) and \
										current_channel == str(ch)):
									# print(split_log_file[cl])
									current_line[cl] = split_log_file[cl]
									count_img = count_img+1
									# print(file, w,', panel ', template, ch, ': ',current_line[cl])
									file = file+1
									# cl=0
									break
								else:
									# print("cl is: ", cl)
									current_line[cl] = ' '


							## print(w,', panel ', template, ': ',current_line[cl])
							# instead do a loop to check all lines for blank.
							if current_line[cl] == ' ':
								count = count+1
								well_with_missing_tile[len(well_with_missing_tile):] = \
								[(w, template, ch, time_stamp[cl])]
								# print(file, w,', panel ', template, ch, ': ',current_line[cl])


						if file > expected_number_of_images or file > length_split_log_file:
							break
					# print('------------------------------------------------------------------')
					if file > expected_number_of_images or file > length_split_log_file:
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
		print('------------------------------------------------------------------------------------------------')

