# GoProJoiner
Really basic python script to sort GoPro files into the correct order and join them together into either a single file or into individual segments for each camera start.

It operates in current working directory & assumes FFMPEG is available in your path; it will attempt to make a directory for you if you ask it to output to a directory that doesn't exist.
It currently performs no error checking to confirm it's not going to overwrite files in the output directory.

I take no responsibilty for any horrific things this does.

Don't expect me to ever do anything else with it unless it breaks for me.
