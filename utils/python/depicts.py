#!/usr/bin/env python

# Don't hold on to this. It _will_ be replaced, shortly.
# (20200226/thisisaaronland)

import mapzen.whosonfirst.utils
import mapzen.whosonfirst.export

if __name__ == "__main__":

    data = "data"
    col_data = "/usr/local/data/sfomuseum-data-collection/data"

    exporter = mapzen.whosonfirst.export.flatfile(data)

    crawl = mapzen.whosonfirst.utils.crawl(data, inflate=True)

    for feature in crawl:

        props = feature["properties"]
        parent_id = props["wof:parent_id"]

        parent_f = mapzen.whosonfirst.utils.load(col_data, parent_id)
        parent_props = parent_f["properties"]

        parent_depicts = parent_props.get("wof:depicts", [])

        if len(parent_depicts) == 0:
            continue

        depicts = props.get("wof:depicts", [])
        updates = False
        
        for id in parent_depicts:

            if not id in depicts:
                depicts.append(id)
                updates = True

        if not updates:
            continue

        feature["properties"] = props
        print exporter.export_feature(feature)
    
