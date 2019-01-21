# Allocine neuron for Kalliope

## Synopsis

Get information about movies times in your favorite theaters.

## Installation

  ```
  kalliope install --git-url https://github.com/vbouchet31/kalliope-allocine.git
  ```

## Options

| parameter          | required |  choices | comment                                                                                                                         |
|--------------------|----------|---------|---------------------------------------------------------------------------------------------------------------------------------|
| option   | yes     | getShowTimesList| See more details in dedicated paragraph|
| theater | no      |         | Only needed if you select an option which requires a theater parameter.                                                                            |

### Possible "option" values

"getShowTimesList": Get today's show time for the given theater.

### Get the theater code

The theater code is the Allocine unique ID  which you can get from the URL of the theater page on Allocine. For example,
"P0057" is the theater code for "Gaumont Toulouse Wilson" theater as per its page on Allocine (http://www.allocine.fr/seance/salle_gen_csalle=P0057.html).

## Return Values

| Name    | Description                   | Type   | sample                                                                                                                        |
|---------|-------------------------------|--------|-------------------------------------------------------------------------------------------------------------------------------|
| events  | A list of events.             | list   | Each event has the following information: event['name'] is the movie name, event['times'] is the list of times, event['all_times_as_string'] are the same times as a string.                                  |


## Synapses example

```
---
  - name: "get-gaumont-show-time-list"
    signals:
      - order: "Quels films au Gaumont"
      - order: "Quel film"
    neurons:
      - allocine:
          theater: "P0057"
          option: "getShowTimesList"
          file_template: "templates/allocine.j2"

```

## Templates example

```
Next showtimes today are:
{% for key, event in events.items() %}
  {{ event['name'] }} at {{ event['all_times_as_string'] }}
{% endfor %}
```