import segyio


def main():
    with segyio.su.open("../../test_data/oseberg/825680.su", endian="little", ignore_geometry=True) as f:
        print(f.header)


if __name__ == '__main__':
    main()
