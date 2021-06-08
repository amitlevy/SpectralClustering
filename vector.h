#ifndef __VECTOR_H__
#define __VECTOR_H__

#define EPSILON 0.0001

/* The following code is related to a structure called vector
   in our case it is a d-long array of doubles */
   
typedef double * vector;

 
static vector vector_new(int d)
{
    vector vec = calloc(d, sizeof(double));
	CHECK_ALLOC(vec);
    return vec;
}

static void vector_add(vector x, vector y, int d)
{
    int i;
    for(i = 0; i < d; i++)
    {
        x[i] += y[i];
    }
}

static bool vector_equals(vector x, vector y, int d)
{
    int i;
    for(i = 0; i < d; i++)
    {
        if((x[i] - y[i]) >= EPSILON || (x[i] - y[i]) <= -EPSILON)
            return false;
    }
    return true;
}

#endif