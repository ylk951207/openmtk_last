#include <stdio.h>
#include <string.h>

#define MAX_LINE_LENGTH 80
#define ZERO 0
#define ONE 1
#define JIFFIES_NUM 4

enum jiffy{USER, USER_NICE, SYSTEM, IDLE} jiffy_enum;

float cpu_usage(void)
{
    char load_data_buf[MAX_LINE_LENGTH] = {0};
    char cpu_id[4] = {0};

    int jiffies[2][JIFFIES_NUM] = {0}, total_jiffies;
    int diff_jiffies[JIFFIES_NUM];
    int idx;
    double cpu_usage_data;
    int j = 0;

//    while(1)
    while(j < 2)
    {
	    FILE* stat_file = fopen("/proc/stat", "r");
	    if(stat_file == NULL)
	    {
        	    fprintf(stderr, "cpu file open error\n");
        	    fclose(stat_file);
	    }
	        fscanf(stat_file, "%s %d %d %d %d",
	            cpu_id, &jiffies[ONE][USER], &jiffies[ONE][USER_NICE],
	            &jiffies[ONE][SYSTEM], &jiffies[ONE][IDLE]);
	    if(stat_file == NULL)
	    {
	            fprintf(stderr, "cpu file scan error\n");
	            fclose(stat_file);
	    }

	    for(idx = 0, total_jiffies = 0; idx < JIFFIES_NUM; ++idx)
        {
		        diff_jiffies[idx] = jiffies[ONE][idx] - jiffies[ZERO][idx];
		        total_jiffies = total_jiffies + diff_jiffies[idx];
        }   
	    cpu_usage_data = 100.0*(1.0-(diff_jiffies[IDLE] / (double)total_jiffies));
//	    printf("Cpu usage : %f%%\n",cpu_usage_data);

	    memcpy(jiffies[ZERO], jiffies[ONE], sizeof(int)*JIFFIES_NUM);
	    fclose(stat_file);
        //sleep(1);
	    j++;
    }
    return cpu_usage_data;
}
/*------------------------------------------------------------------------*/

struct memory_info
{
    int memorytotal;
    int memoryfree;
    int memoryused;
};

struct memory_info memory_usage()
{
        struct memory_info memory;
        char buffer[128] = {0};
        char *token[128] = {NULL, };
        int i = 0;

        /* */
        FILE *fp = fopen("/proc/meminfo", "r");
        if(fp == NULL)
        {
            fprintf(stderr, "memory file open error\n");
            fclose(fp);
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
            memory.memorytotal = atoi(token[1]);

            else if(strcmp(token[0], "MemFree") == 0)
            memory.memoryfree = atoi(token[1]);

        }
        memory.memoryused = memory.memorytotal - memory.memoryfree;

        fclose(fp);
        return memory;
}

    int memory_total(void)
    {
            struct memory_info result;
            result = memory_usage();
//            printf("memorytotal : %d\n", result.memorytotal);
            return result.memorytotal;
    }

    int memory_free(void)
    {
            struct memory_info result;
            result = memory_usage();
//            printf("memoryfree : %d\n", result.memoryfree);
            return result.memoryfree;
    }

    int memory_used(void)
    {
            struct memory_info result;
            result = memory_usage();
//            printf("memoryused : %d\n", result.memoryused);
            return result.memoryused;
    }

//#if 0
int main(void)
{
        memory_total();
        memory_free();
        memory_used();
        cpu_usage();
}
//#endif

