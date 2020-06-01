import pandas as pd
url = 'https://space-facts.com/mars/'
tables = pd.read_html(url)
mars_facts_df = tables[0]
mars_facts_df = mars_facts_df.rename(columns={0:"Parameter", 1:"Value"})
params = mars_facts_df['Parameter'].to_list()
values = mars_facts_df['Value'].to_list()


# mars_facts_df.set_index('Parameter', inplace=True)
# mars_params = mars_facts_df.to_dict()
mars_facts = {}

for i in range(len(params)):
    mars_facts.update( {params[i] : values[i]} )

for fact in mars_facts:
    print(fact, mars_facts[fact])

    