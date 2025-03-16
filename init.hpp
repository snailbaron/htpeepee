#pragma once

namespace pp {

class Init {
public:
    Init();
    ~Init();

    Init(const Init&) = delete;
    Init& operator=(const Init&) = delete;

    Init(Init&&) noexcept = delete;
    Init& operator=(Init&&) noexcept = delete;
};

} // namespace
