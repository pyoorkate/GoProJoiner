import os
import re
import subprocess

print("Less and less basic GoPro File Sort-and-Concatinator")
print("====================================================")
# Written using ChatGPT, a lot of fiddling to get it to kinda work, then me polishing the turd
print("Operates in current working directory & assumes FFMPEG is available in your path\n\n")

video_files = os.listdir('.')

# Do they use a custom file naming convention (Like Nikki does, gods damn it)
custom_naming = ""
print("Do you use custom or default gopro filenames")
print("============================================\n")
print("At the moment, custom just assumes that anything before \nGOPR or GP is the custom name. \nIt will match anything with GOPR or GP in the name")
print("There's a very faint possibility that I might fix this at some point.")
print("\n(D)efault")
print("(C)ustom\n")
custom_naming = input("Custom or Default: ")
while custom_naming != "D" and custom_naming != "C":
	custom_naming = input("Please choose D or C: ")
	
if custom_naming == "D":
	primary_pattern = r'^GOPR\d+\.MP4$'
	primary_pattern_writing = r'^GOPR(\d+)\.MP4$'
	secondary_pattern = r'^GP\d+\.MP4$'
	secondary_pattern_writing = r'^GP\d+(\d{4})\.MP4$'
	
if custom_naming == "C":
# At present custom naming is just playing fast and loose.
	primary_pattern = r'^.*GOPR\d+\.MP4$'
	primary_pattern_writing = r'^.*GOPR(\d+)\.MP4$'	
	secondary_pattern = r'^.*GP\d+\.MP4$'
	secondary_pattern_writing = r'^.*GP\d+(\d{4})\.MP4$'

# Match those files
primary_segments = sorted([x for x in video_files if re.search(primary_pattern, x)])
secondary_segments = sorted([x for x in video_files if re.search(secondary_pattern, x)])


# Basic matching	
# primary_segments = sorted([x for x in video_files if re.search(r'^GOPR\d+\.MP4$', x)])
# secondary_segments = sorted([x for x in video_files if re.search(r'^GP\d+\.MP4$', x)])

# Identify whether the user wants all files combined together, or each camera start
# as a separate file
allasone = ""
print("\nChoose output type")
print("==================\n")
print("(A)ll as one file")
print("(I)ndividual files for each camera start\n")
allasone = input("Ouput type: ")

while allasone != "A" and allasone != "I":
	allasone = input("Ouput type (either A or I): ")


# Do they want to output to a different directory (just here because my friend's script was posher than mine)
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


if allasone == "A":
	print("The following files and segments have been located:\n")
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

	print("List Complete...")
	outputname = input("Please enter filename for joined output (without file extension): ")
	outputname = outputname + ".mp4"
	# join together yon filename and the path input earlier
	output_full_filename = os.path.join(output_directory, outputname)
	# Call FFMPEG using the full filename and directory for output
	subprocess.call(['ffmpeg', '-y', '-f', 'concat', '-i', 'sorted_files.txt', '-c', 'copy', '-map', '0:0', '-map', '0:1', '-map', '0:3', output_full_filename ])
	print(f"Hopefully you have a file called {outputname} in {output_directory}. It should have all the files combined in one.")
	exit()

if allasone == "I":
	segmentcount = 0
	#we'll increment this counter for every file segment, that way when we get to writing the files we know how many.
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

	print("List Complete...")
	outputname = input("Please enter basename for joined output (without file extension): ")
	# initiate loop to call FFMPEG
	# subtract one from segment count because the filenames start at 0, and segment count started at 1.
	# I could use another variable here, but why would I?
	segmentcount = segmentcount - 1
	while segmentcount > -1:
		# Munge together a filename containing the current segment and the all the other bits of the name
		current_segment_file = "sorted_file" + str(segmentcount) + ".txt"
		# join together yon filename and the path input earlier
		segment_count_stringified = str(segmentcount)
		output_full_filename = os.path.join(output_directory, outputname, segment_count_stringified + ".MP4")
		print(f"Launching FFMPEG for " + output_full_filename )
		# Call FFMPEG using the sorted_files filename as a source and outputting to outputname
		subprocess.call(['ffmpeg', '-y', '-f', 'concat', '-i', current_segment_file, '-c', 'copy', '-map', '0:0', '-map', '0:1', '-map', '0:3', output_full_filename ])
		segmentcount = segmentcount - 1
		
		
	print(f"Tada! You have many files. You are truly blessed.")
	exit()
	
else:
	print("Uncaught error (I mean, I did tons of error checking, so this is totally unexpected... ;) )")
	exit()
	
