# COVID-19 Simulation - Mask and Travel Restrictions Impact

This is a Python-based simulation that models the spread of COVID-19 within a community, with parameters for wearing masks and travel restrictions. The simulation calculates the number of infected, hospitalized, recovered, and fatality cases over a specified period. The model takes into account age groups (children, adults, senior citizens) and various probabilities for infection, recovery, and fatality.

## Features

- **Infection Probability**: Varies based on the individual's age group and whether they are wearing a mask.
- **Recovery and Fatality**: Simulates the recovery process (either via hospitalization or immunity) and tracks fatalities.
- **Family Spread**: Models the spread of the virus within families, where family members have a higher chance of being infected if one person is already infected.
- **Input Handling**: Allows for user input on whether masks are being worn or if travel restrictions are in place.
- **Dynamic Data Collection**: Tracks statistics (infected, hospitalized, recovered, fatalities) on a daily basis.
- **Visualization**: Graphs the daily counts of infections, hospitalizations, recoveries, and fatalities.

## Installation

### Prerequisites

- Python 3
- `matplotlib` for data visualization

To install the required dependencies, run the following:

```bash
pip install matplotlib
