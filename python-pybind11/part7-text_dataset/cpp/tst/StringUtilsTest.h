//
// Created by Golebiowski, Jacek on 8/18/18.
//

#ifndef DATASET_UTILS_STRINGUTILSTEST_H
#define DATASET_UTILS_STRINGUTILSTEST_H

namespace test
{
    void testSplitstring();

    void runTestSplitstring(std::string &mystr, std::string &delim, std::vector<std::string> &target);

    void testNgrams();

    void runTestNgrams(std::string &mystr, size_t &n, std::vector<std::string> &target);

    void testReadFile();
}
#endif //DATASET_UTILS_STRINGUTILSTEST_H
