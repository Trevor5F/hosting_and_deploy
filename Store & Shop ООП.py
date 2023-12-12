from abc import ABC, abstractmethod


class Storage(ABC):
    def __init__(self, items, capacity):
        self._items = items  # {название:количество}
        self._capacity = capacity

    @abstractmethod
    def add(self, title, count):  # увеличивает запас items
        pass

    @abstractmethod
    def remove(self, title, count):
        pass

    @property
    @abstractmethod
    def get_free_space(self):
        pass

    @property
    @abstractmethod
    def get_items(self):
        pass

    @property
    @abstractmethod
    def get_unique_items_count(self):
        pass


# ____________________________________________________________________________________________

class Store(Storage):
    def __init__(self):
        self._items = {}
        self._capacity = 100

    def add(self, title, count):
        if title in self._items:
            self._items[title] += count
        else:
            self._items[title] = count
        self._capacity -= count

    def remove(self, title, count):
        res = self._items[title] - count
        if res > 0:
            self._items[title] = res
        else:
            del self._items[title]
        self._capacity += count

    @property
    def get_free_space(self):
        # self._capacity -= sum(self._items.values())
        return self._capacity

    @property
    def get_items(self):
        return self._items

    @get_items.setter
    def get_items(self, new_items):
        self._items = new_items

    @property
    def get_unique_items_count(self):
        return len(self._items.keys())


# ________________________________________________________________________________________

class Shop(Storage):
    def __init__(self):
        self._items = {}
        self._capacity = 20

    def add(self, title, count):
        if title in self._items:
            self._items[title] += count
        else:
            self._items[title] = count
        self._capacity -= count

    def remove(self, title, count):
        res = self._items[title] - count
        if res > 0:
            self._items[title] = res
        else:
            del self._items[title]
        self._capacity += count

    @property
    def get_free_space(self):
        self._capacity -= sum(self._items.values())
        return self._capacity

    @property
    def get_items(self):
        return self._items

    @get_items.setter
    def get_items(self, new_items):
        self._items = new_items

    @property
    def get_unique_items_count(self):
        return len(self._items.keys())


# __________________________________________________________________________________________

class Request:
    def __init__(self, info):
        # info = ['Доставить', '3', 'собачки', 'из', 'склад', 'в', 'магазин']
        self.info = self._split_info(info)
        self.from_ = self.info[4]
        self.to = self.info[6]
        self.amount = int(self.info[1])
        self.product = self.info[2]

    @staticmethod
    def _split_info(info):
        return info.split()

    def __repr__(self):
        return f'Доставить {self.amount} {self.product} из {self.from_} в {self.to}'


def main():
    while (True):
        user_input = input('Введите запрос: ')
        # user_input = 'Доставить 6 кофе из склад в магазин'

        if user_input == 'стоп':
            break

        request = Request(user_input)

        if request.from_ == 'склад':
            if request.product not in shop.get_items:
                print('На складе нет такого товара')
                shop.add(request.product, request.amount)
                continue

            if request.to == 'магазин' and store.get_unique_items_count == 5 and request.product not in store.get_items:
                print("В магазине достаточно уникальных товаров")
                continue

            if store.get_free_space < request.amount:
                print(f'В  магазине не хватает места {store.get_free_space}')
                continue

            if shop.get_items[request.product] >= request.amount:
                print(f'Курьер забрал {request.amount} {request.product} со склада')
                shop.remove(request.product, request.amount)
                store.add(request.product, request.amount)
                print(f'Курьер везет {request.amount} {request.product} со склада в магазин')

            else:
                print(f'Не хватает на складе, осталось {shop.get_items[request.product]}')

        print('\nВ складе хранится:')
        for title, count in shop.get_items.items():
            print(f'{count} {title}')

        print('\nВ магазине хранится: ')
        for title, count in store.get_items.items():
            print(f'{count} {title}')
        print(store.get_free_space)


if __name__ == '__main__':
    store = Store()
    shop = Shop()

    shop_items = {
        'чипсы': 11,
        'сок': 40,
        'кофе': 7,
        'печеньки': 50,
        'чай': 3,
        'пиво': 3,
    }
    store_items = {
        'чипсы': 10,
        'сок': 20,
        'кофе': 7,
        'печеньки': 38,
        'чай': 3
    }

    shop.get_items = shop_items
    store.get_items = store_items

main()
