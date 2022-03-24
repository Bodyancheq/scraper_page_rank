import json
from tqdm import tqdm


def get_links_with_ingoing_links(links: dict):
    # ingoing_links = dict()
    # for link in tqdm(links.keys()):
    #     ingoing_links[link] = []
    #     for key, values in links.items():
    #         if link in values:
    #             ingoing_links[link].append(key)

    with open("ingoing_links.json", "r", encoding="utf-8") as linkfile:
        ingoing_links = json.load(linkfile)
    # with open("ingoing_links_fixed.json", "w", encoding="utf-8") as new_linkfile:
    #     json.dump(ingoing_links, new_linkfile, indent=4, ensure_ascii=False)

    return ingoing_links


def get_pagerank_values(links_outgoing: dict, links_ingoing: dict, d=0.85):
    pagerank_values = dict()
    for link in links_outgoing.keys():
        pagerank_values[link] = 0

    # n = len(pagerank_values.keys())
    for _ in tqdm(range(500)):
        for key in pagerank_values.keys():
            pagerank_values[key] = (1 - d) + d * sum(
                [pagerank_values[link] / len(links_outgoing[link]
                                             )
                 for link in links_ingoing[key]])

    return pagerank_values


if __name__ == '__main__':
    with open("link_data3.json", "r", encoding="utf-8") as linkfile:
        links_outgoing = json.load(linkfile)
        links_ingoing = get_links_with_ingoing_links(links_outgoing)
        pagerank = get_pagerank_values(links_outgoing, links_ingoing)
        with open("pagerank_res_fixed.json", "w", encoding="utf-8") as pagerankfile:
            json.dump(pagerank, pagerankfile, indent=4, ensure_ascii=False)

        check_sum = sum(pagerank.values())
        print(f"{check_sum / len(pagerank.keys())} - sum of pageranks divided by n")

    with open("pagerank_res.json", "r", encoding="utf-8") as linkfile:
        links = json.load(linkfile)
        links = dict(sorted(links.items(), key=lambda item: item[1], reverse=True))
        with open("pagerank_res_sorted.json", "w", encoding="utf-8") as pagerankfile:
            json.dump(links, pagerankfile, indent=4, ensure_ascii=False)
