//
//  new2.h
//  mimircache
//
//  Created by Juncheng on 6/2/16.
//  Copyright © 2016 Juncheng. All rights reserved.
//

#ifndef new2_h
#define new2_h


#include "cache.h" 


#ifdef __cplusplus
extern "C"
{
#endif


struct new2_params{
    GHashTable *hashtable;
    GQueue *list;
    gint64 ts;              // this only works when add_element is called 
};

typedef struct new2_params new2_params_t; 




extern gboolean new2_check_element(struct_cache* cache, cache_line* cp);
extern gboolean new2_add_element(struct_cache* cache, cache_line* cp);


extern void     __new2_insert_element(struct_cache* new2, cache_line* cp);
extern void     __new2_update_element(struct_cache* new2, cache_line* cp);
extern void     __new2_evict_element(struct_cache* new2, cache_line* cp);
extern void*    __new2__evict_with_return(struct_cache* new2, cache_line* cp);


extern void     new2_destroy(struct_cache* cache);
extern void     new2_destroy_unique(struct_cache* cache);


struct_cache*   new2_init(guint64 size, char data_type, int block_size, void* params);


extern void     new2_remove_element(struct_cache* cache, void* data_to_remove);
extern gint64 new2_get_size(struct_cache* cache);


#ifdef __cplusplus
}
#endif


#endif	/* new2_H */
