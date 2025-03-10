from statistics import median


def count_percentile(number_of_requests: float, total_count: float) -> float:
    return (number_of_requests / total_count) * 100


def count_total(requests_data: dict, key: str) -> float:
    count_array = []
    for request in requests_data.values():
        if isinstance(request[key], list):
            count_array.append(sum(request[key]))
            continue
        count_array.append(request[key])
    return sum(count_array)


def count_time_statistics(request_time_array: dict) -> dict:
    time_stats = {}
    for url, data in request_time_array.items():
        time_stats[url] = {
            "sum": sum(data["times"]),
            "avg": sum(data["times"]) / len(data["times"]),
            "max": max(data["times"]),
            "med": median(data["times"]),
        }
    return time_stats
