# poker-data-mining

## Usage

Place hand txt files (only works with PokerStars hands) in `data/` and run

```
python src/filter.py data/
```

It currently will print out the top 30 and bottom 30 players by profit per hand.

## Sample Output

```
data/hh.com_Clorinde_289FR_2019.05.07_0.txt
data/hh.com_Suleika_289FR_2019.05.05_0.txt
data/hh.com_Colocolo_289FR_2019.05.20_0.txt
data/hh.com_Cloanthus_289FR_2019.05.01_0.txt
data/hh.com_Asmodeus_289FR_2019.04.30_0.txt
...
Hands processed: 555466


TOP:
[('rusher_NiNja', 990.9, 3460, 0.28638728323699425),
 ('dragu419', 1220.95, 5969, 0.2045485005863626),
 ('Derekking77', 572.48, 2832, 0.2021468926553671),
 ('TomasQ', 480.26, 2394, 0.20060985797827904),
 ('Marjel555', 494.54, 2486, 0.19893000804505195),
 ...]


BOTTOM:
[('stararia', -45.38, 2111, -0.021496920890573184),
 ('SaneK*3dfX', -47.75, 2103, -0.022705658582976605),
 ('100+x', -67.47, 2947, -0.022894468951476076),
 ('Pelusanator', -47.55, 2008, -0.023680278884462152),
 ('xtrail-mac', -149.77, 6039, -0.024800463652922662),
 ...]
```
