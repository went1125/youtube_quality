#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <error.h>
#include <sys/time.h>
#include <stdlib.h>

#define SHARED_PROPORTION "/shared_proportion"

void define_init_proportion(double *portion)
{
	*portion = 1.0;
}

double get_current_time(struct timeval tval)
{
	return (tval.tv_sec + (tval.tv_usec * 1e-6));
}

int main(int argc, char *argv[]) {

    int flag = O_RDWR | O_CREAT | O_TRUNC;

    int share_id = shm_open(SHARED_PROPORTION, flag, 0666);

    if (share_id < 0) {
        perror("shm_open");
        exit(0);
    }

    ftruncate(share_id, sizeof(double));

    double *adjust_portion = (double *) mmap(NULL, sizeof(double), PROT_READ | PROT_WRITE, MAP_SHARED, share_id, 0);
    
    if (adjust_portion == MAP_FAILED) {
        perror("mmap");
        exit(0);
    }
	
	define_init_proportion(adjust_portion);		

    // Adjust portion
    double portion = strtod(argv[1], NULL);
    *adjust_portion *= portion;
    printf("adjust portion: %lf\n", *adjust_portion);
    msync(NULL, sizeof(double), MS_SYNC);

    //*adjust_portion = 0.1;
    //*adjust_portion *= 34;

    printf("adjust_portion: %lf\n", *adjust_portion);

    //sleep(100);
    if (munmap(adjust_portion, sizeof(double)) < 0) {
        perror("munmap");
    }

    return 0;
}
