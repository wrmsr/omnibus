#include <stdint.h>

#include <vector>


namespace stl_helpers {


struct Uint8VectorHash {
    size_t operator()(const std::vector<uint8_t>& v) const {
        std::hash<uint8_t> hasher;
        size_t seed = 0;
        for (int i : v) {
            seed ^= hasher(i) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
        }
        return seed;
    }
};


};
