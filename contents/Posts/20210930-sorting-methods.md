---
title: Sorting Methods in Algorithm
date: 2021-10-01 15:20
author: Sim
tags: algorithm, programming, sort
summary: Hmm, it's frequently shown but I didn't really grasp it. So maybe I need to summerize it once.
---

## Methods in Action

### Bubble Sort

![](/posts/2021-09-30-10-48-13.png)

Worst complexity: n^2^
Average complexity: n^2^
Best complexity: n
Space complexity: 1
Stable: Yes

### Selection Sort

![](/posts/2021-09-30-10-49-01.png)

Worst complexity: n^2^
Average complexity: n^2^
Best complexity: n^2^
Space complexity: 1
Stable: No

### Insertion Sort

![](/posts/2021-09-30-11-17-48.png)

Worst complexity: n^2^
Average complexity: n^2^
Best complexity: n
Space complexity: 1

### Quicksort

![](/posts/2021-10-01-14-57-43.png)
(Picture from [Techie Delight](https://www.techiedelight.com/quicksort/))

Worst complexity: n^2^
Average complexity: n*log(n)
Best complexity: n*log(n)
Space complexity: log(n)

## Comparisions

### Bubble vs Selection

Their direction is different.
A bubble sort compares the members one by one and swaps when the former is larger than the latter in the current pair.
A selection sort determine the smallest one in an iteration and make it swap with the first number in the array of the current iteration before the iteration ends.
Selection Sort is twice as fast as Bubble Sort. (Complexity still the same as that of Bubble Sort, because in the world of Big O, constants r ignored.)[^1]

### Selection vs Insertion

In an average case, where an array is randomly sorted, they perform similarly.[^1]
If an array is mostly sorted, selection is a better choice.[^1]

### Insertion vs Quicksort

Insertion Sort is actually faster than Quicksort for a best-case scenario. However, Quicksort is much more superior than Insertion Sort in the average scenaro, thus more popular. [^1]

### Overview

![](/posts/2021-10-01-15-13-14.png)

Hmm, I've only seen 4 methods in the referenced guide[^1]. So maybe I'll check others out later.......

Now I'll head out to Leetcode for [some practice](https://leetcode.com/tag/sorting/).  

[^1]: Wengrow, Jay. A Common-Sense Guide to Data Structures and Algorithms. Pragmatic Bookshelf, 2020.