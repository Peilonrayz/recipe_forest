# -*- coding: utf-8 -*-

# Input


class mats(object):
    def __init__(self, mats):
        self.mats = mats


class mat(object):
    def __init__(self, name, amount):
        self.name = name
        self.deName = name
        self.amount = amount


class node(object):
    def __init__(self, name, amount, mats):
        self.name = name
        self.deName = name
        self.amount = amount
        self.mats = mats

    def _amount(self, amount, border):
        return " {1[0]}{0}{1[1]}".format(amount, border) if amount != 1 else ""

    def _string(self, num, amount):
        for i in self.mats:
            # print '{}{}'.format('\t'*(num), i)
            # print '{}{}'.format('\t'*(num), i.deName)
            if type(i.name) == str:
                # print '{}Str: {}'.format('\t'*(num), i.deName)
                ret = "\n{}{}{}".format(
                    "\t" * num, i.name, self._amount(i.amount * amount, "[]")
                )
            else:
                # print '{}Name: {}'.format('\t'*(num), i.name.deName)
                ret = "\n{}".format(i.name.string(num, i.amount * amount))
            # print '{}{}'.format('\t'*(num), repr(ret))
            yield ret

    def string(self, num, amount=1):
        a = amount * self.amount
        ret = "{}{}{}{}{}".format(
            "\t" * num,
            self.name,
            self._amount(self.amount, "{}"),
            self._amount(amount, "[]"),
            "".join(self._string(num + 1, a)),
        )
        # print '{}{}'.format('\t'*(num+1), repr(ret))
        return ret


