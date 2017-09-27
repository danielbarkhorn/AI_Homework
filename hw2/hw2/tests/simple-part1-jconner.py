#!/usr/bin/python

import resolve

print(resolve.resolve(["or", "a", "b", "c"], ["not", "b"]))
print(resolve.resolve(["or", "a", "b", "c"], ["or", "b", ["not", "c"]]))
print(resolve.resolve(["or", ["not", "raining"], "wet ground"], "raining"))
print(resolve.resolve(["or", "a", "b"], "c"))
print(resolve.resolve(["or", ["not", "a"], ["not", "b"], ["not", "c"]],
              ["or", "a", "b", ["not", "d"]]))
print(resolve.resolve("a", ["not", "a"]))
