#ifndef __NODE_H__
#define __NODE_H__

/* The following code defines a doubley linked list, it is doubley linked 
   so deletions and insertions in the beginning could happen in O(1)
   the structure will be used to define the clusters, each cluster will be
   a doubly linked list of all the vectors that are in him, the clusters
   strucure, will be an array of linked lists */

struct Node
{  
    vector x;
    struct Node* next;  
    struct Node* prev;  
}; 
               
static void insert_first(struct Node** head, vector new_x)
{  
    struct Node* new_node = (struct Node*)malloc(sizeof(struct Node));  
    CHECK_ALLOC(new_node);
  
    new_node->x = new_x;
    new_node->next = (*head);  
    new_node->prev = NULL;  
  
    if ((*head) != NULL)
        (*head)->prev = new_node;                                            
    
    (*head) = new_node;  
}

static void delete_node(struct Node** head, struct Node* x)
{
	
	if (x->prev == NULL && x->next == NULL) {
		*head = NULL;
	}
    else if (x->prev == NULL)
    {
        (*head) = x->next;
        (*head)->prev = NULL;
    }
    else if (x->next == NULL)
    {
        x->prev->next = NULL;
    }
    else 
    {
        x->next->prev = x->prev;
        x->prev->next = x->next;
    }
    free(x);
}

static void free_list(struct Node** head, int K)
{
    int i;
    for(i = 0; i < K; i++)
    {
	    struct Node* curr = head[i];
	    while(curr != NULL)
	    {
		    struct Node* next = curr->next;
                    free(curr->x);
                    free(curr);
		    curr = next;
	    }
    }
    free(head);
}

#endif