dic = {
    "Shank": node("Shank", 1, [mat("Iron", 1), mat("Hide", 1)]),
    "Wooden Sword": node("Wooden Sword", 1, [mat("Wood", 3), mat("Iron Ore", 1)]),
    "Titan Scimitar": node(
        "Titan Scimitar", 1, [mat("Scimitar", 1), mat("Sapphire Globe", 1)]
    ),
    "Dartanian Sword": node(
        "Dartanian Sword", 1, [mat("Piercer", 1), mat("Emerald Globe", 1)]
    ),
    "Scholar": node(
        "Scholar", 1, [mat("Sorcerer's Sapphire", 1), mat("Regal Sword", 1)]
    ),
    "Nail Bat": node("Nail Bat", 1, [mat("Iron Ignot", 1), mat("Timber Wood", 1)]),
    "Vindicator Club": node(
        "Vindicator Club", 1, [mat("Nail Bat", 1), mat("Iron Globe", 1)]
    ),
    "Apprentice Wand": node(
        "Apprentice Wand", 1, [mat("Stick", 1), mat("Sapphire Shard", 1)]
    ),
    "Imp Branche": node(
        "Imp Branche", 1, [mat("Apprentice Wand", 1), mat("Gaea Seed", 1)]
    ),
    "Trusty Dagger": node(
        "Trusty Dagger", 1, [mat("Rusty Dagger", 1), mat("Alkahest", 1)]
    ),
    "Assassin Dagger": node(
        "Assassin Dagger", 1, [mat("Trusty Dagger", 1), mat("Ruby Shard", 1)]
    ),
    "Staff of the Magi": node(
        "Staff of the Magi", 1, [mat("Seal of Magi", 1), mat("Wizard's Rod", 1)]
    ),
    "Widow Claw": node("Widow Claw", 1, [mat("Fachata", 1), mat("Ruby Globe", 1)]),
    "Razor Sword": node(
        "Razor Sword", 1, [mat("Wooden Sword", 1), mat("Iron Globe", 5)]
    ),
    "Paladin's Mace": node(
        "Paladin's Mace", 1, [mat("Peace Batton", 1), mat("Angel's Tear", 1)]
    ),
    "Morning Star": node(
        "Morning Star", 1, [mat("Paladin's Mace", 1), mat("Vindicator", 1)]
    ),
    "Deadwood Staff": node(
        "Deadwood Staff", 1, [mat("Imp Staff", 1), mat("Necromancer's Heart", 1)]
    ),
    "Cursed Kris": node("Cursed Kris", 1, [mat("Dagger", 1), mat("Gorgon Blood", 1)]),
    "Regal Sword": node("Regal Sword", 1, [mat("Militia Sword", 1), mat("Leather", 1)]),
    "Gold Ninja Stars": node(
        "Gold Ninja Stars", 5, [mat("Gold Ore", 1), mat("Alkahest", 1)]
    ),
    "Ninja Stars": node("Ninja Stars", 5, [mat("Iron Ore", 1), mat("Alkahest", 1)]),
    "Emerald Dart": node(
        "Emerald Dart", 5, [mat("Emerald Shard", 1), mat("Alkahest", 1)]
    ),
    "Sapphire Dart": node(
        "Sapphire Dart", 5, [mat("Sapphire Shard", 1), mat("Alkahest", 1)]
    ),
    "Ruby Dart": node("Ruby Dart", 5, [mat("Ruby Shard", 1), mat("Alkahest", 1)]),
    "Shuriken": node("Shuriken", 1, [mat("Iron", 1), mat("Alkahest", 1)]),
    "Beetle Shield": node(
        "Beetle Shield", 1, [mat("Animal Hide", 3), mat("Animal Shell", 3)]
    ),
    "Round Shield": node(
        "Round Shield", 1, [mat("Wooden Shield", 1), mat("Iron Ignot", 1)]
    ),
    "Warrior's Shield": node(
        "Warrior's Shield", 1, [mat("Knight's Memento", 1), mat("Round Shield", 1)]
    ),
    "Plate Chest Armor": node(
        "Plate Chest Armor", 1, [mat("Plate", 1), mat("Leather Chest Armor", 1)]
    ),
    "Plate Helmet": node(
        "Plate Helmet", 1, [mat("Leather Helmet", 1), mat("Plate", 1)]
    ),
    "Blast Shield": node(
        "Blast Shield", 1, [mat("Iron Globe", 1), mat("Warrior's Shield", 1)]
    ),
    "Golem Armor": node(
        "Golem Armor", 1, [mat("Leather Armor", 1), mat("Golem Talisman", 1)]
    ),
    "Minotaur Armor": node(
        "Minotaur Armor", 1, [mat("Golem Armor", 1), mat("Minotaur Talisman", 1)]
    ),
    "Paladin Armor": node(
        "Paladin Armor",
        1,
        [mat("Old Guard Armor", 1), mat("Knight Talisman (Mage)", 1)],
    ),
    "Saint Armor": node(
        "Saint Armor", 1, [mat("Paladin Armor", 1), mat("Saint Talisman (Mage)", 1)]
    ),
    "Beetle God's Shield": node(
        "Beetle God's Shield", 1, [mat("Blast Shield", 1), mat("Beetle God Icon", 1)]
    ),
    "Plate Armor": node("Plate Armor", 1, [mat("Leather Armor", 1), mat("Plate", 1)]),
    "Plate Sleeves": node(
        "Plate Sleeves", 1, [mat("Leather Sleeves", 1), mat("Plate", 1)]
    ),
    "Plate Leggings": node(
        "Plate Leggings", 1, [mat("Leather Leggings", 1), mat("Plate", 1)]
    ),
    "Minotaur Chest Armor": node(
        "Minotaur Chest Armor", 1, [mat("Golem Armor", 1), mat("Minotaur Talisman", 1)]
    ),
    "Plate": node("Plate", 1, [mat("Shell", 3), mat("Shell", 3)]),
    "Solid Scale": node("Solid Scale", 1, [mat("Plate", 3), mat("Alkahest", 1)]),
    "Iron Ignot": node("Iron Ignot", 1, [mat("Ore", 3), mat("Ore", 3)]),
    "Iron Globe": node("Iron Globe", 1, [mat("Iron Ignot", 3), mat("Alkahest", 1)]),
    "Timber": node("Timber", 1, [mat("Wood", 3), mat("Wood", 3)]),
    "Leather": node("Leather", 1, [mat("Hide", 3), mat("Hide", 3)]),
    "Treated Leather": node(
        "Treated Leather", 1, [mat("Leather", 3), mat("Alkahest", 1)]
    ),
    "Alkahest": node(
        "Alkahest", 1, [mat("Antidote", 1), mat("Small Healing Potion", 1)]
    ),
    "Emerald": node("Emerald", 1, [mat("Emerald Shard", 3), mat("Emerald Shard", 3)]),
    "Sapphire": node(
        "Sapphire", 1, [mat("Sapphire Shard", 3), mat("Sapphire Shard", 3)]
    ),
    "Ruby": node("Ruby", 1, [mat("Ruby Shard", 3), mat("Ruby Shard", 3)]),
    "Emerald Globe": node("Emerald Globe", 1, [mat("Emerald", 3), mat("Alkahest", 1)]),
    "Sapphire Globe": node(
        "Sapphire Globe", 1, [mat("Sapphire", 3), mat("Alkahest", 1)]
    ),
    "Ruby Globe": node("Ruby Globe", 1, [mat("Ruby", 3), mat("Alkahest", 1)]),
    "Gold Ignot": node("Gold Ignot", 1, [mat("Gold Ore", 3), mat("Gold Ore", 3)]),
    "Gold Globe": node("Gold Globe", 1, [mat("Gold Ignot", 3), mat("Alkahest", 1)]),
    "Sturdy Lumber": node("Sturdy Lumber", 1, [mat("Lumber", 3), mat("Alkahest", 1)]),
    "Small Healing Potion": node(
        "Small Healing Potion", 1, [mat("Healing Herb", 3), mat("Empty Bottle", 1)]
    ),
    "Medium Healing Potion": node(
        "Medium Healing Potion", 1, [mat("Healing Herb", 6), mat("Empty Bottle", 1)]
    ),
    "Large Healing Potion": node(
        "Large Healing Potion", 1, [mat("Healing Herb", 12), mat("Empty Bottle", 1)]
    ),
    "Small Mana Potion": node(
        "Small Mana Potion", 1, [mat("Mana Herb", 3), mat("Empty Bottle", 1)]
    ),
    "Medium Mana Potion": node(
        "Medium Mana Potion", 1, [mat("Mana Herb", 6), mat("Empty Bottle", 1)]
    ),
    "Large Mana Potion": node(
        "Large Mana Potion", 1, [mat("Mana Herb", 12), mat("Empty Bottle", 1)]
    ),
    "Small Berry Potion": node(
        "Small Berry Potion", 1, [mat("Teras Berrie", 3), mat("Empty Bottle", 1)]
    ),
    "Medium Berry Potion": node(
        "Medium Berry Potion", 1, [mat("Teras Berrie", 6), mat("Empty Bottle", 1)]
    ),
    "Large Berry Potion": node(
        "Large Berry Potion", 1, [mat("Teras Berrie", 12), mat("Empty Bottle", 1)]
    ),
    "Ambrosia": node(
        "Ambrosia", 1, [mat("Large Health Potion", 1), mat("Large Mana Potion", 1)]
    ),
    "Panacea": node("Panacea", 1, [mat("Antidote", 5), mat("Medium Health Potion", 1)]),
}


