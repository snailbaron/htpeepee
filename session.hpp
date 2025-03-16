#pragma once

#include <curl/curl.h>

#include <filesystem>
#include <string>

namespace pp {

class Session {
public:
    Session();

    Session(const Session& other);
    Session& operator=(const Session& other);

    Session(Session& other) noexcept;
    Session& operator=(Session&& other) noexcept;

    explicit operator bool() const;
    void reset();

#define SETOPT(OPTION, FUNCTION_NAME, ARGUMENT, CONVERSION) \
    void FUNCTION_NAME(ARGUMENT);
#include "setopt.hpp"

    friend void swap(Session& lhs, Session& rhs);

private:
    CURL* _curl = nullptr;
};

} // namespace
