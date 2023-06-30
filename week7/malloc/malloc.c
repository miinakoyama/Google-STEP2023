//
// >>>> malloc challenge! <<<<
//
// Your task is to improve utilization and speed of the following malloc
// implementation.
// Initial implementation is the same as the one implemented in simple_malloc.c.
// For the detailed explanation, please refer to simple_malloc.c.

#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//
// Interfaces to get memory pages from OS
//

void *mmap_from_system(size_t size); //メモリ割り当てるシステムコール
void munmap_to_system(void *ptr, size_t size); //メモリを解放するシステムコール

//
// Struct definitions
//

typedef struct my_metadata_t {
	size_t size;
	struct my_metadata_t *next;
} my_metadata_t;

typedef struct my_heap_t {
	my_metadata_t *free_head[5];
	my_metadata_t dummy[5];
} my_heap_t;

//
// Static variables (DO NOT ADD ANOTHER STATIC VARIABLES!)
//
my_heap_t my_heap; //free list bin

//
// Helper functions (feel free to add/remove/edit!)
//

//どこのbinに入っているのかを特定する
size_t get_index(size_t size)
{
	if (size <= 256)
		return ((size_t)0);
	if (256 < size && size <= 512)
		return ((size_t)1);
	if (512 < size && size <= 1024)
		return ((size_t)2);
	if (1024 < size && size <= 2048)
		return ((size_t)3);
	if (2048 < size && size <= 4096)
		return ((size_t)4);
}

//ここでmetadataを先頭に入れてる
void my_add_to_free_list(my_metadata_t *metadata) {
	assert(!metadata->next);
	size_t index = get_index(metadata->size);
	metadata->next = my_heap.free_head[get_index(metadata->size)];
	my_heap.free_head[index] = metadata;
}

void my_remove_from_free_list(my_metadata_t *metadata, my_metadata_t *prev) {
	if (prev) {
		prev->next = metadata->next;
	} else {
		size_t index = get_index(metadata->size);
		my_heap.free_head[index] = metadata->next;
	}
	metadata->next = NULL;
}

//
// Interfaces of malloc (DO NOT RENAME FOLLOWING FUNCTIONS!)
//

// This is called at the beginning of each challenge.
void my_initialize() {
	int i = 0;
	while (i < 5)
	{
		my_heap.free_head[i] = &my_heap.dummy[i];
		my_heap.dummy[i].size = 0;
		my_heap.dummy[i].next = NULL;
		i++;
	}
}

// my_malloc() is called every time an object is allocated.
// |size| is guaranteed to be a multiple of 8 bytes and meets 8 <= |size| <=
// 4000. You are not allowed to use any library functions other than
// mmap_from_system() / munmap_to_system().
void *my_malloc(size_t size) {
	size_t index = get_index(size);
	my_metadata_t *metadata = my_heap.free_head[index];
	my_metadata_t *prev = NULL;
	// First-fit: Find the first free slot the object fits.
	// TODO: Update this logic to Best-fit!

	while (index < 5)
	{
		metadata = my_heap.free_head[index];
		prev = NULL;
		while (metadata && metadata->size < size)
		{
			prev = metadata;
			metadata = metadata->next;
		}
		index++;
	}
	// now, metadata points to the first free slot
	// and prev is the previous entry.

	// best-fit
	my_metadata_t *best_metadata = metadata; //fitst-fitで見つけたやつをとりあえずbestにしておく
	my_metadata_t *best_prev = prev;
	// first-fitの次のやつがあったらそこから見る
	if (metadata)
	{
		prev = metadata;
		metadata = metadata->next;
	}
	while (metadata)
	{
		// 確保したいサイズ以上でかつ既存のbestよりもフィットしている(サイズ差が小さい)時はbestを更新する
		if (metadata->size >= size && (best_metadata->size - size) > (metadata->size - size))
		{
			best_metadata = metadata;
			best_prev = prev;
		}
		prev = metadata;
		metadata = metadata->next;
	}
	metadata = best_metadata;
	prev = best_prev;


/*
	//worst-fit(ほとんどbest-fitと同じ)
	my_metadata_t *worst_metadata = metadata; //fitst-fitで見つけたやつをとりあえずworstにしておく
	my_metadata_t *worst_prev = prev;
	if (metadata)
	{
		prev = metadata;
		metadata = metadata->next;
	}
	while (metadata)
	{
		//確保したいサイズ以上でかつ既存のworseよりもさらにfitしていない(サイズ差が大きい)時はworstを更新する
		if (metadata->size > size && (worst_metadata->size - size) < (metadata->size - size))
		{
			worst_metadata = metadata;
			worst_prev = prev;
		}
		prev = metadata;
		metadata = metadata->next;
	}
	metadata = worst_metadata;
	prev = worst_prev;
*/


	if (!metadata) {
		// There was no free slot available. We need to request a new memory region
		// from the system by calling mmap_from_system().
		//
		//     | metadata | free slot |
		//     ^
		//     metadata
		//     <---------------------->
		//            buffer_size
		size_t buffer_size = 4096;
		my_metadata_t *metadata = (my_metadata_t *)mmap_from_system(buffer_size);
		metadata->size = buffer_size - sizeof(my_metadata_t);
		metadata->next = NULL;
		// Add the memory region to the free list.
		my_add_to_free_list(metadata);
		// Now, try my_malloc() again. This should succeed.
		return my_malloc(size);
	}

	// |ptr| is the beginning of the allocated object.
	//
	// ... | metadata | object | ...
	//     ^          ^
	//     metadata   ptr
	void *ptr = metadata + 1;
	size_t remaining_size = metadata->size - size;
	// Remove the free slot from the free list.
	my_remove_from_free_list(metadata, prev);

	if (remaining_size > sizeof(my_metadata_t)) {
		// Shrink the metadata for the allocated object
		// to separate the rest of the region corresponding to remaining_size.
		// If the remaining_size is not large enough to make a new metadata,
		// this code path will not be taken and the region will be managed
		// as a part of the allocated object.
		metadata->size = size;
		// Create a new metadata for the remaining free slot.
		//
		// ... | metadata | object | metadata | free slot | ...
		//     ^          ^        ^
		//     metadata   ptr      new_metadata
		//                 <------><---------------------->
		//                   size       remaining size
		my_metadata_t *new_metadata = (my_metadata_t *)((char *)ptr + size);
		new_metadata->size = remaining_size - sizeof(my_metadata_t);
		new_metadata->next = NULL;
		// Add the remaining free slot to the free list.
		my_add_to_free_list(new_metadata);
	}
	return ptr;
}

// This is called every time an object is freed.  You are not allowed to
// use any library functions other than mmap_from_system / munmap_to_system.
void my_free(void *ptr) {
	// Look up the metadata. The metadata is placed just prior to the object.
	//
	// ... | metadata | object | ...
	//     ^          ^
	//     metadata   ptr
	my_metadata_t *metadata = (my_metadata_t *)ptr - 1;
	// Add the free slot to the free list.
	my_add_to_free_list(metadata);
}

// This is called at the end of each challenge.
void my_finalize() {
	// Nothing is here for now.
	// feel free to add something if you want!
}

void test() {
	// Implement here!
	assert(1 == 1); /* 1 is 1. That's always true! (You can remove this.) */
}
