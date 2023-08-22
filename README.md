# Goal

Check all the specs [here](https://gist.github.com/JessikaCastellano/6e4297fbd245d779d068fb9226b0340c).

Generate a report that lists each student with the total minutes logged and the number of days they attended college. Order the result by the number of minutes from greatest to least.
Discard any record that indicates presences of less than 5 minutes.

Input:
```
Student Marco
Student David
Student Fran
Presence Marco 1 09:02 10:17 R100
Presence Marco 3 10:58 12:05 R205
Presence David 5 14:02 15:46 F505
```

Output:

```
Marco: 142 minutes in 2 days
David: 104 minutes in 1 day
Fran: 0 minutes
```

## TODO List

- [x] Setup base project.
    - [x] Create a manage.py handler to manage report generation and test running.
    - [x] Unit tests.
    - [x] Functional tests.
    - [] (Optional) Setup github actions.
    - [] (Optional) Setup docker.
- [x] Create models.
- [x] Create main GenerateReport.

## Process

### 1. About the modeling
I decided to use dataclasses to make it simple to read and instantiate and order the created objects.
I avoided using third parties, but if I would be easier to validation if you would use [Pydantic](https://docs.pydantic.dev/latest/), [Marshmellow](https://marshmallow.readthedocs.io/en/stable/), or [Cerberus](https://docs.python-cerberus.org/).

The models I created are:

#### a) Student:
Asumí que cada que el name de cada estudiante es único, motivo por el cual implementé un singleton para Student que siempre instancia el mismo objecto para cada estudiante.

#### b) Presence:
The `__new__` dunder method only instantiates presence objects that lasts 5 minutes or more.
We also take advantage of the __post__init__ method of dataclasses in order to cast and validate the presence attributes.

#### c) Report:
Here we implement a sort of singleton, where we group the presences by students. Finally we implement the method `compute_minutes_and_days` that iterate over the list of presences of a student in order to calculate the minuts and days he attends to classes.

### 2. About the controller

I implemented the `GenerateReport` controller which is in charge of reading each input and iterating through each command and finally generating an output with the final report.


## Commands

To generate a report run this command. The output will be generated at the same level of the input file.
```bash
make report `input_filepath`
# Example:
make report data/input1.txt
```

To run all the tests.
```bash
make test
```

To generate a git bundle.
```bash
make bundle
```


