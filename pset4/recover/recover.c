#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <cs50.h>

int main(int argc, char *argv[])
{
	if (argc != 2)
	{
		fprintf(stderr, "Usage: ./recover filename");
		return 1;
	}
	// Open the cardfile and make sure its not broken
	FILE* fraw = fopen(argv[1], "r");	

	if(fraw == NULL)
	{	
			fclose(fraw);
			fprintf(stderr, "Can't open file\n");
			return 1;
	}

	// jpeg checking array
	uint8_t jpg[3] = {0xff, 0xd8, 0xff};
	
	// Count of jpegs for file names
	int count = 0;

	// Setting up the output file
	bool open = false;
	FILE* output;

  // Read 512b blocks from file.
	uint8_t file[512];
	uint8_t check[4];
	
	fread(file, 512, 1, fraw);	

	while(fread(file, 512, 1, fraw) > 0)
	{
			// Check the first 4 bytes
			for(int i = 0; i < 4; i++)
			{
					check[i] = file[i];
			}

			// Check if it is a jpeg
			if (memcmp(jpg, check, 3) == 0)
			{
				// Make the filename
				char filename[8];
				sprintf(filename, "%03d.jpg", count);

				if(!open)
				{
						output = fopen(filename, "w");
						fwrite(file, sizeof(file), 1, output);
						open = true;
				}
				
				output = fopen(filename, "w");
				fwrite(file, sizeof(file), 1, output);
				count++;
					
			}
			else if (open)
			{
				fwrite(file, sizeof(file), 1, output);
			}
	}

	if(output)
	{
	  fclose(output);
	}
	
	fclose(fraw);
	return 0;
}