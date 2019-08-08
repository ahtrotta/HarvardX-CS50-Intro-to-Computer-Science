#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

// define and initialize block size
const int BLOCK_SIZE = 512;

// create data type of byte
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // check for proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: recover filename\n");
        return 1;
    }
    
    // open corrupted image    
    FILE *crrptdImg = fopen(argv[1], "r");
    
    // check if file can be opened
    if (crrptdImg == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", argv[1]);
        return 2;
    }
    
    // create buffer
    BYTE *buffer = malloc(sizeof(BYTE) * BLOCK_SIZE);
    
    // initialize counter variable for the number of JPEGs
    int count = 0;
    
    // initialize trigger variable
    int trigger = 0;
    
    // create filename
    char *filename = malloc(sizeof(char) * 8);
    
    // crate filename_old
    char *filename_old = malloc(sizeof(char) * 8);
    
    // iterate through blocks until EOF, which is smaller than one block
    while ((fread(buffer, 1, BLOCK_SIZE, crrptdImg)) == BLOCK_SIZE)
    {
        // read one block from input file (necessary?)
        // fread(buffer, 1, BLOCK_SIZE, crrptdImg);
        
        // check for JPEG
        if (buffer[0] == 0xff &&
            buffer[1] == 0xd8 &&
            buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // check to see if this is the first JPEG
            if (count == 0 && trigger == 0)
            {
                trigger++;
            }
            else if (count != 0 || (count == 0 && trigger == 1))
            {
                count++;
            }
            
            // generate name of output file
            sprintf(filename, "%03i.jpg", count);
                
            // create output file
            FILE *img = fopen(filename, "w");
            
            // check if output file can be created
            if (img == NULL)
            {
                fprintf(stderr, "Could not create %s.\n", filename);
                return 3;
            }

            // write to output file
            fwrite(buffer, BLOCK_SIZE, 1, img);
            
            // close output file
            fclose(img);
        }
        else 
        {
            // check if JPEG has been found
            if (trigger > 0)
            {
                // generate current filename
                sprintf(filename, "%03i.jpg", count);
                
                // open file
                FILE *img = fopen(filename, "a");
                
                // write to currently open img
                fwrite(buffer, BLOCK_SIZE, 1, img);
                
                // close file
                fclose(img);
            }
        }
    }
    
    // close corrupted image
    fclose(crrptdImg);
    
    // free dynamically allocated memory
    free(buffer);
    free(filename);
    free(filename_old);
    
    // success
    return 0;
}
