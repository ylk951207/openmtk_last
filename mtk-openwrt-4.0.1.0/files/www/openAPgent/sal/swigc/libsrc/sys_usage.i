%module sys_usage
%{
extern float sys_usage_get_cpu_usage(void);
extern int sys_usage_get_memory_total(void);
extern int sys_usage_get_memory_free(void);
extern int sys_usage_get_memory_used(void);


%}
extern float sys_usage_get_cpu_usage(void);
extern int sys_usage_get_memory_total(void);
extern int sys_usage_get_memory_free(void);
extern int sys_usage_get_memory_used(void);