def main():
    for i in dic:
        for j in dic[i].mats:
            try:
                j.name = dic[j.name]
            except:
                pass
    dictList = ["'{}'".format(i) for i in dic]
    dictList.sort()
    dictList = "\n\t" + "\n\t".join(dictList) + "\n"
    while 1:
        inp = raw_input("What Item dous tho want? ")
        try:
            print dic[inp].string(0)
        except:
            if inp.lower() == "list":
                print dictList
            else:
                print "Unknown Item, please try again."


gString = """
Shank 	Iron 	Hide
Wooden Sword 	3X Wood 	Iron Ore
Titan Scimitar 	Scimitar 	Sapphire Globe
Dartanian Sword 	Piercer 	Emerald Globe
Scholar 	Sorcerer's Sapphire 	Regal Sword
Nail Bat 	Iron Ignot 	Timber Wood
Vindicator Club 	Nail Bat 	Iron Globe
Apprentice Wand 	Stick 	Sapphire Shard
Imp Branche 	Apprentice Wand 	Gaea Seed
Trusty Dagger 	Rusty Dagger 	Alkahest
Assassin Dagger 	Trusty Dagger 	Ruby Shard
Staff of the Magi 	Seal of Magi 	Wizard's Rod
Widow Claw 	Fachata 	Ruby Globe
Razor Sword 	Wooden Sword 	5X Iron Globe
Paladin's Mace 	Peace Batton 	Angel's Tear
Morning Star 	Paladin's Mace 	Vindicator
Deadwood Staff 	Imp Staff 	Necromancer's Heart
Cursed Kris 	Dagger 	Gorgon Blood
Regal Sword 	Militia Sword 	Leather

5X Gold Ninja Stars 	Gold Ore 	Alkahest
5X Ninja Stars 	Iron Ore 	Alkahest
5X Emerald Dart 	Emerald Shard 	Alkahest
5X Sapphire Dart 	Sapphire Shard 	Alkahest
5X Ruby Dart 	Ruby Shard 	Alkahest
Shuriken 	Iron 	Alkahest

Beetle Shield 	3X Animal Hide 	3X Animal Shell
Round Shield 	Wooden Shield 	Iron Ignot
Warrior's Shield 	Knight's Memento 	Round Shield
Plate Chest Armor 	Plate 	Leather Chest Armor
Plate Helmet 	Leather Helmet 	Plate
Blast Shield 	Iron Globe 	Warrior's Shield
Golem Armor 	Leather Armor 	Golem Talisman
Minotaur Armor 	Golem Armor 	Minotaur Talisman
Paladin Armor 	Old Guard Armor 	Knight Talisman (Mage)
Saint Armor 	Paladin Armor 	Saint Talisman (Mage)
Beetle God's Shield 	Blast Shield 	Beetle God Icon
Plate Armor 	Leather Armor 	Plate
Plate Sleeves 	Leather Sleeves 	Plate
Plate Leggings 	Leather Leggings 	Plate
Minotaur Chest Armor 	Golem Armor 	Minotaur Talisman

Plate 	3X Shell 	3X Shell
Solid Scale 	3X Plate 	Alkahest
Iron Ignot 	3X Ore 	3X Ore
Iron Globe 	3X Iron Ignot 	Alkahest
Timber 	3X Wood 	3X Wood
Leather 	3X Hide 	3X Hide
Treated Leather 	3X Leather 	Alkahest
Alkahest 	Antidote 	Small Healing Potion
Emerald 	3X Emerald Shard 	3X Emerald Shard
Sapphire 	3X Sapphire Shard 	3X Sapphire Shard
Ruby 	3X Ruby Shard 	3X Ruby Shard
Emerald Globe 	3X Emerald 	Alkahest
Sapphire Globe 	3X Sapphire 	Alkahest
Ruby Globe 	3X Ruby 	Alkahest
Gold Ignot 	3X Gold Ore 	3X Gold Ore
Gold Globe 	3X Gold Ignot 	Alkahest
Sturdy Lumber 	3X Lumber 	Alkahest

Small Healing Potion 	3X Healing Herb 	Empty Bottle
Medium Healing Potion 	6X Healing Herb 	Empty Bottle
Large Healing Potion 	12X Healing Herb 	Empty Bottle
Small Mana Potion 	3X Mana Herb 	Empty Bottle
Medium Mana Potion 	6X Mana Herb 	Empty Bottle
Large Mana Potion 	12X Mana Herb 	Empty Bottle
Small Berry Potion 	3X Teras Berrie 	Empty Bottle
Medium Berry Potion 	6X Teras Berrie 	Empty Bottle
Large Berry Potion 	12X Teras Berrie 	Empty Bottle
Ambrosia 	Large Health Potion 	Large Mana Potion
Panacea 	5X Antidote 	Medium Health Potion"""


def _nameFix(name):
    amount = 1
    if name[0] in "0123456789":
        i = name.find(" ")
        if name[i - 1] == "X":
            amount = name[: i - 1]
            name = name[i + 1 :]
    while name[-1] in " \n\t":
        name = name[:-1]
    return name, amount


def main2():
    gen = (i.split("\t") for i in gString.split("\n"))
    string = ""
    for i in gen:
        try:
            string += "\t{0[0]!r}: node({0[0]!r}, {0[1]}, [mat({1[0]!r}, {1[1]}), mat({2[0]!r}, {2[1]})]),\n".format(
                _nameFix(i[0]), _nameFix(i[1]), _nameFix(i[2])
            )
            print i
        except:
            pass
    print "{{\n{}\n}}".format(string[:-2])


if __name__ == "__main__":
    main()
