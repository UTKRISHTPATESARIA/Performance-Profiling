#define _GNU_SOURCE

#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <signal.h>
#include <time.h>
#include <sched.h>
#include <sys/ioctl.h>
#include <linux/perf_event.h>
#include <asm/unistd.h>

long perf_event_open(struct perf_event_attr* event_attr, pid_t pid, int cpu, int group_fd, unsigned long flags)
{
	return syscall(__NR_perf_event_open, event_attr, pid, cpu, group_fd, flags);
}

int main(int argc, char** argv)
{
	clock_t start, endt;
    int n = atoi(argv[1]), block_size = atoi(argv[2]), end = 1, event_numbers = 19;
    int fd[event_numbers];
    char event_names[19][25] = {"cycles", "instructions", "page-faults", "cache-references", "cache-misses", "L1-icache-load-misses", "L1-dcache-loads",
                                    "L1-dcache-load-misses", "L1-dcache-stores", "LLC-loads", "LLC-load-misses", "LLC-stores", "LLC-store-misses", "iTLB-loads",
                                    "iTLB-load-misses", "dTLB-loads", "dTLB-load-misses", "dTLB-stores", "dTLB-store-misses"};
    char filename[100];
    unsigned long int time_v = (unsigned long)time(NULL);
    sprintf(filename, "ijk_%d_%d_stat_%lu.log", n, block_size, time_v);
    srand(time(NULL));

    float** A = (float**)malloc(n * sizeof(float*));
    float** B = (float**)malloc(n * sizeof(float*));
    float** C = (float**)malloc(n * sizeof(float*));
    for (int i = 0; i < n; ++i){
        A[i] = (float*)malloc(n * sizeof(float));
        B[i] = (float*)malloc(n * sizeof(float));
        C[i] = (float*)malloc(n * sizeof(float));
        for(int j = 0; j < n; ++j){
            A[i][j] = 0.0;
            B[i][j] = ((float)rand()/(float)(RAND_MAX)) * end;
            C[i][j] = ((float)rand()/(float)(RAND_MAX)) * end;
        }
    }
	struct perf_event_attr event_data[event_numbers];
    for(int i = 0; i < event_numbers; ++i){
        memset(&(event_data[i]), 0, sizeof(event_data[0]));
        event_data[i].size = sizeof(event_data[0]);
    }

	event_data[0].type = PERF_TYPE_HARDWARE;
	event_data[1].type = PERF_TYPE_HARDWARE;
	event_data[2].type = PERF_TYPE_SOFTWARE;
    for(int i = 3; i < event_numbers; ++i){
	    event_data[i].type = PERF_TYPE_HW_CACHE;
    }

    
	event_data[0].config = PERF_COUNT_HW_CPU_CYCLES; 
    event_data[1].config = PERF_COUNT_HW_INSTRUCTIONS;
	event_data[2].config = PERF_COUNT_SW_PAGE_FAULTS;
	event_data[3].config = PERF_COUNT_HW_CACHE_REFERENCES;
	event_data[4].config = PERF_COUNT_HW_CACHE_MISSES;
	event_data[5].config = ( PERF_COUNT_HW_CACHE_L1I ) | (PERF_COUNT_HW_CACHE_OP_READ << 8) | (PERF_COUNT_HW_CACHE_RESULT_MISS << 16) ;
	event_data[6].config = ( PERF_COUNT_HW_CACHE_L1D ) | (PERF_COUNT_HW_CACHE_OP_READ << 8) | (PERF_COUNT_HW_CACHE_RESULT_ACCESS << 16); 
	event_data[7].config = ( PERF_COUNT_HW_CACHE_L1D ) | (PERF_COUNT_HW_CACHE_OP_READ << 8) | (PERF_COUNT_HW_CACHE_RESULT_MISS << 16);
	event_data[8].config = ( PERF_COUNT_HW_CACHE_L1D ) | (PERF_COUNT_HW_CACHE_OP_WRITE << 8) | (PERF_COUNT_HW_CACHE_RESULT_ACCESS << 16);
	event_data[9].config = ( PERF_COUNT_HW_CACHE_LL ) | (PERF_COUNT_HW_CACHE_OP_READ << 8) | (PERF_COUNT_HW_CACHE_RESULT_ACCESS << 16);
	event_data[10].config = ( PERF_COUNT_HW_CACHE_LL ) | (PERF_COUNT_HW_CACHE_OP_READ << 8) | (PERF_COUNT_HW_CACHE_RESULT_MISS << 16);
	event_data[11].config = ( PERF_COUNT_HW_CACHE_LL ) | (PERF_COUNT_HW_CACHE_OP_WRITE << 8) | (PERF_COUNT_HW_CACHE_RESULT_ACCESS << 16); 
	event_data[12].config = ( PERF_COUNT_HW_CACHE_LL ) | (PERF_COUNT_HW_CACHE_OP_WRITE << 8) | (PERF_COUNT_HW_CACHE_RESULT_MISS << 16);
	event_data[13].config = ( PERF_COUNT_HW_CACHE_ITLB ) | (PERF_COUNT_HW_CACHE_OP_READ << 8) | (PERF_COUNT_HW_CACHE_RESULT_ACCESS << 16);
	event_data[14].config = ( PERF_COUNT_HW_CACHE_ITLB ) | (PERF_COUNT_HW_CACHE_OP_READ << 8) | (PERF_COUNT_HW_CACHE_RESULT_MISS << 16); 
	event_data[15].config = ( PERF_COUNT_HW_CACHE_DTLB ) | (PERF_COUNT_HW_CACHE_OP_READ << 8) | (PERF_COUNT_HW_CACHE_RESULT_ACCESS << 16);
	event_data[16].config = ( PERF_COUNT_HW_CACHE_DTLB ) | (PERF_COUNT_HW_CACHE_OP_READ << 8) | (PERF_COUNT_HW_CACHE_RESULT_MISS << 16);
	event_data[17].config = ( PERF_COUNT_HW_CACHE_DTLB ) | (PERF_COUNT_HW_CACHE_OP_WRITE << 8) | (PERF_COUNT_HW_CACHE_RESULT_ACCESS << 16); 
	event_data[18].config = ( PERF_COUNT_HW_CACHE_DTLB ) | (PERF_COUNT_HW_CACHE_OP_WRITE << 8) | (PERF_COUNT_HW_CACHE_RESULT_MISS << 16);


	for(int i = 0; i < event_numbers; ++i)
	{
		event_data[i].disabled = 1;
        event_data[i].exclude_kernel = 1;
        event_data[i].exclude_hv = 1;
		fd[i] = perf_event_open(event_data+i, 0, -1, -1, 0);
		if (fd[i] == -1) 
        	{
                printf("Issue with opening perf event %d", i);
                exit(-1);
        	}
    }

    for(int i = 0; i < event_numbers; ++i){
        ioctl(fd[i], PERF_EVENT_IOC_RESET, 0);
        ioctl(fd[i], PERF_EVENT_IOC_ENABLE, 0);
    }

    start = clock();
    for(int i=0;i<n;i+=block_size){
        for(int j=0;j<n;j+=block_size){
            for(int k=0;k<n;k+=block_size){
                for(int ii=i;ii<i+block_size;ii++){
                    for(int jj=j;jj<j+block_size;jj++){
                        for(int kk=k;kk<k+block_size;kk++){
                            A[ii][jj] += B[ii][kk]*C[kk][jj];
                        }
                    }
                }
            }
        }
    }

    endt = clock();

    for(int i = 0; i < event_numbers; ++i){
        ioctl(fd[i], PERF_EVENT_IOC_DISABLE, 0);
    }
    free(A);
    free(B);
    free(C);


    FILE *file;
    file = fopen(filename, "w+");
    char write_data[1000];
    unsigned long long int event_count;
    fprintf(file, "\nPerformance data\n\n");
    for(int i = 0; i < event_numbers; ++i){
        read(fd[i], &event_count, sizeof(event_count));
        sprintf(write_data, "\t%llu\t%s\n", event_count, event_names[i]);
        fprintf(file, write_data);
        close(fd[i]);
    }
	char *s = "seconds time elapsed";
    sprintf(write_data, "\t%lf\t%s\n",((double) (endt - start)) / CLOCKS_PER_SEC, s);
    fprintf(file, write_data);
    fclose(file);
}
    

