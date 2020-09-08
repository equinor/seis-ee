from segdpy import segdpy


def main(filename):
    data, rec_info, chan_sets, trc_hdrs, fem = segdpy.read_segd_file(filename)
    print(123)


if __name__ == '__main__':
    main("../../test_data/grane/full-files/segd-test.sgd")
