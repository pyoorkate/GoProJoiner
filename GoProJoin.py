import os
import re
import subprocess

input_directory = os.getcwd()
input_directory_contents = os.listdir(input_directory)
video_files = [fname for fname in input_directory_contents if fname.endswith('.MP4')] #Filtering only the MP4 files.

print("Less and less basic GoPro File Sort-and-Concatinator")
print("======================v0.3==========================")
print("Should work for all GoPros from 2 through 11 and GoPro Fusion")
print("Operates in current working directory & assumes FFMPEG is available in your path\n")

# Does user use a custom file naming convention
# At present custom naming is just playing fast and loose and just uses a wildcard regex
custom_naming = ""
print("Do you use custom or default GoPro filenames")
print("============================================\n")
print("Note: Custom assumes that anything before the standard camera prefix is the custom name")
while custom_naming != "D" and custom_naming != "C":
 	custom_naming = input("Enter (D)efault or (C)ustom: ")


# Identify Camera Type
# Rather than identify camera type separately for custom/default naming, we'll *presume* no one is silly enough to use the same
# name as a gopro already uses as its prefex, and go with a little wildcad regex lovin'
# Once camera type is identified we set the pattern we'll use to sort them later. 
camera_type = ""
chapters = 0
for video_file in video_files:
	# GoPro 5
	match = re.search (r'^.*GOPR\d+\.MP4$', video_file) # GoPro 2-5 naming convention, will check for chapters in a moment
	if match:
		camera_type = "GP5"
		print(f"\nDetected Camera Type: {camera_type}")
		if custom_naming == "D":
			primary_pattern = r'^GOPR\d+\.MP4$'
			primary_pattern_writing = r'^GOPR(\d+)\.MP4$'
		if custom_naming == "C":
		 	primary_pattern = r'^.*GOPR\d+\.MP4$'
		 	primary_pattern_writing = r'^.*GOPR(\d+)\.MP4$'
	match = None	 		
	match = re.search (r'^.*GP\d+\.MP4$', video_file) # GoPro 2-5 naming convention and has chapters
	if match:
		chapters = 1
		if custom_naming == "D":
			secondary_pattern = r'^GP\d+\.MP4$'
			secondary_pattern_writing = r'^GP\d+(\d{4})\.MP4$'
		if custom_naming == "C":
			secondary_pattern = r'^.*GP\d+\.MP4$'
			secondary_pattern_writing = r'^.*GP\d+(\d{4})\.MP4$'

	# GoPro Fusion
	match = None
	match = re.search (r'^.*GPFR\d+\.MP4$', video_file) # GoPro Fusion naming convention, will check for chapters in a moment
	if match:
		camera_type = "FUSION"
		if custom_naming == "D":
			primary_pattern_front = r'^GPFR\d+\.MP4$'
			primary_pattern_writing_front = r'^GPFR(\d+)\.MP4$'
			primary_pattern_back = r'^GPBK\d+\.MP4$'
			primary_pattern_writing_back = r'^GPBK(\d+)\.MP4$'
		if custom_naming == "C":
			primary_pattern_front = r'^.*GPFR\d+\.MP4$'
			primary_pattern_writing_front = r'^.*GPFR(\d+)\.MP4$'
			primary_pattern_back = r'^.*GPBK\d+\.MP4$'
			primary_pattern_writing_back = r'^.*GPBK(\d+)\.MP4$'
	match = None
	match = re.search (r'^.*GF\d+\.MP4$', video_file) # GoPro Fusion naming convention, and has chapters
	if match:
		chapters = 1
		if custom_naming == "D":
			secondary_pattern_front = r'^GF\d+\.MP4$'
			secondary_pattern_writing_front = r'^GF\d+(\d{4})\.MP4$'
			secondary_pattern_back = r'^GB\d+\.MP4$'
			secondary_pattern_writing_back = r'^GB\d+(\d{4})\.MP4$'
		if custom_naming == "C":
			secondary_pattern_front = r'^.*GF\d+\.MP4$'
			secondary_pattern_writing_front = r'^.*GF\d+(\d{4})\.MP4$'
			secondary_pattern_back = r'^GB\d+\.MP4$'
			secondary_pattern_writing_back = r'^GB\d+(\d{4})\.MP4$'


	# GoPro 360 video
	match = None
	match = re.search (r'^.*GS\d+\.MP4$', video_file) # 360 naming convention, difficult to test for chapters so just going to assume yes at the moment
	if match:
		camera_type = "360"
		chapters = 1
		if custom_naming == "D":
			primary_pattern = r'^GS01\d+\.MP4$'
			primary_pattern_writing = r'^GS(\d+)\.MP4$'
			secondary_pattern = r'^GS(0[2-9]|[1-9][0-9])\d+\.MP4$'
			secondary_pattern_writing = r'^GS(0[2-9]|[1-9][0-9])(\d{4})\.MP4$'
		if custom_naming == "C":
			primary_pattern = r'^.*GS01\d+\.MP4$'
			primary_pattern_writing = r'^.*GS(\d+)\.MP4$'
			secondary_pattern = r'^.*GS(0[2-9]|[1-9][0-9])\d+\.MP4$'
			secondary_pattern_writing = r'^.*GS(0[2-9]|[1-9][0-9])(\d{4})\.MP4$'

	# GoPro Hero 6-11
	# Filenames can start GH or GS
	match = None
	match = re.search (r'^.*GH\d+\.MP4$', video_file) # GoPro Hero naming convention, will check for chapters in a moment
	if match:
		camera_type = "HERO_H"
		if custom_naming == "D":
			primary_pattern = r'^GH01\d+\.MP4$'
			primary_pattern_writing = r'^GH(\d+)\.MP4$'
		if custom_naming == "C":
			primary_pattern = r'^.*GH01\d+\.MP4$'
			primary_pattern_writing = r'^.*GH(\d+)\.MP4$'
	match = None
	match = re.search (r'^.*GX\d+\.MP4$', video_file) # GoPro Hero naming convention, will check for chapters in a moment
	if match:
		camera_type = "HERO_X"
		if custom_naming == "D":
			primary_pattern = r'^GX01\d+\.MP4$'
			primary_pattern_writing = r'^GX(\d+)\.MP4$'
		if custom_naming == "C":
			primary_pattern = r'^.*GX01\d+\.MP4$'
			primary_pattern_writing = r'^.*GX(\d+)\.MP4$'
	match = None
	match = re.search (r'^.*GH02\d+\.MP4$', video_file) # GoPro Hero naming convention, assume that if it has a GH02 it has chapters
	if match:
		chapters = 1
		if custom_naming == "D":
			secondary_pattern = r'^GH(0[2-9]|[1-9][0-9])\d+\.MP4$'
			secondary_pattern_writing = r'^GH(0[2-9]|[1-9][0-9])(\d{4})\.MP4$'
		if custom_naming == "C":
			secondary_pattern = r'^.*GH(0[2-9]|[1-9][0-9])\d+\.MP4$'
			secondary_pattern_writing = r'^.*GH(0[2-9]|[1-9][0-9])(\d{4})\.MP4$'
	match = None
	match = re.search (r'^.*GX02\d+\.MP4$', video_file) # GoPro Hero naming convention, assume that if it has a GX02 it has chapters
	if match:
		chapters = 1
		if custom_naming == "D":
			secondary_pattern = r'^GX(0[2-9]|[1-9][0-9])\d+\.MP4$'
			secondary_pattern_writing = r'^GX(0[2-9]|[1-9][0-9])(\d{4})\.MP4$'
		if custom_naming == "C":
			secondary_pattern = r'^.*GX(0[2-9]|[1-9][0-9])\d+\.MP4$'
			secondary_pattern_writing = r'^.*GX(0[2-9]|[1-9][0-9])(\d{4})\.MP4$'

	# Check for GoPro Hero looping video because we're not handling those yet
	looping_check = re.search (r'^.*GH[a-zA-Z][a-zA-Z]\d+\.MP4$', video_file) 
	if looping_check:	
		print("\nLooping Video from GoPro hero detected. These are not currently handled. Exiting")
		exit()

	# SJCam
	# Add SJCAM HERE!



