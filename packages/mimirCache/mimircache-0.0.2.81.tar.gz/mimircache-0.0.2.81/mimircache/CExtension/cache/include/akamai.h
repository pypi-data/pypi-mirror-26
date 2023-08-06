//
//  akamai.h
//  mimircache
//
//  Created by Juncheng on 6/2/16.
//  Copyright © 2016 Juncheng. All rights reserved.
//

#ifndef akamai_h
#define akamai_h


#include "LRU.h"
#include "LFU.h"
#include "LFUFast.h"
#include "cache.h"


#ifdef __cplusplus
extern "C"
{
#endif
    
    
#define LRU_SEG_SIZE 10000
    
    struct akamai_params{
        gint64 lru_size;
        gint64 lfu_size;
        
        struct_cache *lru;
        struct_cache *lfu;
        
        gint64 ts;              // this only works when add_element is called
    };
    
    typedef struct akamai_params akamai_params_t;
    
    
    
    
    extern gboolean akamai_check_element(struct_cache* cache, cache_line* cp);
    extern gboolean akamai_add_element(struct_cache* cache, cache_line* cp);
    
    
    extern void     __akamai_insert_element(struct_cache* akamai, cache_line* cp);
    extern void     __akamai_update_element(struct_cache* akamai, cache_line* cp);
    extern void     __akamai_evict_element(struct_cache* akamai, cache_line* cp);
    
    
    extern void     akamai_destroy(struct_cache* cache);
    extern void     akamai_destroy_unique(struct_cache* cache);
    
    
    struct_cache*   akamai_init(guint64 size, char data_type, int block_size, void* params);
    
    gint64 akamai_get_size(struct_cache* cache);
    
    
    
#ifdef __cplusplus
}
#endif


#endif	/* akamai_H */
