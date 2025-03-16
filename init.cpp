#include "init.hpp"

#include <mutex>

#include <curl/curl.h>

namespace pp {

namespace {

std::mutex initMutex;
int initCount = 0;

} // namespace

Init::Init()
{
    auto lock = std::lock_guard{initMutex};
    if (initCount == 0) {
        curl_global_init(CURL_GLOBAL_DEFAULT);
    }
}

Init::~Init()
{
    curl_global_cleanup();
}

} // namespace pp
