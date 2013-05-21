from parser import jet


if __name__ == '__main__':
    """
    DEMOTIME!
    Fetch the prices from
    https://www.jet-tankstellen.de/kraftstoff/filialfinder/XJ00690
    and display them
    """
    print jet.get_prices('XJ05668')