# If there are multiple chapters, identify whether the user wants all files combined 
# together, or each camera start as a separate file
allasone = ""
print(f"\nDetected Camera Type: {camera_type}")
if camera_type == "FUSION":
	print("When outputting fusion videos, front and back cameras are handled seperately")
if chapters == 0:
	print("\nNo chapters detected, assuming all single camera starts")
	while allasone != "C" and allasone != "E":
		allasone = input("(C)ombine into one file or (E)xit: ")
	if allasone == "E":
		exit()

if chapters == 1:
	print("\nMultiple chapters detected")
	while allasone != "C" and allasone != "I" and allasone != "E":
		allasone = input("(C)ombine into one file, (I)ndividual files for each camera start or (E)xit: ")	
	if allasone == "E":
		exit()

# Do they want to output to a different directory (just here because Nikki's script was posher than mine)
# Get an output directory, if this is blank use the current working directory
output_directory = input("\nOutput file directory (leave blank for current working directory): ")
if output_directory == "":
	output_directory = os.getcwd()

output_directory_exists = os.path.exists(output_directory)
if output_directory_exists == False:
	create_dir = input ("Directory does not exist. Create directory? (Y/N): ")
	while create_dir != "Y" and create_dir != "N":
		create_dir = input ("Directory does not exist. Create directory? (Y/N): ")

	if create_dir == "Y":
		# Okay then, I'll make the directory myself you lazy toad
		os.mkdir(output_directory)
	
	if create_dir == "N":
		# We could loop back and ask them a directory again, but...I can't be bothered.
		print ("Directory does not exist, user declined creation")
		print ("Program terminating")
		exit ()


