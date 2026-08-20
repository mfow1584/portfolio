class ChainingHashTable:
    def __init__(self, inventory = 40):
        self.table = []
        for i in range(inventory):
            self.table.append([])

    def insert(self, item, key):
        # determine which bucket the key should be located in
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # add the item to the table in the specified bucket
        # bucket_list refers to the chain at the specified bucket
        bucket_list.append(item)

    def search(self, key):
        # determine which bucket the key should be located in
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # bucket_list contains package objects
        # returns a package object if key matches id of package
        for item in bucket_list:
            if key == item.id:
                return item
        return None

    def remove(self, key):
        # determine which bucket the key should be located in
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # bucket_list refers to the chain at the specified bucket
        if key in bucket_list:
            bucket_list.remove(key)