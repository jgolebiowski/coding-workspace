part1: Normal cpp-python project using cmake 
part2: A very simple function written in cpp and called from python using pybinding11
part3: Passing std::vectors between cpp and python
    This approach is quite easy to use, however relies on copying the lists on each call
part4: Passing std::vectors between cpp and python
    This approach does not copy the data but wraps the buffer in a special array-like object
    The new object is defined in the Binding code and can be accessed from both python and cpp
part5: Passing numpy arrays as Eigen arrays between cpp and python by copy
part6: Passing arrays between numpy and Eigen
    Numpy -> Eigen Matrix Passed as an Eigen::Ref<Eigen::Matrix<>>
        Eigen::Ref<Eigen::Matrix<>> is a more general construct than Eigen::Matrix<> that accepts
        also views of matrixes without making a temporary copy. the numpy array is passed as a view
        of an eigen array and the Ref wraps around it without making a copy.
    Eigen -> Numpy Passed natively if the Eigen Matrix is defined as RowMajor