# Output processes for combining into one file.

if allasone == "C":
	if camera_type == "GP5":
		# Match those files
		primary_segments = sorted([x for x in video_files if re.search(primary_pattern, x)])
		secondary_segments = sorted([x for x in video_files if re.search(secondary_pattern, x)])
		print("The following files and segments have been located:")
		print(f"Primary Segments: {primary_segments}")
		print(f"Secondary Segments: {secondary_segments}")
		print("Sorting, combining and creating lists...")
		# Create a new file to write the sorted filenames to
		with open("sorted_files.txt", "w") as f:
			for i, primary_file in enumerate(primary_segments):
				print(f"Primary Segment {i+1}")
				print(primary_file)
				# Write the primary segment file name to the output file
				f.write("file\t" + primary_file + "\n")
				primary_segment_num = int(re.search(primary_pattern_writing, primary_file).group(1))
				matching_secondary_segments = sorted([x for x in secondary_segments if primary_segment_num == int(re.search(secondary_pattern_writing, x).group(1)[:4])])
				print("Secondary segments")
				for secondary_file in matching_secondary_segments:
					print(secondary_file)
					# Write the secondary segment filenames to output file
					f.write("file\t" + secondary_file + "\n")

	if camera_type == "FUSION":
		# Match those files
		primary_segments_front = sorted([x for x in video_files if re.search(primary_pattern_front, x)])
		secondary_segments_front = sorted([x for x in video_files if re.search(secondary_pattern_front, x)])
		primary_segments_back = sorted([x for x in video_files if re.search(primary_pattern_back, x)])
		secondary_segments_back = sorted([x for x in video_files if re.search(secondary_pattern_back, x)])
		print("The following files and segments have been located:")
		print(f"Primary Segments Front: {primary_segments_front}")
		print(f"Secondary Segments Front: {secondary_segments_front}")
		print(f"Primary Segments Back: {primary_segments_back}")
		print(f"Secondary Segments Back: {secondary_segments_back}")
		print("Sorting, combining and creating lists...")
		# Create a new file to write the sorted filenames to
		with open("sorted_files.txt", "w") as f:
			for i, primary_file in enumerate(primary_segments_front):
				print(f"Primary Segment Front {i+1}")
				print(primary_file)
				# Write the primary segment file name to the output file
				f.write("file\t" + primary_file + "\n")
				primary_segment_num = int(re.search(primary_pattern_writing_front, primary_file).group(1))
				matching_secondary_segments = sorted([x for x in secondary_segments_front if primary_segment_num == int(re.search(secondary_pattern_writing_front, x).group(1)[:4])])
				print("Secondary segments")
				for secondary_file in matching_secondary_segments:
					print(secondary_file)
					# Write the secondary segment filenames to output file
					f.write("file\t" + secondary_file + "\n")
			for i, primary_file in enumerate(primary_segments_back):
				print(f"Primary Segment Back {i+1}")
				print(primary_file)
				# Write the primary segment file name to the output file
				f.write("file\t" + primary_file + "\n")
				primary_segment_num = int(re.search(primary_pattern_writing_back, primary_file).group(1))
				matching_secondary_segments = sorted([x for x in secondary_segments_back if primary_segment_num == int(re.search(secondary_pattern_writing_back, x).group(1)[:4])])
				print("Secondary segments")
				for secondary_file in matching_secondary_segments:
					print(secondary_file)
					# Write the secondary segment filenames to output file
					f.write("file\t" + secondary_file + "\n")
				
	if camera_type == "HERO_H" or camera_type == "HERO_X" or camera_type == "360":
		# Match those files
		primary_segments = sorted([x for x in video_files if re.search(primary_pattern, x)])
		secondary_segments = sorted([x for x in video_files if re.search(secondary_pattern, x)])
		print("The following files and segments have been located:")
		print(f"Primary Segments: {primary_segments}")
		print(f"Secondary Segments: {secondary_segments}")
		print("Sorting, combining and creating lists...")

		# Create a new file to write the sorted filenames to
		with open("sorted_files.txt", "w") as f:
			for i, primary_file in enumerate(primary_segments):
				print(f"Primary Segment {i+1}")
				print(primary_file)
				
				# Write the primary segment file name to the output file
				f.write("file\t" + primary_file + "\n")
				primary_segment_num = int(re.search(primary_pattern_writing, primary_file).group(1))
				primary_segment_significant = int (str (primary_segment_num)[-4:])
				
				# Match secondary segments to their primary segmeents
				# Secondary segments need to be matched based off the last four digits of the filename
				matching_segments = []
				for x in secondary_segments:
					match_significant_portion = (str(re.search(secondary_pattern_writing, x).group(2)[:4]))
					if primary_segment_significant == int(match_significant_portion):
						matching_segments.append(x)
				matching_secondary_segments = sorted(matching_segments)
				print("Secondary segments: ")
				for secondary_file in matching_secondary_segments:
					print(secondary_file)
					# Write the secondary segment filenames to output file
					f.write("file\t" + secondary_file + "\n")

	print("Matched list complete...")
	outputname = input("Please enter filename for output (without file extension): ")
	outputname = outputname + ".mp4"
	# join together yon filename and the path input earlier
	output_full_filename = os.path.join(output_directory, outputname)
	# Call FFMPEG using the full filename and directory for output
	subprocess.run(['ffmpeg', '-y', '-f', 'concat', '-i', 'sorted_files.txt', '-c', 'copy', '-map', '0:0', '-map', '0:1', '-map', '0:3', output_full_filename ])
	print(f"Hopefully you have a file called {outputname} in {output_directory}. It should have all the files combined in one.")
	exit()				
				

