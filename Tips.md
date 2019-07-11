## Tips

There are several tips to have training with Frovedis work well, and gain much speedups with [SX-Aurora TSUBASA, Vector engine](https://www.nec.com/en/global/solutions/hpc/sx/vector_engine.html).

### Prerequisite

Build and install [Frovedis](https://github.com/frovedis/frovedis). Please follow tutorial ([Python](https://github.com/frovedis/frovedis/blob/master/doc/tutorial_python/tutorial_python.md) / [Spark](https://github.com/frovedis/frovedis/blob/master/doc/tutorial_spark/tutorial_spark.md)) to use Python/Spark interface

### Choosing datasets

- Use large training datasets. It tends to use the HW resources in vector engine more efficiently if you feed datasets with a large number of samples and features. 
- Take care that actual size of dataset does not exceed the device memory of vector engine. It is required to prevent out of memory error. 
- Sparse data is preferred to dense data. This is because operation for sparse matrix is highly optimized in Frovedis. 

### Misc

- Make binary dumps of dataset and load them in each training time. Each library supports binary format of data (For example, numpy/scipy supports `.npz` file to save matrix). It is waste of time to load text file for every time.

