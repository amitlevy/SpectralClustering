#ifndef __AUX_ALGO_H__
#define __AUX_ALGO_H__

/* The folllowing code is the algorithmic functions that will be used in the
   final "main" function */

static vector cluster_mean(struct Node** head, int d)
{   
    vector sum = vector_new(d);
    int size = 0;
    struct Node* temp = (*head);
    int i;
    while (temp != NULL)
    {
        size += 1;
        vector_add(sum, temp->x, d);
        temp = temp->next;
    }
    for (i = 0; i < d; i++)
    {
        CHECK_DIV_ZERO(size);
		sum[i] /= size;
    }
    return sum;
}

static double compute_norm(vector x, vector mu, int d)
{
    double norm = 0;
    int i;
    for(i = 0; i < d; i++)
    {
        norm += (x[i] - mu[i])*(x[i] - mu[i]);
    }
    return norm;
}

/* arr is a two dimensional array of size d*K
   it is an array of the mu's */

static int find_cluster(vector x, vector *arr, int d, int K)
{
    double minNorm = compute_norm(x, arr[0], d);
    int ind = 0;
    int i;
    double norm;
    for(i = 1; i < K; i++)
    {
        norm = compute_norm(x, arr[i], d);
        if(norm < minNorm)
        {
            minNorm = norm;
            ind = i;
        }
    }
    return ind;
}

/* The function updates the mu values in mus array, and returns true if
   at least one of the mus has changed since the last iteration */

static bool update_mus(vector *arr, struct Node** S, int d, int K)
{
    bool hasChanged = false;
    vector mu;
    int i;
    for(i = 0; i < K; i++)
    {
        mu = cluster_mean(&(S[i]), d);
		if(!vector_equals(mu, arr[i], d)) {
           hasChanged = true;
		}
        free(arr[i]);
        arr[i] = mu;
    }
    return hasChanged;
}

static vector array_to_vector(double *arr,int d)
{
    int j;
    vector mu = vector_new(d);
    for(j = 0; j < d; j++)
    {
        mu[j] =  arr[j];
    }
    return mu;
}

#endif