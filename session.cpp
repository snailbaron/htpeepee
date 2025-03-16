#include "session.hpp"

#include <utility>

namespace pp {

Session::Session()
    : _curl(curl_easy_init())
{ }

Session::Session(const Session& other)
    : _curl(curl_easy_duphandle(other._curl))
{ }

Session& Session::operator=(const Session& other)
{
    if (this != &other) {
        reset();
        _curl = curl_easy_duphandle(other._curl);
    }
    return *this;
}

Session::Session(Session& other) noexcept
{
    swap(*this, other);
}

Session& Session::operator=(Session&& other) noexcept
{
    if (this != &other) {
        reset();
        swap(*this, other);
    }
    return *this;
}

Session::operator bool() const
{
    return _curl != nullptr;
}

void Session::reset()
{
    if (*this) {
        curl_easy_reset(_curl);
        _curl = nullptr;
    }
}


#define SETOPT(OPTION, FUNCTION_NAME, ARGUMENT, CONVERSION)                 \
void Session::FUNCTION_NAME(ARGUMENT)                                       \
{                                                                           \
    curl_easy_setopt(_curl, OPTION, CONVERSION);                            \
}
#include "setopt.hpp"

void swap(Session& lhs, Session& rhs)
{
    std::swap(lhs._curl, rhs._curl);
}

} // namespace pp
