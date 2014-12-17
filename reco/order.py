#!/usr/bin/env python
# -*- coding:utf8 ---

class Order():
    """
    user_item: user-item matrix
        {userA: (item1, item2, item3, ...)}
        {userB: (item2, item4, item5, ...)}
        ...

    item_user: item-user matrix
        {itemA: (user1, user2, user3, ...)}
        {itemB: (user2, user4, user5, ...)}
    """

    def __init__(self, *details):
        self.user_item = {}
        self.item_user = {}
        for user, item in details:
            self.add_order(user, item)

    def add_order(self, user, item):
        self.add_user(user, item)
        self.add_item(user, item)


    def add_user(self, user, item):
        _i_u = self.item_user

        _i_u[item] = _i_u.get(item, set())
        _i_u[item].add(user)


    def add_item(self, user, item):
        _u_i = self.user_item

        _u_i[user] = _u_i.get(user, set())
        _u_i[user].add(item)