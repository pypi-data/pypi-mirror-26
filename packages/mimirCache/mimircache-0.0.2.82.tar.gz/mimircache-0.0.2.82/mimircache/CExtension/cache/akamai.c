//
//  akamai.h
//  mimircache
//
//  Created by Juncheng on 10/6/17.
//  Copyright © 2017 Juncheng. All rights reserved.
//


#include "akamai.h"

#ifdef __cplusplus
extern "C"
{
#endif


void __akamai_insert_element(struct_cache* akamai, cache_line* cp){
    // this funciton includes eviction
    
    akamai_params_t* akamai_params = (struct akamai_params*)(akamai->cache_params);
    
    __LRU_insert_element(akamai_params->lru, cp);
    if (LRU_get_size(akamai_params->lru) > akamai_params->lru_size){
        // evict one and add to LFU (if exists)
        gpointer gp = __LRU__evict_with_return(akamai_params->lru, cp);
        if (akamai_params->lfu){
            gpointer old_cp_content = cp->item_p;
            cp->item_p = gp;
            akamai_params->lfu->core->add_element(akamai_params->lfu, cp);
            cp->item_p = old_cp_content;
        }
        g_free(gp);
    }
}

gboolean akamai_check_element(struct_cache* cache, cache_line* cp){
    struct akamai_params* akamai_params = (struct akamai_params*)(cache->cache_params);
    gboolean in_lru = akamai_params->lru->core->check_element(akamai_params->lru, cp);
    if (!in_lru)
        if (akamai_params->lfu)
            return akamai_params->lfu->core->check_element(akamai_params->lfu, cp);
        else
            return FALSE;
    else
        return TRUE;
}


void __akamai_update_element(struct_cache* cache, cache_line* cp){
    
    // TODO: Do we update LFU on each req or only when it is evicted from LRU?
    // Currently only when it is evicted and freq is cleared when evicted
    
    struct akamai_params* akamai_params = (struct akamai_params*)(cache->cache_params);
    if (akamai_params->lru->core->check_element(akamai_params->lru, cp)){
        akamai_params->lru->core->__update_element(akamai_params->lru, cp);
    }
    else if (akamai_params->lfu && akamai_params->lfu->core->check_element(akamai_params->lfu, cp)){
        akamai_params->lfu->core->__update_element(akamai_params->lfu, cp);
    }
    else{
        ERROR("update element, but not in LRU nor LFU\n");
        abort();
    }
}


void __akamai_evict_element(struct_cache* akamai, cache_line* cp){
//    struct akamai_params* akamai_params = (struct akamai_params*)(akamai->cache_params);

    ERROR("this should not be used\n");
    abort();
}




gboolean akamai_add_element(struct_cache* cache, cache_line* cp){
    struct akamai_params* akamai_params = (struct akamai_params*)(cache->cache_params);
    if (akamai_check_element(cache, cp)){
        __akamai_update_element(cache, cp);
        akamai_params->ts ++;
        return TRUE;
    }
    else{
        __akamai_insert_element(cache, cp);
        akamai_params->ts ++;
        return FALSE;
    }
}





void akamai_destroy(struct_cache* cache){
    struct akamai_params* akamai_params = (struct akamai_params*)(cache->cache_params);
    akamai_params->lru->core->destroy(akamai_params->lru);
    if (akamai_params->lfu)
        akamai_params->lfu->core->destroy(akamai_params->lfu);
    cache_destroy(cache);
}

void akamai_destroy_unique(struct_cache* cache){
    /* the difference between destroy_unique and destroy
     is that the former one only free the resources that are
     unique to the cache, freeing these resources won't affect
     other caches copied from original cache
     in Optimal, next_access should not be freed in destroy_unique,
     because it is shared between different caches copied from the original one.
     */
    
    akamai_destroy(cache);
}


/*-----------------------------------------------------------------------------
 *
 * akamai_init --
 *      initialize a akamai cache
 *
 * Input: 
 *      size:       cache size
 *      data_type:  the type of data, currently support l for long or c for string
 *      block_size: the basic unit size of block, used for profiling with size
 *                  if not profiling with size, this is 0
 *      params:     params used for initialization, NULL for akamai 
 *
 * Return:
 *      a akamai cache struct
 *
 *-----------------------------------------------------------------------------
 */
struct_cache* akamai_init(guint64 size, char data_type, int block_size, void* params){
    struct_cache *cache = cache_init(size, data_type, block_size);
    cache->cache_params = g_new0(struct akamai_params, 1);
    struct akamai_params* akamai_params = (struct akamai_params*)(cache->cache_params);
    
    if ((gint64) size >= LRU_SEG_SIZE ){
        akamai_params->lru_size = LRU_SEG_SIZE + (long) ((size - LRU_SEG_SIZE) * 0.2);
        akamai_params->lfu_size = size - akamai_params->lru_size;
//        akamai_params->lfu = LFU_init(akamai_params->lfu_size, data_type, block_size, params);
        akamai_params->lfu = LFU_fast_init(akamai_params->lfu_size, data_type, block_size, params);
    }
    else {
        akamai_params->lru_size = size;
        akamai_params->lfu_size = 0;
        akamai_params->lfu = NULL;
    }
    
    akamai_params->lru = LRU_init(akamai_params->lru_size, data_type, block_size, params);
    
    cache->core->type                   =   e_akamai;
    cache->core->cache_init             =   akamai_init;
    cache->core->destroy                =   akamai_destroy;
    cache->core->destroy_unique         =   akamai_destroy_unique;
    cache->core->add_element            =   akamai_add_element;
    cache->core->check_element          =   akamai_check_element;
    cache->core->__insert_element       =   __akamai_insert_element;
    cache->core->__update_element       =   __akamai_update_element;
    cache->core->__evict_element        =   __akamai_evict_element;
    cache->core->__evict_with_return    =   NULL;
    cache->core->get_size               =   akamai_get_size;
//    cache->core->remove_element         =   akamai_remove_element;
    cache->core->cache_init_params      =   NULL;
    

    return cache;
}



//
//void akamai_remove_element(struct_cache* cache, void* data_to_remove){
//    struct akamai_params* akamai_params = (struct akamai_params*)(cache->cache_params);
//    
//    gpointer data = g_hash_table_lookup(akamai_params->hashtable, data_to_remove);
//    if (!data){
//        fprintf(stderr, "akamai_remove_element: data to remove is not in the cache\n");
//        exit(1);
//    }
//    g_queue_delete_link(akamai_params->list, (GList*) data);
//    g_hash_table_remove(akamai_params->hashtable, data_to_remove);
//}

gint64 akamai_get_size(struct_cache* cache){
    struct akamai_params* akamai_params = (struct akamai_params*)(cache->cache_params);
    return akamai_params->lru->core->get_size(akamai_params->lru) +
                akamai_params->lfu->core->get_size(akamai_params->lfu);
}






#ifdef __cplusplus
}
#endif
