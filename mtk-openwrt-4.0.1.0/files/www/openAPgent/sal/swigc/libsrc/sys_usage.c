#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h>

#define ZERO 0
#define ONE 1
#define JIFFIES_NUM 4

#define MAX_LINE_LENGTH 80

struct memory_info
{
    int memorytotal;
    int memoryfree;
    int memoryused;
};

enum jiffy{USER, USER_NICE, SYSTEM, IDLE} jiffy_enum;



/**
 * Get cpu usage 
 */
float
sys_usage_get_cpu_usage(void)
{
	int idx;
	int diff_jiffies[JIFFIES_NUM];
	int jiffies[2][JIFFIES_NUM] = {0}, total_jiffies;
    char load_data_buf[MAX_LINE_LENGTH] = {0};
    char cpu_id[4] = {0};
	float cpu_usage_data = 0;
	FILE* stat_file;

	stat_file = fopen("/proc/stat", "r");
	    if(stat_file == NULL)
	    {
		fprintf(stderr, "cpu fopen() error %s\n", strerror(errno));
        	    fclose(stat_file);
		return cpu_usage_data;
	    }
	
	        fscanf(stat_file, "%s %d %d %d %d",
								cpu_id,
								&jiffies[ONE][USER],
								&jiffies[ONE][USER_NICE],
								&jiffies[ONE][SYSTEM],
								&jiffies[ONE][IDLE]);

	    for(idx = 0, total_jiffies = 0; idx < JIFFIES_NUM; ++idx)
        {
		        diff_jiffies[idx] = jiffies[ONE][idx] - jiffies[ZERO][idx];
		        total_jiffies = total_jiffies + diff_jiffies[idx];
        }   
	    cpu_usage_data = 100.0*(1.0-(diff_jiffies[IDLE] / (double)total_jiffies));

	    memcpy(jiffies[ZERO], jiffies[ONE], sizeof(int)*JIFFIES_NUM);
	    fclose(stat_file);
        
    return cpu_usage_data;
}


/**
 * Get memory usage (total, free, used)
 */
void
sys_usage_get_memory_usage(struct memory_info *memory)
{
	int i = 0;
        char buffer[128] = {0};
        char *token[128] = {NULL, };
	FILE *fp;

	memset (memory, 0x00, sizeof (struct memory_info));

	fp = fopen("/proc/meminfo", "r");
        if(fp == NULL)
        {
		fprintf(stderr, "memory fopen() error %s\n", strerror(errno));
            fclose(fp);
		return;
        }

        while(fgets(buffer, 128, fp) != NULL)
        {
            char *ptr = strtok(buffer, ":");

            while(ptr != NULL)
            {
                token[i] = ptr;
                i++;
                ptr = strtok(NULL, " ");
            }

		if(strcmp(token[0], "MemTotal") == 0)
			memory->memorytotal = atoi(token[1]);
            else if(strcmp(token[0], "MemFree") == 0)
			memory->memoryfree = atoi(token[1]);
        }
	memory->memoryused = memory->memorytotal - memory->memoryfree;

        fclose(fp);
	return;
}

int 
sys_usage_get_memory_total(void)
    {
	struct memory_info memory;

	sys_usage_get_memory_usage(&memory);
	return memory.memorytotal;
    }

int 
sys_usage_get_memory_free(void)
    {
	struct memory_info memory;
	
	sys_usage_get_memory_usage(&memory);
	return memory.memoryfree;
    }

int 
sys_usage_get_memory_used(void)
{
	struct memory_info memory;
	
	sys_usage_get_memory_usage(&memory);
	return memory.memoryused;
}

