## Install

After cloning `pytodo`, `cd` into `pytodo` and run:

```
$ pip install .
```

## Initializing a New Project

`cd` to your project directory and run:

```
$ pyt -i
```

## List Issues

```
$ pyt
   4. Limit completed issues to last 5
   7. Display helpful error messages
   12. Display usage
 ✓ 2. Integrate with gitea
 ✓ 3. Integrate with gitlab
```

## Add New Issue

```
$ pyt -a 'Fix major bug'
```

## Complete Issue

```
$ pyt -c <id>
```

## Reopen Completed Issue

```
$ pyt -o <id>
```

