from pack import pack

data = {
    "name": "Jane Smith",
    "age": 25,
    "height": 1.6,
    "hobbies": [
        "reading",
        "painting",
        {"name": "hiking", "location": "mountain"},
        10,
        3.14,
    ],
    "address": {
        "street": "456 Oak Ave",
        "city": "Somewhereville",
        "state": "NY",
        "zip": "67890",
    },
}


if __name__ == "__main__":
    print("Will pack this data:", data)
    packed = pack(data)
    print("Pack result:", packed)
