from collector.wanted_collector import collect_from_wanted

if __name__ == '__main__':
    for offset in range(0, 501, 100):
        collect_from_wanted(offset)
