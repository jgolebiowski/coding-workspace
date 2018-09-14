//
// Created by Golebiowski, Jacek on 8/18/18.
//

#include <string>
#include <vector>
#include <StringUtils.h>
#include <iostream>
#include "StringUtilsTest.h"

void test::testSplitstring()
{
    std::string mystr = "Jestem jacek i mam placek!";
    std::string delim = " ";
    std::vector<std::string> target({"Jestem", "jacek", "i", "mam", "placek!"});
    test::runTestSplitstring(mystr, delim, target);

    std::string mystr2 = "jestem$$$kloc$$$i$$$mam$$$moc";
    std::string delim2 = "$$$";
    std::vector<std::string> target2({"jestem", "kloc", "i", "mam", "moc"});
    test::runTestSplitstring(mystr2, delim2, target2);
}

void test::runTestSplitstring(std::string &mystr, std::string &delim, std::vector<std::string> &target)
{
    auto tokenized = new std::vector<std::string>;
    stringUtils::splitstring(mystr, delim, tokenized);
    bool failed = false;

    for (size_t i = 0; i < tokenized->size(); ++i)
    {
        if (target.at(i) != tokenized->at(i))
        {
            std::cout <<
                      "<" << target.at(i) << ">"
                      << " != " <<
                      "<" << tokenized->at(i) << ">"
                      << " <at " << i << std::endl;
            failed = true;
        }
    }
    if (failed)
        std::cout << "runTestSplitstring failed for: "
                  << mystr << " -> "
                  << delim << std::endl;
    delete (tokenized);
}

void test::testNgrams()
{
    std::string mystr = "Jestem";
    size_t n = 2;
    std::vector<std::string> target({"Je", "es", "st", "te", "em"});
    test::runTestNgrams(mystr, n, target);

    std::string mystr2 = "jacek";
    size_t n2 = 3;
    std::vector<std::string> target2({"jac", "ace", "cek"});
    test::runTestNgrams(mystr2, n2, target2);

}

void test::runTestNgrams(std::string &mystr, size_t &n, std::vector<std::string> &target)
{
    auto ngrams = new std::vector<std::string>;
    stringUtils::getNGrams(mystr, n, ngrams);

    bool failed = false;

    for (size_t i = 0; i < ngrams->size(); ++i)
    {
        if (target.at(i) != ngrams->at(i))
        {
            std::cout <<
                      "<" << target.at(i) << ">"
                      << " != " <<
                      "<" << ngrams->at(i) << ">"
                      << " <at " << i << std::endl;
            failed = true;
        }
    }
    if (failed)
        std::cout << "runTestNgrams failed for: "
                  << mystr << " -> "
                  << n << std::endl;
    delete (ngrams);
}

void test::testReadFile()
{
    std::string filename = "../cpp/tst/data.txt";
    std::string target = "Jestem super placek i mam niezle testy tutaj mordino";
    auto contents = new std::string;
    stringUtils::readFile(filename, contents);

    if (target != *contents)
        std::cout << "testReadFile failed for: " << std::endl
                  << filename << " -> " << *contents << std::endl
                  << "target" << " -> " << target << std::endl;

    delete (contents);
}
