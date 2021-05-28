## Introduction

This is a replication of the Netlogo model [Wealth Distribution](https://ccl.northwestern.edu/netlogo/models/Daisyworld) in Python.

Turtles and patches in the netlogo model are referred to as agents and world in this implementation

## Requirements

- Python >= 3.7

## How to run it
 
Simply run the model using

```python main.py```

## Outputs

The program outputs four stats of the model in terminal, they are:

```tick, low income agent count, med income agent count, high income agent count, gini index```

## Parameters

You can view and change the parameters in ```settings.json```


| Parameter                   |Type       | Description  |
|-----------------------------|-----------|-------------------------------------------------------------------|
| x                           | Intrinsic | Horizontal Dimension of the world (Intrinsic Netlogo parameter)| 
| y                           | Intrinsic | Vertical Dimension of the world|
| max_grain                   | Intrinsic | Maximum grain capacity for the world, also used in grain distribution initialization|
| life_expectancy_min         | Agent     | Minimum age that the agent could die|
| life_expectancy_max         | Agent     | Maximum age that the agent could die|
| max_metabolism              | Agent     | Maximum metabolism possible for an agent|
| max_vision                  | Agent     | Maximum vision possible for an agent|
| num_people                  | World     | Population for the world|
| percent_best_land           | World     | Fraction of best land, used in grain distribution initialization|
| grain_growth_interval       | World     | Number of ticks between grain growth|
| num_grain_grown             | World     | Number of grains increase in each growth|
| refresh_interval            | System    | Seconds between each tick|
| report_interval             | System    | Ticks between data records|
| reproducing_error           | System    | Whether the model reproduces the implementation error in Netlogo code, see the notes below for more information|
| inherit_extension           | Extension | Toggle for the Inheritance extension|
| property_extension          | Extension | Toggle for the Property extension to the model|
| agent_purchase_patch_buffer | Extension | Amount of grain the agent cannot spend on purchasing patches|
| purchase_price_multiplier   | Extension | Multiplier of the number of grains to determine the land value|
| rent_percentage_of_yield    | Extension | Fraction of the land value to determine the rent|

## Extensions

### Inheritance

Enables wealth inheritance.

### Property

Enables the agents to buy and sell patches and collect rent as capital income.

## Notes

There is one major discrepancy between the Netlogo code and its description. The description states:

>The offspring has a random metabolism and a random amount of grain, ranging from the poorest person’s amount of grain to the richest person’s amount of grain

Instead, the Netlogo code has the same method for generating initial wealth for both first generation turtles and their offsprings 

Also, there are some behaviors that are not explicitly explained

In all, these characteristics are replicated:

- Initial age of the turtle is set to a random integer in range ```0``` to ```life_expectancy_max```
- Initial Wealth is set to metabolism + random integer in range ```0``` to ```50```
- Wealth of Offsprings of agents are initialized with the same method as the first generation ones. You can let the model behave like in the Netlogo description by using the flag ```reproducing_error```

## References

- Wilensky, U. (1998). NetLogo Wealth Distribution model. http://ccl.northwestern.edu/netlogo/models/WealthDistribution. Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.
- Wilensky, U. (1999). NetLogo. http://ccl.northwestern.edu/netlogo/. Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.