# Outputting Individual Files...

if allasone == "I":
	if camera_type == "GP5":
		segmentcount = 0
		primary_segments = sorted([x for x in video_files if re.search(primary_pattern, x)])
		secondary_segments = sorted([x for x in video_files if re.search(secondary_pattern, x)])
		# We'll increment this counter for every file segment, that way when we get to writing the files we know how many.
		# Don't open file yet...because we need that to happen separately for each segment.
		print("The following files and segments have been located:/n")
		for i, primary_file in enumerate(primary_segments):
			segmentcount = segmentcount + 1
			print(f"Primary Segment {i+1}")
			print(primary_file)
			with open("sorted_file%s.txt" % i, "w") as f:
				# Write the primary segment file name to the output file
				f.write("file\t" + primary_file + "\n")
				primary_segment_num = int(re.search(primary_pattern_writing, primary_file).group(1))
				matching_secondary_segments = sorted([x for x in secondary_segments if primary_segment_num == int(re.search(secondary_pattern_writing, x).group(1)[:4])])
				print("Secondary segments")
				for secondary_file in matching_secondary_segments:
					print(secondary_file)
					# Write the secondary segment filenames to output file
					f.write("file\t" + secondary_file + "\n")
			f.close()

	if camera_type == "FUSION":
		segmentcount = 0		
		# We'll increment this counter for every file segment, that way when we get to writing the files we know how many.
		# Don't open file yet...because we need that to happen separately for each segment.		
		primary_segments_front = sorted([x for x in video_files if re.search(primary_pattern_front, x)])
		secondary_segments_front = sorted([x for x in video_files if re.search(secondary_pattern_front, x)])
		primary_segments_back = sorted([x for x in video_files if re.search(primary_pattern_back, x)])
		secondary_segments_back = sorted([x for x in video_files if re.search(secondary_pattern_back, x)])
		print(f"Primary Segments Front: {primary_segments_front}")
		print(f"Secondary Segments Front: {secondary_segments_front}")
		print(f"Primary Segments Back: {primary_segments_back}")
		print(f"Secondary Segments Back: {secondary_segments_back}")
		print("Sorting, combining and creating lists...")

		# Create a new file to write the sorted filenames to
		for i, primary_file in enumerate(primary_segments_front):
			segmentcount = segmentcount + 1
			print(f"Primary Segment Front {i+1}")
			print(primary_file)
			with open("sorted_file%s.txt" % i, "w") as f:
				# Write the primary segment file name to the output file
				f.write("file\t" + primary_file + "\n")
				primary_segment_num = int(re.search(primary_pattern_writing_front, primary_file).group(1))
				matching_secondary_segments = sorted([x for x in secondary_segments_front if primary_segment_num == int(re.search(secondary_pattern_writing_front, x).group(1)[:4])])
				print("Secondary segments")
				for secondary_file in matching_secondary_segments:
					print(secondary_file)
					# Write the secondary segment filenames to output file
					f.write("file\t" + secondary_file + "\n")
		for i, primary_file in enumerate(primary_segments_back):
			sorted_file_count = segmentcount
			segmentcount = segmentcount + 1
			print(f"Primary Segment Back {i+1}")
			print(primary_file)
			with open("sorted_file%s.txt" % sorted_file_count, "w") as f:
				# Write the primary segment file name to the output file
				f.write("file\t" + primary_file + "\n")
				primary_segment_num = int(re.search(primary_pattern_writing_back, primary_file).group(1))
				matching_secondary_segments = sorted([x for x in secondary_segments_back if primary_segment_num == int(re.search(secondary_pattern_writing_back, x).group(1)[:4])])
				print("Secondary segments")
				for secondary_file in matching_secondary_segments:
					print(secondary_file)
					# Write the secondary segment filenames to output file
					f.write("file\t" + secondary_file + "\n")
		f.close()
						

	if camera_type == "HERO_H" or camera_type == "HERO_X" or camera_type == "360":
		# Match those files
		primary_segments = sorted([x for x in video_files if re.search(primary_pattern, x)])
		secondary_segments = sorted([x for x in video_files if re.search(secondary_pattern, x)])
		print("The following files and segments have been located:")
		print(f"Primary Segments: {primary_segments}")
		print(f"Secondary Segments: {secondary_segments}")
		print("Sorting, combining and creating lists...")
		segmentcount = 0
		# We'll increment this counter for every file segment, that way when we get to writing the files we know how many.
		# Don't open file yet...because we need that to happen separately for each segment.
		for i, primary_file in enumerate(primary_segments):
			segmentcount = segmentcount + 1
	
			# Create a new file to write the sorted filenames to
			print(f"Primary Segment {i+1}")
			print(primary_file)
			with open("sorted_file%s.txt" % i, "w") as f:
				# Write the primary segment file name to the output file
				f.write("file\t" + primary_file + "\n")

				# Identify the important bit of the filename for matching
				primary_segment_num = int(re.search(primary_pattern_writing, primary_file).group(1))
				primary_segment_significant = int (str (primary_segment_num)[-4:])
				
				# Match secondary segments to their primary segmeents
				# Secondary segments need to be matched based off the last four digits of the filename
				matching_segments = []
				for x in secondary_segments:
					match_significant_portion = (str(re.search(secondary_pattern_writing, x).group(2)[:4]))
					if primary_segment_significant == int(match_significant_portion):
						matching_segments.append(x)
				matching_secondary_segments = sorted(matching_segments)
				print("Secondary segments: ")
				for secondary_file in matching_secondary_segments:
					print(secondary_file)
					# Write the secondary segment filenames to output file
					f.write("file\t" + secondary_file + "\n")
			f.close()

	if camera_type == "BLANK":
		segmentcount = 0
		# We'll increment this counter for every file segment, that way when we get to writing the files we know how many.
		# Don't open file yet...because we need that to happen separately for each segment.
		print("The following files and segments have been located:/n")
		for i, primary_file in enumerate(primary_segments):
			segmentcount = segmentcount + 1
			print(f"Primary Segment {i+1}")
			print(primary_file)
			with open("sorted_file%s.txt" % i, "w") as f:
				# Write the primary segment file name to the output file
				f.write("file\t" + primary_file + "\n")
				primary_segment_num = int(re.search(primary_pattern_writing, primary_file).group(1))
				matching_secondary_segments = sorted([x for x in secondary_segments if primary_segment_num == int(re.search(secondary_pattern_writing, x).group(1)[:4])])
				print("Secondary segments")
				for secondary_file in matching_secondary_segments:
					print(secondary_file)
					# Write the secondary segment filenames to output file
					f.write("file\t" + secondary_file + "\n")
			f.close()
			
		
	if camera_type == "":
		print("No valid camera type detected, exiting (sorry!).")
		exit()

	print("Matched list complete...")
	outputname = input("Please enter basename for output (without file extension): ")
	print("Calling FFMPEG to do the actual joining...")

	# initiate loop to call FFMPEG
	# subtract one from segment count because the filenames start at 0, and segment count started at 1.
	# I could use another variable here, but why would I?
	segmentcount = segmentcount - 1
	while segmentcount > -1:
		# Munge together a filename containing the current segment and the all the other bits of the name
		current_segment_file = "sorted_file" + str(segmentcount) + ".txt"
	
		# join together yon filename and the path input earlier
		segment_count_stringified = str(segmentcount)
		output_full_name = outputname + segment_count_stringified + ".mp4"
		output_full_filename_with_path = os.path.join(output_directory, output_full_name)
		# Call FFMPEG using the sorted_files filename as a source and outputting to outputname
		# print(f"\nDEBUG OUTPUT: {current_segment_file}")
		subprocess.run(['ffmpeg', '-y', '-f', 'concat', '-i', current_segment_file, '-c', 'copy', '-map', '0:0', '-map', '0:1', '-map', '0:3', output_full_filename_with_path ])
		segmentcount = segmentcount - 1
		
	print(f"Tada! You have many files. You are truly blessed.")
exit()
