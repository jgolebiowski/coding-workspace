//
// Created by Golebiowski, Jacek on 8/18/18.
//

#include <iostream>
#include <Utilities.h>
#include <fstream>
#include <sstream>
#include <vector>
#include "StringUtils.h"

void stringUtils::readFile(const std::string &filename,
                           std::string *contents)
{
    std::ifstream myfile(filename);
    std::stringstream buffer;

    if (myfile.is_open())
    {
        buffer << myfile.rdbuf();
        *contents = buffer.str();
        myfile.close();
    }
}

void stringUtils::splitstring(const std::string &s,
                              const std::string &delimiter,
                              std::vector<std::string> *tokenized)
{
    tokenized->clear();
    size_t startidx = 0;
    size_t stopidx = 0;
    while (stopidx < s.length())
    {
        stopidx = s.find(delimiter, startidx);
        tokenized->push_back(s.substr(startidx, stopidx - startidx));
        startidx = stopidx + delimiter.length();
    }
}

void stringUtils::getNGrams(const std::string &s,
                            const size_t &n,
                            std::vector<std::string> *ngrams)
{
    ngrams->clear();
    size_t currentPos = 0;
    while (currentPos + n < s.size())
    {
        ngrams->push_back(s.substr(currentPos, n));
        currentPos++;
    }
}
