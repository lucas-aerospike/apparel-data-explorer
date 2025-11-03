# Aerospike AI/ML Data Explorer

## What is Does
- Allows interactive iPython notebook exploration of vintage women's clothing data using cross-sectional queries on secondary indexes.
- Given a SKU (`itemID`) for one dress, performs **Retrieval-Augmented Recommendation** using a remote OpenAI call.
- Given a SKU, OpenAI will recommend three other SKUs and explain its reasoning.

## How to Use It
- You can run it through an iPython notebook or the command line.
- However you run it, make sure that you've already cloned the [**apparel-data-feeder**](https://github.com/lucas-aerospike/apparel-data-feeder) project and followed the appropriate steps to start the local docker server with `docker compose up` and then fed in the vintage women's apparel data set. **If you don't perform this step, there will be no data to explore or to use to make recommendations.**
- If running it through the command line, usage is `./main.py <sku>` where `<sku>` is the `itemId` of *exemplar* garment that describes a particular style. You'll get back recommendations for three other garments of a similar style to the exemplar.

## Example
- Here's an example of a command line run using the dress with `itemId = 2900` as an exemplar. Note the call to OpenAI and the explained reasoning for why OpenAI chose the dresses with SKUs / itemIds 2887, 5616, and 4340.
```
{ 'top3': [{'itemId': 2887,
           'score': 0.8,
           'why': 'Shift dress from the 1980s with a solid pattern, similar '
                  'era and pattern to the exemplar. The color is different '
                  '(jade vs azure), but the material is a cotton blend, which '
                  'is similar in feel to linen.'},
          {'itemId': 5615,
           'score': 0.75,
           'why': 'Empire waist dress from the 1980s with a solid pattern. The '
                  'color (rosewood) is not a match, but the era and pattern '
                  'are aligned. The material is silk, which is smooth like '
                  'linen.'},
          {'itemId': 4340,
           'score': 0.7,
           'why': 'Sundress from the 1980s with a solid pattern. The color '
                  '(rouge) is different, but the era and pattern match. The '
                  'material is wool jersey, which is less similar to linen.'}],

  'notes': 'The top matches prioritize silhouette and era, with a focus on '
          'solid patterns. While none are bodycon, the shift and empire waist '
          'styles are closer in silhouette than mumu or trapeze. The color '
          'match is less precise, but the era and pattern alignment help '
          'compensate. Fabric similarity is considered, though not all matches '
          'are linen or similar in texture.'
}
```