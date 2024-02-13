#include <iostream>
#include <vector>
#include <cmath>
#include <set>

const int SIZE = 4;
const int MIN_LEN = 4;
const int MAX_LEN = 7;

bool is_close_int(double n) {
    n = std::fmod(std::abs(n), 1);
    double eps = 0.0001;
    return n < eps || (1.0 - n) < eps;
}

int to_number_0(const std::pair<int, int>& p) {
    return 6 - p.second * 3 + p.first;
}

std::vector<std::pair<int, int>> get_inbetween_points(const std::pair<int, int>& p1, const std::pair<int, int>& p2) {
    int xdiff = p2.first - p1.first;

    if (xdiff == 0) {
        std::vector<std::pair<int, int>> result;
        int y_range_start = std::min(p1.second, p2.second) + 1;
        int y_range_end = std::max(p1.second, p2.second);
        for (int y = y_range_start; y < y_range_end; y++) {
            result.push_back(std::make_pair(p1.first, y));
        }
        return result;
    } else {
        double slope = static_cast<double>(p2.second - p1.second) / xdiff;
        double init = p2.second - slope * p2.first;

        std::vector<std::pair<int, int>> result;
        int x_range_start = std::min(p1.first, p2.first) + 1;
        int x_range_end = std::max(p1.first, p2.first);
        for (int x = x_range_start; x < x_range_end; x++) {
            double y = slope * x + init;
            if (is_close_int(y)) {
                result.push_back(std::make_pair(x, std::round(y)));
            }
        }
        return result;
    }
}

std::vector<std::pair<int, int>> gen_all_points() {
    std::vector<std::pair<int, int>> result;
    for (int x = 0; x < SIZE; x++) {
        for (int y = 0; y < SIZE; y++) {
            result.push_back(std::make_pair(x, y));
        }
    }
    return result;
}

int choose_next_point(std::set<std::pair<int, int>>& used_points, std::pair<int, int> last_point) {
    int found_possibilities = 0;

    if (used_points.size() >= MIN_LEN) {
        found_possibilities += 1;
        if (used_points.size() == MAX_LEN) {
            return found_possibilities;
        }
    }

    for (const auto& p : gen_all_points()) {
        if(!used_points.contains(p)) {
            bool valid = true;
            for (const auto& between_p : get_inbetween_points(last_point, p)) {
                if(!used_points.contains(between_p)) {
                    valid = false;
                    break;
                }
            }
            if (valid) {
                std::set<std::pair<int, int>> used_points_copy = used_points;
                used_points_copy.insert(p);
                found_possibilities += choose_next_point(used_points_copy, p);
            }
        }
    }

    return found_possibilities;
}

int main() {
    int total = 0;

    for (const auto& p : gen_all_points()) {
        auto a = to_number_0(p);
        std::cout << "Starting start point (" << p.first << ", " << p.second << ") (" << a << ")" << std::endl;
        std::set<std::pair<int, int>> used_points = {p};
        total += choose_next_point(used_points, p);
        std::cout << "Finished start point (" << p.first << ", " << p.second << ")" << std::endl;
    }

    std::cout << "Sum: " << total << std::endl;

    return 0;
}
