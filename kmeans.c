#define PY_SSIZE_T_CLEAN
#include <Python.h>

typedef int bool;
#define false 0
#define true 1

#define CHECK_ALLOC(PTR) \
do { \
   if (!(PTR)) { \
	   fprintf(stderr, "FATAL: Allocation failed at %s:%d\n", __FILE__, __LINE__); \
	   fflush(stderr); \
	   exit(1); \
   } \
} while (0)
	
#define CHECK_DIV_ZERO(VAL) \
do { \
   if (VAL == 0) { \
	   fprintf(stderr, "FATAL: devision by zero at %s:%d\n", __FILE__, __LINE__); \
	   fflush(stderr); \
	   exit(1); \
   } \
} while (0)

#include "vector.h"
#include "node.h"
#include "aux_algo.h"

static PyObject* ckmeansMain(PyObject *self, PyObject *args) // was main
{

	int K; 
	int N;
    int d;
    int MAX_iter;
    PyObject *_initialMus, *_observations;
    PyObject *item;
    PyObject *innerItem;

    int i,j;

    if (!PyArg_ParseTuple(args, "iiiiOO", &K, &N, &d, &MAX_iter,&_observations, &_initialMus)){
        return NULL;
    }

    if (!PyList_Check(_initialMus) || !PyList_Check(_observations))
    {
        return NULL;
    }

    double **c_initialMus = (double **)malloc(sizeof(double *) * K);
    for (i = 0; i < K; i++)
    {
        c_initialMus[i] =(double *)malloc(d * sizeof(double));
    }

    double **c_observations = (double **)malloc(sizeof(double *) * N);
    for (i = 0; i < N; i++)
    {
        c_observations[i] =(double *)malloc(d * sizeof(double));
    }

    for (i = 0; i < K; i++)
    {
        item = PyList_GetItem(_initialMus, i);
        for (j = 0; j < d; j++) {
            innerItem = PyList_GetItem(item,j);
            c_initialMus[i][j] = PyFloat_AsDouble(innerItem);
        }
    }

    for (i = 0; i < N; i++)
    {
        item = PyList_GetItem(_observations, i);
        for (j = 0; j < d; j++) {
            innerItem = PyList_GetItem(item,j);
            c_observations[i][j] = PyFloat_AsDouble(innerItem);
        }
    }

    vector *mus = calloc(K, sizeof(vector));
    struct Node** clusters = calloc(K, sizeof(struct Node*));
    int iter = 1;
    bool toContinue;


    CHECK_ALLOC(mus);
    CHECK_ALLOC(clusters);

    for(i = 0; i < K; i++)
    {
        mus[i] = array_to_vector(c_initialMus[i],d);
    }

    for(i = 0; i < N; i++) 
    {
        vector x = array_to_vector(c_observations[i],d);
        int ind = find_cluster(x, mus, d, K);
		insert_first(&clusters[ind], x);
    }

    toContinue = update_mus(mus, clusters, d, K);
    while(iter <= MAX_iter && toContinue)
    {
        for(i = 0; i < K; i++)
        {
            struct Node* curr = clusters[i];
            while(curr != NULL)
            {
                int ind = find_cluster(curr->x, mus, d, K);
                struct Node* next = curr->next;

                if(ind != i)
                {
                    insert_first(&clusters[ind], curr->x);
                    delete_node(&clusters[i], curr);
                }
				curr = next;
				
            }
        }
        toContinue = update_mus(mus, clusters, d, K);
        iter += 1;
    }



    free_list(clusters, K);
    PyObject* obs_inds_per_clusters = PyList_New(0);
    for (i = 0; i < K; i++)
    {
        PyObject* tmp = PyList_New(0);
        PyList_Append(obs_inds_per_clusters,tmp);
        Py_DECREF(tmp);
    }

    for(i = 0; i < N; i++)
    {
        vector x = array_to_vector(c_observations[i],d);
        int ind = find_cluster(x, mus, d, K);
        PyObject* py_i= PyFloat_FromDouble((double)i);
        PyObject* cluster_py_list = PyList_GetItem(obs_inds_per_clusters, ind);

        PyList_Append(cluster_py_list,py_i);
        Py_DECREF(py_i);
        free(c_observations[i]);
    }
    for(i = 0; i < K; i++)
    {
        free(c_initialMus[i]);
    }

    for(i = 0; i < K; i++)
    {
        free(mus[i]);
    }
    free(mus);

    free(c_observations);
    free(c_initialMus);

    return obs_inds_per_clusters;
}

static PyMethodDef kmeansMethods[] = {
        {"ckmeans",                   /* the Python method name that will be used */
                (PyCFunction) ckmeansMain, /* the C-function that implements the Python function and returns static PyObject*  */
                METH_VARARGS,           /* flags indicating parametersaccepted for this function */
                        PyDoc_STR("Calculates the centroids, given initial centroids and observations.")}, /*  The docstring for the function */
        {NULL, NULL, 0, NULL}     /* The last entry must be all NULL as shown to act as a
                                 sentinel. Python looks for this entry to know that all
                                 of the functions for the module have been defined. */
};


/* This initiates the module using the above definitions. */
static struct PyModuleDef _moduledef = {
        PyModuleDef_HEAD_INIT,
        "mykmeanssp", /* name of module */
        NULL, /* module documentation, may be NULL */
        -1,  /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
        kmeansMethods /* the PyMethodDef array from before containing the methods of the extension */
};


/*
 * The PyModuleDef structure, in turn, must be passed to the interpreter in the module’s initialization function.
 * The initialization function must be named PyInit_name(), where name is the name of the module and should match
 * what we wrote in struct PyModuleDef.
 * This should be the only non-static item defined in the module file
 */
PyMODINIT_FUNC
PyInit_mykmeanssp(void)
{
    PyObject *m;
    m = PyModule_Create(&_moduledef);
    if (!m) {
        return NULL;
    }
    return m;
}
