# Bitmask Tricks Cheat Sheet

## Basic Operations

-   **Check if the i-th bit is set**

    ``` python
    mask & (1 << i)
    ```

-   **Set the i-th bit**

    ``` python
    mask | (1 << i)
    ```

-   **Unset the i-th bit**

    ``` python
    mask & ~(1 << i)
    ```

-   **Toggle the i-th bit**

    ``` python
    mask ^ (1 << i)
    ```

-   **Get the number of set bits**

    ``` python
    number.bit_count()
    ```

------------------------------------------------------------------------
## All bits set (visited all states)
```python
if mask == (1 << T) - 1:
    return 1
```

## Submask Enumeration Trick

Iterate through all subsets of a bitmask `row`:

``` python
s = row
while True:
    # use s here

    if s == 0:
        break
    s = (s - 1) & row
```

This generates all submasks of `row`, including 0, without duplicates.
