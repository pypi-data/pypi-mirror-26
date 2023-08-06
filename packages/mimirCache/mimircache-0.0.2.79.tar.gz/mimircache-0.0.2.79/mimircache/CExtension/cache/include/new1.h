//
//  new1.h
//  mimircache
//
//  Created by Juncheng on 6/2/16.
//  Copyright © 2016 Juncheng. All rights reserved.
//

#ifndef new1_h
#define new1_h


#include "cache.h" 


#ifdef __cplusplus
extern "C"
{
#endif


struct new1_params{
    GHashTable *hashtable;
    GQueue *list;
    gint64 ts;              // this only works when add_element is called 
};

typedef struct new1_params new1_params_t; 




extern gboolean new1_check_element(struct_cache* cache, cache_line* cp);
extern gboolean new1_add_element(struct_cache* cache, cache_line* cp);


extern void     __new1_insert_element(struct_cache* new1, cache_line* cp);
extern void     __new1_update_element(struct_cache* new1, cache_line* cp);
extern void     __new1_evict_element(struct_cache* new1, cache_line* cp);
extern void*    __new1__evict_with_return(struct_cache* new1, cache_line* cp);


extern void     new1_destroy(struct_cache* cache);
extern void     new1_destroy_unique(struct_cache* cache);


struct_cache*   new1_init(guint64 size, char data_type, int block_size, void* params);


extern void     new1_remove_element(struct_cache* cache, void* data_to_remove);
extern gint64 new1_get_size(struct_cache* cache);


#ifdef __cplusplus
}
#endif


#endif	/* new1_H */
