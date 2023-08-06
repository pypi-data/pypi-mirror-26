//
//  new2.h
//  mimircache
//
//  Created by Juncheng on 6/2/16.
//  Copyright © 2016 Juncheng. All rights reserved.
//


#include "new2.h"

#ifdef __cplusplus
extern "C"
{
#endif


void __new2_insert_element(struct_cache* new2, cache_line* cp){
    struct new2_params* new2_params = (struct new2_params*)(new2->cache_params);
    
    gpointer key;
    if (cp->type == 'l'){
        key = (gpointer)g_new(guint64, 1);
        *(guint64*)key = *(guint64*)(cp->item_p);
    }
    else{
        key = (gpointer)g_strdup((gchar*)(cp->item_p));
    }
    
    GList* node = g_list_alloc();
    node->data = key;
    
    
    g_queue_push_tail_link(new2_params->list, node);
    g_hash_table_insert(new2_params->hashtable, (gpointer)key, (gpointer)node);
    
}

gboolean new2_check_element(struct_cache* cache, cache_line* cp){
    struct new2_params* new2_params = (struct new2_params*)(cache->cache_params);
    return g_hash_table_contains( new2_params->hashtable, cp->item_p );
}


void __new2_update_element(struct_cache* cache, cache_line* cp){
    struct new2_params* new2_params = (struct new2_params*)(cache->cache_params);
    GList* node = (GList* ) g_hash_table_lookup(new2_params->hashtable, cp->item_p);
    g_queue_unlink(new2_params->list, node);
    g_queue_push_tail_link(new2_params->list, node);
}


void __new2_evict_element(struct_cache* new2, cache_line* cp){
    struct new2_params* new2_params = (struct new2_params*)(new2->cache_params);

    if (new2->core->cache_debug_level == 2){     // compare to Oracle
        while (new2_params->ts > (gint64) g_array_index(new2->core->bp->array, guint64, new2->core->bp_pos)){
            if ( (long) g_array_index(new2->core->bp->array, guint64, new2->core->bp_pos) -
                (long) g_array_index(new2->core->bp->array, guint64, new2->core->bp_pos-1) != 0 ){
                
                new2->core->evict_err_array[new2->core->bp_pos-1] = new2->core->evict_err /
                    (g_array_index(new2->core->bp->array, guint64, new2->core->bp_pos) -
                        g_array_index(new2->core->bp->array, guint64, new2->core->bp_pos-1));
                new2->core->evict_err = 0;
            }
            else
                new2->core->evict_err_array[new2->core->bp_pos-1] = 0;
            
            new2->core->evict_err = 0;
            new2->core->bp_pos++;
        }
        
        if (new2_params->ts == (long) g_array_index(new2->core->bp->array, guint64, new2->core->bp_pos)){
            new2->core->evict_err_array[new2->core->bp_pos-1] = (double)new2->core->evict_err /
            (g_array_index(new2->core->bp->array, guint64, new2->core->bp_pos) -
             g_array_index(new2->core->bp->array, guint64, new2->core->bp_pos-1));
            new2->core->evict_err = 0;
            new2->core->bp_pos ++;
        }
            
        gpointer data = g_queue_peek_head(new2_params->list);
        if (cp->type == 'l'){
            if (*(guint64*)(data) != ((guint64*)new2->core->oracle)[new2_params->ts]){
                printf("error at %lu, new2: %lu, Optimal: %lu\n", new2_params->ts,
                       *(guint64*)(data), ((guint64*)new2->core->oracle)[new2_params->ts]);
                new2->core->evict_err ++;
            }
            else
                printf("no error at %lu: %lu, %lu\n", new2_params->ts, *(guint64*)(data),
                       *(guint64*)(g_queue_peek_tail(new2_params->list)));
            gpointer data_oracle = g_hash_table_lookup(new2_params->hashtable,
                                        (gpointer)&((guint64* )new2->core->oracle)[new2_params->ts]);
            g_queue_delete_link(new2_params->list, (GList*)data_oracle);
            g_hash_table_remove(new2_params->hashtable, (gpointer)&((guint64*)new2->core->oracle)[new2_params->ts]);
        }
        else{
            if (strcmp((gchar*)data, ((gchar**)(new2->core->oracle))[new2_params->ts]) != 0)
                new2->core->evict_err ++;
            gpointer data_oracle = g_hash_table_lookup(new2_params->hashtable,
                                                       (gpointer)((gchar**)new2->core->oracle)[new2_params->ts]);
            g_hash_table_remove(new2_params->hashtable,
                                (gpointer)((gchar**)new2->core->oracle)[new2_params->ts]);
            g_queue_remove(new2_params->list, ((GList*) data_oracle)->data);
        }
        
    }
    
    else if (new2->core->cache_debug_level == 1){
        // record eviction list
        
        gpointer data = g_queue_pop_head(new2_params->list);
        if (cp->type == 'l'){
            ((guint64*)(new2->core->eviction_array))[new2_params->ts] = *(guint64*)(data);
        }
        else{
            gchar* key = g_strdup((gchar*)(data));
            ((gchar**)(new2->core->eviction_array))[new2_params->ts] = key;
        }

        g_hash_table_remove(new2_params->hashtable, (gconstpointer)data);
    }

    
    else{
        gpointer data = g_queue_pop_head(new2_params->list);
        g_hash_table_remove(new2_params->hashtable, (gconstpointer)data);
    }
}


gpointer __new2__evict_with_return(struct_cache* new2, cache_line* cp){
    /** evict one element and return the evicted element, 
     * needs to free the memory of returned data 
     */
    
    struct new2_params* new2_params = (struct new2_params*)(new2->cache_params);
    
    gpointer data = g_queue_pop_head(new2_params->list);
    
    gpointer evicted_key;
    if (cp->type == 'l'){
        evicted_key = (gpointer)g_new(guint64, 1);
        *(guint64*)evicted_key = *(guint64*)(data);
    }
    else{
        evicted_key = (gpointer)g_strdup((gchar*)data);
    }

    g_hash_table_remove(new2_params->hashtable, (gconstpointer)data);
    return evicted_key;
}




gboolean new2_add_element(struct_cache* cache, cache_line* cp){
    struct new2_params* new2_params = (struct new2_params*)(cache->cache_params);
    if (new2_check_element(cache, cp)){
        __new2_update_element(cache, cp);
        new2_params->ts ++;
        return TRUE;
    }
    else{
        __new2_insert_element(cache, cp);
        if ((long)g_hash_table_size(new2_params->hashtable) > cache->core->size)
            __new2_evict_element(cache, cp);
        new2_params->ts ++;
        return FALSE;
    }
}


gboolean new2_add_element_only(struct_cache* cache, cache_line* cp){
    struct new2_params* new2_params = (struct new2_params*)(cache->cache_params);
    if (new2_check_element(cache, cp)){
        __new2_update_element(cache, cp);
        return TRUE;
    }
    else{
        __new2_insert_element(cache, cp);
        while ((long)g_hash_table_size(new2_params->hashtable) > cache->core->size)
            __new2_evict_element(cache, cp);
        return FALSE;
    }
}


gboolean new2_add_element_withsize(struct_cache* cache, cache_line* cp){
    int i;
    gboolean ret_val;
    
    *(gint64*)(cp->item_p) = (gint64) (*(gint64*)(cp->item_p) *
                                       cp->disk_sector_size /
                                       cache->core->block_unit_size);
    ret_val = new2_add_element(cache, cp);
    
    int n = (int)ceil((double) cp->size/cache->core->block_unit_size);
    
    for (i=0; i<n-1; i++){
        (*(guint64*)(cp->item_p)) ++;
        new2_add_element_only(cache, cp);
    }
    *(gint64*)(cp->item_p) -= (n-1);
    return ret_val;
}





void new2_destroy(struct_cache* cache){
    struct new2_params* new2_params = (struct new2_params*)(cache->cache_params);

//    g_queue_free(new2_params->list);                 // Jason: should call g_queue_free_full to free the memory of node content
    // 0921
    g_queue_free(new2_params->list);
    g_hash_table_destroy(new2_params->hashtable);
    cache_destroy(cache);
}

void new2_destroy_unique(struct_cache* cache){
    /* the difference between destroy_unique and destroy
     is that the former one only free the resources that are
     unique to the cache, freeing these resources won't affect
     other caches copied from original cache
     in Optimal, next_access should not be freed in destroy_unique,
     because it is shared between different caches copied from the original one.
     */
    
    new2_destroy(cache);
}


/*-----------------------------------------------------------------------------
 *
 * new2_init --
 *      initialize a new2 cache
 *
 * Input: 
 *      size:       cache size
 *      data_type:  the type of data, currently support l for long or c for string
 *      block_size: the basic unit size of block, used for profiling with size
 *                  if not profiling with size, this is 0
 *      params:     params used for initialization, NULL for new2 
 *
 * Return:
 *      a new2 cache struct
 *
 *-----------------------------------------------------------------------------
 */
struct_cache* new2_init(guint64 size, char data_type, int block_size, void* params){
    struct_cache *cache = cache_init(size, data_type, block_size);
    cache->cache_params = g_new0(struct new2_params, 1);
    struct new2_params* new2_params = (struct new2_params*)(cache->cache_params);
    
    cache->core->type                   =   e_new2;
    cache->core->cache_init             =   new2_init;
    cache->core->destroy                =   new2_destroy;
    cache->core->destroy_unique         =   new2_destroy_unique;
    cache->core->add_element            =   new2_add_element;
    cache->core->check_element          =   new2_check_element;
    cache->core->__insert_element       =   __new2_insert_element;
    cache->core->__update_element       =   __new2_update_element;
    cache->core->__evict_element        =   __new2_evict_element;
    cache->core->__evict_with_return    =   __new2__evict_with_return;
    cache->core->get_size               =   new2_get_size;
    cache->core->remove_element         =   new2_remove_element; 
    cache->core->cache_init_params      =   NULL;
    cache->core->add_element_only       =   new2_add_element_only; 
    cache->core->add_element_withsize   =   new2_add_element_withsize;
    

    if (data_type == 'l'){
        new2_params->hashtable = g_hash_table_new_full(g_int64_hash, g_int64_equal,
                                                      simple_g_key_value_destroyer, NULL);
    }
    else if (data_type == 'c'){
        new2_params->hashtable = g_hash_table_new_full(g_str_hash, g_str_equal,
                                                      simple_g_key_value_destroyer, NULL);
    }
    else{
        ERROR("does not support given data type: %c\n", data_type);
    }
    new2_params->list = g_queue_new();
    
    
    return cache;
}




void new2_remove_element(struct_cache* cache, void* data_to_remove){
    struct new2_params* new2_params = (struct new2_params*)(cache->cache_params);
    
    gpointer data = g_hash_table_lookup(new2_params->hashtable, data_to_remove);
    if (!data){
        fprintf(stderr, "new2_remove_element: data to remove is not in the cache\n");
        exit(1);
    }
    g_queue_delete_link(new2_params->list, (GList*) data);
    g_hash_table_remove(new2_params->hashtable, data_to_remove);
}

gint64 new2_get_size(struct_cache* cache){
    struct new2_params* new2_params = (struct new2_params*)(cache->cache_params);
    return (guint64) g_hash_table_size(new2_params->hashtable);
}






#ifdef __cplusplus
}
#endif
